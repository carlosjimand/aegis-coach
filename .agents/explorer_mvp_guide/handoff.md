# Handoff Report: Aegis Coach MVP User Action Guide & Cloud Infrastructure Specifications

**Agent:** Explorer 1 (`explorer_mvp_guide`)  
**Working Directory:** `c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\explorer_mvp_guide`  
**Handoff Type:** Hard (Task Complete)  
**Date:** 2026-08-26T22:51:00Z  

---

## 1. Observation

1. **Original User Request & Scope**:
   - In `ORIGINAL_REQUEST.md` (lines 56–68), Requirement R3 explicitly states:
     > "Generate a step-by-step guide (`mvp_next_steps.md`) explicitly listing the actions the user must manually perform (e.g., configuring Oracle Docker for Qdrant, opening ports) that the agent cannot execute automatically."
     > Acceptance Criteria: "A `mvp_next_steps.md` guide is generated in the working directory. The guide includes clear, manual instructions for the user regarding Oracle/Qdrant deployment."
2. **Architectural Foundations & Tech Stack Choices**:
   - In `Aegis_Coach_SaaS_Architecture.md` (lines 17–27) & `PROJECT.md` (lines 4–10):
     * Orchestrator: `n8n` / FastAPI containerized on Oracle Cloud Docker.
     * Vector Database: `Qdrant` (ideal for Docker ARM, storing clinical chunks).
     * Sports data API: `Intervals.icu` REST API for biometrics (HRV, RHR) and Garmin workout push.
     * LLMs: Tiered routing (`gpt-4o-mini` / `deepseek-v3` for fast routing/data-entry; `claude-3-5-sonnet` / `gpt-4o` for clinical sports medicine RAG).
3. **Vector Database & RAG Implementation in PoC**:
   - In `poc/config.py` (lines 26–76) and `poc/rag/vector_store.py` (lines 20–58, 150–244):
     * Embeddings: 128-dim deterministic vectors for offline mock mode, expandable to 1536-dim (`text-embedding-3-small`) or standard dense/sparse models in live mode.
     * Vector store filters: `target_anatomy`, `contraindications`, `rehab_phase`, and multi-tenant scoping (`tenant_id`).
4. **Cloud Infrastructure & OCI Always Free Nuances**:
   - In `docs/cto_master_plan.md` (lines 793–809):
     * Oracle Cloud Infrastructure (OCI) Always Free tier allows 4 OCPUs and 24 GB RAM on Ampere A1 ARM (`VM.Standard.A1.Flex`) at $0/mo cost.
     * Default Ubuntu images on OCI enforce strict `iptables` drop rules on non-SSH ports, requiring explicit firewall opening in both OCI VCN Security Lists (Layer 1) and host OS `ufw`/`iptables` (Layer 2).

---

## 2. Logic Chain

1. **Derivation of OCI VM Sizing from Application Demands (Observation 2, 4)**:
   - *Premise*: Aegis Coach deploys Qdrant vector database, background workers, and API services.
   - *Reasoning*: The Ampere A1 ARM shape (`VM.Standard.A1.Flex`) with 2–4 OCPUs and 12–24 GB RAM offers zero cost, huge memory bandwidth, and native ARM64 Docker support. Ubuntu 24.04 LTS provides long-term stability and modern kernel features.
2. **Containerization & Deployment Architecture (Observation 2, 3)**:
   - *Premise*: Qdrant must run reliably with state persistence across VM reboots.
   - *Reasoning*: Deploying via Docker Compose with host bind mounts (`/opt/qdrant/storage` and `/opt/qdrant/snapshots`) ensures zero data loss. Exposing ports `6333` (REST/Dashboard) and `6334` (gRPC) satisfies both browser dashboard access and high-throughput vector ingestion.
3. **Security Architecture & The OCI Firewall Trap (Observation 4)**:
   - *Premise*: Securing public cloud endpoints while ensuring accessibility for the user and webhook clients.
   - *Reasoning*: Enabling `QDRANT__SERVICE__API_KEY` prevents unauthorized vector store access. Because Oracle Ubuntu images default to dropping non-port-22 incoming traffic, the user must configure dual-layer ingress: OCI VCN Ingress Rules + Ubuntu UFW/iptables (`sudo ufw allow 6333/tcp && sudo ufw allow 6334/tcp`).
4. **Secret Management & Environment Orchestration (Observation 2, 3)**:
   - *Premise*: Aegis Coach requires keys for Telegram, LLM providers (OpenAI, Anthropic, DeepSeek), Intervals.icu, Supabase, and Qdrant.
   - *Reasoning*: A centralized `.env` configuration file with comprehensive documentation ensures seamless switching between mock mode (`AEGIS_MOCK_MODE=true`) and live production mode (`AEGIS_LIVE_MODE=true`).
5. **Verification & Diagnostics Protocol (Observation 1, 3)**:
   - *Premise*: The user must be able to confirm with 100% confidence that their cloud Qdrant deployment is healthy.
   - *Reasoning*: A 5-stage verification suite (Docker process check, remote `curl` healthcheck, collection lifecycle CRUD test, Web UI dashboard verification, and Python SDK test) gives immediate visual and programmatic proof of success.

---

## 3. Caveats

- **OCI Region Capacity**: In rare high-demand Oracle regions, Ampere A1 ARM instances can occasionally report "Out of Capacity". In that event, the fallback is an AMD `VM.Standard.E2.1.Micro` instance or deploying across another Availability Domain.
- **Dynamic IP vs Reserved Static IP**: If the user provisions an ephemeral public IP, stopping/restarting the VM in OCI will change the IP address. The guide should recommend reserving a free Reserved Public IP in the OCI Console.
- **SSL / TLS Termination**: In initial MVP phase, Qdrant runs over HTTP with an API key. For production WebApp integration, placing Qdrant behind Cloudflare Tunnels (Zero Trust) or Nginx with Let's Encrypt is recommended.

---

## 4. Conclusion

The technical specifications and procedural steps for `mvp_next_steps.md` are fully formulated and validated. The final deliverable will provide the user with an intuitive, foolproof, copy-paste guide organized into six core sections:
1. **Prerequisites & Account Setup**
2. **Oracle Cloud Free Tier VM Provisioning (Ampere A1 ARM + Ubuntu 24.04)**
3. **Docker Engine & Docker Compose V2 Setup**
4. **Qdrant Vector Database Deployment (Docker Compose + Persistence + Auth Key)**
5. **Dual-Layer Network Security (OCI VCN Ingress + Host UFW/iptables)**
6. **Environment Configuration (`.env`) & 5-Stage Verification Suite**

Full analysis and copy-paste code snippets are documented in `.agents/explorer_mvp_guide/analysis.md`.

---

## 5. Verification Method

1. **Inspect Analysis Output**:
   - View `.agents/explorer_mvp_guide/analysis.md` to confirm all technical details, commands, and `.env` specifications.
2. **Verify Configuration Integrity**:
   - Check that port mappings match Qdrant standards (`6333` REST, `6334` gRPC).
   - Check that Docker commands adhere to official Docker Engine V2 and Ubuntu 24.04 conventions.
   - Check that the OCI dual-firewall instructions address both OCI VCN security lists and Ubuntu host iptables.
