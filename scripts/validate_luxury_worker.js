const fs = require('fs');
const vm = require('vm');
const path = require('path');

const indexTs = fs.readFileSync(path.join(__dirname, '../cloudflare/src/index.ts'), 'utf8');

console.log('--- 1. Testing index.ts structure ---');
if (!indexTs.includes('DEFAULT_PLAN')) throw new Error('Missing DEFAULT_PLAN');
if (!indexTs.includes('getLuxuryDashboardHtml')) throw new Error('Missing getLuxuryDashboardHtml');

console.log('--- 2. Checking Luxury Color Palette from Reference ---');
const requiredColors = [
  '#141522', // App Background (Slate Obsidian)
  '#1D1E2C', // Card Surface
  '#FF5E80', // Neon Coral Pink (Gradient peak)
  '#7B88FF', // Neon Periwinkle Blue
  '#2D2F45', // Card Border
  '#20D994'  // Mint Green
];
for (const color of requiredColors) {
  const count = (indexTs.match(new RegExp(color, 'gi')) || []).length;
  console.log(`Color ${color}: found ${count} occurrences.`);
  if (count === 0) throw new Error(`Missing required color ${color}!`);
}

console.log('--- 3. Checking Typography & Spline Area Chart ---');
if (!indexTs.includes('Plus Jakarta Sans')) throw new Error('Missing Plus Jakarta Sans font!');
if (!indexTs.includes('weeklySplineChart')) throw new Error('Missing weeklySplineChart canvas!');
if (!indexTs.includes('tension: 0.4')) throw new Error('Missing tension 0.4 for smooth spline!');
console.log('Typography and Spline chart verified!');

console.log('--- 4. Extracting HTML and Testing Client JS Syntax in VM ---');
const matchFn = indexTs.match(/function getLuxuryDashboardHtml[\s\S]*?\n\}/);
const matchPlan = indexTs.match(/const DEFAULT_PLAN: any = ([\s\S]*?);\n\nconst WEEKLY_EVO_DATA/);
const matchWeekly = indexTs.match(/const WEEKLY_EVO_DATA: any = ([\s\S]*?);\n\nexport default/);

if (!matchFn || !matchPlan || !matchWeekly) {
  throw new Error('Could not extract function or plans');
}

const sandbox = {
  DEFAULT_PLAN: JSON.parse(matchPlan[1]),
  WEEKLY_EVO_DATA: JSON.parse(matchWeekly[1]),
  Intl,
  Date,
  Math,
  getTodayMadridISO: () => '2026-11-16',
  calculateDaysRemaining: (target, today) => 13,
  module: { exports: {} }
};

const cleanCode = matchFn[0]
  .replace(/:\s*any(\[\])?/g, '')
  .replace(/:\s*number/g, '')
  .replace(/:\s*string/g, '') + '\nmodule.exports = getLuxuryDashboardHtml;';
vm.runInNewContext(cleanCode, sandbox);

const html = sandbox.module.exports(sandbox.DEFAULT_PLAN);
console.log('Generated HTML size:', html.length);

const scripts = html.match(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi) || [];
console.log(`Found ${scripts.length} inline script block(s).`);

scripts.forEach((scriptTag, idx) => {
  const code = scriptTag.replace(/<script[^>]*>/i, '').replace(/<\/script>/i, '');
  console.log(`Parsing inline script #${idx + 1} (length ${code.length})...`);
  try {
    new vm.Script(code);
    console.log(`SUCCESS: Inline script #${idx + 1} has 100% valid JavaScript syntax!`);
  } catch (err) {
    console.error(`SYNTAX ERROR in script #${idx + 1}:`, err.message);
    process.exit(1);
  }
});

console.log('=== ALL TESTS PASSED WITH 100% COMPLIANCE! ===');
