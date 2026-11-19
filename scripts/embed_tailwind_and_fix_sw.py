import re

# Read compiled css
with open('cloudflare/public_exercises/compiled_tailwind.css', 'r', encoding='utf-8') as f:
    compiled_css = f.read()

# Clean up any duplicate style separators
compiled_css = compiled_css.replace('/* --- NEXT STYLE --- */', '\n')

with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update sw.js:
# - CACHE_NAME = 'aegis-coach-v7'
# - if (requestUrl.origin !== location.origin) return;
old_sw_fetch = """self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const requestUrl = new URL(req.url);

  // Bypass cache for API and Webhook requests
  if (requestUrl.pathname.startsWith('/api/') || requestUrl.pathname.startsWith('/webhook')) {
    return;
  }"""

new_sw_fetch = """self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const requestUrl = new URL(req.url);

  // CRITICAL: Bypass Service Worker for ALL cross-origin requests (CDNs, fonts, third-party APIs).
  // Browser native HTTP stack handles CDN caching cleanly without opaque ERR_FAILED bugs.
  if (requestUrl.origin !== location.origin) {
    return;
  }

  // Bypass cache for API and Webhook requests
  if (requestUrl.pathname.startsWith('/api/') || requestUrl.pathname.startsWith('/webhook')) {
    return;
  }"""

code = code.replace("const CACHE_NAME = 'aegis-coach-v6';", "const CACHE_NAME = 'aegis-coach-v7';")
code = code.replace(old_sw_fetch, new_sw_fetch)

# 2. Embed compiled CSS into <style> tag so styling is 100% self-contained and instant
# Find the start of <style>
style_marker = "<style>\n    /* ================================================================="
if style_marker in code:
    print("Found style marker!")
    # Replace the existing style block header with compiled CSS + custom rules
    # We want compiled_css inserted right after <style>
    code = code.replace("<style>", f"<style>\n/* === SELF-CONTAINED TAILWIND PRODUCTION BUNDLE === */\n{compiled_css}\n")
else:
    print("WARNING: style marker not found directly, searching for <style>")
    code = code.replace("<style>", f"<style>\n/* === SELF-CONTAINED TAILWIND PRODUCTION BUNDLE === */\n{compiled_css}\n", 1)

with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated index.ts with self-contained CSS bundle and cross-origin SW bypass!")
