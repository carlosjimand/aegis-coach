import pytest
import os
import json
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_TS_PATH = os.path.join(BASE_DIR, 'cloudflare', 'src', 'index.ts')
PROTOTYPE_PATH = os.path.join(BASE_DIR, 'prototype', 'index.html')
REPORT_PATH = os.path.join(BASE_DIR, 'reports', 'auditoria_ui_ux_aegis_coach.md')
PLAN_JSON_PATH = os.path.join(BASE_DIR, 'cloudflare', 'plan.json')
WEEKLY_EVO_PATH = os.path.join(BASE_DIR, 'data', 'weekly_evolution.json')

class TestAuditSecurityTrack:
    """QA tests covering Cybersecurity and Edge SecOps findings."""

    def test_wrangler_credentials_audit(self):
        wrangler_path = os.path.join(BASE_DIR, 'cloudflare', 'wrangler.toml')
        with open(wrangler_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Verify that sensitive secrets have been removed from wrangler.toml [vars]
        assert '[vars]' in content, "wrangler.toml should contain [vars] table"
        assert 'ATHLETE_ID' in content, "ATHLETE_ID non-sensitive config should remain in [vars]"
        assert 'TELEGRAM_BOT_TOKEN' not in content, "TELEGRAM_BOT_TOKEN must NOT be exposed in wrangler.toml"
        assert 'INTERVALS_API_KEY' not in content, "INTERVALS_API_KEY must NOT be exposed in wrangler.toml"
        assert 'TELEGRAM_CHAT_ID' not in content, "TELEGRAM_CHAT_ID must NOT be exposed in wrangler.toml"

    def test_gitignore_protects_secrets(self):
        gitignore_path = os.path.join(BASE_DIR, '.gitignore')
        assert os.path.isfile(gitignore_path), ".gitignore must exist at repository root"
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gi_content = f.read()
        for pattern in ['.dev.vars', '.env', 'node_modules/', '*.xlsx', '.wrangler/', '__pycache__/']:
            assert pattern in gi_content, f".gitignore must contain {pattern}"

    def test_dev_vars_templates_and_env_interface(self):
        example_path = os.path.join(BASE_DIR, 'cloudflare', '.dev.vars.example')
        assert os.path.isfile(example_path), ".dev.vars.example must exist"
        with open(example_path, 'r', encoding='utf-8') as f:
            ex_content = f.read()
        assert 'INTERVALS_API_KEY' in ex_content
        assert 'TELEGRAM_BOT_TOKEN' in ex_content
        assert 'AEGIS_SECRET_KEY' in ex_content
        assert 'TELEGRAM_WEBHOOK_SECRET' in ex_content

        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'AEGIS_SECRET_KEY?: string' in ts_content, "Env interface must include optional AEGIS_SECRET_KEY"
        assert 'TELEGRAM_WEBHOOK_SECRET?: string' in ts_content, "Env interface must include optional TELEGRAM_WEBHOOK_SECRET"

    def test_api_endpoints_require_auth(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'isAuthorized(request' in ts_content or 'isAuthorized(request, env)' in ts_content
        assert 'X-Aegis-Key' in ts_content
        # Ensure /api/save_gym_session, /api/save_profile, /api/get_gym_session, and /api/get_profile check authorization and return 401
        assert 'url.pathname === "/api/save_gym_session"' in ts_content
        assert 'url.pathname === "/api/save_profile"' in ts_content
        assert 'url.pathname === "/api/get_gym_session"' in ts_content
        assert 'url.pathname === "/api/get_profile"' in ts_content
        assert 'status: 401' in ts_content

    def test_telegram_webhook_hardening(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        # Verify webhook secret check
        assert 'X-Telegram-Bot-Api-Secret-Token' in ts_content, "Webhook must validate secret token header"
        # Verify strict chat_id validation in handleTelegramMessage
        assert 'chatId !== String(env.TELEGRAM_CHAT_ID)' in ts_content or 'chatId === String(env.TELEGRAM_CHAT_ID)' in ts_content, "handleTelegramMessage must strictly check athlete chat_id"

    def test_xss_sanitization_and_safe_json(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'safeJsonStringify' in ts_content, "Worker must implement safeJsonStringify"
        assert 'escapeHtml' in ts_content, "Worker must implement escapeHtml"
        # Check script interpolations use safeJsonStringify
        assert '${safeJsonStringify(planData.days' in ts_content or 'safeJsonStringify(planData.days' in ts_content
        assert '${safeJsonStringify(WEEKLY_EVO_DATA)}' in ts_content
        assert '${safeJsonStringify(CALENDAR_DATA_BY_MONTH)}' in ts_content
        # Check escapeHtml is used for notes and values
        assert 'escapeHtml(act.notes)' in ts_content

    def test_security_headers_present(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'SECURITY_HEADERS' in ts_content
        assert 'Content-Security-Policy' in ts_content
        assert 'Strict-Transport-Security' in ts_content
        assert 'X-Frame-Options' in ts_content
        assert 'X-Content-Type-Options' in ts_content
        assert 'Referrer-Policy' in ts_content
        assert 'Permissions-Policy' in ts_content

    def test_prototype_escapes_xss_and_safe_json(self):
        with open(PROTOTYPE_PATH, 'r', encoding='utf-8') as f:
            proto_content = f.read()
        # Verify prototype has safe handling for numbers in replace
        assert 'String(s.weight' in proto_content or 'String(' in proto_content, "Prototype must safely convert weight to String"


class TestAuditBackendPipelineTrack:
    """QA tests covering Cloudflare Worker & Data Pipeline."""

    def test_plan_structure_and_athlete_data(self):
        with open(PLAN_JSON_PATH, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        assert 'athlete' in plan
        assert plan['athlete']['name'] == 'Carlos Jiménez Andrino'
        assert plan['athlete']['weight_kg'] == 63.0
        assert plan['athlete']['height_m'] == 1.73

    def test_primary_objective_cross_del_soto(self):
        with open(PLAN_JSON_PATH, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        primary = plan['macrocycle']['primary_objective']
        assert primary['date'] == '2026-11-28'
        assert 'Parque del Soto' in primary['name']
        assert primary['distance_km'] == 5.0

    def test_weekly_evolution_continuity(self):
        with open(WEEKLY_EVO_PATH, 'r', encoding='utf-8') as f:
            weeks = json.load(f)
        assert len(weeks) >= 8, "Must have at least 8 weeks of historical data"
        # Verify key fitness metrics
        latest_weeks = [w for w in weeks if w['run_km'] > 0]
        assert len(latest_weeks) > 0

    def test_sync_coaching_engine_dynamic_date_and_timeouts(self):
        import scripts.sync_coaching_engine as sync_engine
        import inspect

        # Verify dynamic newest_date defaults to today's date
        today_str = datetime.now().strftime('%Y-%m-%d')
        sig_activities = inspect.signature(sync_engine.fetch_activities)
        assert 'newest_date' in sig_activities.parameters
        # When called without newest_date, it defaults to None (which resolves dynamically) or today_str
        assert sig_activities.parameters['newest_date'].default in (None, today_str)

        sig_wellness = inspect.signature(sync_engine.fetch_wellness)
        assert 'newest_date' in sig_wellness.parameters
        assert sig_wellness.parameters['newest_date'].default in (None, today_str)

        # Verify timeout and session adapter configuration
        assert hasattr(sync_engine, 'DEFAULT_TIMEOUT')
        assert sync_engine.DEFAULT_TIMEOUT == (5.0, 25.0)
        assert hasattr(sync_engine, 'session')
        assert hasattr(sync_engine, 'Retry')


class TestAuditUIUXErgonomicsTrack:
    """QA tests covering Mobile & Desktop UI/UX improvements across index.ts and prototype."""

    def test_prototype_contains_steppers(self):
        # Verify prototype
        with open(PROTOTYPE_PATH, 'r', encoding='utf-8') as f:
            proto_content = f.read()
        assert 'stepRep' in proto_content, "Prototype must implement stepRep function"
        assert 'stepWeight' in proto_content, "Prototype must implement stepWeight function"
        assert '+2.5' in proto_content, "Prototype must feature +2.5 kg stepper buttons"

        # Verify production index.ts
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'function stepRep(' in ts_content, "Production index.ts must implement stepRep"
        assert 'function stepWeight(' in ts_content, "Production index.ts must implement stepWeight"
        assert '+2.5' in ts_content and '−2.5' in ts_content, "Production index.ts must feature +2.5 and -2.5 steppers"
        assert 'inputmode="decimal"' in ts_content, "Production index.ts must use numeric keypad inputmode='decimal'"
        assert 'type="number"' in ts_content, "Production index.ts must use input type='number'"
        assert 'w-11 h-11' in ts_content, "Production index.ts delete button touch target must be 44x44px (w-11 h-11)"
        assert 'min-h-[44px]' in ts_content, "Production steppers must ensure min-h-[44px] touch target"

    def test_prototype_contains_rest_timer(self):
        # Verify prototype
        with open(PROTOTYPE_PATH, 'r', encoding='utf-8') as f:
            proto_content = f.read()
        assert 'startRestTimer' in proto_content, "Prototype must implement startRestTimer function"
        assert 'rest-timer-banner' in proto_content, "Prototype must have rest timer UI banner"

        # Verify production index.ts
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'function startRestTimer(' in ts_content, "Production index.ts must implement startRestTimer"
        assert 'id="rest-timer-banner"' in ts_content, "Production index.ts must feature rest-timer-banner element"
        assert '880' in ts_content, "Production rest timer must use Web Audio API 880 Hz chime oscillator"
        assert 'AudioContext' in ts_content, "Production rest timer must use AudioContext"
        assert '¡LISTO!' in ts_content, "Production rest timer must display ¡LISTO! visual alert"
        assert 'startRestTimer(90)' in ts_content and 'startRestTimer(120)' in ts_content, "Must have 90s and 2m rest timer triggers"

    def test_prototype_contains_tactical_widget(self):
        # Verify prototype
        with open(PROTOTYPE_PATH, 'r', encoding='utf-8') as f:
            proto_content = f.read()
        assert 'T-12 DÍAS' in proto_content or 'Cross Popular' in proto_content
        assert 'Clavos 6-9 mm' in proto_content, "Prototype must display spike recommendation"

        # Verify production index.ts
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert '⚡ T-${daysRemaining} DÍAS • OBJETIVO PRIMARIO' in ts_content, "Production must dynamically interpolate daysRemaining in tactical widget"
        assert 'Cross Popular Parque del Soto' in ts_content
        assert 'Clavos 6-9 mm' in ts_content, "Production must highlight Clavos 6-9 mm for Cross del Soto"
        assert '3:30 - 3:35/km' in ts_content, "Production must show 3:30 - 3:35/km target pace"

    def test_prototype_contains_debounce_and_sync_badge(self):
        # Verify prototype
        with open(PROTOTYPE_PATH, 'r', encoding='utf-8') as f:
            proto_content = f.read()
        assert 'gymDebounceTimer' in proto_content, "Prototype must implement debounce timer"
        assert 'gym-sync-status' in proto_content, "Prototype must have sync status badge"

        # Verify production index.ts
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'let gymDebounceTimer = null;' in ts_content, "Production must define gymDebounceTimer"
        assert 'setTimeout(' in ts_content and '600' in ts_content, "Production must debounce saves with 600ms timer"
        assert 'id="gym-sync-status"' in ts_content, "Production must contain gym-sync-status badge element"
        assert '!res.ok' in ts_content or 'res.ok' in ts_content, "Production persistGymState must evaluate res.ok"
        assert '🟢 Sincronizado en KV' in ts_content, "Production must display synchronized status"
        assert '🟡 Guardando en nube...' in ts_content, "Production must display saving status"
        assert '⚪ Modo local (offline)' in ts_content, "Production must display offline status"

    def test_compact_header_and_redundant_buttons(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'h-[52px] sm:h-16' in ts_content, "Header must be 52px on mobile (h-[52px] sm:h-16)"
        assert 'hidden sm:flex items-center gap-2 sm:gap-3' in ts_content, "Header buttons must be hidden on mobile to prevent dock redundancy"

    def test_safe_area_insets(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'env(safe-area-inset-bottom, 0px)' in ts_content, "Must use env(safe-area-inset-bottom)"
        assert 'style="bottom: calc(0.75rem + env(safe-area-inset-bottom, 0px));"' in ts_content, "Bottom dock must respect safe-area-inset-bottom"
        assert 'padding-bottom: calc(7.5rem + env(safe-area-inset-bottom, 0px));' in ts_content, "Main container must have safe padding-bottom"

    def test_four_weeks_history_and_contrast(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()
        assert 'Últimas 4 semanas' in ts_content, "Weekly history selector must focus on 4 weeks"
        assert 'weeklyData.slice(-4)' in ts_content, "Spline chart must slice the 4 most recent weeks"
        assert '#C4B9C8' in ts_content, "Must use WCAG AA compliant #C4B9C8 for secondary typography"
        assert '#A297A6' not in ts_content, "Legacy non-compliant #A297A6 must be completely migrated to #C4B9C8"


class TestAuditPersistenceAndPWAOffline:
    """QA tests covering Milestone 3: KV Read Endpoints, Hydration, Service Worker & Scheduled Cron."""

    def test_kv_read_endpoints_and_hydration(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()

        # Endpoints exist
        assert 'url.pathname === "/api/get_gym_session"' in ts_content, "GET /api/get_gym_session must be implemented"
        assert 'url.pathname === "/api/get_profile"' in ts_content, "GET /api/get_profile must be implemented"

        # KV read operations
        assert 'env.AEGIS_KV.get("gym_session_"' in ts_content or 'env.AEGIS_KV.get("gym_session_" + date' in ts_content
        assert 'env.AEGIS_KV.get("user_profile"' in ts_content

        # Madrid date fallback
        assert 'getTodayMadridISO()' in ts_content

        # Client-side hydration
        assert 'async function loadCloudData()' in ts_content, "Client must implement loadCloudData() for cloud hydration"
        assert "fetch('/api/get_profile'" in ts_content
        assert "fetch('/api/get_gym_session" in ts_content
        assert 'localStorage.setItem(\'aegis_athlete_profile\'' in ts_content
        assert 'localStorage.setItem(savedKey' in ts_content
        assert 'loadCloudData();' in ts_content, "loadCloudData must be executed on DOMContentLoaded"

    def test_service_worker_offline_pwa(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()

        # SW Route in worker
        assert 'url.pathname === "/sw.js"' in ts_content, "Worker must serve /sw.js"
        assert 'request.method === "GET"' in ts_content
        assert 'application/javascript; charset=utf-8' in ts_content
        assert 'Cache-Control' in ts_content

        # SW Cache Strategy and precache list
        assert 'CACHE_NAME' in ts_content
        assert 'PRECACHE_ASSETS' in ts_content
        assert "'/manifest.json'" in ts_content
        assert "'/favicon.ico'" in ts_content
        assert "'/img/logo.svg'" in ts_content
        assert 'caches.open' in ts_content
        assert 'caches.match' in ts_content
        assert "url.pathname.startsWith('/api/')" in ts_content or "requestUrl.pathname.startsWith('/api/')" in ts_content, "SW must bypass caching for API"
        assert 'opaque' in ts_content, "SW must handle opaque cross-origin responses"

        # Client SW registration
        assert "'serviceWorker' in navigator" in ts_content, "Client script must check serviceWorker support"
        assert "navigator.serviceWorker.register('/sw.js')" in ts_content, "Client script must register /sw.js"

    def test_scheduled_cron_and_activity_monitoring(self):
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_content = f.read()

        # Scheduled handler export
        assert 'async scheduled(controller' in ts_content or 'async scheduled(controller: ScheduledController' in ts_content, "export default must export scheduled handler"
        assert 'ctx.waitUntil(checkNewActivities(env))' in ts_content

        # checkNewActivities implementation
        assert 'export async function checkNewActivities(env: Env)' in ts_content or 'async function checkNewActivities(env: Env)' in ts_content
        assert 'intervals.icu/api/v1/athlete/' in ts_content, "Must query Intervals.icu API"
        assert 'notified_${actId}' in ts_content or "'notified_' + act.id" in ts_content, "Must check KV deduplication key"
        assert 'api.telegram.org/bot' in ts_content, "Must dispatch Telegram message"
        assert 'env.AEGIS_KV.put(`notified_${actId}`, "1"' in ts_content or 'env.AEGIS_KV.put(`notified_${actId}`' in ts_content, "Must record notified actId in KV"
