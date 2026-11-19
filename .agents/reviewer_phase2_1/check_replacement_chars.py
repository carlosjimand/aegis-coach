import sys
from pathlib import Path
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

clean_mds = sorted(list(Path("data/papers/markdown").glob("*.md")))

for m in clean_mds:
    text = m.read_text(encoding="utf-8")
    repl_count = text.count("\ufffd")
    print(f"{m.name}: unicode replacement count = {repl_count}")
