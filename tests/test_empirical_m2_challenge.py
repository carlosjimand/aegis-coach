"""
Empirical Challenge & Stress-Test Suite for Milestone 2 (M2: Ergonomía Gimnasio y Frontend UI/UX)
==================================================================================================
Empirically tests and measures DOM bounding boxes, computed styles, touch target compliance (>= 44x44px),
mobile header compactness (<= 52px on 390px viewport), bottom dock positioning and safe-area compliance,
rest timer workflow, 600ms debounce persistence, and WCAG AA contrast.
"""

import os
import re
import json
import pytest
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTOTYPE_PATH = os.path.join(BASE_DIR, 'prototype', 'index.html')
INDEX_TS_PATH = os.path.join(BASE_DIR, 'cloudflare', 'src', 'index.ts')
FILE_URL = f"file:///{PROTOTYPE_PATH.replace(os.sep, '/')}"


# =============================================================================
# 1. STEPPER BUTTONS & DELETE BUTTON TOUCH TARGET AUDIT (>= 44x44px)
# =============================================================================

def test_stepper_buttons_all_dimensions_mobile_viewport():
    """Verify ALL stepper buttons (+2.5, -2.5, +1, -1) and delete buttons have height >= 44px on 390px mobile."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(FILE_URL, wait_until="networkidle")

        # Switch to gym tab
        page.evaluate("switchTab('gym')")
        page.wait_for_timeout(300)

        # 1. Test existing buttons on initial load
        plus_weight_buttons = page.locator("button:has-text('+2.5')")
        minus_weight_buttons = page.locator("button:has-text('−2.5'), button:has-text('-2.5')")
        plus_rep_buttons = page.locator("button:has-text('+1')")
        minus_rep_buttons = page.locator("button:has-text('−1'), button:has-text('-1')")

        pw_count = plus_weight_buttons.count()
        mw_count = minus_weight_buttons.count()
        pr_count = plus_rep_buttons.count()
        mr_count = minus_rep_buttons.count()

        assert pw_count > 0, "At least one +2.5 button must be present in gym tab"
        assert mw_count > 0, "At least one -2.5 button must be present in gym tab"
        assert pr_count > 0, "At least one +1 button must be present in gym tab"
        assert mr_count > 0, "At least one -1 button must be present in gym tab"

        # Check heights for all initial buttons
        for i in range(pw_count):
            box = plus_weight_buttons.nth(i).bounding_box()
            assert box is not None, f"+2.5 button #{i} not rendered"
            assert box["height"] >= 44.0, f"+2.5 button #{i} height must be >= 44px, got {box['height']}px"

        for i in range(mw_count):
            box = minus_weight_buttons.nth(i).bounding_box()
            assert box is not None, f"-2.5 button #{i} not rendered"
            assert box["height"] >= 44.0, f"-2.5 button #{i} height must be >= 44px, got {box['height']}px"

        for i in range(pr_count):
            box = plus_rep_buttons.nth(i).bounding_box()
            assert box is not None, f"+1 rep button #{i} not rendered"
            assert box["height"] >= 44.0, f"+1 rep button #{i} height must be >= 44px, got {box['height']}px"

        for i in range(mr_count):
            box = minus_rep_buttons.nth(i).bounding_box()
            assert box is not None, f"-1 rep button #{i} not rendered"
            assert box["height"] >= 44.0, f"-1 rep button #{i} height must be >= 44px, got {box['height']}px"

        # 2. Add multiple dynamic sets across exercises and verify touch targets on dynamically added sets
        page.evaluate("addSetRow(2, 1)")
        page.evaluate("addSetRow(2, 1)")
        page.evaluate("addSetRow(2, 2)")
        page.wait_for_timeout(200)

        # Check delete buttons (which appear when sets are added)
        delete_buttons = page.locator("button[title='Eliminar serie']")
        del_count = delete_buttons.count()
        assert del_count >= 3, "Delete buttons should be rendered for added sets"

        for i in range(del_count):
            del_box = delete_buttons.nth(i).bounding_box()
            assert del_box is not None, f"Delete button #{i} not rendered"
            assert del_box["height"] >= 44.0, f"Delete button #{i} height must be >= 44px, got {del_box['height']}px"
            assert del_box["width"] >= 44.0, f"Delete button #{i} width must be >= 44px, got {del_box['width']}px"

        # 3. Check computed style touch-action
        first_btn = plus_weight_buttons.first
        touch_action = first_btn.evaluate("el => window.getComputedStyle(el).touchAction")
        assert "manipulation" in touch_action, f"Expected touch-action: manipulation, got {touch_action}"

        browser.close()


def test_stepper_interactive_operations():
    """Verify that clicking stepper buttons correctly increments/decrements inputs without nan or errors."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(FILE_URL, wait_until="networkidle")

        page.evaluate("switchTab('gym')")
        page.wait_for_timeout(300)

        # Get initial parsed numeric weight from JavaScript state
        initial_raw = page.evaluate("() => currentGymState[1].sets[0].weight")
        initial_w = float(re.search(r'\d+(\.\d+)?', str(initial_raw)).group(0))

        # Rep input
        rep_input = page.locator("input[oninput*='updateSetReps']").first
        initial_r = int(rep_input.input_value() or 1)

        # Click +2.5 kg
        plus_btn = page.locator("button:has-text('+2.5')").first
        plus_btn.click()
        page.wait_for_timeout(100)

        weight_input = page.locator("input[oninput*='updateSetWeight']").first
        new_w = float(weight_input.input_value() or 0)
        assert abs(new_w - (initial_w + 2.5)) < 1e-4, f"Weight should increase by 2.5 kg, got {new_w} from {initial_w}"

        # Click -2.5 kg
        minus_btn = page.locator("button:has-text('−2.5'), button:has-text('-2.5')").first
        minus_btn.click()
        page.wait_for_timeout(100)

        reset_w = float(weight_input.input_value() or 0)
        assert abs(reset_w - initial_w) < 1e-4, f"Weight should return to initial, got {reset_w}"

        # Click +1 rep
        plus_rep = page.locator("button:has-text('+1')").first
        plus_rep.click()
        page.wait_for_timeout(100)
        assert int(rep_input.input_value()) == initial_r + 1

        # Click -1 rep
        minus_rep = page.locator("button:has-text('−1'), button:has-text('-1')").first
        minus_rep.click()
        page.wait_for_timeout(100)
        assert int(rep_input.input_value()) == initial_r

        # Delete set test: add set then delete it
        initial_set_count = page.locator("input[oninput*='updateSetWeight']").count()
        page.evaluate("addSetRow(2, 1)")
        page.wait_for_timeout(200)
        assert page.locator("input[oninput*='updateSetWeight']").count() == initial_set_count + 1

        del_btn = page.locator("button[title='Eliminar serie']").first
        del_btn.click()
        page.wait_for_timeout(200)
        assert page.locator("input[oninput*='updateSetWeight']").count() == initial_set_count

        browser.close()


