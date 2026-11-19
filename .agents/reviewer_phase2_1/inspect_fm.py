import json, yaml, re
from pathlib import Path

clean_mds = sorted(list(Path("data/papers/markdown").glob("*.md")))

for m in clean_mds:
    text = m.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if fm_match:
        data = yaml.safe_load(fm_match.group(1))
        print(f"=== {m.name} ===")
        print(f"Keys: {list(data.keys())}")
        print(f"Title: {data.get('title')}")
        print(f"Authors: {data.get('authors')}")
        print(f"Domain: {data.get('domain')}")
        print(f"Topics: {data.get('topics')}")
        print(f"Key Protocols: {data.get('key_protocols')}")
        print()
