import sys, re
from pathlib import Path
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

text = Path("data/papers/markdown/millet_2011_ultra_trail_fatigue.md").read_text(encoding="utf-8")
lines = text.splitlines()

print("=== First 50 lines of millet_2011_ultra_trail_fatigue.md ===")
for l in lines[:50]:
    print(l)

print("\n=== Searching for immunity in millet_2011_ultra_trail_fatigue.md ===")
for idx, l in enumerate(lines, 1):
    if "immunity" in l.lower() or "infection" in l.lower() or "miceduetolimited" in l.lower():
        print(f"L{idx}: {l}")
