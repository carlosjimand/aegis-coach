# Original User Request

## 2026-08-26T20:01:10Z

# Teamwork Project Prompt — Draft

> Status: Ready for launch — awaiting user approval
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Full team

Conduct a comprehensive CTO-level architectural research and design phase for "Aegis Coach", a multi-tenant B2C AI Personal Trainer platform. The team must evaluate UI approaches (Telegram vs WebApp vs Native), cloud infrastructure (Serverless vs VPS), AI frameworks (Swarm/Multi-agent vs Monolithic), and RAG implementations for medical/sports science, culminating in a definitive technical blueprint and scaling roadmap.

Working directory: ~/teamwork_projects/aegis_coach_research
Integrity mode: development

## Requirements

### R1. Architectural Research & Master Plan
Investigate and compare UI interfaces (Telegram vs WebApp vs Native), cloud infrastructure (VPS vs Serverless vs BaaS), and AI frameworks (Multi-agent Swarm vs Monolithic, RAG implementations). Synthesize the findings into a definitive CTO master plan document that outlines the final tech stack and a step-by-step roadmap from MVP to Production.

### R2. Technical Proof of Concept (PoC)
Develop functional Proof of Concept (PoC) scripts or prototypes to validate the most critical or riskiest parts of the chosen architecture (e.g., a script to ingest and query a vector database, or a basic multi-agent router).

## Acceptance Criteria

### Documentation
- [ ] A markdown document is generated containing a clear comparison of at least 3 UI options, 3 backend/cloud options, and 2 AI orchestration frameworks.
- [ ] The document includes a justified final recommendation for the tech stack.
- [ ] The document includes a roadmap divided into distinct phases (e.g., MVP, Testing, Scaling).

### Proof of Concept
- [ ] At least one executable script or prototype is created in the working directory.
- [ ] The PoC successfully runs and demonstrates a core capability (e.g., successful vector search or agent routing) without critical errors.

## 2026-08-26T20:48:13Z

# Teamwork Project Prompt — Draft

> Status: Ready for launch — awaiting user approval
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Full team (with browser subagent capabilities)

Research, download, and convert high-quality scientific papers on trail running, polarized training (80/20), hamstring rehabilitation (Askling protocol), and biomechanics into markdown using `markitdown`. This will form the core RAG database for Aegis Coach.

Working directory: ~/teamwork_projects/aegis_coach_rag_pipeline
Integrity mode: development

## Requirements

### R1. Scientific Literature Acquisition
Use the `browser` subagent to search for and download 5 to 10 high-quality, "Gold Standard" scientific papers (PDFs) focusing on: Trail running polarized training (e.g., Seiler 80/20), Hamstring rehabilitation (e.g., Askling L-Protocol), and Silbernagel's pain model.

### R2. Markdown Conversion
Convert the downloaded PDF files into well-formatted Markdown files using the `markitdown` CLI tool (which is already installed locally at `C:\Users\carlo\AppData\Local\Python\pythoncore-3.14-64\Scripts\markitdown.exe` or by running `python -m markitdown`), ensuring token-efficient and highly readable text for the RAG vector store.

### R3. User Action Guide
Generate a step-by-step guide (`mvp_next_steps.md`) explicitly listing the actions the user must manually perform (e.g., configuring Oracle Docker for Qdrant, opening ports) that the agent cannot execute automatically.

## Acceptance Criteria

### RAG Data Files
- [ ] At least 5 markdown files corresponding to the scientific papers are present in the working directory.
- [ ] The markdown files contain clean, parsed text without raw PDF binary artifacts.

### Next Steps Guide
- [ ] A `mvp_next_steps.md` guide is generated in the working directory.
- [ ] The guide includes clear, manual instructions for the user regarding Oracle/Qdrant deployment.

