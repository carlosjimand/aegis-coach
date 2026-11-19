async function testLive() {
  const res = await fetch('https://aegis-intervals-sync.uranuslabs.workers.dev');
  console.log('Status:', res.status);
  console.log('Content-Type:', res.headers.get('content-type'));
  const html = await res.text();
  console.log('HTML size:', html.length);
  console.log('Includes Outfit:', html.includes('Outfit'));
  console.log('Includes Manrope:', html.includes('Manrope'));
  console.log('Includes #05161A:', html.includes('#05161A'));
  console.log('Includes #0F969C:', html.includes('#0F969C'));
  console.log('Includes #072E33:', html.includes('#072E33'));
  console.log('Includes #0C7075:', html.includes('#0C7075'));
  console.log('Includes #6DA5C0:', html.includes('#6DA5C0'));
  console.log('Includes #294D61:', html.includes('#294D61'));
  const daysMatches = html.match(/id="card-day-/g) || [];
  console.log('Rendered day cards count:', daysMatches.length);
  const vm = require('vm');
  const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
  let match;
  let sIdx = 0;
  while ((match = scriptRegex.exec(html)) !== null) {
    sIdx++;
    new vm.Script(match[1]);
    console.log(`Live script #${sIdx} syntax 100% valid!`);
  }
}
testLive().catch(console.error);
