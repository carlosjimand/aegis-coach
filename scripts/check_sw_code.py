with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('// CRITICAL: Bypass Service Worker for ALL cross-origin requests')
print("Cross-origin bypass present:", idx != -1)
if idx != -1:
    print(text[idx:idx+400])
