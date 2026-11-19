import re
from pathlib import Path

for p in sorted(Path("data/papers/markdown").glob("*.md")):
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    table_blocks = []
    curr = []
    for idx, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith("|") and s.endswith("|"):
            curr.append((idx, s))
        else:
            if curr:
                table_blocks.append(curr)
                curr = []
    if curr:
        table_blocks.append(curr)
    
    print(f"=== {p.name}: {len(table_blocks)} table blocks found ===")
    for b_idx, b in enumerate(table_blocks, 1):
        print(f"  Block {b_idx} (lines {b[0][0]}-{b[-1][0]}):")
        for line_num, l_text in b[:4]:
            print(f"    L{line_num}: {l_text[:70]}")
        if len(b) > 4:
            print(f"    ... ({len(b)} total lines)")
