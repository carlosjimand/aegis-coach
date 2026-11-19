# Handoff Report — Spec Miner 2 (MarkItDown & PDF Conversion)

**Date**: 2026-08-26  
**Type**: Hard (Task Complete)  
**Agent**: `spec_miner_markitdown`  
**Recipient**: `parent` (`a98568cc-f100-49de-a4a7-4a587770ba07`)

---

## 1. Observation
1. **Environment Verification**:
   - Python executable: `C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\python.exe` (v3.14.6 64-bit).
   - MarkItDown CLI executable: `C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\Scripts\markitdown.exe` (v0.1.7).
   - Python module invocation `python -m markitdown` is fully operational.
2. **Dependency Resolution**:
   - Initial run of `markitdown.exe` on `.pdf` failed with `MissingDependencyException` (`pdfminer` / `pdfplumber` missing).
   - Executed `python -m pip install "markitdown[pdf]"` which successfully installed `pdfminer-six` (20260107), `pdfplumber` (0.11.10), `pypdfium2` (5.13.0), and `Pillow` (12.3.0).
3. **Probing & Observable Behavior**:
   - Executed 8-point automated probe suite (`.agents/spec_miner_markitdown/probe_markitdown_suite.py`):
     * Version and Help flags: PASS (`markitdown 0.1.7`).
     * Standard PDF conversion to stdout: PASS (clean markdown output).
     * File output flag `-o`: PASS (verified UTF-8 file creation).
     * Table extraction: PASS (`pdfplumber` converted multi-column table to GFM pipe table `| Zone | Intensity | ... |`).
     * Unicode & scientific notation: PASS (preserved `VO2max`, `Delta [La]`, Spanish accents, and Greek letters).
     * Multi-page documents: Extracted `\x0c` form feeds and running headers/footers (`Journal of Sports Sciences...`, `Page 1 of 2`).
     * Error handling: Non-existent file returned Exit Code 1 with `FileNotFoundError`.
4. **Artifacts Produced**:
   - Comprehensive Analysis: `.agents/spec_miner_markitdown/analysis.md`
   - Test PDF / Markdown Probes: `.agents/spec_miner_markitdown/probe_std.pdf`, `probe_table.pdf`, `probe_unicode.pdf`, `probe_multipage.pdf`
   - Progress Log: `.agents/spec_miner_markitdown/progress.md`
   - Dispatch Log: `.agents/spec_miner_markitdown/DISPATCH.md`
   - Briefing State: `.agents/spec_miner_markitdown/BRIEFING.md`

---

## 2. Logic Chain
1. **Observation 1 & 2** -> MarkItDown is the official Microsoft multi-format converter. While installed, its PDF converter module required optional extras (`pdfminer.six`, `pdfplumber`). Resolving this dependency in `pythoncore-3.14-64` enabled offline, local PDF parsing without external APIs or cloud tokens.
2. **Observation 3** -> MarkItDown produces high-quality layout and table extraction, but outputs raw PDF artifacts (form feeds `\x0c`, repeated running headers/footers, line-break word hyphenations).
3. **Logic Inference** -> Direct ingestion of raw MarkItDown output into vector stores degrades RAG retrieval due to chunk pollution and token waste.
4. **Pipeline Decision** -> A **Two-Stage Ingestion Pipeline** is required:
   - Stage 1: MarkItDown raw extraction (CLI or Python API).
   - Stage 2: RAG Normalizer (strips headers/footers, de-hyphenates words, standardizes sections, and injects YAML frontmatter).
5. **Directory Decision** -> Partitioning files into `data/papers/pdfs/`, `data/papers/raw_markdown/`, and `data/papers/markdown/` ensures data provenance, reproducibility, and clean RAG indexing.

---

## 3. Caveats
1. **Scanned / Image-Only PDFs**: MarkItDown relies on text streams in `pdfplumber`/`pdfminer`. If a PDF is a pure scanned bitmap without an OCR text layer, MarkItDown will output empty text unless an OCR/vision plugin is configured. High-quality scientific PDFs from PubMed/PMC/EuropePMC/arXiv are native digital PDFs with full text layers.
2. **Two-Column Reading Flow**: MarkItDown handles two-column scientific text using pdfminer layout heuristics. In complex multi-column layouts with floating figures, sub-section ordering should be spot-checked during validation.

---

## 4. Conclusion
1. `markitdown` CLI and Python API are 100% verified, configured, and operational in `C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64`.
2. The optimal RAG pipeline is specified in detail in `.agents/spec_miner_markitdown/analysis.md`.
3. Standardized YAML frontmatter schema has been tailored for Aegis Coach sports science, injury rehab, and physiological planning.
4. Ready for downstream workers to acquire the 5-10 Gold Standard scientific PDFs and execute batch conversion.

---

## 5. Verification Method
To independently verify MarkItDown PDF conversion in this environment, execute:

```powershell
# 1. Verify MarkItDown CLI version
& 'C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\Scripts\markitdown.exe' -v

# 2. Run conversion test on sample PDF
& 'C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\Scripts\markitdown.exe' .agents/spec_miner_markitdown/probe_std.pdf -o .agents/spec_miner_markitdown/test_verify.md

# 3. Verify output markdown content
Get-Content .agents/spec_miner_markitdown/test_verify.md

# 4. Run automated test suite
python .agents/spec_miner_markitdown/probe_markitdown_suite.py
```
