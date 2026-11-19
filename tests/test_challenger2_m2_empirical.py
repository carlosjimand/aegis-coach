"""
Challenger 2 Empirical Stress-Test Suite for Milestone 2 (M2: Ergonomía Gimnasio y Frontend UI/UX)
===================================================================================================
Empirically stress-tests dynamic behaviors:
1. Rest Timer countdown execution (90s, 120s / 2m, decrement, audio oscillator 880Hz, cancellation, completion alert).
2. Debounce and network traffic throttling (600ms debounce, exactly 1 fetch dispatched, badge transitions).
3. Color contrast mathematical verification (WCAG 2.1 AA >= 4.5:1 with #C4B9C8 across dark backgrounds).
4. Cross-testing against both prototype/index.html and production worker-rendered HTML.
"""

import os
import re
import json
import time
import pytest
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTOTYPE_PATH = os.path.join(BASE_DIR, 'prototype', 'index.html')
INDEX_TS_PATH = os.path.join(BASE_DIR, 'cloudflare', 'src', 'index.ts')
PROTOTYPE_URL = f"file:///{PROTOTYPE_PATH.replace(os.sep, '/')}"


# =============================================================================
# 1. REST TIMER COUNTDOWN EXECUTION & AUDIO OSCILLATOR STRESS-TEST
# =============================================================================

