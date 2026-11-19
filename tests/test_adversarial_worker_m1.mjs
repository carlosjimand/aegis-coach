import assert from 'node:assert';
import * as workerModule from './worker_compiled.mjs';

const { isAuthorized, escapeHtml, safeJsonStringify, SECURITY_HEADERS } = workerModule;
const fetchHandler = workerModule.default ? workerModule.default.fetch : workerModule.fetch;


// In-memory mock KV store
function createMockKV(initialStore = {}) {
  const store = new Map(Object.entries(initialStore));
  return {
    _store: store,
    async get(key, options = {}) {
      if (!store.has(key)) return null;
      const val = store.get(key);
      if (options.type === 'json') {
        return typeof val === 'string' ? JSON.parse(val) : val;
      }
      return val;
    },
    async put(key, val) {
      store.set(key, typeof val === 'string' ? val : JSON.stringify(val));
    }
  };
}

const mockEnv = {
  AEGIS_KV: createMockKV({
    current_plan: JSON.stringify({
      macrocycle: {
        current_microcycle: "Test Microcycle",
        primary_objective: { name: "Cross Popular Parque del Soto", date: "2026-11-28", distance_km: 5.0 }
      },
      days: [
        {
          date: "2026-11-16",
          day_name: "Lunes",
          running: { is_rest: false, title: "Rodaje Drenaje", duration_min: 35, target_distance_km: 7.0, target_pace: "5:00/km", hr_zone: "Z1" },
          gym: { is_rest: false, routine_name: "Rutina 2", highlight_exercises: [] }
        }
      ]
    })
  }),
  ATHLETE_ID: "i690671",
  INTERVALS_API_KEY: "dummy_key",
  TELEGRAM_BOT_TOKEN: "dummy_bot_token",
  TELEGRAM_CHAT_ID: "641498158",
  AEGIS_SECRET_KEY: "super_secret_aegis_key_2026",
  TELEGRAM_WEBHOOK_SECRET: "telegram_webhook_secret_999"
};

let testsRun = 0;
let testsPassed = 0;

function it(name, fn) {
  testsRun++;
  try {
    fn();
    testsPassed++;
    console.log(`  ✓ ${name}`);
  } catch (err) {
    console.error(`  ✗ ${name}`);
    console.error(err);
    throw err;
  }
}

async function itAsync(name, fn) {
  testsRun++;
  try {
    await fn();
    testsPassed++;
    console.log(`  ✓ ${name}`);
  } catch (err) {
    console.error(`  ✗ ${name}`);
    console.error(err);
    throw err;
  }
}

console.log('=== TEST SUITE: M1 Worker Hardening & Security ===');

// ----------------------------------------------------
// 1. isAuthorized function unit stress tests
// ----------------------------------------------------
console.log('\n[1] isAuthorized function stress tests:');

it('rejects request with omitted headers', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', { method: 'POST' });
  assert.strictEqual(isAuthorized(req, mockEnv), false);
});

it('rejects request with empty X-Aegis-Key', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'X-Aegis-Key': '' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), false);
});

it('rejects request with invalid X-Aegis-Key', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'X-Aegis-Key': 'invalid_token_attempt' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), false);
});

it('rejects request with empty Authorization header', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'Authorization': '' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), false);
});

it('rejects request with malformed Bearer token (no space)', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'Authorization': 'Bearersuper_secret_aegis_key_2026' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), false);
});

it('rejects request with malformed Bearer token (empty after Bearer )', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), false);
});

it('rejects request with wrong scheme (Basic)', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'Authorization': 'Basic c3VwZXJfc2VjcmV0X2FlZ2lzX2tleV8yMDI2' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), false);
});

it('rejects request with lowercase bearer (case sensitivity check)', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'Authorization': 'bearer super_secret_aegis_key_2026' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), false);
});

it('accepts request with valid X-Aegis-Key', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'X-Aegis-Key': 'super_secret_aegis_key_2026' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), true);
});

it('accepts request with valid Authorization Bearer token', () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer super_secret_aegis_key_2026' }
  });
  assert.strictEqual(isAuthorized(req, mockEnv), true);
});

it('falls back to true if AEGIS_SECRET_KEY is not configured in env (graceful migration)', () => {
  const envNoKey = { ...mockEnv, AEGIS_SECRET_KEY: undefined };
  const req = new Request('https://aegis.coach/api/save_gym_session', { method: 'POST' });
  assert.strictEqual(isAuthorized(req, envNoKey), true);
});

// ----------------------------------------------------
// 2. HTTP Endpoint /api/save_gym_session verification
// ----------------------------------------------------
console.log('\n[2] /api/save_gym_session endpoint tests:');

