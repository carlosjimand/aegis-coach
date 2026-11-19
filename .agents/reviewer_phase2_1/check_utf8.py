import json, yaml, re
from pathlib import Path

clean_mds = sorted(list(Path("data/papers/markdown").glob("*.md")))

for m in clean_mds:
    raw_bytes = m.read_bytes()
    try:
        text = raw_bytes.decode("utf-8")
        print(f"{m.name}: Valid UTF-8 ({len(text)} chars)")
    except Exception as e:
        print(f"{m.name}: UTF-8 DECODING ERROR: {e}")
