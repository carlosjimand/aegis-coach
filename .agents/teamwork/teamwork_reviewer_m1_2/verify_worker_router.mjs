// Independent integration test of Worker fetch handler
import worker from '../../../cloudflare/src/index.ts';

// Mock KV Namespace
class MockKV {
  constructor() {
    this.store = new Map();
  }
  async get(key, options = {}) {
    const val = this.store.get(key);
    if (!val) return null;
    if (options.type === 'json') return JSON.parse(val);
    return val;
  }
  async put(key, value) {
    this.store.set(key, typeof value === 'string' ? value : JSON.stringify(value));
  }
}

const mockKv = new MockKV();
const env = {
  AEGIS_KV: mockKv,
  ATHLETE_ID: 'i690671',
  INTERVALS_API_KEY: 'test_key',
  TELEGRAM_BOT_TOKEN: '12345:TEST_BOT_TOKEN',
  TELEGRAM_CHAT_ID: '641498158',
  AEGIS_SECRET_KEY: 'secret_m1_test',
  TELEGRAM_WEBHOOK_SECRET: 'webhook_m1_test'
};

async function runTests() {
  const issues = [];

  // Test 1: POST /api/save_gym_session without auth -> must return 401
  {
    const req = new Request('https://worker.local/api/save_gym_session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date: '2026-11-16', routine_id: 1, state: {} })
    });
    const res = await worker.fetch(req, env);
    if (res.status !== 401) {
      issues.push(`Expected 401 for unauthenticated save_gym_session, got ${res.status}`);
    }
    if (res.headers.get('x-frame-options') !== 'DENY') {
      issues.push(`Expected X-Frame-Options: DENY on 401 response`);
    }
  }

  // Test 2: POST /api/save_gym_session with wrong auth -> must return 401
  {
    const req = new Request('https://worker.local/api/save_gym_session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Aegis-Key': 'wrong_secret' },
      body: JSON.stringify({ date: '2026-11-16', routine_id: 1, state: {} })
    });
    const res = await worker.fetch(req, env);
    if (res.status !== 401) {
      issues.push(`Expected 401 for bad key on save_gym_session, got ${res.status}`);
    }
  }

  // Test 3: POST /api/save_gym_session with valid X-Aegis-Key -> must return 200
  {
    const req = new Request('https://worker.local/api/save_gym_session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Aegis-Key': 'secret_m1_test' },
      body: JSON.stringify({ date: '2026-11-16', routine_id: 1, state: {} })
    });
    const res = await worker.fetch(req, env);
    if (res.status !== 200) {
      issues.push(`Expected 200 for valid X-Aegis-Key, got ${res.status}`);
    }
    const data = await res.json();
    if (!data.ok || data.key !== 'gym_session_2026-11-16') {
      issues.push(`Expected data.ok: true, got ${JSON.stringify(data)}`);
    }
  }

  // Test 4: POST /api/save_profile without auth -> must return 401
  {
    const req = new Request('https://worker.local/api/save_profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ weight: 63.0, height: 1.73 })
    });
    const res = await worker.fetch(req, env);
    if (res.status !== 401) {
      issues.push(`Expected 401 for unauthenticated save_profile, got ${res.status}`);
    }
  }

  // Test 5: POST /api/save_profile with Bearer auth -> must return 200
  {
    const req = new Request('https://worker.local/api/save_profile', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer secret_m1_test'
      },
      body: JSON.stringify({ weight: 63.0, height: 1.73 })
    });
    const res = await worker.fetch(req, env);
    if (res.status !== 200) {
      issues.push(`Expected 200 for Bearer auth on save_profile, got ${res.status}`);
    }
    const saved = await mockKv.get('user_profile', { type: 'json' });
    if (!saved || saved.weight !== 63.0) {
      issues.push(`Expected profile to be persisted in KV, got ${JSON.stringify(saved)}`);
    }
  }

  // Test 6: POST /webhook without secret token -> must return 401
  {
    const req = new Request('https://worker.local/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: { chat: { id: 641498158 }, text: '/hoy' } })
    });
    const res = await worker.fetch(req, env);
    if (res.status !== 401) {
      issues.push(`Expected 401 for missing Telegram webhook secret token, got ${res.status}`);
    }
  }

  // Test 7: POST /webhook with wrong secret token -> must return 401
  {
    const req = new Request('https://worker.local/webhook', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Telegram-Bot-Api-Secret-Token': 'wrong_secret'
      },
      body: JSON.stringify({ message: { chat: { id: 641498158 }, text: '/hoy' } })
    });
    const res = await worker.fetch(req, env);
    if (res.status !== 401) {
      issues.push(`Expected 401 for invalid Telegram webhook secret token, got ${res.status}`);
    }
  }

  // Test 8: GET / -> must return HTML with full security headers
  {
    const req = new Request('https://worker.local/', { method: 'GET' });
    const res = await worker.fetch(req, env);
    if (res.status !== 200) {
      issues.push(`Expected 200 for GET /, got ${res.status}`);
    }
    const csp = res.headers.get('content-security-policy');
    const xfo = res.headers.get('x-frame-options');
    const xcto = res.headers.get('x-content-type-options');
    const rp = res.headers.get('referrer-policy');
    const hsts = res.headers.get('strict-transport-security');
    if (!csp || !csp.includes("frame-ancestors 'none'")) issues.push('Missing or invalid CSP header');
    if (xfo !== 'DENY') issues.push(`Expected X-Frame-Options: DENY, got ${xfo}`);
    if (xcto !== 'nosniff') issues.push(`Expected X-Content-Type-Options: nosniff, got ${xcto}`);
    if (rp !== 'strict-origin-when-cross-origin') issues.push(`Expected Referrer-Policy, got ${rp}`);
    if (!hsts || !hsts.includes('max-age=31536000')) issues.push(`Expected Strict-Transport-Security, got ${hsts}`);
  }

  // Test 9 & 10: Telegram webhook chat_id verification (Mocking global fetch)
  const origFetch = globalThis.fetch;
  let telegramFetchCalls = [];
  globalThis.fetch = async (url, options) => {
    if (typeof url === 'string' && url.includes('api.telegram.org')) {
      telegramFetchCalls.push({ url, options });
      return new Response(JSON.stringify({ ok: true }), { status: 200 });
    }
    return origFetch(url, options);
  };

  try {
    // Test 9: Webhook with valid secret token but UNKNOWN/UNAUTHORIZED chat_id (e.g. 99999999)
    telegramFetchCalls = [];
    const reqUnauthorizedChat = new Request('https://worker.local/webhook', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Telegram-Bot-Api-Secret-Token': 'webhook_m1_test'
      },
      body: JSON.stringify({ message: { chat: { id: 99999999 }, text: '/hoy' } })
    });
    await worker.fetch(reqUnauthorizedChat, env);
    if (telegramFetchCalls.length > 0) {
      issues.push(`CRITICAL: Telegram API was called for unauthorized chat ID 99999999! Leaking athlete data.`);
    }

    // Test 10: Webhook with valid secret token and AUTHORIZED chat_id (641498158)
    telegramFetchCalls = [];
    const reqAuthorizedChat = new Request('https://worker.local/webhook', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Telegram-Bot-Api-Secret-Token': 'webhook_m1_test'
      },
      body: JSON.stringify({ message: { chat: { id: 641498158 }, text: '/hoy' } })
    });
    await worker.fetch(reqAuthorizedChat, env);
    if (telegramFetchCalls.length === 0) {
      issues.push(`Expected Telegram sendMessage to be called for authorized athlete chat ID, but was not.`);
    } else {
      const sentPayload = JSON.parse(telegramFetchCalls[0].options.body);
      if (sentPayload.chat_id !== '641498158' || !sentPayload.text.includes('ENTRENAMIENTO DE HOY')) {
        issues.push(`Unexpected payload sent to Telegram: ${JSON.stringify(sentPayload)}`);
      }
    }
  } finally {
    globalThis.fetch = origFetch;
  }

  console.log('Worker router integration test finished.');
  if (issues.length > 0) {
    console.error('ISSUES ENCOUNTERED:');
    issues.forEach(i => console.error(' -', i));
    process.exit(1);
  } else {
    console.log('ALL 10 ROUTER INTEGRATION & ADVERSARIAL TESTS PASSED PERFECTLY!');
  }
}

runTests().catch(err => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