await itAsync('POST /api/save_gym_session returns 401 when no auth header is provided', async () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ date: '2026-11-16', routine_id: 1 })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 401);
  const data = await res.json();
  assert.strictEqual(data.error, 'Unauthorized');
  assert.strictEqual(res.headers.get('X-Frame-Options'), 'DENY');
  assert.strictEqual(res.headers.get('X-Content-Type-Options'), 'nosniff');
});

await itAsync('POST /api/save_gym_session returns 401 with invalid X-Aegis-Key', async () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Aegis-Key': 'hacker_key'
    },
    body: JSON.stringify({ date: '2026-11-16', routine_id: 1 })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 401);
});

await itAsync('POST /api/save_gym_session returns 401 with malformed Bearer', async () => {
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer bad_key'
    },
    body: JSON.stringify({ date: '2026-11-16', routine_id: 1 })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 401);
});

await itAsync('POST /api/save_gym_session returns 200 and saves when valid X-Aegis-Key provided', async () => {
  const kv = createMockKV();
  const env = { ...mockEnv, AEGIS_KV: kv };
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Aegis-Key': 'super_secret_aegis_key_2026'
    },
    body: JSON.stringify({
      date: '2026-11-16',
      routine_id: 1,
      routine_name: 'Rutina 1',
      state: { "1": { sets: [{ reps: "5", weight: "80" }] } }
    })
  });
  const res = await fetchHandler(req, env, {});
  assert.strictEqual(res.status, 200);
  const data = await res.json();
  assert.strictEqual(data.ok, true);
  assert.strictEqual(data.key, 'gym_session_2026-11-16');

  // Verify KV content
  const stored = await kv.get('gym_session_2026-11-16', { type: 'json' });
  assert.strictEqual(stored.routine_name, 'Rutina 1');
});

await itAsync('POST /api/save_gym_session returns 200 with valid Bearer auth', async () => {
  const kv = createMockKV();
  const env = { ...mockEnv, AEGIS_KV: kv };
  const req = new Request('https://aegis.coach/api/save_gym_session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer super_secret_aegis_key_2026'
    },
    body: JSON.stringify({ date: '2026-11-17', routine_id: 2 })
  });
  const res = await fetchHandler(req, env, {});
  assert.strictEqual(res.status, 200);
  const data = await res.json();
  assert.strictEqual(data.ok, true);
  assert.strictEqual(data.key, 'gym_session_2026-11-17');
});

// ----------------------------------------------------
// 3. HTTP Endpoint /api/save_profile verification
// ----------------------------------------------------
console.log('\n[3] /api/save_profile endpoint tests:');

await itAsync('POST /api/save_profile returns 401 when no auth header is provided', async () => {
  const req = new Request('https://aegis.coach/api/save_profile', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ weight: 63.0, height: 1.73 })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 401);
  const data = await res.json();
  assert.strictEqual(data.error, 'Unauthorized');
});

await itAsync('POST /api/save_profile returns 401 with invalid key', async () => {
  const req = new Request('https://aegis.coach/api/save_profile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Aegis-Key': 'wrong_key'
    },
    body: JSON.stringify({ weight: 63.0 })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 401);
});

await itAsync('POST /api/save_profile returns 200 and saves profile with valid key', async () => {
  const kv = createMockKV();
  const env = { ...mockEnv, AEGIS_KV: kv };
  const req = new Request('https://aegis.coach/api/save_profile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Aegis-Key': 'super_secret_aegis_key_2026'
    },
    body: JSON.stringify({ weight: 63.2, height: 1.73, age: 23, fcr: 44 })
  });
  const res = await fetchHandler(req, env, {});
  assert.strictEqual(res.status, 200);
  const data = await res.json();
  assert.strictEqual(data.ok, true);

  const stored = await kv.get('user_profile', { type: 'json' });
  assert.strictEqual(stored.weight, 63.2);
});

// ----------------------------------------------------
// 4. Telegram Webhook (/webhook) stress tests
// ----------------------------------------------------
console.log('\n[4] /webhook endpoint & Telegram hardening tests:');

await itAsync('POST /webhook returns 401 when X-Telegram-Bot-Api-Secret-Token is missing', async () => {
  const req = new Request('https://aegis.coach/webhook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: { chat: { id: 641498158 }, text: '/hoy' } })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 401);
  const data = await res.json();
  assert.strictEqual(data.error, 'Unauthorized');
});

await itAsync('POST /webhook returns 401 when secret token is wrong', async () => {
  const req = new Request('https://aegis.coach/webhook', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Telegram-Bot-Api-Secret-Token': 'wrong_webhook_secret'
    },
    body: JSON.stringify({ message: { chat: { id: 641498158 }, text: '/hoy' } })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 401);
});

