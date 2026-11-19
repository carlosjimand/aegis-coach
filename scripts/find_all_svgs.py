with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

import re
svgs = [m.start() for m in re.finditer(r'<svg', text)]
print(f"Total <svg occurrences: {len(svgs)}")
for idx in svgs:
    print(text[idx:idx+120].replace('\n', ' '))
