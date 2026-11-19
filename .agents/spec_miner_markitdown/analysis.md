# Aegis Coach — MarkItDown & PDF-to-Markdown Specification Analysis

**Author**: Spec Miner 2 (MarkItDown Specialist)  
**Date**: 2026-08-26  
**Status**: Authoritative Specification Document  
**Scope**: PDF ingestion, Microsoft MarkItDown tool probing, environment audit, RAG cleaning pipeline, metadata schema, and target directory layout.

---

## 1. Executive Summary

This report establishes the technical specification for converting academic sports science and sports medicine PDFs into high-quality, token-efficient, clean Markdown documents for the **Aegis Coach RAG Knowledge Base**.

During our environmental probing, we audited the local Python 3.14 installation (`C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64`), verified the `markitdown` CLI and Python API, identified and resolved a missing optional dependency requirement (`pdfminer-six` and `pdfplumber` installed via `markitdown[pdf]`), probed edge cases (tables, multi-column layouts, Greek symbols, running headers/footers, unicode accents), designed an automated two-stage conversion and RAG-cleaning pipeline, specified the YAML frontmatter schema for clinical athletic metadata, and mapped out the recommended target directory layout.

---

## 2. Environment & CLI Tool Specification

### 2.1 Python Runtime & Executables
- **Python Version**: Python 3.14.6 (64-bit)
- **Python Path**: `C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\python.exe` (and available in PATH as `python`)
- **MarkItDown Executable**: `C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\Scripts\markitdown.exe`
- **MarkItDown Version**: `0.1.7` (Official Microsoft MarkItDown package)

### 2.2 Dependency Status
MarkItDown utilizes a modular converter architecture. For PDF conversion, it relies on `PdfConverter` which requires `pdfminer.six` and `pdfplumber`.
- **Installed Packages**:
  - `markitdown`: 0.1.7
  - `pdfminer-six`: 20260107 (Verified)
  - `pdfplumber`: 0.11.10 (Verified)
  - `pypdfium2`: 5.13.0 (Verified)
  - `pillow`: 12.3.0 (Verified)
  - `beautifulsoup4`: 4.15.0 (Verified)
  - `markdownify`: 1.2.3 (Verified)
  - `magika`: 0.6.2 (Verified)
  - `requests`: 2.34.2 (Verified)

### 2.3 Supported Invocation Methods
1. **Direct CLI Tool**:
   ```powershell
   & 'C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\Scripts\markitdown.exe' input.pdf -o output.md
   ```
2. **Python Module CLI**:
   ```powershell
   python -m markitdown input.pdf -o output.md
   ```
3. **Piped Input / Redirection**:
   ```powershell
   Get-Content -Raw input.pdf | & markitdown.exe -x pdf -o output.md
   ```
4. **Programmatic Python API**:
   ```python
   from markitdown import MarkItDown
   md = MarkItDown()
   result = md.convert('path/to/paper.pdf')
   raw_markdown = result.text_content
   ```

---

## 3. MarkItDown Internal Architecture for PDF Conversion

Inspection of `markitdown/converters/_pdf_converter.py` reveals a dual-tier parsing strategy:
1. **Tier 1 (pdfplumber Word Geometry Analysis)**:
   - Evaluates word bounding boxes `(x0, x1, top, bottom)`.
   - Computes adaptive column clustering based on gap percentiles (70th percentile).
   - Detects structured/borderless tables and formats them as standard GitHub Flavored Markdown (GFM) tables with header separators (`| Col1 | Col2 |`).
2. **Tier 2 (pdfminer.six Continuous Layout Fallback)**:
   - If no form/table content is detected or if `pdfplumber` encounters parsing errors, falls back to `pdfminer.high_level.extract_text()` for prose extraction.
3. **Built-in Post-Processing**:
   - Executes `_merge_partial_numbering_lines()` to fix MasterFormat-style split line numbers (`.1`, `.2`).

---

