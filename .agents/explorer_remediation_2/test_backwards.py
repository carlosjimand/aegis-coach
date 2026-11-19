import re
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_phase2_rag_and_guide import validate_gfm_table_syntax

BACKWARDS_SUBSTRINGS = [
    ("gniniart", "training"),
    ("ytisnetni", "intensity"),
    ("emit .tni", "int. time"),
    ("emit.tni", "int. time"),
    ("deunitnoc", "continued"),
    ("eulav-p", "p-value"),
    ("dnuorgkcab", "background"),
    ("ecnatsiser", "resistance"),
    ("cirtemoylp", "plyometric"),
    ("lavretni", "interval"),
    ("noitnevretni", "intervention"),
    ("selbairav", "variables"),
    ("gninnur", "running"),
    ("htgnerts", "strength"),
    ("tnirps", "sprint"),
    ("emulov", "volume"),
    ("deziralop", "polarized"),
    ("lanoitaercer", "recreational"),
    ("stnapicitrap", "participants"),
    ("sessalc", "classes"),
    ("cinortcele", "electronic"),
    ("lanoitan", "national"),
    ("evitcepsorp", "prospective"),
    ("detaler", "related"),
]

def clean_backwards_text(text: str) -> str:
    """Normalize backwards OCR tokens and phrases from vertical/axis PDF text."""
    for pattern, replacement in BACKWARDS_SUBSTRINGS:
        # Case-insensitive substring replacement while preserving case if simple
        text = re.sub(re.escape(pattern), replacement, text, flags=re.IGNORECASE)
    return text

if __name__ == '__main__':
    raw_md_dir = PROJECT_ROOT / 'data' / 'papers' / 'raw_markdown'
    all_ok = True
    for p in sorted(raw_md_dir.glob('*.raw.md')):
        raw = p.read_text(encoding='utf-8')
        cleaned = clean_backwards_text(raw)
        
        found = []
        for term in ['gniniart', 'ytisnetni', 'emit .tni']:
            if term in cleaned.lower():
                found.append(term)
        if found:
            print(f"FAILED backwards text {found} in {p.name}")
            all_ok = False
        else:
            print(f"PASS backwards text in {p.name}")
    print(f"All backwards text cleaned: {all_ok}")