def test_rest_timer_90s_and_2m_countdown_and_cancellation():
    """Empirically test startRestTimer for 90s and 2m (120s), decrements, and cancellation."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(PROTOTYPE_URL, wait_until="networkidle")

        page.evaluate("switchTab('gym')")
        page.wait_for_timeout(200)

        banner = page.locator("#rest-timer-banner")
        countdown = page.locator("#rest-timer-countdown")

        # Initially banner must be hidden
        assert not banner.is_visible(), "Rest timer banner should be initially hidden"

        # 1. Trigger 90s timer
        btn_90 = page.locator("button[onclick*='startRestTimer(90)']").first
        assert btn_90.is_visible(), "90s rest timer button must be visible in gym tab"
        btn_90.click()
        page.wait_for_timeout(100)

        # Banner should appear
        assert banner.is_visible(), "Banner must be visible after clicking 90s"
        t0_val = countdown.text_content().strip()
        assert t0_val in ("1:30", "01:30"), f"Expected 1:30 at start, got {t0_val}"

        # Wait 1.1s and verify countdown decrements
        page.wait_for_timeout(1150)
        t1_val = countdown.text_content().strip()
        assert t1_val in ("1:29", "01:29", "1:28"), f"Expected countdown to decrement to 1:29, got {t1_val}"

        # 2. Trigger 2m (120s) timer - should reset and not leak previous interval
        btn_2m = page.locator("button[onclick*='startRestTimer(120)']").first
        assert btn_2m.is_visible(), "2m rest timer button must be visible in gym tab"
        btn_2m.click()
        page.wait_for_timeout(100)

        t2_val = countdown.text_content().strip()
        assert t2_val in ("2:00", "02:00"), f"Expected 2:00 at start of 2m timer, got {t2_val}"

        # Wait 1.1s and verify countdown decrements
        page.wait_for_timeout(1150)
        t3_val = countdown.text_content().strip()
        assert t3_val in ("1:59", "01:59", "1:58"), f"Expected countdown to decrement to 1:59, got {t3_val}"

        # 3. Test cancellation
        cancel_btn = page.locator("#rest-timer-banner button[onclick*='cancelRestTimer']").first
        assert cancel_btn.is_visible(), "Cancel button must be visible in rest timer banner"
        cancel_btn.click()
        page.wait_for_timeout(150)

        assert not banner.is_visible(), "Rest timer banner must be hidden after cancelRestTimer()"

        # Verify interval is truly stopped after cancellation
        val_after_cancel = countdown.text_content().strip()
        page.wait_for_timeout(1200)
        val_after_wait = countdown.text_content().strip()
        assert val_after_cancel == val_after_wait, f"Timer continued ticking after cancellation: {val_after_cancel} -> {val_after_wait}"

        browser.close()


def test_rest_timer_audio_oscillator_and_completion_alert():
    """Empirically test Web Audio oscillator initialization, 880Hz frequency, and ¡LISTO! visual alert."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(PROTOTYPE_URL, wait_until="networkidle")

        page.evaluate("switchTab('gym')")
        page.wait_for_timeout(200)

        # Inject Web Audio API spy in browser context
        page.evaluate("""() => {
            window.__audioLog = [];
            const OrigAudioContext = window.AudioContext || window.webkitAudioContext;
            window.AudioContext = class extends OrigAudioContext {
                constructor() {
                    super();
                    window.__audioLog.push({ type: 'AudioContext_created', time: this.currentTime });
                }
                createOscillator() {
                    const osc = super.createOscillator();
                    const origSetVal = osc.frequency.setValueAtTime.bind(osc.frequency);
                    osc.frequency.setValueAtTime = function(val, time) {
                        window.__audioLog.push({ type: 'osc_frequency', value: val, time: time });
                        return origSetVal(val, time);
                    };
                    const origStart = osc.start.bind(osc);
                    osc.start = function() {
                        window.__audioLog.push({ type: 'osc_start', oscType: osc.type });
                        return origStart();
                    };
                    const origStop = osc.stop.bind(osc);
                    osc.stop = function(time) {
                        window.__audioLog.push({ type: 'osc_stop', stopTime: time });
                        return origStop(time);
                    };
                    return osc;
                }
                createGain() {
                    const gain = super.createGain();
                    const origRamp = gain.gain.exponentialRampToValueAtTime.bind(gain.gain);
                    gain.gain.exponentialRampToValueAtTime = function(val, time) {
                        window.__audioLog.push({ type: 'gain_exponential_ramp', target: val, time: time });
                        return origRamp(val, time);
                    };
                    return gain;
                }
            };
        }""")

        # Fast-forward test: start timer with 1 second remaining
        page.evaluate("""() => {
            startRestTimer(1);
        }""")
        page.wait_for_timeout(100)

        banner = page.locator("#rest-timer-banner")
        countdown = page.locator("#rest-timer-countdown")
        assert banner.is_visible()

        # Wait 1.2s for countdown to hit 0 and trigger completion
        page.wait_for_timeout(1200)

        # 1. Verify ¡LISTO! text
        assert "¡LISTO!" in countdown.text_content(), f"Expected ¡LISTO!, got {countdown.text_content()}"

        # 2. Verify emerald visual styling
        banner_class = banner.get_attribute("class") or ""
        assert "border-emerald-500" in banner_class, f"Banner must get border-emerald-500, got: {banner_class}"

        # 3. Verify audio logs recorded by spy
        audio_log = page.evaluate("() => window.__audioLog")
        assert len(audio_log) > 0, "Audio operations must be recorded"

        freq_events = [e for e in audio_log if e.get("type") == "osc_frequency"]
        assert len(freq_events) >= 1, f"Expected osc_frequency event, got: {audio_log}"
        assert freq_events[0]["value"] == 880, f"Oscillator frequency must be exactly 880 Hz (La5), got {freq_events[0]['value']}"

        start_events = [e for e in audio_log if e.get("type") == "osc_start"]
        assert len(start_events) >= 1, "Oscillator must be started"
        assert start_events[0]["oscType"] == "sine", f"Oscillator type must be sine, got {start_events[0]['oscType']}"

        ramp_events = [e for e in audio_log if e.get("type") == "gain_exponential_ramp"]
        assert len(ramp_events) >= 1, "Gain exponential ramp must be applied for audio envelope"
        assert ramp_events[0]["target"] == 0.001, f"Gain ramp target must be 0.001, got {ramp_events[0]['target']}"

        # 4. Verify auto-hide after 2500ms
        page.wait_for_timeout(2600)
        assert not banner.is_visible(), "Banner should auto-hide after 2.5s"

        browser.close()


