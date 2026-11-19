# Handoff Report: Survey Ciberseguridad y Backend (Requirement R1)

- **Date:** 2026-11-16
- **Author:** Explorer 1 (Survey Ciberseguridad & Backend Pipeline)
- **Target Component:** Aegis Coach — Requirement R1 (Ciberseguridad y Correcciones Críticas)
- **State Folder:** `c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\teamwork\teamwork_explorer_survey_1`

---

## 1. Observation

### 1.1 Secrets Management and Storage
- **`cloudflare/wrangler.toml` (lines 12–16):**
  Sensitive production credentials are hardcoded under the public `[vars]` table:
  ```toml
  [vars]
  ATHLETE_ID = "i690671"
  INTERVALS_API_KEY = "4cvqxm8a5intat925ttdcmpja"
  TELEGRAM_BOT_TOKEN = "8241016023:AAETPRI5gvisT4OayuLKdvYewAOPUOxTNtI"
  TELEGRAM_CHAT_ID = "641498158"
  ```
- **`cloudflare/src/index.ts` (lines 12–18):**
  The `Env` interface expects these variables from the environment but lacks typing for an API key or webhook secret:
  ```typescript
  export interface Env {
    AEGIS_KV: KVNamespace;
    ATHLETE_ID: string;
    INTERVALS_API_KEY: string;
    TELEGRAM_BOT_TOKEN: string;
    TELEGRAM_CHAT_ID: string;
  }
  ```
  `AEGIS_SECRET_KEY` and `TELEGRAM_WEBHOOK_SECRET` are completely absent from `Env`.
- **`scripts/sync_coaching_engine.py` (lines 14–18):**
  Credentials are directly hardcoded in the Python script:
  ```python
  ATHLETE_ID = 'i690671'
  API_KEY = '4cvqxm8a5intat925ttdcmpja'
  ```
  Additionally, identical hardcoded `api_key = '4cvqxm8a5intat925ttdcmpja'` was found in:
  - `scripts/analyze_intervals.py:7`
  - `scripts/analyze_series.py:4`
  - `scripts/check_fit.py:4`
  - `scripts/deep_inspect.py:4`
  - `scripts/dump_details.py:4`
  - `scripts/inspect_last_week.py:4`
  - `scripts/inspect_race_week.py:4`
  - `scripts/inspect_week2.py:4`
  - Root `AGENTS.md:105-107`
- **Missing configuration & gitignore:**
  Neither `.env` nor `.dev.vars` exists in the repository. Furthermore, there is **no `.gitignore` file** at the root or within `cloudflare/`, meaning any local environment file created could easily be committed by accident.

---

### 1.2 Authentication on `/api/save_gym_session` and `/api/save_profile`
- **`cloudflare/src/index.ts` (lines 3684–3710):**
  ```typescript
  // Endpoint: Guardar Sesión de Gimnasio
  if (url.pathname === "/api/save_gym_session" && request.method === "POST") {
    try {
      const body: any = await request.json();
      const date = body.date || getTodayMadridISO();
      const key = "gym_session_" + date;
      await env.AEGIS_KV.put(key, JSON.stringify(body));
      return new Response(JSON.stringify({ ok: true, key }), {
        headers: { "Content-Type": "application/json" }
      });
    } catch (err: any) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { "Content-Type": "application/json" } });
    }
  }

  // Endpoint: Guardar Perfil de Usuario (Peso, Altura, etc.)
  if (url.pathname === "/api/save_profile" && request.method === "POST") {
    try {
      const body: any = await request.json();
      await env.AEGIS_KV.put("user_profile", JSON.stringify(body));
      return new Response(JSON.stringify({ ok: true }), {
        headers: { "Content-Type": "application/json" }
      });
    } catch (err: any) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { "Content-Type": "application/json" } });
    }
  }
  ```
  Neither endpoint performs any header validation, token validation, or cookie inspection. Any HTTP client worldwide can send arbitrary payloads to overwrite athlete workout records or the athlete profile in Cloudflare KV.
- **Client invocation (`cloudflare/src/index.ts` lines 5288 and 5757):**
  The browser frontend calls these endpoints without transmitting any authentication header (`X-Aegis-Key` or `Authorization`).

---

