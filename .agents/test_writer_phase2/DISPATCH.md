## 2026-08-26T20:58:20Z

You are Test Writer for Aegis Coach Phase 2 (E2E Testing Suite).
Your Working Directory: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\test_writer_phase2
Original Request Path: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\ORIGINAL_REQUEST.md
Project Blueprint: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\PROJECT.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Write Ownership (Exclusive):
You own:
- `tests/test_phase2_rag_and_guide.py` (and test helper fixtures if needed in `tests/`)

Tasks:
1. Read ORIGINAL_REQUEST.md and PROJECT.md.
2. Implement a comprehensive 4-Tier test suite in `tests/test_phase2_rag_and_guide.py`:
   - Tier 1: Feature Coverage (Verification of downloaded PDF presence >= 5 to 10 papers, markdown conversions, frontmatter YAML structure, `mvp_next_steps.md` existence).
   - Tier 2: Boundary & Formatting Quality (Absence of raw PDF binary artifacts/form feeds `\x0c`, minimum token/word count per paper >= 1000 words, valid YAML frontmatter parsing, table GFM pipe syntax, heading hierarchy).
   - Tier 3: Cross-Feature Domain & Clinical Integrity (Checks that Polarized 80/20, Askling Hamstring L-Protocol, and Silbernagel Pain-Monitoring papers are all present with correct clinical tags, target anatomy, and protocol rules).
   - Tier 4: Real-World Ingestion & Guide Usability (Validation of `manifest.json` schema, test parsing of markdown chunks for vector store ingestion, verification of copy-pasteable bash/docker commands in `mvp_next_steps.md` including ports 6333/6334, API keys, and curl healthchecks).
3. Run `pytest tests/test_phase2_rag_and_guide.py` (or note initial run status if awaiting files).
4. Write your handoff report to `handoff.md` and send a message back to the orchestrator when done.