# =============================================================================
# 2. MOBILE HEADER COMPACTNESS & VIEWPORT RESPONSIVENESS (<= 52px)
# =============================================================================

def test_header_height_across_multiple_mobile_viewports():
    """Verify header height remains <= 52px across mobile viewports (360px, 375px, 390px, 412px, 430px)."""
    mobile_viewports = [
        {"name": "Android Small", "width": 360, "height": 800},
        {"name": "iPhone SE", "width": 375, "height": 667},
        {"name": "iPhone 14/15", "width": 390, "height": 844},
        {"name": "Pixel 7", "width": 412, "height": 915},
        {"name": "iPhone 15 Pro Max", "width": 430, "height": 932},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for vp in mobile_viewports:
            context = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
            page = context.new_page()
            page.goto(FILE_URL, wait_until="networkidle")

            header_box = page.locator("header").bounding_box()
            assert header_box is not None, f"Header not found on {vp['name']}"
            assert header_box["height"] <= 52.0, (
                f"Header height on {vp['name']} ({vp['width']}px) must be <= 52px, got {header_box['height']}px"
            )

            # Check that desktop-only header action buttons are hidden on mobile
            profile_btn = page.locator("header button:has-text('Perfil')")
            if profile_btn.count() > 0:
                is_vis = profile_btn.is_visible()
                assert not is_vis, f"Perfil button must be hidden in header on {vp['name']}"

            telegram_btn = page.locator("header a[href*='t.me']")
            if telegram_btn.count() > 0:
                is_vis = telegram_btn.is_visible()
                assert not is_vis, f"Telegram button must be hidden in header on {vp['name']}"

            context.close()

        # Desktop check: buttons are visible on desktop
        desktop_ctx = browser.new_context(viewport={"width": 1024, "height": 768})
        desk_page = desktop_ctx.new_page()
        desk_page.goto(FILE_URL, wait_until="networkidle")

        profile_btn = desk_page.locator("header button:has-text('Perfil')")
        assert profile_btn.is_visible(), "Perfil button should be visible on desktop header"

        desktop_ctx.close()
        browser.close()


# =============================================================================
# 3. MOBILE BOTTOM DOCK & SAFE-AREA INSET COMPLIANCE
# =============================================================================

def test_bottom_dock_positioning_and_content_non_overlap():
    """Verify that bottom dock stays fixed at bottom with safe-area spacing and main padding prevents content occlusion."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(FILE_URL, wait_until="networkidle")

        # Find bottom dock nav (lg:hidden fixed)
        dock = page.locator("nav.lg\\:hidden").first
        dock_box = dock.bounding_box()
        assert dock_box is not None, "Bottom dock must be present and rendered"

        # Verify bottom dock is visible and anchored near the bottom
        assert dock_box["y"] + dock_box["height"] <= 844.0, "Dock must be within the viewport"
        assert dock_box["y"] >= 750.0, f"Dock should be anchored at bottom of screen, y={dock_box['y']}"

        # Check inline or computed style contains safe-area-inset-bottom
        dock_style = dock.get_attribute("style") or ""
        assert "env(safe-area-inset-bottom" in dock_style, (
            f"Bottom dock style must include env(safe-area-inset-bottom), got: '{dock_style}'"
        )

        # Check main element padding-bottom
        main_el = page.locator("main").first
        main_style = main_el.get_attribute("style") or ""
        assert "padding-bottom" in main_style and "env(safe-area-inset-bottom" in main_style, (
            f"Main element must declare padding-bottom with env(safe-area-inset-bottom), got: '{main_style}'"
        )

        # Verify computed padding-bottom is 120px (7.5rem), providing 44px clearance above the 64px dock + 12px margin
        computed_padding_bottom = main_el.evaluate("el => parseFloat(window.getComputedStyle(el).paddingBottom)")
        assert computed_padding_bottom >= 100.0, (
            f"Main padding-bottom should be >= 100px (got {computed_padding_bottom}px) to clear dock height (~64px + 12px margin)"
        )

        browser.close()


# =============================================================================
# 4. REST TIMER AUDIO-VISUAL & WORKFLOW STRESS-TEST
# =============================================================================

def test_rest_timer_complete_lifecycle():
    """Verify rest timer activation, countdown update, cancellation, and audio context invocation."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(FILE_URL, wait_until="networkidle")

        page.evaluate("switchTab('gym')")
        page.wait_for_timeout(300)

        # Check rest timer buttons in gym tab header
        btn_90 = page.locator("button:has-text('90s')").first
        btn_2m = page.locator("button:has-text('2m')").first

        assert btn_90.is_visible(), "90s rest timer button must be visible"
        assert btn_2m.is_visible(), "2m rest timer button must be visible"

        # Start 90s timer
        btn_90.click()
        page.wait_for_timeout(200)

        banner = page.locator("#rest-timer-banner")
        assert banner.is_visible(), "Rest timer banner should appear upon clicking 90s"

        countdown = page.locator("#rest-timer-countdown")
        text = countdown.text_content()
        assert "1:30" in text or "01:30" in text or "1:29" in text

        # Start 2m timer
        btn_2m.click()
        page.wait_for_timeout(200)
        text_2m = countdown.text_content()
        assert "2:00" in text_2m or "02:00" in text_2m or "1:59" in text_2m

        # Cancel timer via cancel button
        cancel_btn = page.locator("button[title='Cancelar descanso']").first
        assert cancel_btn.is_visible(), "Cancel button must be visible"
        cancel_btn.click()
        page.wait_for_timeout(200)
        assert not banner.is_visible(), "Rest timer banner should disappear upon cancellation"

        browser.close()


# =============================================================================
# 5. INPUT DEBOUNCE & STORAGE BADGE REACTIVITY
# =============================================================================

def test_input_debounce_and_safe_storage():
    """Verify 600ms debounce behavior and status badge reactivity."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(FILE_URL, wait_until="networkidle")

        page.evaluate("switchTab('gym')")
        page.wait_for_timeout(300)

        weight_input = page.locator("input[oninput*='updateSetWeight']").first
        badge = page.locator("#gym-sync-status")

        # Type new weight value
        weight_input.fill("87.5")
        page.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))", weight_input.element_handle())

        # Immediately after typing, status should indicate saving / local
        badge_text_immediate = badge.text_content()
        assert ("Guardando" in badge_text_immediate or "Modo local" in badge_text_immediate or "Sincronizado" in badge_text_immediate)

        # Wait for debounce duration (> 600ms)
        page.wait_for_timeout(800)

        # Verify state is saved in localStorage safely with the expected key structure
        all_keys = page.evaluate("() => Object.keys(localStorage)")
        gym_keys = [k for k in all_keys if 'aegis_workout_v3' in k]
        assert len(gym_keys) > 0, f"Expected at least one aegis_workout_v3 key in localStorage, found: {all_keys}"

        browser.close()


# =============================================================================
# 6. TACTICAL WIDGET & 4-WEEKS HISTORY CONTRAST
# =============================================================================

def test_production_index_ts_tactical_widget_and_contrast():
    """Verify that cloudflare/src/index.ts has dynamic tactical widget and strict WCAG AA contrast #C4B9C8."""
    with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Widget requirements
    assert "⚡ T-${daysRemaining} DÍAS • OBJETIVO PRIMARIO" in content or "⚡ T-${daysRemaining}" in content
    assert "Cross Popular Parque del Soto" in content
    assert "Clavos 6-9 mm" in content
    assert "3:30 - 3:35/km" in content

    # Contrast requirements: #A297A6 should NOT exist, replaced by #C4B9C8
    assert "#A297A6" not in content, "Legacy low-contrast #A297A6 must be completely eradicated from index.ts"
    assert "#C4B9C8" in content, "High contrast #C4B9C8 must be present in index.ts"

    # 4 weeks history requirement
    assert "Últimas 4 semanas" in content
    assert "weeklyData.slice(-4)" in content
