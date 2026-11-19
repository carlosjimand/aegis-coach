"""
Challenger 1 Detailed Forensic Diagnostics for Iteration 2 Gate
"""
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "papers"
MARKDOWN_DIR = DATA_DIR / "markdown"

def test_audit_all_backwards_text():
    md_dir = MARKDOWN_DIR
    dictionary_words = [
        'training', 'intensity', 'strength', 'running', 'velocity', 'protocol',
        'recovery', 'fatigue', 'endurance', 'muscle', 'tendon', 'hamstring',
        'achilles', 'exercise', 'volume', 'threshold', 'lactate', 'frequency',
        'isometric', 'eccentric', 'concentric', 'hypertrophy', 'neuromuscular',
        'repetition', 'marathon', 'performance', 'period', 'between', 'different',
        'matched', 'high', 'with', 'repeated', 'measures', 'group', 'blood'
    ]
    
    inventory = {}
    for md_file in sorted(md_dir.glob('*.md')):
        text = md_file.read_text(encoding='utf-8')
        lines = text.splitlines()
        file_findings = []
        for line_idx, line in enumerate(lines, 1):
            for w in dictionary_words:
                rev = w[::-1]
                if len(rev) >= 4:
                    if rev.lower() in line.lower():
                        file_findings.append((line_idx, rev, w, line.strip()[:80]))
        if file_findings:
            inventory[md_file.name] = file_findings

    print(f"\n--- AUDIT RESULTS: {len(inventory)} files affected ---")
    for fname, items in inventory.items():
        print(f"\nFile: {fname} (Total occurrences: {len(items)})")
        for line_idx, rev, orig, snippet in items[:10]:
            print(f"  Line {line_idx}: '{rev}' (reversed '{orig}') -> {snippet}")
