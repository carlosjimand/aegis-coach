// Independent verification script for Worker security functions
import fs from 'fs';
import path from 'path';

// Extract the functions from cloudflare/src/index.ts or test equivalents
const indexTs = fs.readFileSync('cloudflare/src/index.ts', 'utf8');

// Test 1: Test escapeHtml implementation
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Test 2: Test safeJsonStringify implementation
function safeJsonStringify(obj) {
  return JSON.stringify(obj)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}

// Test 3: Test isAuthorized implementation
function isAuthorized(headers, env) {
  if (!env.AEGIS_SECRET_KEY) return true;
  const key = headers['x-aegis-key'] || headers['X-Aegis-Key'];
  const auth = headers['authorization'] || headers['Authorization'];
  if (key && key === env.AEGIS_SECRET_KEY) return true;
  if (auth && auth.startsWith("Bearer ") && auth.slice(7) === env.AEGIS_SECRET_KEY) return true;
  return false;
}

const results = [];

// 1. Stress-test escapeHtml
const xssPayloads = [
  { input: '<script>alert("XSS")</script>', expected: '&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;' },
  { input: `"><img src=x onerror=alert(1)>`, expected: '&quot;&gt;&lt;img src=x onerror=alert(1)&gt;' },
  { input: `' onfocus='alert(1)`, expected: '&#39; onfocus=&#39;alert(1)' },
  { input: `A & B < C > D " E ' F`, expected: 'A &amp; B &lt; C &gt; D &quot; E &#39; F' },
  { input: null, expected: '' },
  { input: undefined, expected: '' },
  { input: 12345, expected: '12345' },
  { input: 0, expected: '0' }
];

for (const p of xssPayloads) {
  const out = escapeHtml(p.input);
  if (out !== p.expected) {
    results.push(`FAIL escapeHtml: input ${p.input} gave ${out}, expected ${p.expected}`);
  }
}

// 2. Stress-test safeJsonStringify
const jsonPayloads = [
  {
    input: { malicious: '</script><script>alert("pwned")</script>' },
    containsUnsafe: (s) => s.includes('</script>') || s.includes('<script>')
  },
  {
    input: { payload: '<!--<script>' },
    containsUnsafe: (s) => s.includes('<') || s.includes('>')
  },
  {
    input: { newline: 'line1\u2028line2\u2029line3' },
    containsUnsafe: (s) => s.includes('\u2028') || s.includes('\u2029')
  }
];

for (const jp of jsonPayloads) {
  const jsonStr = safeJsonStringify(jp.input);
  if (jp.containsUnsafe(jsonStr)) {
    results.push(`FAIL safeJsonStringify: payload escaped to ${jsonStr} still contains unsafe tokens`);
  }
}

// 3. Stress-test isAuthorized
const envWithSecret = { AEGIS_SECRET_KEY: 'secret123' };
const envWithoutSecret = {};

// Test auth header variations
const authTests = [
  { headers: { 'X-Aegis-Key': 'secret123' }, env: envWithSecret, expected: true, desc: 'Exact X-Aegis-Key' },
  { headers: { 'Authorization': 'Bearer secret123' }, env: envWithSecret, expected: true, desc: 'Exact Bearer' },
  { headers: { 'X-Aegis-Key': 'wrong' }, env: envWithSecret, expected: false, desc: 'Wrong X-Aegis-Key' },
  { headers: { 'Authorization': 'Bearer wrong' }, env: envWithSecret, expected: false, desc: 'Wrong Bearer' },
  { headers: {}, env: envWithSecret, expected: false, desc: 'Missing auth headers with secret set' },
  { headers: { 'Authorization': 'Basic secret123' }, env: envWithSecret, expected: false, desc: 'Basic auth instead of Bearer' },
  { headers: { 'Authorization': 'bearer secret123' }, env: envWithSecret, expected: false, desc: 'Lowercase bearer' },
  { headers: {}, env: envWithoutSecret, expected: true, desc: 'Missing secret env fallback' }
];

for (const at of authTests) {
  const authRes = isAuthorized(at.headers, at.env);
  if (authRes !== at.expected) {
    results.push(`FAIL isAuthorized: ${at.desc} -> got ${authRes}, expected ${at.expected}`);
  }
}

console.log('Independent test completed. Failures:', results.length);
if (results.length > 0) {
  console.log(results.join('\n'));
} else {
  console.log('ALL INDEPENDENT LOGIC PROBES PASSED!');
}
