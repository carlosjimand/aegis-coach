# Dispatch Log

## 2026-08-26T20:48:50Z

User Objective & Requirements:
1. R1. Scientific Literature Acquisition:
   Search for and download 5 to 10 high-quality, "Gold Standard" scientific papers (PDFs) focusing on:
   - Trail running polarized training (e.g., Stephen Seiler 80/20 model)
   - Hamstring rehabilitation (e.g., Carl Askling L-Protocol)
   - Silbernagel's pain-monitoring model / tendon rehabilitation & biomechanics.

2. R2. Markdown Conversion:
   Convert all downloaded PDF files into clean, well-formatted Markdown files using the `markitdown` CLI tool (available locally at `C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\Scripts\markitdown.exe` or `python -m markitdown`), ensuring token-efficient and highly readable text ready for RAG vector stores.

3. R3. User Action Guide:
   Generate a step-by-step guide (`mvp_next_steps.md` in the project workspace) explicitly listing manual actions the user must perform (e.g., configuring Oracle Cloud free tier / Docker instance for Qdrant vector database, opening ports/firewall rules, environment secrets) that cannot be executed automatically.

4. Deliverables & Acceptance Criteria:
   - At least 5 markdown files corresponding to the scientific papers in the project workspace (e.g., in a dedicated `data/papers/` or `rag/papers/` or workspace directory).
   - Clean, parsed markdown without raw PDF binary artifacts.
   - `mvp_next_steps.md` generated with clear deployment/manual configuration instructions.
   - Comprehensive test suite / verification validating markdown readability, token formatting, and presence of all required papers and guides.
