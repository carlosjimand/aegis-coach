const fs = require('fs');
const vm = require('vm');
const path = require('path');

const indexTs = fs.readFileSync(path.join(__dirname, '../cloudflare/src/index.ts'), 'utf8');

console.log('--- 1. Testing index.ts structure ---');
if (!indexTs.includes('DEFAULT_PLAN')) throw new Error('Missing DEFAULT_PLAN');
if (!indexTs.includes('getMobileDashboardHtml')) throw new Error('Missing getMobileDashboardHtml');

console.log('--- 2. Checking Color Palette strictly ---');
const requiredColors = [
  '#05161A', // Base / Fondo principal
  '#072E33', // Contenedores / Tarjetas principales
  '#0C7075', // Elementos interactivos / Botones secundarios
  '#0F969C', // Acento primario / Badges vivos
  '#6DA5C0', // Texto secundario / Métricas
  '#294D61'  // Bordes sutiles / Separadores
];
for (const color of requiredColors) {
  const count = (indexTs.match(new RegExp(color, 'gi')) || []).length;
  console.log(`Color ${color}: found ${count} occurrences.`);
  if (count === 0) throw new Error(`Missing required color ${color}!`);
}

console.log('--- 3. Checking Typography ---');
if (!indexTs.includes('Outfit')) throw new Error('Missing Outfit font!');
if (!indexTs.includes('Manrope')) throw new Error('Missing Manrope font!');
console.log('Typography Outfit + Manrope verified!');

console.log('--- 4. Generating HTML and testing script syntax ---');
// Extract getMobileDashboardHtml function and DEFAULT_PLAN
const matchFn = indexTs.match(/function getMobileDashboardHtml[\s\S]*?\n\}/);
const matchPlan = indexTs.match(/const DEFAULT_PLAN: any = ([\s\S]*?);\n\nexport default/);

if (!matchFn || !matchPlan) {
  throw new Error('Could not extract function or default plan');
}

const sandbox = {
  DEFAULT_PLAN: JSON.parse(matchPlan[1]),
  Intl,
  Date,
  Math,
  getTodayMadridISO: () => '2026-11-16',
  calculateDaysRemaining: (target, today) => {
    const t = new Date(target + 'T00:00:00Z').getTime();
    const d = new Date(today + 'T00:00:00Z').getTime();
    return Math.max(0, Math.ceil((t - d) / (1000 * 60 * 60 * 24)));
  },
  module: { exports: {} }
};

const cleanCode = matchFn[0]
  .replace(/:\s*any(\[\])?/g, '')
  .replace(/:\s*number/g, '')
  .replace(/:\s*string/g, '') + '\nmodule.exports = getMobileDashboardHtml;';
vm.runInNewContext(cleanCode, sandbox);

const html = sandbox.module.exports(null);
console.log('Generated HTML size:', html.length);

// Extract and validate all <script> tags
const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
let matchScript;
let scriptIdx = 0;
while ((matchScript = scriptRegex.exec(html)) !== null) {
  scriptIdx++;
  console.log(`Parsing inline script #${scriptIdx}...`);
  try {
    new vm.Script(matchScript[1]);
    console.log(`SUCCESS: Inline script #${scriptIdx} has 100% valid JavaScript syntax!`);
  } catch (err) {
    console.error(`SYNTAX ERROR in script #${scriptIdx}:`, err.message);
    const lines = matchScript[1].split('\n');
    const errStack = err.stack;
    console.log('Error stack:', errStack);
    // Find where the syntax error is
    for (let i = 0; i < lines.length; i++) {
      try {
        new vm.Script(lines.slice(0, i + 1).join('\n'));
      } catch (lineErr) {
        if (!lineErr.message.includes('Unexpected end of input') && !lineErr.message.includes('missing ) after argument list')) {
          console.log(`Failed around line ${i + 1}: ${lines[i]}`);
          console.log('Context:');
          for (let c = Math.max(0, i - 3); c <= Math.min(lines.length - 1, i + 3); c++) {
            console.log(`${c + 1}: ${lines[c]}`);
          }
          break;
        }
      }
    }
    process.exit(1);
  }
}

console.log('--- 5. Checking 14-day calendar presence in HTML ---');
const daysCount = (html.match(/id="card-day-/g) || []).length;
console.log(`Found ${daysCount} day cards in rendered HTML (Expected: 14)`);
if (daysCount !== 14) {
  throw new Error(`Expected 14 day cards, got ${daysCount}`);
}

console.log('--- 6. Checking Routine & Exercise structures ---');
for (let r = 1; r <= 4; r++) {
  if (!html.includes(`selectGymRoutine(${r})`)) {
    throw new Error(`Missing routine ${r} button trigger!`);
  }
}
console.log('All 4 routine triggers verified!');

console.log('=== ALL TESTS PASSED WITH FLYING COLORS! ===');