### 1.3 Telegram Webhook (`/webhook`) Verification
- **`cloudflare/src/index.ts` (lines 3713–3723):**
  ```typescript
  // Webhook de Telegram
  if (url.pathname === "/webhook" && request.method === "POST") {
    try {
      const update: any = await request.json();
      if (update && update.message) {
        await handleTelegramMessage(update.message, env);
      }
      return new Response("OK", { status: 200 });
    } catch (err: any) {
      return new Response("Error", { status: 500 });
    }
  }
  ```
  - The incoming request does not check `request.headers.get("X-Telegram-Bot-Api-Secret-Token")`.
- **`cloudflare/src/index.ts` (lines 3742–3787):**
  ```typescript
  async function handleTelegramMessage(message: any, env: Env) {
    const chatId = message.chat.id;
    const text = (message.text || "").trim();
    // ... builds reply with training details, knee status, injuries, macrocycle ...
    await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: chatId,
        text: reply,
        parse_mode: "Markdown"
      })
    });
  }
  ```
  - `message.chat.id` is extracted and used directly as the destination for the response without checking if `String(chatId) === String(env.TELEGRAM_CHAT_ID)`.
  - An unauthorized user messaging the bot or posting a crafted webhook payload receives Carlos' private training details, knee pain score, and schedule.

---

### 1.4 Cross-Site Scripting (XSS) Vulnerabilities
- **Script Block JSON Injection (`cloudflare/src/index.ts` lines 4903–4906):**
  ```typescript
  <script>
    const daysData = ${JSON.stringify(planData.days || [])};
    const weeklyData = ${JSON.stringify(WEEKLY_EVO_DATA)};
    const calendarDataByMonth = ${JSON.stringify(CALENDAR_DATA_BY_MONTH)};
  ```
  Standard `JSON.stringify` does not escape the literal `</script>`. If any field in `planData` stored in KV contains `</script><script>...`, browser HTML parsers terminate the script block and execute the injected script tags.
- **Unescaped DOM Concatenation via `innerHTML` (`cloudflare/src/index.ts`):**
  - Line 5588–5591:
    ```javascript
    notesContainer.innerHTML = '<div class="mt-3 p-3.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-xs text-[#A297A6] leading-relaxed">' +
      '<span class="font-bold text-white block mb-1">📝 Notas de Carlos (Garmin):</span>' +
      '<div class="whitespace-pre-line text-white/90">' + act.notes + '</div>' +
    '</div>';
    ```
    `act.notes` (originating from Garmin / Intervals.icu activity descriptions) is directly inserted into `innerHTML`.
  - Line 5192:
    ```javascript
    '<input type="text" value="' + (currentGymState[ex.num].notes || '') + '" oninput="updateExerciseNotes(' + routineId + ', ' + ex.num + ', this.value)" ...>'
    ```
    Values in gym inputs are inserted inside double quotes without attribute escaping. Entering `"` allows breaking out of the attribute and injecting inline handlers (`onload`, `onfocus`).
  - Lines 5632–5660:
    `day.day_name`, `day.running.title`, `day.gym.routine_name`, and `day.running.main_work` are concatenated directly into accordion HTML strings.
- **Utility functions:**
  Neither `escapeHtml()` nor `safeJsonStringify()` exists anywhere in `cloudflare/src/index.ts`.

---

### 1.5 HTTP Security Headers on Worker Responses
- **`cloudflare/src/index.ts` (lines 3733–3738):**
  ```typescript
  return new Response(html, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-cache, no-store, must-revalidate"
    }
  });
  ```
  The response headers include only `Content-Type` and `Cache-Control`. The following headers are entirely absent:
  - `Content-Security-Policy` (CSP)
  - `Strict-Transport-Security` (HSTS)
  - `X-Frame-Options`
  - `X-Content-Type-Options`
  - `Referrer-Policy`
  - `Permissions-Policy`

---

### 1.6 `scripts/sync_coaching_engine.py` Reliability and Timeouts
- **Hardcoded Date cutoff (lines 25 and 74):**
  ```python
  def fetch_activities(oldest_date='2026-08-15', newest_date='2026-11-15'):
  ...
  def fetch_wellness(oldest_date='2026-08-15', newest_date='2026-11-15'):
  ```
  `newest_date` is frozen at `'2026-11-15'`. Any workout logged after November 15, 2026 is silently ignored and excluded from data syncing.
