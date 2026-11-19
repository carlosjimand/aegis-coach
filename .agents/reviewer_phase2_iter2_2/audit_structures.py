import json
import re
import yaml
import pypdf
from pathlib import Path

project_root = Path(".").resolve()
data_dir = project_root / "data" / "papers"
md_dir = data_dir / "markdown"
pdf_dir = data_dir / "pdfs"
manifest_path = data_dir / "manifest.json"

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print(f"--- PDF Physical & Structural Audit ---")
for p in manifest["papers"]:
    pid = p["id"]
    pdf_path = pdf_dir / f"{pid}.pdf"
    assert pdf_path.exists(), f"PDF missing: {pdf_path}"
    size = pdf_path.stat().st_size
    reader = pypdf.PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    print(f"PDF {pid:<35} | Size: {size:>8} bytes | Pages: {num_pages:>2} | >50KB: {size > 50000}")
    assert size > 50000, f"PDF {pid} is smaller than 50KB: {size}"
    assert num_pages >= 1, f"PDF {pid} has 0 pages"

print(f"\n--- GFM Table Syntax Audit ---")
def check_table_syntax(text: str, filename: str):
    lines = text.split("\n")
    in_table = False
    cur_tbl = []
    tables = []
    for line in lines:
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            in_table = True
            cur_tbl.append(s)
        else:
            if in_table:
                tables.append(cur_tbl)
                in_table = False
                cur_tbl = []
    if in_table:
        tables.append(cur_tbl)
    
    errors = []
    for t_idx, tbl in enumerate(tables):
        if len(tbl) < 2:
            errors.append(f"Table {t_idx} too short ({len(tbl)} lines)")
            continue
        header = tbl[0]
        h_cols = len([c.strip() for c in header.split("|")[1:-1]])
        delim = tbl[1]
        if not re.match(r"^\|(\s*:?-{1,}:?\s*\|)+$", delim):
            errors.append(f"Table {t_idx} invalid delimiter: {delim}")
            continue
        d_cols = len([c.strip() for c in delim.split("|")[1:-1]])
        if h_cols != d_cols:
            errors.append(f"Table {t_idx} header cols ({h_cols}) != delim cols ({d_cols})")
        for r_idx, row in enumerate(tbl[2:], start=3):
            r_cols = len([c.strip() for c in row.split("|")[1:-1]])
            if r_cols != h_cols:
                errors.append(f"Table {t_idx} row {r_idx} cols ({r_cols}) != header cols ({h_cols})")
    return len(tables), errors

total_tables = 0
all_table_errors = []
for p in manifest["papers"]:
    pid = p["id"]
    md_file = md_dir / f"{pid}.md"
    content = md_file.read_text(encoding="utf-8")
    count, errs = check_table_syntax(content, f"{pid}.md")
    total_tables += count
    if errs:
        all_table_errors.extend([f"{pid}.md: {e}" for e in errs])
        print(f"MD {pid:<35} | Tables: {count:>2} | ERRORS: {errs}")
    else:
        print(f"MD {pid:<35} | Tables: {count:>2} | GFM Syntax: VALID")

print(f"Total tables found: {total_tables}, Total syntax errors: {len(all_table_errors)}")
assert len(all_table_errors) == 0, f"Table syntax errors found: {all_table_errors}"

print(f"\n--- YAML Frontmatter Schema Audit ---")
required_keys = [
    "title", "authors", "year", "journal", "doi", "domain", "topics",
    "target_anatomy", "key_protocols", "evidence_level", "ingestion"
]

for p in manifest["papers"]:
    pid = p["id"]
    md_file = md_dir / f"{pid}.md"
    content = md_file.read_text(encoding="utf-8")
    assert content.startswith("---\n"), f"{pid} does not start with YAML delimiter"
    parts = content.split("---\n", 2)
    fm = yaml.safe_load(parts[1])
    assert isinstance(fm, dict), f"{pid} YAML is not a dict"
    for k in required_keys:
        assert k in fm, f"{pid} missing key {k}"
    assert isinstance(fm["authors"], list) and len(fm["authors"]) > 0, f"{pid} authors invalid"
    assert isinstance(fm["key_protocols"], list) and len(fm["key_protocols"]) > 0, f"{pid} key_protocols invalid"
    assert isinstance(fm["topics"], list) and len(fm["topics"]) > 0, f"{pid} topics invalid"
    assert isinstance(fm["target_anatomy"], list) and len(fm["target_anatomy"]) > 0, f"{pid} target_anatomy invalid"
    assert fm["ingestion"]["cleaned"] is True, f"{pid} ingestion.cleaned not True"
    assert fm["ingestion"]["tables_preserved"] is True, f"{pid} ingestion.tables_preserved not True"
    print(f"YAML {pid:<35} | Schema: VALID | Evidence: {fm['evidence_level']}")

print("\nALL STRUCTURAL AND SYNTACTIC CHECKS PASSED.")
