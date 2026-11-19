import { escapeHtml, safeJsonStringify, SECURITY_HEADERS } from '../cloudflare/src/index.ts';

console.log('--- TEST 1: safeJsonStringify Edge Cases ---');

// 1.1 Script tag breakouts
const scriptPayload = '</script><script>alert("xss")</script>';
const scriptRes = safeJsonStringify({ payload: scriptPayload });
console.log('Script tag test:');
console.log('  Result:', scriptRes);
console.log('  Contains </script>?', scriptRes.toLowerCase().includes('</script>'));
console.log('  Contains <script>?', scriptRes.toLowerCase().includes('<script>'));
console.log('  Roundtrip JSON.parse match?', JSON.parse(scriptRes).payload === scriptPayload);

// 1.2 HTML Comment breakout
const commentPayload = '<!-- <script>alert(1)</script> -->';
const commentRes = safeJsonStringify({ c: commentPayload });
console.log('\nHTML comment test:');
console.log('  Result:', commentRes);
console.log('  Contains <!-- ?', commentRes.includes('<!--'));
console.log('  Roundtrip JSON.parse match?', JSON.parse(commentRes).c === commentPayload);

// 1.3 Unicode line separators U+2028 and U+2029
const unicodePayload = 'Line1\u2028Line2\u2029Line3';
const unicodeRes = safeJsonStringify({ text: unicodePayload });
console.log('\nUnicode line separator test:');
console.log('  Result:', JSON.stringify(unicodeRes));
console.log('  Contains raw \\u2028?', unicodeRes.includes('\u2028'));
console.log('  Contains raw \\u2029?', unicodeRes.includes('\u2029'));
console.log('  Contains escaped \\\\u2028?', unicodeRes.includes('\\u2028'));
console.log('  Contains escaped \\\\u2029?', unicodeRes.includes('\\u2029'));
console.log('  Roundtrip JSON.parse match?', JSON.parse(unicodeRes).text === unicodePayload);

// 1.4 Nested objects
const nestedPayload = {
  level1: {
    level2: [
      { text: '</script><script>alert(1)</script>' },
      { text: '\u2028\u2029' }
    ],
    empty: {},
    bool: true,
    num: 42.5
  }
};
const nestedRes = safeJsonStringify(nestedPayload);
console.log('\nNested objects test:');
console.log('  Contains </script>?', nestedRes.toLowerCase().includes('</script>'));
console.log('  Roundtrip match?', JSON.stringify(JSON.parse(nestedRes)) === JSON.stringify(nestedPayload));

// 1.5 Backticks and double quotes
const quotesPayload = {
  backtick: '`',
  quote: '"',
  combined: '`"; alert(1); //',
  templateExpr: '${alert(1)}'
};
const quotesRes = safeJsonStringify(quotesPayload);
console.log('\nBackticks & quotes test:');
console.log('  Result:', quotesRes);
console.log('  Roundtrip match?', JSON.stringify(JSON.parse(quotesRes)) === JSON.stringify(quotesPayload));

// 1.6 null and undefined
console.log('\nNull and undefined test:');
const nullRes = safeJsonStringify(null);
console.log('  safeJsonStringify(null):', nullRes);
try {
  const undefRes = safeJsonStringify(undefined);
  console.log('  safeJsonStringify(undefined):', undefRes);
} catch (e) {
  console.log('  safeJsonStringify(undefined) EXCEPTION:', e.name, e.message);
}

// 1.7 Object with undefined properties vs bare undefined
const objWithUndef = { a: undefined, b: null, c: 'ok' };
console.log('  safeJsonStringify({a: undefined}):', safeJsonStringify(objWithUndef));

console.log('\n--- TEST 2: escapeHtml Injection Vectors ---');

const htmlVectors = [
  { name: 'Image onerror', input: '<img src=x onerror=alert(1)>' },
  { name: 'Breakout script', input: '"><script>alert(1)</script>' },
  { name: 'Single quote handler', input: "' onfocus='alert(1)' autofocus" },
  { name: 'Double quote handler', input: '" onfocus="alert(1)" autofocus' },
  { name: 'Ampersand entity collision', input: '&amp; &lt; &gt; &quot; &#39; & unknown' },
  { name: 'Mixed quotes & tags', input: '<div class="test" data-id=\'123\'>&copy;</div>' },
  { name: 'null', input: null },
  { name: 'undefined', input: undefined },
  { name: 'number 0', input: 0 },
  { name: 'number 100', input: 100 },
  { name: 'boolean false', input: false }
];

for (const vec of htmlVectors) {
  const out = escapeHtml(vec.input);
  const dangerousRawChars = ['<', '>', '"', "'"];
  const containsRaw = dangerousRawChars.some(c => out.includes(c));
  console.log(`Vector [${vec.name}]:`);
  console.log(`  Input:  ${JSON.stringify(vec.input)}`);
  console.log(`  Output: ${JSON.stringify(out)}`);
  console.log(`  Contains raw dangerous chars (<, >, ", ')? ${containsRaw}`);
}

console.log('\n--- TEST 3: SECURITY_HEADERS Compliance ---');
console.log('Headers:', JSON.stringify(SECURITY_HEADERS, null, 2));

const csp = SECURITY_HEADERS['Content-Security-Policy'] || '';
const xfo = SECURITY_HEADERS['X-Frame-Options'] || '';
const xcto = SECURITY_HEADERS['X-Content-Type-Options'] || '';
const hsts = SECURITY_HEADERS['Strict-Transport-Security'] || '';
const referrer = SECURITY_HEADERS['Referrer-Policy'] || '';
const permissions = SECURITY_HEADERS['Permissions-Policy'] || '';

console.log('\nCSP checks:');
console.log('  CSP present?', Boolean(csp));
console.log('  script-src has wildcards (*)?', /script-src[^;]*\*/.test(csp));
console.log('  style-src has wildcards (*)?', /style-src[^;]*\*/.test(csp));
console.log('  default-src present?', csp.includes("default-src 'self'"));
console.log('  frame-ancestors present?', csp.includes("frame-ancestors 'none'"));

console.log('\nOther headers:');
console.log('  X-Frame-Options is DENY?', xfo === 'DENY');
console.log('  X-Content-Type-Options is nosniff?', xcto === 'nosniff');
console.log('  HSTS has max-age >= 31536000?', /max-age=([0-9]+)/.test(hsts) && parseInt(hsts.match(/max-age=([0-9]+)/)[1]) >= 31536000);
console.log('  HSTS includeSubDomains?', hsts.includes('includeSubDomains'));
console.log('  HSTS preload?', hsts.includes('preload'));
console.log('  Referrer-Policy?', referrer);
console.log('  Permissions-Policy?', permissions);
