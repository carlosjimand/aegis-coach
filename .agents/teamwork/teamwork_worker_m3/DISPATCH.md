## 2026-11-16T15:22:13Z
You are a Worker agent implementing Milestone 3 (M3: Persistencia Cloudflare KV & PWA Offline Total) for Aegis Coach.

Working directory: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach
State folder: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\teamwork\teamwork_worker_m3

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Mandatory reading before starting:
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\teamwork\ORIGINAL_REQUEST.md
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\PROJECT.md
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\teamwork\teamwork_explorer_survey_3\handoff.md

Your Scope of Work:
1. [F14: Endpoints de lectura en KV & Sincronización Bidireccional]:
   - In `cloudflare/src/index.ts`:
     - Implement `GET /api/get_gym_session`: read `date` query param (defaulting to Madrid ISO today), query `env.AEGIS_KV.get("gym_session_" + date, { type: "json" })`, return JSON response with `SECURITY_HEADERS`. Require auth via `isAuthorized(request, env)` (401 if unauthorized).
     - Implement `GET /api/get_profile`: query `env.AEGIS_KV.get("user_profile", { type: "json" })`, return JSON response with `SECURITY_HEADERS`. Require auth via `isAuthorized(request, env)` (401 if unauthorized).
     - In frontend client script in `cloudflare/src/index.ts`: Implement hydration on page load (`loadCloudData()`) that queries `GET /api/get_profile` and `GET /api/get_gym_session` using `X-Aegis-Key`, updating `localStorage` and refreshing the UI so data saved on mobile is instantly reflected on desktop and vice-versa.
2. [F15: Service Worker Offline (`/sw.js`) y Registro PWA]:
   - In `cloudflare/src/index.ts`:
     - Add route `if (url.pathname === "/sw.js" && request.method === "GET")`: return JavaScript service worker with Cache-First / Stale-While-Revalidate caching for static shell (`/`, `/manifest.json`, `/favicon.ico`, `/img/logo.svg`) and CDN assets (Tailwind, Lucide, Chart.js, Google Fonts). Handle opaque cross-origin requests gracefully without throwing. Headers: `Content-Type: application/javascript; charset=utf-8`, `Cache-Control: no-cache`, plus `SECURITY_HEADERS`.
     - In client HTML `<script>`: Register the Service Worker via:
       ```javascript
       if ('serviceWorker' in navigator) {
         window.addEventListener('load', () => {
           navigator.serviceWorker.register('/sw.js').catch(err => console.warn('SW registration failed:', err));
         });
       }
       ```
3. [F16: Handler Scheduled (Cron cada 4 horas)]:
   - In `cloudflare/src/index.ts`:
     - In `export default`:
       ```typescript
       export default {
         async fetch(request: Request, env: Env): Promise<Response> { ... },
         async scheduled(controller: ScheduledController, env: Env, ctx: ExecutionContext): Promise<void> {
           ctx.waitUntil(checkNewActivities(env));
         }
       };
       ```
     - Implement `checkNewActivities(env: Env)`: query Intervals.icu API (`https://intervals.icu/api/v1/athlete/${env.ATHLETE_ID}/activities`), check `env.AEGIS_KV.get('notified_' + act.id)`, format Telegram alert summary in Markdown, dispatch via `https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage` to `env.TELEGRAM_CHAT_ID`, and record `await env.AEGIS_KV.put('notified_' + act.id, '1')`. Wrap in try/catch with proper timeouts.
4. Verification:
   - Add/update tests in `tests/test_audit_suite.py` asserting that `GET /api/get_gym_session` and `GET /api/get_profile` return expected status and require auth, that `/sw.js` is served and registered, and that `scheduled` is exported in `cloudflare/src/index.ts`.
   - Run `python -m pytest tests/` (confirm 100% pass).
   - Run `cd cloudflare && npx wrangler deploy --dry-run` (confirm 0 errors).
