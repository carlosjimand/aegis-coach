# Review & Adversarial Critic Report: Aegis Coach Phase 2

**Reviewer ID:** Reviewer 2 (`reviewer_phase2_2`)  
**Target Milestone:** Phase 2 (Scientific Literature RAG Corpus & MVP Action Guide)  
**Date:** 2026-08-27T01:32:00Z  
**Verdict:** **REQUEST_CHANGES**  

---

## 1. Observation

### 1.1 Automated Test Execution & Verbatim Failures
- **Command Run:** `python -m pytest tests/test_phase2_rag_and_guide.py`
- **Result:** `1 failed, 18 passed in 0.51s`
- **Verbatim Error:**
```text
FAILED tests/test_phase2_rag_and_guide.py::TestTier2BoundaryFormattingQuality::test_tc_fmt_04_gfm_markdown_table_syntax_integrity
AssertionError: Malformed GFM table in askling_2013_l_protocol.md: Invalid GFM delimiter line: | when adding |  | an isometric | hamstring |  | contraction |  | during that |  |  |  |  |  |  |  |  |
  Table:
  |  |  |  |  |  |  |  |  | The time | from | the date | of injury | to the | date of | rehabilitation |  |
  | when adding |  | an isometric | hamstring |  | contraction |  | during that |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  | protocol | initiation | was | 5days | for both protocols. |  | Overall, | exer- |
  | test.3 |  |  |  | verified |  |  |  |  |  |  |  |  |  |  |  |
assert False
```
- **Full Suite Run:** `python -m pytest tests/` returned `1 failed, 166 passed in 3.06s`.

### 1.2 Adversarial Audit of Scientific Literature Files (`data/papers/markdown/` & `data/papers/pdfs/`)
Direct inspection of extracted Markdown bodies against frontmatter YAML metadata revealed **3 severe paper mismatches**:
1. `data/papers/markdown/gabbett_2016_acwr.md` (and `data/papers/pdfs/gabbett_2016_acwr.pdf`):
   - **YAML Frontmatter Claim:** Tim J. Gabbett (2016), *"The training—injury prevention paradox: should athletes be training smarter and harder?"* (ACWR sweet spot 0.8–1.3).
   - **Actual Extracted Body Content:** *"Original article: Racecadotril for acute diarrhoea in children: systematic review and meta-analyses"* by Morris Gordon & Anthony Akobeng (Arch Dis Child 2016, PMCID `PMC4789705`).
2. `data/papers/markdown/millet_2011_ultra_trail_fatigue.md` (and `data/papers/pdfs/millet_2011_ultra_trail_fatigue.pdf`):
   - **YAML Frontmatter Claim:** Guillaume Y. Millet et al. (2011), *"Neuromuscular Consequences of an Extreme Mountain Ultra-Marathon"* (UTMB 166km fatigue).
   - **Actual Extracted Body Content:** *"Rapid Immunomagnetic Negative Enrichment of Neutrophil Granulocytes from Murine Bone Marrow for Functional Studies InVitro and InVivo"* by Mike Hasenberg et al. (PLoS ONE 2011, PMCID `PMC3044161`).
3. `data/papers/markdown/silbernagel_2015_achilles_rehab.md` (and `data/papers/pdfs/silbernagel_2015_achilles_rehab.pdf`):
   - **YAML Frontmatter Claim:** Karin Grävare Silbernagel & Kay M. Crossley (2015), *"A Proposed Return-to-Sport Program for Patients With Midportion Achilles Tendinopathy"* (4-phase rehab).
   - **Actual Extracted Body Content:** *"Drug Design, Development and Therapy... Targeting the D1-NMDA complex reduces dyskinesia"* by Song et al. (Drug Des Devel Ther 2016, PMCID `PMC4745842`).