await itAsync('POST /webhook returns 401 when secret token is empty string', async () => {
  const req = new Request('https://aegis.coach/webhook', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Telegram-Bot-Api-Secret-Token': ''
    },
    body: JSON.stringify({ message: { chat: { id: 641498158 }, text: '/hoy' } })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 401);
});

await itAsync('POST /webhook accepts valid secret token and returns 200', async () => {
  const req = new Request('https://aegis.coach/webhook', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Telegram-Bot-Api-Secret-Token': 'telegram_webhook_secret_999'
    },
    body: JSON.stringify({
      update_id: 12345,
      message: {
        chat: { id: 641498158 },
        text: '/start'
      }
    })
  });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 200);
  const text = await res.text();
  assert.strictEqual(text, 'OK');
});

await itAsync('POST /webhook with valid secret but spoofed chat.id does NOT disclose data', async () => {
  // Mock global fetch to ensure Telegram sendMessage is NEVER called for spoofed chat
  const originalFetch = globalThis.fetch;
  let telegramCalled = false;
  let interceptedUrl = '';

  globalThis.fetch = async (url, opts) => {
    if (typeof url === 'string' && url.includes('api.telegram.org')) {
      telegramCalled = true;
      interceptedUrl = url;
      return new Response(JSON.stringify({ ok: true }));
    }
    return originalFetch(url, opts);
  };

  try {
    const req = new Request('https://aegis.coach/webhook', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Telegram-Bot-Api-Secret-Token': 'telegram_webhook_secret_999'
      },
      body: JSON.stringify({
        update_id: 67890,
        message: {
          chat: { id: 999999999 }, // Attacker chat id
          text: '/hoy'
        }
      })
    });
    const res = await fetchHandler(req, mockEnv, {});
    assert.strictEqual(res.status, 200);
    // CRITICAL: Telegram API must NEVER have been called for unauthorized chat id!
    assert.strictEqual(telegramCalled, false, 'Telegram API must NOT be called for spoofed chat ID');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

// ----------------------------------------------------
// 5. XSS Sanitization & Safe JSON Stringify
// ----------------------------------------------------
console.log('\n[5] XSS Sanitization & safeJsonStringify tests:');

it('escapeHtml escapes dangerous HTML characters', () => {
  const payload = '<script>alert("xss & evil")</script>\'test\'';
  const escaped = escapeHtml(payload);
  assert.strictEqual(escaped, '&lt;script&gt;alert(&quot;xss &amp; evil&quot;)&lt;/script&gt;&#39;test&#39;');
});

it('escapeHtml handles null and undefined gracefully', () => {
  assert.strictEqual(escapeHtml(null), '');
  assert.strictEqual(escapeHtml(undefined), '');
  assert.strictEqual(escapeHtml(0), '0');
  assert.strictEqual(escapeHtml(false), 'false');
});

it('safeJsonStringify neutralizes closing script tags and Unicode line separators', () => {
  const payload = {
    malicious: "</script><script>alert('pwned')</script>",
    unicode1: "line\u2028break",
    unicode2: "paragraph\u2029break"
  };
  const stringified = safeJsonStringify(payload);
  assert.ok(!stringified.includes('</script>'), 'Must not contain literal </script>');
  assert.ok(stringified.includes('\\u003c/script\\u003e'), 'Must contain escaped \\u003c/script\\u003e');
  assert.ok(!stringified.includes('\u2028'), 'Must not contain raw U+2028');
  assert.ok(!stringified.includes('\u2029'), 'Must not contain raw U+2029');
});

// ----------------------------------------------------
// 6. Security Headers verification
// ----------------------------------------------------
console.log('\n[6] Security Headers tests:');

await itAsync('Worker responses include all required security headers', async () => {
  const req = new Request('https://aegis.coach/', { method: 'GET' });
  const res = await fetchHandler(req, mockEnv, {});
  assert.strictEqual(res.status, 200);
  assert.strictEqual(res.headers.get('Strict-Transport-Security'), 'max-age=31536000; includeSubDomains; preload');
  assert.strictEqual(res.headers.get('X-Frame-Options'), 'DENY');
  assert.strictEqual(res.headers.get('X-Content-Type-Options'), 'nosniff');
  assert.strictEqual(res.headers.get('Referrer-Policy'), 'strict-origin-when-cross-origin');
  assert.ok(res.headers.get('Content-Security-Policy').includes("default-src 'self'"));
  assert.strictEqual(res.headers.get('Permissions-Policy'), 'camera=(), microphone=(), geolocation=(), payment=()');
});

console.log(`\n========================================`);
console.log(`ALL CHALLENGE TESTS PASSED: ${testsPassed}/${testsRun}`);
console.log(`========================================\n`);