- **Missing HTTP Timeouts on all Network Requests:**
  - Line 27: `requests.get(url, headers=HEADERS)` — no timeout
  - Line 35: `requests.get(url, headers=HEADERS)` — no timeout
  - Line 40: `requests.get(url, headers=HEADERS)` — no timeout
  - Line 45: `requests.get(url, headers=HEADERS)` — no timeout
  - Line 76: `requests.get(url, headers=HEADERS)` — no timeout
  In Python `requests`, calls without timeouts can hang indefinitely if the TCP socket stays open or packets drop.
- **Lack of Backoff and Retries:**
  The script loops through all activities (`for a in activities:`, line 100), issuing up to 3 HTTP requests per activity (`fetch_activity_detail`, `fetch_activity_fit_laps`, `fetch_activity_intervals`). For a 12-week cycle (~50 activities), this causes 100–150 consecutive synchronous requests. Any rate-limit (HTTP 429) or transient 500 error causes immediate data loss or corrupts the Excel output without retrying.

---

## 2. Logic Chain

1. **Exposure of Secrets $\rightarrow$ Unauthorized Cloudflare/Telegram Access:**
   Placing `TELEGRAM_BOT_TOKEN`, `INTERVALS_API_KEY`, and `TELEGRAM_CHAT_ID` in `wrangler.toml` under `[vars]` causes Wrangler to expose them as plain text environment variables rather than encrypted secrets. Because `wrangler.toml` is committed to source control and there is no `.gitignore`, these credentials are functionally public. Anyone with the bot token can impersonate the bot, delete webhooks, or inspect webhook traffic.
2. **Missing Endpoint Auth $\rightarrow$ Tampering with Athlete Data:**
   Because `/api/save_gym_session` and `/api/save_profile` accept unauthenticated POST requests from any IP address, an attacker can overwrite `gym_session_<date>` or `user_profile` in Cloudflare KV. This can alter athlete weight/height, corrupt training logs, or exhaust KV write quotas.
3. **Unvalidated Webhook $\rightarrow$ Unauthorized Information Disclosure:**
   Because `/webhook` does not validate `X-Telegram-Bot-Api-Secret-Token`, fake webhook updates can be posted directly to the Worker URL. Because `handleTelegramMessage` does not verify that `message.chat.id` equals `TELEGRAM_CHAT_ID`, any user who discovers or contacts `@aegis_coach_chatbot` can trigger commands (`/hoy`, `/semana`, `/rodilla`) and receive private medical and training data.
4. **Unescaped Content $\rightarrow$ Stored / DOM XSS:**
   Activity notes and workout details can contain characters like `<`, `>`, `"`, or `</script>`. When interpolated directly into `<script>` variables or `innerHTML` containers without `escapeHtml()` and `safeJsonStringify()`, the browser executes malicious scripts within the athlete's session context, potentially stealing `localStorage` keys or altering the UI.
5. **Missing Headers $\rightarrow$ Clickjacking and MIME Confusion:**
   Without `X-Frame-Options` or `Content-Security-Policy: frame-ancestors 'none'`, the dashboard can be embedded in an iframe on an external domain (Clickjacking). Without `X-Content-Type-Options: nosniff`, MIME sniffing attacks become possible.
6. **Hardcoded Cutoff & Missing Timeouts $\rightarrow$ Pipeline Stalling:**
   Because `newest_date='2026-11-15'`, executions on or after November 16 fail to retrieve current workouts. Because requests lack timeouts and backoff, transient network lag or rate limits cause the synchronization script to stall or fail to generate `historial_entrenamientos_carlos.xlsx`.

---

## 3. Caveats

- **No Caveats regarding Vulnerability Existence:** All 6 security and reliability issues were directly observed and confirmed in the source code.
- **Local Dev vs Cloudflare Production Secrets:** In production, Cloudflare Secrets are encrypted via `wrangler secret put <NAME>`. For local development with `wrangler dev`, secrets are loaded from `.dev.vars` (which must be added to `.gitignore`).
- **Frontend Key Storage:** For the PWA to authenticate against `/api/save_gym_session` and `/api/save_profile`, the client must possess the key. Storing it in `localStorage` or injecting an encrypted session token allows seamless offline capability while preventing anonymous external writes.