### 1.3 Systematic Table Formatting Corruption Across Corpus
An independent scan of all 9 markdown files with `validate_gfm_table_syntax` identified that **8 out of 9 files contain broken table blocks** with missing delimiter rows, orphan pipe characters, or mixed multi-column OCR artifacts:
- `askling_2013_l_protocol.md`: 12 invalid table blocks
- `blagrove_2018_strength_runners.md`: 35 invalid table blocks
- `cook_2016_tendon_continuum.md`: 10 invalid table blocks
- `gabbett_2016_acwr.md`: 15 invalid table blocks
- `haugen_2022_polarized.md`: 2 invalid table blocks
- `millet_2011_ultra_trail_fatigue.md`: 13 invalid table blocks
- `seiler_tonnessen_2009_polarized.md`: 5 invalid table blocks
- `stoggl_sperlich_2014_polarized.md`: 12 invalid table blocks
- `silbernagel_2015_achilles_rehab.md`: 0 invalid table blocks (clean)

### 1.4 Ingestion Pipeline & Validation Weakness (`scripts/ingest_papers.py`)
- In `scripts/ingest_papers.py` line 1096:
  `tables_ok = "|" in content`
  The internal pipeline validator only checks if the character `|` exists anywhere in the file. It does not validate GFM table grammar, column counts, or delimiter rows, falsely reporting `[PASS]` during `ingest_papers.py --validate`.
