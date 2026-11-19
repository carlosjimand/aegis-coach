with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i in range(max(0, 4430), min(len(lines), 4445)):
    print(f"Line {i+1} (len {len(lines[i])}): {lines[i][:120]} ... {lines[i][-60:]}")