---

## 4. Conclusion & Technical Remediation Specification

To satisfy Requirement R1, the following concrete modifications must be implemented by the implementation agent:

### 4.1 Secret Migration and Environment Structure
1. Create `.gitignore` at root:
   ```gitignore
   node_modules/
   .dev.vars
   .env
   .wrangler/
   *.xlsx
   __pycache__/
   ```
2. Clean `cloudflare/wrangler.toml`:
   - Keep only non-sensitive config in `[vars]`:
     ```toml
     [vars]
     ATHLETE_ID = "i690671"
     ```
   - Remove `INTERVALS_API_KEY`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID` from `[vars]`.
3. Create `cloudflare/.dev.vars.example` and `cloudflare/.dev.vars`:
   ```bash
   ATHLETE_ID="i690671"
   INTERVALS_API_KEY="4cvqxm8a5intat925ttdcmpja"
   TELEGRAM_BOT_TOKEN="8241016023:AAETPRI5gvisT4OayuLKdvYewAOPUOxTNtI"
   TELEGRAM_CHAT_ID="641498158"
   AEGIS_SECRET_KEY="<generate_secure_random_hex>"
   TELEGRAM_WEBHOOK_SECRET="<generate_secure_random_hex>"
   ```
4. Update `cloudflare/src/index.ts` `Env` interface:
   ```typescript
   export interface Env {
     AEGIS_KV: KVNamespace;
     ATHLETE_ID: string;
     INTERVALS_API_KEY: string;
     TELEGRAM_BOT_TOKEN: string;
     TELEGRAM_CHAT_ID: string;
     AEGIS_SECRET_KEY?: string;
     TELEGRAM_WEBHOOK_SECRET?: string;
   }
   ```

### 4.2 Endpoint Authentication Check
Implement an auth verification helper in `cloudflare/src/index.ts`:
```typescript
function isAuthorized(request: Request, env: Env): boolean {
  if (!env.AEGIS_SECRET_KEY) return true; // Fallback during initial migration if not set
  const key = request.headers.get("X-Aegis-Key");
  const auth = request.headers.get("Authorization");
  if (key && key === env.AEGIS_SECRET_KEY) return true;
  if (auth && auth.startsWith("Bearer ") && auth.slice(7) === env.AEGIS_SECRET_KEY) return true;
  return false;
}
```
Protect `/api/save_gym_session`, `/api/save_profile`, and new R3 endpoints (`/api/get_gym_session`, `/api/get_profile`):
```typescript
if (!isAuthorized(request, env)) {
  return new Response(JSON.stringify({ error: "Unauthorized" }), {
    status: 401,
    headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
  });
}
```
In client JavaScript, attach `X-Aegis-Key`:
```javascript
const clientKey = localStorage.getItem('aegis_key') || '${env.AEGIS_SECRET_KEY || ""}';
fetch('/api/save_gym_session', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Aegis-Key': clientKey
  },
  body: JSON.stringify(payload)
});
```

### 4.3 Telegram Webhook Hardening
In `cloudflare/src/index.ts` under `if (url.pathname === "/webhook" && request.method === "POST")`:
```typescript
if (env.TELEGRAM_WEBHOOK_SECRET) {
  const secretHeader = request.headers.get("X-Telegram-Bot-Api-Secret-Token");
  if (secretHeader !== env.TELEGRAM_WEBHOOK_SECRET) {
    return new Response("Unauthorized", { status: 401 });
  }
}
```
In `handleTelegramMessage`:
```typescript
const chatId = String(message?.chat?.id || "");
if (env.TELEGRAM_CHAT_ID && chatId !== String(env.TELEGRAM_CHAT_ID)) {
  console.warn("Rejected unauthorized Telegram message from chat_id:", chatId);
  return; // Reject silently or with 403, do not disclose athlete data
}
```

### 4.4 XSS Sanitization & Safe JSON Stringification
Add escaping helpers to `cloudflare/src/index.ts`:
```typescript
function escapeHtml(str: any): string {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function safeJsonStringify(obj: any): string {
  return JSON.stringify(obj)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}
```
- In HTML script generation:
  ```typescript
  const daysData = ${safeJsonStringify(planData.days || [])};
  const weeklyData = ${safeJsonStringify(WEEKLY_EVO_DATA)};
  const calendarDataByMonth = ${safeJsonStringify(CALENDAR_DATA_BY_MONTH)};
  ```
- In client-side JavaScript, replicate `escapeHtml()` and apply it to:
  - `escapeHtml(act.notes)` inside `notesContainer.innerHTML`
  - `escapeHtml(currentGymState[ex.num].notes)` in `<input value="...">`
  - `escapeHtml(day.running.title)`, `escapeHtml(day.running.main_work)`, etc.

### 4.5 HTTP Security Headers
Define a reusable header object:
```typescript
const SECURITY_HEADERS: Record<string, string> = {
  "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; connect-src 'self' https://api.telegram.org; frame-ancestors 'none';",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
  "X-Frame-Options": "DENY",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()"
};
```
Merge these headers into all Worker HTML responses and API responses.

### 4.6 `scripts/sync_coaching_engine.py` Fixes
1. **Dynamic Dates:**
   ```python
   def fetch_activities(oldest_date='2026-08-15', newest_date=None):
       if newest_date is None:
           newest_date = datetime.now().strftime('%Y-%m-%d')
   ```
2. **Timeouts and Retry Session:**
   ```python
   import requests
   from urllib3.util import Retry
   from requests.adapters import HTTPAdapter

   session = requests.Session()
   retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
   session.mount('https://', HTTPAdapter(max_retries=retries))
   DEFAULT_TIMEOUT = (5.0, 25.0)

   def fetch_activities(...):
       r = session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
   ```
3. **Environment Credentials:**
   ```python
   ATHLETE_ID = os.getenv('ATHLETE_ID', 'i690671')
   API_KEY = os.getenv('INTERVALS_API_KEY', '4cvqxm8a5intat925ttdcmpja')
   ```

---

## 5. Verification Method

### 5.1 Automated Pytest Verification
Run the pytest test suite:
```powershell
python -m pytest tests/test_audit_suite.py -v
```
To test the remediations once implemented:
1. `test_wrangler_credentials_audit`: Update assertion to verify that sensitive keys (`TELEGRAM_BOT_TOKEN`, `INTERVALS_API_KEY`) are NOT present under `[vars]` in `wrangler.toml`.
2. Add test `test_api_endpoints_require_auth`: Send POST to `/api/save_gym_session` without `X-Aegis-Key` and assert 401 response.
3. Add test `test_webhook_requires_secret_token_and_chat_id`: Send POST to `/webhook` without secret or with non-matching `chat.id` and assert rejection.
4. Add test `test_security_headers_present`: Assert presence of `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options` on HTML responses.
5. Add test `test_sync_coaching_engine_dynamic_date`: Import `fetch_activities` from `sync_coaching_engine` and assert that default `newest_date` equals today's date (`>= 2026-11-16`).

### 5.2 Manual / Scripted Verification
- **Header Check:**
  ```powershell
  curl -I http://localhost:8787/
  ```
  Verify all 6 security headers are returned.
- **Unauthorized POST Check:**
  ```powershell
  curl -X POST http://localhost:8787/api/save_gym_session -H "Content-Type: application/json" -d "{}"
  ```
  Expected status: `401 Unauthorized`.
- **Authorized POST Check:**
  ```powershell
  curl -X POST http://localhost:8787/api/save_gym_session -H "Content-Type: application/json" -H "X-Aegis-Key: <key>" -d "{\"date\":\"2026-11-16\"}"
  ```
  Expected status: `200 OK`.

### 5.3 Invalidation Conditions
- If `wrangler.toml` still contains `TELEGRAM_BOT_TOKEN` or `INTERVALS_API_KEY` under `[vars]`.
- If `/api/save_gym_session` returns 200 to an unauthenticated request.
- If `/webhook` replies to an update from an unauthorized `chat.id`.
- If `<script>` blocks render unescaped `</script>` tags from KV JSON.
- If `scripts/sync_coaching_engine.py` retains `newest_date='2026-11-15'`.
