## 2026-08-26T20:04:17Z
You are worker_m2 for the Aegis Coach project.
Your working directory is: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\worker_m2

MANDATORY FIRST STEP: Read the authoritative user request at:
c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\ORIGINAL_REQUEST.md

Read the project blueprint and survey findings at:
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\PROJECT.md
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\explorer_survey_1\handoff.md
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\explorer_survey_3\handoff.md

Your task: Implement Milestone M2 — Architectural Research & CTO Master Plan Document.
Target file to write: `c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\docs\cto_master_plan.md` (You own `docs/` exclusively).

Requirements:
Write an exhaustive, high-level CTO master architectural blueprint covering:
1. Executive Summary & Problem Formulation (Data fragmentation, Lack of clinical/biomechanical reasoning in AI fitness apps, Friction in daily logging).
2. Comparative Technology Evaluation (Matrix with detailed scoring, trade-offs, and latency/cost metrics):
   - 2.1 UI/Frontend: Telegram Bot + Telegram Mini App (TMA) vs Progressive Web App (PWA / Next.js) vs Native Mobile (React Native / Flutter).
   - 2.2 Cloud & Backend: Dedicated Containers / VPS (Docker, Hetzner/Fly.io) vs Serverless (AWS Lambda/Vercel) vs Managed BaaS (Supabase).
   - 2.3 AI Orchestration Frameworks: Multi-Agent Swarm / State Graph (LangGraph) vs Monolithic Single LLM Prompt Chains vs CrewAI/AutoGen vs n8n.
3. Sports Science & Clinical RAG Architecture:
   - Domain knowledge corpus (Askling L-protocol, Silbernagel pain monitoring <=3/10, Banister ACWR CTL/ATL/TSB sweet spot [0.8-1.3] vs danger zone [>1.5], Seiler polarized 80/20, AMPK/mTOR concurrent interference).
   - Ingestion, semantic chunking, and metadata tagging.
   - Vector database comparison (Qdrant vs pgvector vs Pinecone vs Chroma).
   - Hybrid Search pipeline (Dense + BM25 Sparse + Cross-Encoder Reranking) & Medical Red-Flag Triage.
4. Target Architecture & Recommended Tech Stack:
   - Definitive tech stack with in-depth justification.
   - End-to-end dataflow sequence diagrams (Mermaid / text diagrams).
5. Data Models, Multi-Tenancy & Security Architecture:
   - Relational PostgreSQL schemas (Users, AthleteProfile, Workouts, CheckIns, InjuryHistory).
   - Multi-tenant isolation via Row-Level Security (RLS) & Qdrant payload filters.
   - Sensitive biometric data protection & GDPR/Health compliance (AES-256-GCM token encryption, right to be forgotten).
6. Phased Implementation Roadmap:
   - Phase 1: MVP & Core Validation (Months 1-2).
   - Phase 2: Alpha Testing & Clinical Hardening (Months 3-4).
   - Phase 3: Production, Multi-Tenancy & Commercial Scaling (Months 5-6).
7. Operational Cost Modeling & Unit Economics:
   - LLM Token cost per user/month (fast-path GPT-4o-mini vs deep clinical Claude 3.5 Sonnet).
   - Infrastructure scaling costs (100, 1,000, 10,000 users).
   - Unit economics ($12-$15/month subscription vs ~$0.95/month marginal cost).
8. Risk Management & Fallback Matrix.
