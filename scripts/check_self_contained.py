with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'SELF-CONTAINED', text)]
print("SELF-CONTAINED occurrences:", len(matches))
for m in matches:
    print(text[m:m+200])
