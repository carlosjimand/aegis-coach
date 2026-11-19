import sys, re
from pathlib import Path
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

content = Path("data/papers/markdown/askling_2013_l_protocol.md").read_text(encoding="utf-8")
lines = content.splitlines()

for idx, line in enumerate(lines, 1):
    if "when adding" in line or "The time | from" in line or "test.3" in line:
        print(f"L{idx}: {line}")