## 4. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | CLI | `-v, --version` | Displays installed MarkItDown version. | None | `markitdown 0.1.7` (stdout) | Exit 0 | CLI probe |
| 2 | CLI | `-h, --help` | Displays usage syntax and all supported arguments. | None | Help message (stdout) | Exit 0 | CLI probe |
| 3 | CLI | `-o, --output` | Writes converted Markdown directly to specified file path. | Target file path (`-o out.md`) | File created with UTF-8 text | Exit 0 if writable, Exit 1 if invalid path | CLI probe |
| 4 | CLI | Stdin conversion | Converts PDF content piped via standard input stream. | Piped binary stream + `-x pdf` | Markdown string to stdout | Exit 1 if type cannot be guessed without hint | CLI probe |
| 5 | CLI | `--keep-data-uris` | Controls retention of base64 data URIs in output. | Flag | Retains or truncates image URIs | Exit 0 | CLI probe |
| 6 | PDF Engine | Table Detection & Extraction | Detects aligned columns and borders; renders Markdown tables. | PDF with tables | GFM pipe tables `| A | B |` | Falls back to plain text if unstructured | `_pdf_converter.py` & Test Suite |
| 7 | PDF Engine | Scientific Character Support | Extracts Greek letters (α, β, Δ), superscripts (VO₂max), math symbols. | PDF with scientific fonts | UTF-8 unicode text string | Preserves characters cleanly | Test Suite (`probe_unicode.pdf`) |
| 8 | PDF Engine | Multilingual Accents | Accurately extracts Spanish, Scandinavian, and accented characters (e.g. é, í, ñ, ü, å, ø). | Accented PDF text | UTF-8 unicode text string | Preserves accents without mojibake | Test Suite (`probe_unicode.pdf`) |
| 9 | Python API | `MarkItDown.convert()` | Programmatic conversion method accepting file paths or file streams. | `str` path or `io.IOBase` stream | `DocumentConverterResult` object | Raises `FileConversionException` on unrecoverable errors | Python API probe |
| 10 | Python API | `DocumentConverterResult` | Container with `.text_content`, `.markdown`, and `.title` attributes. | Ingestion output | Markdown string & metadata | None | Python API probe |

---

## 5. Edge Cases & Observed Behaviors

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Table Extraction | Multi-column table with borders and headers (`probe_table.pdf`) | Converted cleanly into pipe-delimited GFM table (`| Zone | Intensity | ... |`). |
| 2 | Multi-Page Running Headers | PDF with running journal header on pages 1 and 2 | Header text extracted on every page, interspersed with content. |
| 3 | Multi-Page Running Footers | PDF with page numbers and confidentiality notice | Footer text extracted on every page, requiring RAG regex cleanup. |
| 4 | Page Boundaries | 2-page document | Form feed character `\x0c` (`\f`) inserted at page breaks. |
| 5 | Line-Break Hyphenation | Text with broken words across line endings (`length-\nening`) | MarkItDown preserves literal hyphen and newline; requires de-hyphenation post-processor. |
| 6 | Non-Existent File | `non_existent.pdf` | Exits with Exit Code 1 and `FileNotFoundError` in stderr. |
| 7 | Corrupt PDF Header | Binary file with invalid PDF magic bytes | MarkItDown handles without crash (returns empty or handles gracefully depending on fallback). |
| 8 | Scientific Notation & Units | `VO2max = 72.5 mL/kg/min`, `Delta [La] = 4.2 mmol/L` | Extracted with 100% fidelity, zero character distortion. |

---

## 6. RAG Ingestion Pipeline & Cleaning Strategy

Raw PDF extraction contains artifacts that degrade embedding quality, cause chunk boundary pollution, and waste token budget. Aegis Coach requires a **Two-Stage Ingestion Pipeline**:

```
[Raw Scientific PDFs] (data/papers/pdfs/*.pdf)
         │
         ▼
[Stage 1: MarkItDown Engine]
         │ (markitdown.convert() -> raw intermediate markdown)
         ▼
[Stage 2: RAG Normalizer & Semantic Enricher]
  ├── 1. Strip Form Feeds (\x0c -> \n\n)
  ├── 2. Remove Running Headers / Footers / Page Numbers (Regex filter)
  ├── 3. De-hyphenate Broken Line-Wraps (rehabili-\ntation -> rehabilitation)
  ├── 4. Normalize Paragraph Flow (join unwrapped lines, preserve headers & tables)
  ├── 5. Section Header Standardizer (# Title, ## Abstract, ## Methods, ## Results)
  └── 6. YAML Frontmatter Injection (Clinical & Sports Science Metadata)
         │
         ▼
[Clean RAG Corpus] (data/papers/markdown/*.md)
```

### 6.1 Detailed Cleaning & Normalization Rules

1. **Form Feed Stripping**:
   - Replace all occurrences of `\x0c` with standard paragraph separators (`\n\n`).
2. **Header & Footer Elimination**:
   - Filter out lines matching recurring header/footer signatures:
     - `^Page \d+( of \d+)?$`
     - `^Downloaded from .*$`
     - `^Copyright © .*$`
     - Known journal running banners (e.g. `^Journal of Sports Sciences.*$`, `^British Journal of Sports Medicine.*$`, `^Scandinavian Journal of Medicine.*$`).
3. **De-Hyphenation**:
   - Match regex `(\b[a-zA-Z]{2,})-\n\s*([a-zA-Z]{2,}\b)` and join as `$1$2` while verifying table borders and code blocks are not impacted.
