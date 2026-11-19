with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find(r'\2c')
print(r"Found \2c at:", idx)
if idx != -1:
    print(text[idx-100:idx+100])
