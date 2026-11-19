import os, glob, json, yaml, re
from pathlib import Path

data_dir = Path('data/papers')
pdfs = sorted(list(data_dir.glob('pdfs/*.pdf')))
raw_mds = sorted(list(data_dir.glob('raw_markdown/*.raw.md')))
clean_mds = sorted(list(data_dir.glob('markdown/*.md')))

print(f'Found {len(pdfs)} PDFs, {len(raw_mds)} Raw MDs, {len(clean_mds)} Clean MDs')

manifest_path = data_dir / 'manifest.json'
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    papers = manifest.get('papers', [])
    print(f'Manifest present with {len(papers)} papers.')
    for idx, p in enumerate(papers, 1):
        print(f"  {idx}. ID: {p.get('id')} | Domain: {p.get('domain')} | Year: {p.get('year')} | Title: {p.get('title')[:60]}...")
else:
    print('MANIFEST MISSING!')

print('\n--- PDF Signatures & Verification ---')
for p in pdfs:
    with open(p, 'rb') as f:
        header = f.read(10)
        size = p.stat().st_size
        valid_pdf = header.startswith(b'%PDF-')
        print(f'{p.name}: size={size:,} bytes | valid_header={valid_pdf} ({header[:5]})')

print('\n--- Clean Markdown Inspections ---')
required_fm_keys = {'id', 'title', 'authors', 'year', 'domain', 'topics', 'key_protocols'}
for m in clean_mds:
    text = m.read_text(encoding='utf-8')
    has_form_feed = '\x0c' in text
    has_null = '\x00' in text
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    fm_valid = False
    missing_keys = set()
    fm_data = {}
    if fm_match:
        try:
            fm_data = yaml.safe_load(fm_match.group(1))
            fm_valid = isinstance(fm_data, dict)
            if fm_valid:
                missing_keys = required_fm_keys - set(fm_data.keys())
        except Exception as e:
            fm_valid = False
    
    # Check tables
    has_table = bool(re.search(r'\|[^\n]+\|\n\|[\s\-:]+\|\n\|[^\n]+\|', text))
    trailing_hyphens = len(re.findall(r'[a-zA-Z]{3,}-\n[a-zA-Z]{3,}', text))
    
    print(f'{m.name}:')
    print(f'  Length: {len(text):,} chars | Lines: {len(text.splitlines()):,}')
    print(f'  FormFeed(\\x0c): {has_form_feed} | NullByte(\\x00): {has_null}')
    print(f'  Frontmatter: valid={fm_valid}, keys={len(fm_data)}, missing={missing_keys}')
    print(f'  Has GFM Tables: {has_table} | Line-broken hyphens: {trailing_hyphens}')
