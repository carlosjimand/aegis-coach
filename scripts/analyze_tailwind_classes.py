with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

import re
classes = set()
for match in re.finditer(r'class="([^"]+)"', text):
    for c in match.group(1).split():
        if '${' not in c:
            classes.add(c)

print(f"Total unique classes: {len(classes)}")
sorted_classes = sorted(list(classes))
print("Sample classes (first 50):", sorted_classes[:50])
