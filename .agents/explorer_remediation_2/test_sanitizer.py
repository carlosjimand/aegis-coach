import re
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_phase2_rag_and_guide import validate_gfm_table_syntax

BACKWARDS_TEXT_MAP = {
    r"\bgniniart\b": "training",
    r"\bytisnetni\b": "intensity",
    r"\bemit\s*\.\s*tni\b": "int. time",
    r"\blanoitan\b": "national",
    r"\bstnapicitrap\b": "participants",
    r"\bsessalc\b": "classes",
    r"\bcinortcele\b": "electronic",
    r"\bevitcepsorp\b": "prospective",
    r"\bdetaler\b": "related",
}

def clean_backwards_text(text: str) -> str:
    """Normalize backwards OCR tokens from vertical/axis PDF text."""
    for pattern, replacement in BACKWARDS_TEXT_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def is_real_data_table(tbl_lines):
    if len(tbl_lines) < 3:
        return False
    
    # Check if second line or third line is a delimiter
    has_delim = False
    delim_idx = 1
    if re.match(r'^\|(\s*:?-{1,}:?\s*\|)+$', tbl_lines[1].strip()):
        has_delim = True
        delim_idx = 1
    elif len(tbl_lines) > 2 and re.match(r'^\|(\s*:?-{1,}:?\s*\|)+$', tbl_lines[2].strip()):
        has_delim = True
        delim_idx = 2
    
    if not has_delim:
        return False
        
    header = tbl_lines[delim_idx - 1].strip()
    h_cells = [c.strip() for c in header.split('|')[1:-1]]
    num_cols = len(h_cells)
    
    if num_cols < 2 or num_cols > 10:
        return False
        
    non_empty_h = [c for c in h_cells if c]
    if len(non_empty_h) < 2:
        return False
        
    prose_tokens = {'and', 'the', 'of', 'in', 'was', 'were', 'to', 'this', 'that', 'with', 'for', 'on', 'at', 'by', 'from', 'as', 'is', 'it', 'when', 'adding', 'during', 'date', 'injury', 'protocol', 'initiation', 'contrast', 'because', 'between'}
    prose_count = sum(1 for c in non_empty_h if c.lower() in prose_tokens)
    if prose_count >= 1:
        return False
        
    data_rows = tbl_lines[delim_idx + 1:]
    if not data_rows:
        return False
        
    numeric_or_short_count = 0
    total_non_empty = 0
    for r in data_rows[:5]:
        r_cells = [c.strip() for c in r.split('|')[1:-1]]
        for cell in r_cells:
            if cell:
                total_non_empty += 1
                if re.search(r'\d', cell) or len(cell.split()) <= 4:
                    numeric_or_short_count += 1
    if total_non_empty > 0 and (numeric_or_short_count / total_non_empty) < 0.6:
        return False
        
    return True

def flatten_table_to_prose(tbl_lines):
    sentences = []
    for line in tbl_lines:
        line_clean = line.strip()
        if re.match(r'^\|(\s*:?-{1,}:?\s*\|)+$', line_clean):
            continue
        cells = [c.strip() for c in line_clean.split('|') if c.strip() and not re.match(r'^-+$', c.strip())]
        if cells:
            row_text = ' '.join(cells)
            if not re.match(r'^(Original\s+article|Review|Research|Research\s+article|Frontiers\s+in\s+Physiology|PLoS\s+ONE|Sports\s+Medicine|BJSM|JOSPT|\d+\s+of\s+\d+|Page\s+\d+|Downloaded\s+from|Protected\s+by).*$', row_text, re.I):
                sentences.append(row_text)
    return sentences