# =============================================================================
# 2. INPUT DEBOUNCE (600MS) & NETWORK TRAFFIC THROTTLING STRESS-TEST
# =============================================================================

def test_debounce_network_throttling_and_badge_transitions():
    """Verify that rapid consecutive clicks dispatch ONLY 1 fetch after 600ms, and verify badge transitions."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(PROTOTYPE_URL, wait_until="networkidle")

        page.evaluate("switchTab('gym')")
        page.wait_for_timeout(200)

        # Spy on window.fetch and track outgoing network requests to /api/save_gym_session
        page.evaluate("""() => {
            window.__fetchCalls = [];
            window.__mockFail = false;
            const origFetch = window.fetch;
            window.fetch = function(url, options) {
                if (typeof url === 'string' && url.includes('/api/save_gym_session')) {
                    window.__fetchCalls.push({
                        url: url,
                        options: options,
                        timestamp: Date.now()
                    });
                    if (window.__mockFail) {
                        return Promise.reject(new Error('Network offline or 500'));
                    }
                    return Promise.resolve({
                        ok: true,
                        status: 200,
                        json: async () => ({ ok: true, key: 'gym_session_2026-11-16' })
                    });
                }
                return origFetch(url, options);
            };
        }""")

        badge = page.locator("#gym-sync-status")
        assert badge.is_visible(), "Gym sync status badge must be present"

        # 1. Burst test: Rapidly trigger 5 stepper clicks spaced by 40ms (burst finishes at 160ms)
        page.evaluate("""() => {
            const btn = document.querySelector("button[onclick*='stepWeight']");
            for (let i = 0; i < 5; i++) {
                setTimeout(() => {
                    const b = document.querySelector("button[onclick*='stepWeight']");
                    if (b) b.click();
                }, i * 40);
            }
        }""")

        # Wait 50ms for first click to trigger
        page.wait_for_timeout(50)

        # Immediately after clicks start, badge must display saving indicator
        badge_immediate = badge.text_content().strip()
        assert "Guardando en nube..." in badge_immediate, f"Badge should be '🟡 Guardando en nube...', got '{badge_immediate}'"

        # At t=250ms (90ms after last click at 160ms): 0 fetch calls (< 600ms debounce)
        page.wait_for_timeout(200)
        calls_at_250 = page.evaluate("() => window.__fetchCalls.length")
        assert calls_at_250 == 0, f"Expected 0 fetch calls at 250ms (before 600ms debounce), got {calls_at_250}"

        # At t=500ms (340ms after last click < 600ms): STILL 0 fetch calls
        page.wait_for_timeout(250)
        calls_at_500 = page.evaluate("() => window.__fetchCalls.length")
        assert calls_at_500 == 0, f"Expected 0 fetch calls at 500ms (before 600ms debounce), got {calls_at_500}"

        # Wait additional 450ms (total time elapsed since last click > 750ms > 600ms)
        page.wait_for_timeout(450)
        calls_after_debounce = page.evaluate("() => window.__fetchCalls.length")
        assert calls_after_debounce == 1, f"Expected EXACTLY 1 fetch call dispatched after 600ms debounce, got {calls_after_debounce}"

        # Verify badge transitioned to "🟢 Sincronizado en KV"
        page.wait_for_timeout(100)
        badge_synced = badge.text_content().strip()
        assert "Sincronizado en KV" in badge_synced, f"Badge must be '🟢 Sincronizado en KV', got '{badge_synced}'"
        assert "text-emerald-400" in (badge.get_attribute("class") or ""), "Badge must have emerald text"

        # Verify payload sent in the single throttled fetch call
        fetch_call = page.evaluate("() => window.__fetchCalls[0]")
        body = json.loads(fetch_call["options"]["body"])
        assert "routine_id" in body
        assert "state" in body
        assert "date" in body

        # 2. Test Offline / Network Error Fallback Badge Transition
        # Set mock to fail
        page.evaluate("() => { window.__mockFail = true; }")

        # Trigger save
        page.evaluate("""() => {
            const btn = document.querySelector("button[onclick*='stepWeight']");
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(50)

        badge_saving = badge.text_content().strip()
        assert "Guardando en nube..." in badge_saving

        # Wait for debounce (> 600ms)
        page.wait_for_timeout(750)

        # Total calls should now be 2
        total_calls = page.evaluate("() => window.__fetchCalls.length")
        assert total_calls == 2, f"Expected 2 total fetch calls, got {total_calls}"

        # Badge must catch error and show "⚪ Modo local (offline)"
        badge_offline = badge.text_content().strip()
        assert "Modo local (offline)" in badge_offline, f"Badge must transition to '⚪ Modo local (offline)', got '{badge_offline}'"
        assert "#C4B9C8" in (badge.get_attribute("class") or ""), "Badge offline text must use #C4B9C8"

        browser.close()


# =============================================================================
# 3. MATHEMATICAL COLOR CONTRAST VERIFICATION (WCAG 2.1 AA >= 4.5:1)
# =============================================================================

def srgb_to_relative_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance according to WCAG 2.1 specification."""
    def channel_lum(val: int) -> float:
        c = val / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * channel_lum(r) + 0.7152 * channel_lum(g) + 0.0722 * channel_lum(b)

def hex_to_rgb(hex_code: str):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def calculate_contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    """Calculate contrast ratio between two hex colors according to WCAG 2.1."""
    lum1 = srgb_to_relative_luminance(*hex_to_rgb(fg_hex))
    lum2 = srgb_to_relative_luminance(*hex_to_rgb(bg_hex))
    l_max = max(lum1, lum2)
    l_min = min(lum1, lum2)
    return (l_max + 0.05) / (l_min + 0.05)


def test_secondary_typography_contrast_ratio():
    """Verify #C4B9C8 satisfies WCAG AA (>= 4.5:1) across ALL dark backgrounds used in the application."""
    secondary_text = "#C4B9C8"
    legacy_text = "#A297A6"

    # All dark background surfaces in Aegis Coach
    dark_surfaces = [
        ("#171821", "Primary dashboard background"),
        ("#181622", "Card container background"),
        ("#25283D", "Dark accent section background"),
        ("#292631", "Card header and pill background"),
        ("#3d3846", "Elevated button / border hover surface"),
        ("#0f0c13", "Base viewport dark background"),
    ]

    for bg_hex, name in dark_surfaces:
        ratio = calculate_contrast_ratio(secondary_text, bg_hex)
        assert ratio >= 4.5, f"Contrast ratio for {secondary_text} against {bg_hex} ({name}) must be >= 4.5:1, got {ratio:.2f}:1"

    # Confirm legacy #A297A6 fails on #3d3846 (< 4.5:1), demonstrating why migration was necessary
    legacy_ratio = calculate_contrast_ratio(legacy_text, "#3d3846")
    assert legacy_ratio < 4.5, f"Legacy color #A297A6 should fail WCAG AA on #3d3846, got {legacy_ratio:.2f}:1"


def test_zero_occurrences_of_legacy_contrast_color():
    """Verify zero occurrences of deprecated #A297A6 across production files."""
    with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
        ts_content = f.read()
    assert "#A297A6" not in ts_content, "Deprecated low-contrast #A297A6 must be 0 in cloudflare/src/index.ts"
    assert ts_content.count("#C4B9C8") >= 50, f"Production index.ts must widely use #C4B9C8 (found {ts_content.count('#C4B9C8')})"

    with open(PROTOTYPE_PATH, 'r', encoding='utf-8') as f:
        proto_content = f.read()
    assert "#A297A6" not in proto_content, "Deprecated low-contrast #A297A6 must be 0 in prototype/index.html"
    assert proto_content.count("#C4B9C8") >= 50, f"Prototype index.html must widely use #C4B9C8 (found {proto_content.count('#C4B9C8')})"