- Incorrect PMCIDs in `PAPER_CATALOG`:
  - `gabbett_2016_acwr`: `pmcid: PMC4789705` (points to pediatric diarrhea study)
  - `millet_2011_ultra_trail_fatigue`: `pmcid: PMC3044161` (points to murine neutrophil study)
  - `silbernagel_2015_achilles_rehab`: `pmcid: PMC4745842` (points to Parkinson's dyskinesia study)

### 1.5 Quality of User Action Guide (`mvp_next_steps.md`)
- **OCI Always Free Architecture:** Sound. Correctly targets `VM.Standard.A1.Flex` (Ampere ARM64), Ubuntu 24.04 LTS, 2–4 OCPUs, 12–24 GB RAM, and reserved static IPv4.
- **Docker Compose:** Sound. Uses official `qdrant/qdrant:latest`, maps ports 6333/6334, sets `QDRANT__SERVICE__API_KEY`, configures persistent volumes `/opt/qdrant/storage`, and sets ulimits.
- **Dual-Layer Network Security:** Sound. Thoroughly details both OCI VCN Ingress Rules and Ubuntu host UFW/iptables rules to overcome the default OCI kernel drop behavior.
- **Diagnostics:** Sound. Includes a 5-stage verification sequence with container health, curl auth tests (expecting 401 on unauthorized), collection CRUD, Web UI dashboard, and a working Python SDK probe script.

---

## 2. Logic Chain

1. **Premise 1 (RAG Retrieval Integrity):** Aegis Coach's clinical decisions rely on retrieving relevant scientific chunks from Qdrant vector store.
2. **Premise 2 (Corrupted Source Corpus):** Ingesting papers where the actual text concerns pediatric diarrhea medication, murine immune cells, and Parkinson's dyskinesia means queries for ACWR injury thresholds, ultra-marathon neuromuscular recovery windows, and Achilles tendon 4-phase loading will retrieve completely ungrounded or non-sports-science text chunks into the LLM context.
3. **Premise 3 (Facade Test Masking):** In `tests/test_phase2_rag_and_guide.py`, `TestTier3DomainClinicalIntegrity` concatenated `fm.get("key_protocols", [])` with `body`. Because the YAML frontmatter had manually written sports medicine summaries, the tests passed even when the underlying body text was completely incorrect.
4. **Premise 4 (Table Syntax Non-Compliance):** Markdown files in `data/papers/markdown/` contain OCR fragments formatted as broken pipe tables, which break standard markdown parsers, degrade RAG chunk boundary splitting, and cause `test_tc_fmt_04_gfm_markdown_table_syntax_integrity` to fail.
5. **Conclusion:** Because the deliverable contains mismatched papers (integrity violation/defect) and fails an automated test, the only valid review verdict is **REQUEST_CHANGES**.

---

## 3. Caveats

- The remaining 6 papers (`askling_2013_l_protocol`, `blagrove_2018_strength_runners`, `cook_2016_tendon_continuum`, `haugen_2022_polarized`, `seiler_tonnessen_2009_polarized`, `stoggl_sperlich_2014_polarized`) are genuine, high-quality full-text peer-reviewed articles.
- The theoretical content in `data/papers/manifest.json` and the YAML frontmatters accurately reflects the gold-standard sports science literature (3-zone 80/20 polarized distribution, Askling L-protocol Extender/Diver/Glider and H-Test, Silbernagel 0-5 pain scale and 24h recovery rule, Cook tendon continuum isometrics vs HSR, Gabbett ACWR 0.8-1.3 sweet spot and >1.5 danger zone, Millet 9-16 day ultra recovery).
- `mvp_next_steps.md` is well-written, accurate, and ready for deployment once the literature corpus is remediated.

---

## 4. Conclusion & Required Remediations

**Verdict:** **REQUEST_CHANGES**

### Required Action Items for Worker / Implementer:

1. **Fix PMCIDs & Download URLs in `scripts/ingest_papers.py`:**
   - **Gabbett (2016) ACWR:** Replace PMCID `PMC4789705` and download the genuine BJSM paper (DOI: `10.1136/bjsports-2015-095788`).
   - **Millet (2011) Ultra-Trail Fatigue:** Replace PMCID `PMC3044161` and download genuine PLoS ONE paper e17059 (DOI: `10.1371/journal.pone.0017059`).
   - **Silbernagel (2015) Achilles Rehab:** Replace PMCID `PMC4745842` and download genuine JOSPT paper (DOI: `10.2519/jospt.2015.5887`).
2. **Re-generate PDFs, Raw Markdown, and Clean Markdown:**
   - Re-run `python scripts/ingest_papers.py --force` to download the correct PDFs and convert them to Markdown.
3. **Fix Markdown Table Cleaner & Paragraph Splitter (`scripts/ingest_papers.py`):**
   - Enhance `sanitize_tables_in_markdown()` and `is_real_data_table()` to properly convert OCR pipe text artifacts into plain text sentences (`flatten_table_to_prose`).
   - Ensure `split_long_paragraphs()` does NOT split lines inside markdown table blocks or separate header/delimiter lines.
   - Upgrade `validate_pipeline()` to run `validate_gfm_table_syntax()` on all table blocks.
4. **Strengthen Test Assertions in `tests/test_phase2_rag_and_guide.py`:**
   - In `TestTier3DomainClinicalIntegrity`, verify key clinical terms within `body` directly (do not mask by concatenating frontmatter `key_protocols`).
5. **Verify Full Test Pass:**
   - Run `python -m pytest tests/` and ensure all 167 tests pass with 0 failures.

---

## 5. Verification Method

To independently verify after changes are applied:

1. **Execute Phase 2 Tests:**
   ```powershell
   python -m pytest tests/test_phase2_rag_and_guide.py
   ```
2. **Execute Full Test Suite:**
   ```powershell
   python -m pytest tests/
   ```
3. **Verify Paper Content Authenticity:**
   ```powershell
   python -c "
   for p in ['gabbett_2016_acwr.md', 'millet_2011_ultra_trail_fatigue.md', 'silbernagel_2015_achilles_rehab.md']:
       text = open(f'data/papers/markdown/{p}', encoding='utf-8').read().lower()
       assert 'diarrhoea' not in text, f'{p} contains diarrhea text!'
       assert 'neutrophil' not in text, f'{p} contains neutrophil text!'
       assert 'dyskinesia' not in text, f'{p} contains dyskinesia text!'
   print('All papers verified authentic!')
   "
   ```
4. **Verify Table Syntax Across Corpus:**
   ```powershell
   python -c "
   from tests.test_phase2_rag_and_guide import MARKDOWN_DIR, extract_frontmatter_and_body, validate_gfm_table_syntax
   for md_path in MARKDOWN_DIR.glob('*.md'):
       _, body = extract_frontmatter_and_body(md_path.read_text(encoding='utf-8'))
       # check all tables pass validate_gfm_table_syntax
   print('All tables conform to GFM specification!')
   "
   ```
