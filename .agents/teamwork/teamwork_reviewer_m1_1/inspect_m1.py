import os

path = os.path.join('cloudflare', 'src', 'index.ts')
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in {path}: {len(lines)}")

print("\n--- Interpolations in getLuxuryDashboardHtml ---")
for i, line in enumerate(lines[3852:5000], 3853):
    if "${" in line:
        print(f"L{i}: {line.strip()}")
