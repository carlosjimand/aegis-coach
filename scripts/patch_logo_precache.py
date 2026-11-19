with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("  '/favicon.ico',", "  '/favicon.ico',\n  '/img/logo.svg',")

with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added '/img/logo.svg' to PRECACHE_ASSETS!")
