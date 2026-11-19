with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function switchTab(')
print(text[idx:idx+1500])