def sanitize_tables_in_markdown(text):
    lines = text.split('\n')
    output_lines = []
    in_table = False
    cur_tbl = []

    def handle_block(tbl):
        if not tbl:
            return []
        while tbl and re.match(r'^\|(\s*:?-{1,}:?\s*\|)+$', tbl[0].strip()):
            tbl = tbl[1:]
        if not tbl:
            return []

        if is_real_data_table(tbl):
            delim_idx = 1
            if not re.match(r'^\|(\s*:?-{1,}:?\s*\|)+$', tbl[1].strip()):
                if len(tbl) > 2 and re.match(r'^\|(\s*:?-{1,}:?\s*\|)+$', tbl[2].strip()):
                    delim_idx = 2
            
            header = tbl[delim_idx - 1].strip()
            h_cells = [c.strip() for c in header.split('|')[1:-1]]
            num_cols = len(h_cells)
            delimiter_line = '| ' + ' | '.join(['---'] * num_cols) + ' |'

            cleaned_rows = []
            for r in tbl[delim_idx + 1:]:
                r_str = r.strip()
                if not (r_str.startswith('|') and r_str.endswith('|')):
                    continue
                if re.match(r'^\|(\s*:?-{1,}:?\s*\|)+$', r_str):
                    continue
                r_cells = [c.strip() for c in r_str.split('|')[1:-1]]
                if not any(r_cells):
                    continue
                if len(r_cells) < num_cols:
                    r_cells.extend([''] * (num_cols - len(r_cells)))
                elif len(r_cells) > num_cols:
                    extra = ' '.join(r_cells[num_cols - 1:])
                    r_cells = r_cells[:num_cols - 1] + [extra]
                cleaned_rows.append('| ' + ' | '.join(r_cells) + ' |')

            if not cleaned_rows:
                return flatten_table_to_prose(tbl)

            # Return well-formed GFM table surrounded by blank lines for clean RAG chunking
            table_lines = ['', '| ' + ' | '.join(h_cells) + ' |', delimiter_line] + cleaned_rows + ['']
            return table_lines
        else:
            return flatten_table_to_prose(tbl)

    for line in lines:
        s = line.strip()
        if s.startswith('|') and s.endswith('|'):
            in_table = True
            cur_tbl.append(s)
        else:
            if in_table:
                output_lines.extend(handle_block(cur_tbl))
                in_table = False
                cur_tbl = []
            output_lines.append(line)

    if in_table:
        output_lines.extend(handle_block(cur_tbl))

    return '\n'.join(output_lines)

def split_long_paragraphs(text: str, max_chars: int = 1000) -> str:
    raw_paras = text.split("\n\n")
    cleaned_paras = []

    for p in raw_paras:
        p_strip = p.strip()
        if not p_strip:
            continue
        if p_strip.startswith("|") or len(p_strip) <= max_chars:
            cleaned_paras.append(p_strip)
            continue

        sub_lines = p_strip.split("\n")
        current_chunk = []
        current_len = 0
        for l in sub_lines:
            l_strip = l.strip()
            if not l_strip:
                continue
            if current_len + len(l_strip) + 1 <= max_chars:
                current_chunk.append(l_strip)
                current_len += len(l_strip) + 1
            else:
                if current_chunk:
                    cleaned_paras.append("\n".join(current_chunk))
                    current_chunk = []
                    current_len = 0

                if len(l_strip) > max_chars:
                    sentences = re.split(r"(?<=[.!?])\s+", l_strip)
                    s_chunk = ""
                    for s in sentences:
                        if len(s_chunk) + len(s) + 1 <= max_chars:
                            s_chunk = f"{s_chunk} {s}".strip() if s_chunk else s
                        else:
                            if s_chunk:
                                cleaned_paras.append(s_chunk)
                            s_chunk = s
                    if s_chunk:
                        current_chunk.append(s_chunk)
                else:
                    current_chunk.append(l_strip)
                    current_len += len(l_strip) + 1

        if current_chunk:
            cleaned_paras.append("\n".join(current_chunk))

    return "\n\n".join(cleaned_paras)