4. **Paragraph Unification**:
   - Join adjacent non-empty lines belonging to the same prose block, but preserve:
     - Markdown headings (`#`, `##`, `###`)
     - Table rows (lines starting and ending with `|`)
     - Unordered / ordered lists (`- `, `* `, `1. `, `2. `)
     - Blockquotes (`> `)
5. **Token Efficiency Optimization**:
   - Collapse multiple blank lines (`\n{3,}` -> `\n\n`).
   - Remove redundant white spaces at ends of lines.
   - Clean reference sections or isolate them under a standardized `## References` heading so chunkers can apply dedicated handling.

---

## 7. YAML Frontmatter Metadata Schema for Aegis Coach RAG

Every converted Markdown file must include structured YAML frontmatter to enable deterministic pre-filtering in `poc/rag/vector_store.py` and `poc/agents/medical_agent.py`:

```yaml
---
paper_id: "askling-2013-hamstring-l-protocol"
title: "Acute hamstring injuries in Swedish elite football: a prospective randomised controlled clinical trial comparing two rehabilitation protocols"
authors:
  - "Carl M. Askling"
  - "Magnus Tengvar"
  - "Alf Thorstensson"
year: 2013
journal: "British Journal of Sports Medicine"
doi: "10.1136/bjsports-2013-092165"
category: "sports_medicine_rehab"
target_anatomy:
  - "hamstrings"
  - "biceps_femoris"
  - "semitendinosus"
  - "semimembranosus"
contraindications:
  - "acute_passive_stretching_grade_3"
  - "high_speed_sprinting_phase_1"
rehab_phase:
  - "acute"
  - "subacute"
  - "return_to_sport"
evidence_level: "Level 1b (Randomized Controlled Trial)"
sport_discipline:
  - "sprint"
  - "football"
  - "trail_running"
key_protocols:
  - "Askling L-Protocol (The Extender, The Diver, The Glider)"
summary: "Demonstrates that lengthening exercises (L-Protocol) emphasizing eccentric contractions in elongated positions significantly shorten return-to-play time (28 vs 51 days) compared to conventional protocols without increasing re-injury risk."
---
```

---

## 8. Target Directory Layout

To maintain clean project organization following `PROJECT.md` standards:

```
aegis-coach/
├── data/
│   └── papers/
│       ├── pdfs/                                 # Raw downloaded scientific PDFs (5 to 10 files)
│       │   ├── seiler_2010_polarized_training.pdf
│       │   ├── askling_2013_hamstring_l_protocol.pdf
│       │   ├── askling_2014_acute_hamstring_sprinters.pdf
│       │   ├── silbernagel_2007_achilles_tendinopathy_pain_model.pdf
│       │   ├── laursen_2002_hiit_endurance_performance.pdf
│       │   ├── blagrove_2018_strength_training_runners.pdf
│       │   └── ...
│       ├── raw_markdown/                         # Intermediate direct output from MarkItDown
│       │   ├── seiler_2010_polarized_training.raw.md
│       │   ├── askling_2013_hamstring_l_protocol.raw.md
│       │   └── ...
│       └── markdown/                             # Final clean RAG-ready markdown with frontmatter
│           ├── seiler_2010_polarized_training.md
│           ├── askling_2013_hamstring_l_protocol.md
│           ├── askling_2014_acute_hamstring_sprinters.md
│           ├── silbernagel_2007_achilles_tendinopathy_pain_model.md
│           ├── laursen_2002_hiit_endurance_performance.md
│           ├── blagrove_2018_strength_training_runners.md
│           └── ...
├── scripts/
│   ├── ingest_papers.py                          # Automated batch converter & RAG cleaner
│   └── validate_rag_markdown.py                  # Schema & quality linter for RAG documents
└── docs/
    └── mvp_next_steps.md                         # Guide for Oracle/Qdrant vector deployment
```

---

## 9. Ingestion Pipeline Script Design (`scripts/ingest_papers.py`)

The proposed ingestion script will provide both CLI and programmatic interfaces:
- **Batch Processing**: Scans `data/papers/pdfs/*.pdf`, checks if markdown exists or if `--force` is specified.
- **Conversion**: Invokes `MarkItDown().convert(pdf_path)`.
- **Cleaning**: Applies regex cleaning, header/footer removal, de-hyphenation, and table preservation.
- **Metadata Matching**: Looks up metadata from a structured JSON/YAML catalog (`data/papers/metadata_catalog.json`) and prepends YAML frontmatter.
- **Validation**: Verifies that generated markdown contains non-empty body, valid frontmatter, no raw binary artifacts, and valid Markdown tables.

---

## 10. Conclusion & Handoff Readiness

The local environment and `markitdown` tooling have been thoroughly probed, verified, and characterized. The specifications, cleaning heuristics, directory layouts, and frontmatter schemas are ready for immediate execution by the worker agents in Phase 2.
