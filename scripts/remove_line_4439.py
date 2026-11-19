with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if len(line) > 5000 and '--tw-border-spacing-x' in line:
        print(f"Removed line {i+1} with length {len(line)}")
        continue
    new_lines.append(line)

with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Saved clean index.ts without long tailwind line!")
