## 2026-08-26T20:58:19Z
You are Worker M2.1 for Aegis Coach Phase 2 (Literature Acquisition & Markdown Pipeline).
Your Working Directory: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\worker_m2_1_literature
Original Request Path: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\ORIGINAL_REQUEST.md
Project Blueprint: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\PROJECT.md
Spec Miner Papers Analysis: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\spec_miner_papers\analysis.md
Spec Miner MarkItDown Analysis: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\spec_miner_markitdown\analysis.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Write Ownership (Exclusive):
You own:
- `data/papers/pdfs/` (all PDF files)
- `data/papers/raw_markdown/` (raw markitdown conversions)
- `data/papers/markdown/` (clean, enriched markdown files)
- `data/papers/manifest.json` (metadata index)
- `scripts/ingest_papers.py` (download, conversion, cleaning, validation script)

Tasks:
1. Read ORIGINAL_REQUEST.md and the survey analysis files.
2. Implement `scripts/ingest_papers.py` to:
   - Download the 11 Gold Standard open-access scientific papers (from PMC, frontiers, etc. identified in spec_miner_papers/analysis.md) into `data/papers/pdfs/`.
   - Ensure resilient download with valid headers/User-Agent, content-type/magic-byte checks, and fallback mechanisms.
   - Run `markitdown` CLI / Python API (`from markitdown import MarkItDown`) to convert each PDF to raw markdown in `data/papers/raw_markdown/`.
   - Apply the two-stage cleaning and normalization:
     * Remove `\x0c` form feeds and excessive whitespace.
     * Clean running headers/footers and page number artifacts.
     * De-hyphenate broken words across line breaks.
     * Preserve tables in GitHub Flavored Markdown (GFM).
     * Inject structured YAML frontmatter matching `PROJECT.md` schema (title, authors, year, journal, doi, pmid, pmcid, domain, topics, target_anatomy, key_protocols, contraindications, evidence_level, ingestion info).
   - Write clean, enriched markdown files to `data/papers/markdown/`.
   - Generate `data/papers/manifest.json`.
3. Execute `python scripts/ingest_papers.py` to verify that at least 5 to 11 papers are fully downloaded, converted, cleaned, and indexed.
4. Run validation checks on markdown readability, token formatting, and table integrity.
5. Write your handoff report to `handoff.md` and detailed execution log to `progress.md` in your working directory.
6. Send a message back to the orchestrator when complete.
