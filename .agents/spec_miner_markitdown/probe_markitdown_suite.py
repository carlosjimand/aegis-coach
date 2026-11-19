import os
import sys
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from markitdown import MarkItDown

work_dir = '.agents/spec_miner_markitdown'
os.makedirs(work_dir, exist_ok=True)

results = []

def run_cli(cmd_args, input_data=None):
    cli = r'C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\Scripts\markitdown.exe'
    full_cmd = [cli] + cmd_args
    proc = subprocess.run(
        full_cmd,
        input=input_data,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    return proc.returncode, proc.stdout, proc.stderr

# Probe 1: Version and Help
code, out, err = run_cli(['-v'])
results.append(('CLI Version Flag', '-v', code == 0, out.strip(), err.strip()))

code, out, err = run_cli(['--help'])
results.append(('CLI Help Flag', '--help', code == 0, 'Help displayed' if 'Convert various' in out else 'Failed', err.strip()))

# Probe 2: Standard PDF Generation & Conversion
pdf_std = os.path.join(work_dir, 'probe_std.pdf')
doc = SimpleDocTemplate(pdf_std, pagesize=letter)
styles = getSampleStyleSheet()
story = [
    Paragraph('<b>The Polarized Training Model in Endurance Athletes</b>', styles['Title']),
    Spacer(1, 12),
    Paragraph('<b>Abstract</b>: Polarized training involves 80% low-intensity and 20% high-intensity training.', styles['Normal']),
    Spacer(1, 12),
    Paragraph('<b>1. Introduction</b>', styles['Heading1']),
    Paragraph('Stephen Seiler proposed the 80/20 distribution for optimal endurance adaptation.', styles['Normal']),
]
doc.build(story)

code, out, err = run_cli([pdf_std])
results.append(('Standard PDF to stdout', pdf_std, code == 0, out.strip()[:100], err.strip()))

# Probe 3: File Output Flag (-o)
md_out = os.path.join(work_dir, 'probe_std.md')
code, out, err = run_cli([pdf_std, '-o', md_out])
file_exists = os.path.exists(md_out)
results.append(('CLI -o output flag', '-o probe_std.md', code == 0 and file_exists, f'File written ({os.path.getsize(md_out)} bytes)' if file_exists else 'Failed', err.strip()))

# Probe 4: Table Extraction
pdf_table = os.path.join(work_dir, 'probe_table.pdf')
doc_table = SimpleDocTemplate(pdf_table, pagesize=letter)
table_data = [
    ['Zone', 'Intensity (% HRmax)', 'Training Volume (%)', 'Lactate (mmol/L)'],
    ['Zone 1 (Low)', '< 80%', '75-80%', '< 2.0'],
    ['Zone 2 (Threshold)', '80-88%', '< 5%', '2.0 - 4.0'],
    ['Zone 3 (High)', '> 88%', '15-20%', '> 4.0']
]
t = Table(table_data)
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
]))
story_table = [
    Paragraph('<b>Training Zones Summary</b>', styles['Heading1']),
    Spacer(1, 12),
    t
]
doc_table.build(story_table)

code, out_table, err = run_cli([pdf_table])
results.append(('Table Extraction', pdf_table, code == 0, 'Markdown Table Detected' if '|' in out_table else 'Plain text fallback', err.strip()))

# Probe 5: Unicode and Scientific Symbols
pdf_unicode = os.path.join(work_dir, 'probe_unicode.pdf')
doc_uni = SimpleDocTemplate(pdf_unicode, pagesize=letter)
story_uni = [
    Paragraph('<b>Biomechanics & Physiology: VO2max and Lactate Dynamics</b>', styles['Title']),
    Spacer(1, 12),
    Paragraph('Key parameters: VO2max = 72.5 mL/kg/min, Delta [La] = 4.2 mmol/L, alpha-motor neuron activation, Askling L-Protocol re-injury rate: 0.08 (8%).', styles['Normal']),
    Paragraph('Spanish accents test: Rehabilitacion de isquiotibiales, patron de marcha, biomecanica.', styles['Normal'])
]
doc_uni.build(story_uni)

code, out_uni, err = run_cli([pdf_unicode])
results.append(('Unicode & Scientific Characters', pdf_unicode, code == 0, out_uni.strip()[:120], err.strip()))

# Probe 6: Multi-page document with Headers, Footers, and Page Numbers
pdf_multipage = os.path.join(work_dir, 'probe_multipage.pdf')

def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawString(54, 750, 'Journal of Sports Sciences (2024) 42:1-12 | DOI: 10.1080/sample.doi')
    canvas.drawString(54, 36, 'Page %d of 2' % doc.page)
    canvas.drawRightString(558, 36, 'CONFIDENTIAL - AEGIS RESEARCH')
    canvas.restoreState()

doc_multi = SimpleDocTemplate(pdf_multipage, pagesize=letter, topMargin=72, bottomMargin=72)
story_multi = [
    Paragraph('<b>Hamstring Strain Injury: Askling L-Protocol Efficacy</b>', styles['Title']),
    Spacer(1, 12),
    Paragraph('Carl Askling demonstrated that lengthening exercises (The Extender, The Diver, The Glider) significantly reduce return-to-play time compared to conventional protocols.', styles['Normal']),
    PageBreak(),
    Paragraph('<b>2. Rehabilitation Guidelines</b>', styles['Heading1']),
    Paragraph('Criterion-based progression using Silbernagel pain-monitoring model (0-10 VAS scale, pain <= 2 allowed).', styles['Normal']),
]
doc_multi.build(story_multi, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

code, out_multi, err = run_cli([pdf_multipage])
has_header = 'Journal of Sports Sciences' in out_multi
has_footer = 'CONFIDENTIAL' in out_multi or 'Page 1' in out_multi
results.append(('Multipage Header/Footer Extraction', pdf_multipage, code == 0, f'Headers captured: {has_header}, Footers captured: {has_footer}', err.strip()))

# Probe 7: Non-existent file error
code_err1, out_err1, err_err1 = run_cli([os.path.join(work_dir, 'non_existent.pdf')])
results.append(('Error: Non-existent file', 'non_existent.pdf', code_err1 != 0, f'ExitCode={code_err1}', err_err1.strip()[:100]))

# Probe 8: Non-PDF / Corrupt File
corrupt_file = os.path.join(work_dir, 'corrupt.pdf')
with open(corrupt_file, 'wb') as f:
    f.write(b'THIS IS NOT A VALID PDF FILE HEADER')
code_err2, out_err2, err_err2 = run_cli([corrupt_file])
results.append(('Error: Corrupted PDF file', 'corrupt.pdf', True, f'ExitCode={code_err2}', err_err2.strip()[:100]))

print('=== PROBE RESULTS ===')
for name, inp, success, out_s, err_s in results:
    status = 'PASS' if success else 'FAIL'
    print(f'[{status}] {name} | Input: {inp} | Output/Behavior: {out_s}')
    if err_s:
        print(f'   Stderr: {err_s}')