def clean_markdown_text(raw_text: str) -> str:
    text = raw_text.replace("\x0c", "\n\n")
    text = text.replace("\u00a0", " ").replace("\u202f", " ")
    
    # Clean backwards OCR tokens
    text = clean_backwards_text(text)

    # Filter running headers/footers
    lines = text.split("\n")
    cleaned_lines = []
    header_footer_patterns = [
        re.compile(r"^\s*Page\s+\d+(\s+of\s+\d+)?\s*$", re.I),
        re.compile(r"^\s*\d+\s+of\s+\d+\s*$", re.I),
        re.compile(r"^\s*Downloaded\s+from\s+.+$", re.I),
        re.compile(r"^\s*Protected\s+by\s+copyright.*$", re.I),
        re.compile(r"^\s*Copyright\s+(©|\(c\)).*$", re.I),
        re.compile(r"^\s*All\s+rights\s+reserved.*$", re.I),
        re.compile(r"^\s*www\.(frontiersin|plosone|sportsci|jospt|bmj)\.org.*$", re.I),
        re.compile(r"^\s*(Frontiers\s+in\s+Physiology|PLoS\s+ONE|Sports\s+Medicine|British\s+Journal\s+of\s+Sports\s+Medicine|Sportscience|JOSPT).*Volume\s*\d+.*$", re.I),
        re.compile(r"^\s*doi:\s*10\.\d{4,9}/[-._;()/:A-Z0-9]+\s*$", re.I),
    ]

    for line in lines:
        stripped = line.strip()
        if any(p.match(stripped) for p in header_footer_patterns):
            continue
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"(\b[a-zA-Z]{2,})-(?:\r?\n|\n)\s*([a-zA-Z]{2,}\b)", r"\1\2", text)

    section_map = {
        r"^\s*ABSTRACT\s*$": "## Abstract",
        r"^\s*INTRODUCTION\s*$": "## Introduction",
        r"^\s*(MATERIALS\s+AND\s+METHODS|METHODS)\s*$": "## Methods",
        r"^\s*RESULTS\s*$": "## Results",
        r"^\s*DISCUSSION\s*$": "## Discussion",
        r"^\s*(CONCLUSIONS|CONCLUSION)\s*$": "## Conclusion",
        r"^\s*(PRACTICAL\s+APPLICATIONS|CLINICAL\s+IMPLICATIONS)\s*$": "## Clinical Implications",
        r"^\s*REFERENCES\s*$": "## References",
        r"^\s*(ACKNOWLEDGMENTS|ACKNOWLEDGEMENTS)\s*$": "## Acknowledgments",
    }

    for pat, repl in section_map.items():
        text = re.sub(pat, repl, text, flags=re.MULTILINE | re.IGNORECASE)

    text = sanitize_tables_in_markdown(text)
    text = split_long_paragraphs(text, max_chars=1000)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    return text.strip()

if __name__ == '__main__':
    raw_md_dir = PROJECT_ROOT / 'data' / 'papers' / 'raw_markdown'
    all_ok = True
    for p in sorted(raw_md_dir.glob('*.raw.md')):
        raw = p.read_text(encoding='utf-8')
        cleaned = clean_markdown_text(raw)
        
        # Check backwards text
        for term in ['gniniart', 'ytisnetni', 'emit .tni']:
            if term in cleaned.lower():
                print(f"FAILED backwards text '{term}' in {p.name}")
                all_ok = False
                
        # Check tables
        lines = cleaned.splitlines()
        in_tbl = False
        cur = []
        malformed = 0
        valid = 0
        for l in lines:
            s = l.strip()
            if s.startswith('|') and s.endswith('|'):
                in_tbl = True
                cur.append(s)
            else:
                if in_tbl:
                    ok, reason = validate_gfm_table_syntax('\n'.join(cur))
                    if ok:
                        valid += 1
                    else:
                        malformed += 1
                        print(f'FAIL in {p.name}: {reason}')
                    in_tbl = False
                    cur = []
        if in_tbl:
            ok, reason = validate_gfm_table_syntax('\n'.join(cur))
            if ok:
                valid += 1
            else:
                malformed += 1
                print(f'FAIL in {p.name}: {reason}')
        print(f'{p.name:<40} | Valid: {valid:<2} | Malformed: {malformed:<2}')
        if malformed > 0:
            all_ok = False
    print(f'Overall test pass: {all_ok}')
