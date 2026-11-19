with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<svg' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
