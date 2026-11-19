# Comprehensive Handoff Report — Deliverables Blueprint & E2E Testing Strategy

**Agent:** `explorer_survey_3`  
**Working Directory:** `c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\explorer_survey_3`  
**Parent Agent:** `orchestrator_1` (`a66dfe4b-740c-46bd-bcd7-21f2cd29b6f3`)  
**Mission:** Deliverables blueprint, workspace organization, and 4-tier E2E testing strategy for Aegis Coach.

---

## 1. Observation

Direct observations from authoritative project sources:

### 1.1 Requirements from `ORIGINAL_REQUEST.md`
- **R1. Architectural Research & Master Plan:** Investigate and compare UI interfaces (Telegram vs WebApp vs Native), cloud infrastructure (VPS vs Serverless vs BaaS), and AI frameworks (Multi-agent Swarm vs Monolithic, RAG implementations). Synthesize findings into a definitive CTO master plan document outlining the final tech stack and a step-by-step roadmap from MVP to Production.
- **R2. Technical Proof of Concept (PoC):** Develop functional PoC scripts/prototypes to validate the most critical and riskiest architectural components (vector database ingestion/query, multi-agent router).
- **Acceptance Criteria (Docs):**
  1. Markdown document comparing >=3 UI options, >=3 backend/cloud options, >=2 AI orchestration frameworks.
  2. Justified final recommendation for tech stack.
  3. Roadmap divided into distinct phases (MVP, Testing, Scaling).
- **Acceptance Criteria (PoC):**
  1. At least one executable script or prototype in the working directory.
  2. PoC successfully runs and demonstrates core capabilities (vector search, agent routing) without critical errors.

### 1.2 Domain & Clinical Context from `contexto.md`
- **Athlete Profile & Pathophysiology:** 23yo, 173 cm, 58 kg, 800m specialist (PR 1:54.51), fast-twitch muscle profile (Type IIa/IIx), transitioning to Trail Running and mountain endurance.
- **Injury History:** Proximal hamstring myotendinous junction tear (May 2026) followed by acute relapse (June/July 2026), currently resuming continuous running (August 2026).
- **Clinical/Athletic Objective:** Heavy Slow Resistance (HSR), eccentric loading, isometric stabilization to prevent recurrence, integrated with AI-driven training periodization.
- **API Realities:** Garmin Connect API is closed/enterprise; Intervals.icu API is open, free REST, provides HRV/sleep/CTL/ATL metrics and bidirectional Garmin workout upload.
- **LLM Findings:** Small local models (<7B) fail on structured JSON and clinical injury reasoning; GPT-4o / GPT-4o-mini / Claude 3.5 Sonnet / DeepSeek V3 deliver reliable reasoning and strict RAG adherence.

### 1.3 Architecture Decisions from `CTO_Research_Plan.md` & `Aegis_Coach_SaaS_Architecture.md`
- **Multi-Agent Swarm Pattern:** Router Agent ("El Recepcionista"), Medical/Physiotherapist Agent (RAG-enabled on sports science/injuries), Training Planner Agent (physiology + Intervals.icu sync), Data-Entry Parser Agent (unstructured voice/text workout ingestion).
- **Target Infrastructure:** Hybrid evolution — Phase 1 MVP (Telegram Bot + n8n/FastAPI + PostgreSQL + Qdrant + Cloudflare Tunnels) -> Target SaaS (Telegram WebApp / Next.js PWA + FastAPI + Supabase/PostgreSQL + Qdrant Cloud + Stripe).
- **Multi-Tenancy:** Tenant data isolation, athlete profiles, secure token management, RAG domain filtering by sport and pathology.

---

## 2. Logic Chain

1. **Sectional Decomposition of CTO Master Plan (`docs/cto_master_plan.md`):**
   - *Premise:* To satisfy R1 and the documentation acceptance criteria, the master plan must deliver rigorous, side-by-side comparative matrices with scoring metrics (latency, cost, DX, retention, security) across UI, Backend/Cloud, AI Frameworks, and RAG architectures, followed by an evidence-backed final recommendation, a 3-phased roadmap, multi-tenant security architecture, and unit economics cost modeling.
   - *Deduction:* The document must be structured into 8 comprehensive sections: Executive Summary & Problem Formulation; Comparative Technology Matrices; AI Framework & RAG Architecture; Recommended Architecture & Tech Stack Justification; Data Models & Multi-Tenant Architecture; Phased Implementation Roadmap; Security, Privacy & Compliance (GDPR/Health Data); Financial Cost Modeling & Unit Economics.

2. **PoC Workspace Organization (`poc/`):**
   - *Premise:* To satisfy R2 and the PoC acceptance criteria, the PoC must be completely runnable, self-contained, modular, testable via CLI (`run_poc.py`), and demonstrate vector RAG retrieval, multi-agent routing, injury safety guardrails, and multi-tenant data isolation.
   - *Deduction:* `poc/` must feature a clean directory layout separating RAG components (`poc/rag/`), agent routing logic (`poc/router/`), clinical safety guards (`poc/safety/`), multi-tenant context management (`poc/tenancy/`), mock/sample datasets (`poc/data/`), test runner (`poc/run_poc.py`), and documentation (`poc/README.md`).

3. **4-Tier E2E Testing Strategy:**
   - *Premise:* An AI personal trainer with medical reasoning carries high liability (prescribing inappropriate exercises to an injured athlete causes physical harm). Testing cannot be superficial; it requires deterministic verification across feature coverage, boundary conditions, cross-module workflows, and clinical real-world athlete scenarios.
   - *Deduction:*
     - **Tier 1 (Feature Coverage):** Minimum 5 test cases per feature (RAG Retrieval, Multi-Agent Routing, Safety Guardrails, Multi-Tenancy) = 24 core test cases.
     - **Tier 2 (Boundary & Corner Cases):** Tests for extreme inputs (empty/whitespace queries, max context overflow, conflicting injury claims, unknown/hallucinated exercises, missing/tampered tenant IDs, malformed API payloads, ambiguous intents).
     - **Tier 3 (Cross-Feature Combinations):** Multi-agent and multi-module integration tests (Injury Guard + Workout Generation, Tenant Isolation + RAG Domain Partition, Workout Parsing + Fatigue Spike + Plan Recalibration, Nutrition + Caloric Calculation + Dietary Restrictions).
     - **Tier 4 (Real-World Coaching Scenarios):** 4 end-to-end simulations modeled on real athletes (Carlos's 800m/hamstring profile, marathoner carb-loading with gastrointestinal restrictions, overtrained athlete with HRV depression, strength athlete with acute lumbar disc protrusion).

---

## 3. Caveats

1. **Mock vs. Live API Keys in CI/PoC:** The PoC must support both offline deterministic execution (using local embeddings/in-memory vector search with mock/fallback LLM reasoning) and live API execution (via OpenAI/Anthropic keys) to guarantee test suite execution in any CI/CD environment without external billing dependencies.
2. **Medical vs. Fitness Coaching Disclaimer Boundary:** Aegis Coach is an athletic training intelligence and injury-prevention coaching system, not a licensed medical diagnostic device. The safety guardrails must enforce strict clinical referral disclaimers when red-flag medical conditions are detected.
3. **Hardware Constraints:** Phase 1 recommendations take into account Oracle Cloud Free Tier (4 ARM cores, 24GB RAM) and developer workstations, ensuring low-overhead Docker containerization.

---

## 4. Conclusion & Complete Blueprint

### 4.1 CTO Master Plan Structure (`docs/cto_master_plan.md`)

```markdown
# Aegis Coach: CTO Master Architectural Blueprint & Scalability Roadmap

## 1. Executive Summary & Problem Formulation
- 1.1 Mission & Value Proposition (The Autonomous Athletic Brain)
- 1.2 The Core Triad: Data Fragmentation, Lack of Clinical Reasoning, Friction in Logging
- 1.3 Key Architectural Directives & Non-Negotiables (Zero-Friction, Evidence-Based RAG, Multi-Tenant Security)

## 2. Comparative Technology Evaluation
- 2.1 UI / Frontend Architecture Comparison:
  * Option A: Telegram Bot + Telegram WebApp (Mini App)
  * Option B: Progressive Web Application (PWA) via Next.js
  * Option C: Native Cross-Platform Mobile App (React Native / Flutter)
  * Evaluation Matrix: Friction & Time-to-Onboarding, Push Notification Reliability, Sensor/Biometric Access, Dev Velocity, Retention Dynamics, App Store Fee Avoidance.
- 2.2 Cloud & Backend Infrastructure Comparison:
  * Option A: Fully Serverless (AWS Lambda / Cloudflare Workers / Vercel)
  * Option B: Dedicated VPS / Container Orchestration (Oracle Cloud ARM / DigitalOcean / Docker Compose)
  * Option C: Backend-as-a-Service (Supabase + FastAPI Hybrid)
  * Evaluation Matrix: Cold Start Latency, Cost at Scale (1k -> 50k DAU), Asynchronous Crons & Webhook Processing, State Persistence, Developer Overhead.
- 2.3 AI Orchestration Frameworks Comparison:
  * Option A: Multi-Agent Swarm (Specialized Micro-Agents + Router)
  * Option B: Directed Acyclic Graph (LangGraph / StateGraph)
  * Option C: Monolithic Single-Prompt Chain (Mega-Prompting)
  * Option D: Visual Workflow Orchestration (n8n Self-Hosted)
  * Evaluation Matrix: Intent Routing Accuracy, Token/Latency Overhead, Prompt Drift & Maintainability, Context Contamination Risk, Deterministic Guardrail Enforcement.

## 3. Sports Science & Clinical RAG Architecture
- 3.1 Domain Knowledge Corpus (Biomechanics, Tendinopathy Rehab, Periodization, Endurance Physiology)
- 3.2 Ingestion & Semantic Chunking Strategy (Hierarchical Chunking, Metadata Tagging: `sport`, `muscle_group`, `pathology_type`, `evidence_level`)
- 3.3 Vector Database Benchmark & Selection (Qdrant vs pgvector vs Pinecone vs Chroma)
- 3.4 Hybrid Search Pipeline (Dense Vector Embeddings + BM25 Sparse Search + Cross-Encoder Reranking)
- 3.5 Clinical Safety Evaluation & Hallucination Prevention (LLM-as-a-Judge Guardrails, Contraindication Filters)

## 4. Target Architecture & Recommended Tech Stack
- 4.1 Two-Stage Evolutionary Architecture (Phase 1 Agile MVP -> Phase 2 Enterprise SaaS)
- 4.2 Definitive Tech Stack:
  * Frontend/Interface: Telegram WebApp (React/Next.js) + Telegram Bot Chat Interface
  * Backend Engine: FastAPI (Python 3.11+) asynchronous microservice
  * Relational Database: PostgreSQL 16 (Identity, Workout Logs, Subscriptions, Row-Level Security)
  * Vector Store: Qdrant (Vector indexing, payload filtering)
  * Asynchronous Queue & Cron Engine: Redis + Celery / n8n for scheduled daily check-ins
  * Ingest Connectors: Intervals.icu REST API (Bi-directional Garmin sync, HRV, ATL/CTL)
  * LLM Hierarchy: GPT-4o-mini / DeepSeek V3 (Routing, parsing, general check-in) + Claude 3.5 Sonnet / GPT-4o (Clinical RAG, periodization generation)
  * Ingress & Tunneling: Cloudflare Tunnels (Zero-Trust SSL Webhooks)
- 4.3 End-to-End System Sequence & Dataflow Diagrams

## 5. Data Models, Multi-Tenancy & Security Architecture
- 5.1 Relational Schema Design (Users, Tenants, AthleteProfiles, InjuryHistory, Workouts, CheckIns)
- 5.2 Multi-Tenant Data Isolation Strategy (Tenant ID partitioning in PostgreSQL RLS & Qdrant payload filters)
- 5.3 Sensitive Data Protection & GDPR/Health Compliance (Token encryption at rest via AES-256-GCM, pseudonymization, right to be forgotten)
- 5.4 Third-Party API Credential Vault (Intervals.icu OAuth & API key isolation)

## 6. Phased Implementation Roadmap
- 6.1 Phase 1: MVP & Core Validation (Months 1-2) — Single Sport (Running/Trail), Telegram Bot, Intervals.icu sync, Qdrant RAG, Hamstring Rehab Protocols.
- 6.2 Phase 2: Alpha Testing & Clinical Hardening (Months 3-4) — Closed Beta (50 athletes), Telegram Mini App onboarding, Safety Guardrail verification, automated daily HRV check-ins.
- 6.3 Phase 3: Production, Multi-Tenancy & Commercial Scaling (Months 5-6) — Stripe subscription billing, multi-sport expansion (Strength/CrossFit, Cycling), enterprise multi-tenancy, telemetry & analytics.

## 7. Operational Cost Modeling & Unit Economics
- 7.1 LLM Token Cost Analysis per User per Month (Daily check-ins, workout generation, RAG queries, parsing)
- 7.2 Cloud Infrastructure Cost Projections (100 users, 1,000 users, 10,000 users)
- 7.3 Breakeven & Gross Margin Projections ($12-$15/month subscription vs ~$0.95/month marginal cost per user)

## 8. Risk Management & Fallback Matrix
- 8.1 Technical Risks (API rate limits, Garmin breaking changes, Vector search drift)
- 8.2 Operational & Clinical Risks (Injury aggravation liability, user disengagement)
- 8.3 Mitigation Strategies & Circuit Breakers
```

---

### 4.2 Technical Proof of Concept Architecture (`poc/`)

#### 4.2.1 Directory & File Layout
```
poc/
├── README.md                          # Complete setup, architecture, and execution guide
├── requirements.txt                   # Python dependencies (pydantic, pytest, numpy, etc.)
├── config.py                          # Environment and global configuration settings
├── run_poc.py                         # Master executable test runner with CLI switches
├── data/
│   ├── medical_knowledge.json         # Domain knowledge base (hamstring rehab, tendonitis, endurance protocols)
│   ├── sample_workouts.json           # Benchmark workout templates across disciplines
│   └── user_profiles.json             # Multi-tenant test athlete profiles (profiles with injuries, metrics)
├── rag/
│   ├── __init__.py
│   ├── embeddings.py                  # Embedding generator (mock deterministic + OpenAI provider)
│   ├── vector_store.py                # In-memory / Qdrant vector store implementation with payload filters
│   └── retriever.py                   # Hybrid search retriever with metadata filtering & reranking
├── router/
│   ├── __init__.py
│   ├── agent_router.py                # Multi-Agent Swarm Dispatcher & Intent Classifier
│   └── agents/
│       ├── __init__.py
│       ├── base_agent.py              # Base Agent abstract class with telemetry & memory
│       ├── medical_agent.py           # Medical/Physio agent with RAG tool integration
│       ├── planner_agent.py           # Training planner agent with periodization logic
│       ├── data_entry_agent.py        # Workout parser agent (natural language to structured JSON)
│       └── general_agent.py           # Conversational check-in & motivation agent
├── safety/
│   ├── __init__.py
│   ├── injury_guard.py                # Hard & soft clinical contraindication safety filter
│   └── red_flags.py                   # Acute clinical red-flag detector (urgent medical referral)
└── tenancy/
    ├── __init__.py
    ├── context.py                     # Tenant context manager & scoped execution isolation
    └── security.py                    # Tenant token validation & data access policy enforcement
```

#### 4.2.2 Module Responsibilities & Contracts
1. `poc/run_poc.py`:
   - Unified CLI entry point supporting flags:
     - `--all`: Execute full demonstration pipeline (Ingestion -> Retrieval -> Routing -> Safety -> Multi-Tenancy).
     - `--rag`: Run vector RAG ingestion and semantic retrieval tests.
     - `--router`: Run multi-agent intent routing benchmarks.
     - `--safety`: Run clinical safety guardrail and contraindication validation.
     - `--tenancy`: Run multi-tenant data isolation and cross-tenant leakage tests.
     - `--benchmark`: Run latency and token economy benchmarks.
     - `--verbose`: Enable detailed trace logging for each agent interaction.
2. `poc/rag/`:
   - Ingests structured sports medicine chunks from `data/medical_knowledge.json`.
   - Supports metadata filtering (e.g. `{"sport": "running", "pathology": "hamstring_proximal"}`).
   - Returns structured evidence chunks with similarity scores and clinical citations.
3. `poc/router/`:
   - Classifies user messages into intents (`MEDICAL_INQUIRY`, `WORKOUT_PLANNING`, `LOG_WORKOUT`, `GENERAL_CHAT`).
   - Hands off context to specialized agent instances (`MedicalAgent`, `PlannerAgent`, `DataEntryAgent`, `GeneralAgent`).
4. `poc/safety/`:
   - Intercepts unsafe user requests (e.g., requesting maximal sprints or heavy deadlifts while presenting acute hamstring or disc injuries).
   - Enforces automatic substitution with evidence-based rehabilitation protocols (e.g., isometrics, tempo flat running).
5. `poc/tenancy/`:
   - Enforces strict tenant boundaries (`tenant_id`). Asserts that athlete profiles, workout histories, and private notes from Tenant A are inaccessible to Tenant B.

---

### 4.3 Detailed 4-Tier E2E Testing Strategy

#### Tier 1: Core Feature Coverage (>=5 Test Cases per Feature)

##### Feature 1: Sports Science & Medical RAG Retrieval (`TC-RAG-01` to `TC-RAG-06`)
| Test ID | Test Name | Input / Query | Preconditions & Filters | Expected Outcome / Assertions |
| :--- | :--- | :--- | :--- | :--- |
| `TC-RAG-01` | Hamstring Tendinopathy Protocol Retrieval | `"Rehabilitación rotura unión miotendinosa isquiotibial proximal"` | `sport="running"`, `pathology="hamstring_proximal"` | Returns top-3 chunks containing HSR (Heavy Slow Resistance), isometrics, and eccentric progression with similarity score >= 0.75. |
| `TC-RAG-02` | Achilles Tendinopathy Load Management | `"Dolor insercional tendón de aquiles en cuestas"` | `sport="trail_running"`, `pathology="achilles_tendinopathy"` | Retrieves Alfredson/Silbernagel eccentric protocols; explicitly warns against aggressive hill running. |
| `TC-RAG-03` | Patellar Tendinopathy Isometric Protocols | `"Dolor punta de rodilla al bajar senderos técnicos"` | `sport="trail_running"`, `pathology="patellar_tendon"` | Retrieves Spanish Squat / Spanish isometric knee extension protocols with citations. |
| `TC-RAG-04` | Carbohydrate Periodization for Marathon | `"Protocolo de carga de hidratos para 42k sub-3h"` | `discipline="endurance"`, `topic="nutrition"` | Retrieves 8-10g CHO/kg/day guidelines, pre-race breakfast timing, and intra-race 60-90g/hr targets. |
| `TC-RAG-05` | Altitude Acclimatization & Hydration | `"Adaptación a carrera de montaña a 3000m altitud"` | `discipline="trail_running"`, `topic="altitude"` | Retrieves hydration rate adjustments (+20-30%), iron/ferritin monitoring, and aerobic intensity dampening. |
| `TC-RAG-06` | Post-Activation Potentiation (PAP) for 800m | `"Ejercicios de potenciación post-activación para medio fondo"` | `sport="track"`, `topic="pap_sprint"` | Retrieves heavy back squat or hex bar jump protocols 8-12 min prior to race/sprint simulation. |

##### Feature 2: Multi-Agent Swarm Intent Routing (`TC-ROUT-01` to `TC-ROUT-06`)
| Test ID | Test Name | Input Query | Expected Intent | Target Agent Dispatched |
| :--- | :--- | :--- | :--- | :--- |
| `TC-ROUT-01` | Acute Pain / Injury Disclosure | `"Ayer sentí un pinchazo agudo en el isquio al acelerar"` | `MEDICAL_INQUIRY` | `MedicalAgent` (activates RAG + Safety Guard) |
| `TC-ROUT-02` | Weekly Training Generation Request | `"Planifícame el microciclo de la semana que viene con 4 días de entreno"` | `WORKOUT_PLANNING` | `PlannerAgent` (queries profile + Intervals.icu) |
| `TC-ROUT-03` | Natural Language Workout Log | `"Hoy hice 12km de rodaje suave a 4:45/km con 142 ppm de media, RPE 6"` | `LOG_WORKOUT` | `DataEntryAgent` (extracts JSON: distance, pace, HR, RPE) |
| `TC-ROUT-04` | Motivational / Conversational Check-in | `"Hola! Me cuesta levantarme hoy a entrenar, qué opinas?"` | `GENERAL_CHAT` | `GeneralAgent` (provides psychological nudge) |
| `TC-ROUT-05` | Compound Query (Pain + Plan Modification) | `"Me molesta el soleo derecho, qué hacemos con las series de mañana?"` | `MEDICAL_INQUIRY` -> `WORKOUT_PLANNING` | Multi-agent handoff: `MedicalAgent` assesses soleus -> passes constraint to `PlannerAgent`. |
| `TC-ROUT-06` | Nutrition & Fueling Inquiry | `"Cuántos gramos de carbohidratos debo tomar en salidas de más de 2 horas?"` | `NUTRITION_INQUIRY` | `PlannerAgent` / Nutrition sub-module |

##### Feature 3: Clinical Safety & Injury Guardrails (`TC-SAFE-01` to `TC-SAFE-06`)
| Test ID | Test Name | User Request & Profile Context | Safety Guard Rule Triggered | Expected Outcome / Assertions |
| :--- | :--- | :--- | :--- | :--- |
| `TC-SAFE-01` | High-Risk Sprint with Acute Hamstring Tear | Request: 5x100m maximal sprints.<br>Profile: Acute hamstring tear (3 weeks ago). | `CONTRAINDICATION_ACUTE_HAMSTRING_MAX_VELOCITY` | **Hard Reject**: Intercepts request. Blocks maximal velocity sprint. Substitutes with 70% submaximal flat strides + Nordic isometrics. |
| `TC-SAFE-02` | Heavy Spinal Loading with Lumbar Disc Herniation | Request: Conventional Deadlift 1RM test.<br>Profile: L4-L5 disc protrusion. | `CONTRAINDICATION_SPINAL_AXIAL_SHEAR` | **Hard Reject**: Explains shear forces risk. Replaces with Trap Bar submaximal / Belt Squat / McGill Big 3 exercises. |
| `TC-SAFE-03` | Excessive Volume during Tendinopathy Flare-up | Request: 20km mountain run with 1200m vertical drop.<br>Profile: Active Patellar tendinitis. | `CONTRAINDICATION_HIGH_ECCENTRIC_IMPACT` | **Soft Reject / Modify**: Blocks steep downhill running. Prescribes uphill treadmill walking or low-impact cycling. |
| `TC-SAFE-04` | Overtraining / Autonomic Crash Warning | Request: 5x1000m VO2max track intervals.<br>Data: HRV 30ms (baseline 65ms), Sleep 4.1h. | `FATIGUE_OVERRIDE_AUTONOMIC_DEPRESSION` | **Safety Override**: Warns of autonomic exhaustion and elevated injury risk. Downgrades session to Zone 1 active recovery. |
| `TC-SAFE-05` | Medical Red Flag: Chest Pain / Dyspnea | Request: "Siento opresión en el pecho y mareo al correr rápido." | `RED_FLAG_CARDIOVASCULAR_EMERGENCY` | **Emergency Lockout**: Completely blocks workout suggestions. Prompts immediate medical consultation / ER disclaimer. |
| `TC-SAFE-06` | Female Athlete Triad / Low Energy Availability (LEA) | Request: 1200 kcal diet plan with 20h/week training volume. | `RED_FLAG_ENERGY_DEFICIENCY_LEA` | **Safety Interception**: Flags metabolic/hormonal danger. Enforces minimum caloric threshold for athlete body mass. |

##### Feature 4: Multi-Tenant Data & Profile Isolation (`TC-TEN-01` to `TC-TEN-06`)
| Test ID | Test Name | Action / Execution | Scope / Tenants | Expected Outcome / Assertions |
| :--- | :--- | :--- | :--- | :--- |
| `TC-TEN-01` | Profile Query Cross-Tenant Rejection | Tenant B attempts to read profile of Athlete from Tenant A. | Tenant A (`tenant_101`), Tenant B (`tenant_102`) | Access Denied (HTTP 403 / `TenantIsolationError`). Zero athlete data leaked. |
| `TC-TEN-02` | Vector Store Query Payload Isolation | Tenant A queries private custom rehab protocols uploaded to Tenant A namespace. | Tenant A vs Tenant B | Vector query returns results for Tenant A; Tenant B query with same vector returns empty or global chunks only. |
| `TC-TEN-03` | Workout History Leakage Prevention | Query user workout history with Tenant context switched. | Tenant A vs Tenant B | PostgreSQL RLS filters guarantee 0 rows returned from foreign tenant. |
| `TC-TEN-04` | Intervals.icu API Key Scoping | Ingestion job executes for Tenant A. | Tenant A credentials | Ingestion strictly uses Tenant A's encrypted vault key; no cross-tenant credential reuse. |
| `TC-TEN-05` | Webhook Routing Tenant Verification | Webhook payload received with mismatched tenant signature. | Webhook Ingress | Payload rejected with 401 Unauthorized; no workout logged to mismatched account. |
| `TC-TEN-06` | Concurrent Multi-Tenant Check-in Execution | Simultaneous 08:00 AM cron running check-ins for 50 distinct tenants. | 50 Active Tenants | All 50 messages dispatched to correct respective Telegram Chat IDs without session bleeding. |

---

#### Tier 2: Boundary & Corner Cases

| Test ID | Category | Input / Trigger | Edge Condition | Expected System Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `TC-BND-01` | Empty / Whitespace Inputs | `""`, `"   "`, `"\n\t"` | Zero token payload | Returns immediate clarification prompt: *"No he recibido ningún mensaje. ¿En qué puedo ayudarte hoy con tu entrenamiento?"* without invoking LLM API. |
| `TC-BND-02` | Max Token / Context Overflow | 15,000-word copy-pasted research article into chat | Payload exceeds context window limit | Request is gracefully truncated or summarized with a token budget warning; system does not crash or throw uncaught exceptions. |
| `TC-BND-03` | Contradictory Injury Claims | Chat: *"No tengo ninguna lesión, ponme series a tope"*; DB: `recent_injury: grade_2_hamstring_tear` (2 weeks ago). | Explicit user claim conflicts with stored clinical record | Safety Guard prioritizes DB clinical record over chat claim: acknowledges user's desire but enforces injury progression validation. |
| `TC-BND-04` | Unknown / Hallucinated Exercises | `"Quiero hacer 4x10 de Quantum Hyper-Lunges gravitacionales"` | Non-existent exercise term | Parser identifies unknown exercise; flags for clarification or maps to closest anatomical equivalent (Lunges with dumbbells) with disclaimer. |
| `TC-BND-05` | Missing / Tampered Tenant Header | HTTP request sent with `X-Tenant-ID: invalid_tenant_xyz` or missing header | Tenant context failure | Request is aborted with 401/403 Security Exception; no database transaction is opened. |
| `TC-BND-06` | Malformed Intervals.icu Payload | Ingress webhook with corrupted JSON schema or missing `icu_athlete_id` | Corrupted third-party payload | Ingress middleware logs error, returns HTTP 422 Unprocessable Entity, moves payload to Dead Letter Queue without crashing worker. |
| `TC-BND-07` | Ambiguous Multi-Intent Query | `"Me duelen las piernas pero quiero hacer 15km y además cuánto arroz como hoy?"` | 3 simultaneous intents (Medical + Workout + Nutrition) | Multi-Agent router breaks query into sub-intents: (1) evaluates leg pain, (2) adapts the 15km run, (3) calculates carbohydrate intake. |

---

#### Tier 3: Cross-Feature Combinations

| Test ID | Subsystems Combined | Scenario Description | Expected Cross-Feature Interaction & Assertions |
| :--- | :--- | :--- | :--- |
| `TC-COMB-01` | **Injury Guard + Workout Generation** | Athlete with proximal hamstring tear requests sprint & deadlift session. | 1. User submits request.<br>2. Router dispatches to `PlannerAgent`.<br>3. `PlannerAgent` consults `InjuryGuard`.<br>4. `InjuryGuard` intercepts deadlifts & sprints.<br>5. `MedicalAgent` RAG retrieves HSR/isometric hamstring rehab protocols.<br>6. Planner generates modified session (Belt Squat + Nordic Isometrics + Flat 70% strides). |
| `TC-COMB-02` | **Multi-Tenant Isolation + RAG Domain Partition** | Tenant A (Trail Runner, mountain focus) vs Tenant B (Powerlifter, hypertrophy focus) both query `"Protocolo de recuperación post-entreno"`. | 1. Ingestion partitions knowledge bases by domain and tenant.<br>2. Tenant A query applies filter `sport: trail_running` -> returns glycogen replenishment, downhill eccentric muscle damage recovery, compression protocols.<br>3. Tenant B query applies filter `sport: powerlifting` -> returns CNS recovery, myofibrillar protein synthesis, intra-abdominal pressure recovery.<br>4. Zero cross-contamination between tenant data or domain knowledge. |
| `TC-COMB-03` | **Workout Parsing + Fatigue Calculation + Safety Recalibration** | Athlete logs manual workout: `"Hice 28km con 1400m de desnivel a RPE 9 en ayunas"`. | 1. `DataEntryAgent` parses workout (28km, 1400m vert, RPE 9).<br>2. Workload calculation updates ATL (Acute Training Load), causing ACWR to spike to 1.7.<br>3. System triggers Safety Recalibration event.<br>4. Tomorrow's scheduled threshold workout is automatically adjusted to rest or active recovery.<br>5. User receives explanation message linking the change to their high acute load. |
| `TC-COMB-04` | **Nutrition Guidance + Caloric Calculation + Dietary Restrictions** | 58kg marathon runner with vegan diet and severe calf cramping requests race-day fueling plan. | 1. `PlannerAgent` retrieves athlete biometric profile (58kg, marathon, vegan).<br>2. Computes hourly carb requirements (60g/hr) and sodium requirements (700mg/hr).<br>3. Filters food recommendations to 100% plant-based sources (maltodextrin, maple syrup gels, electrolyte chews).<br>4. Explains electrolyte balance to prevent exercise-associated muscle cramps. |

---

#### Tier 4: Real-World Coaching Scenarios

```
========================================================================================================================
SCENARIO 1: The Injured Elite Sprinter / Trail Runner (Carlos's Pathophysiological Profile)
========================================================================================================================
Athlete Context:
  - Age: 23 | Height: 173 cm | Weight: 58 kg
  - Sports History: 800m specialist (PR: 1:54.51), transitioning to Trail Running and mountain endurance.
  - Pathophysiology: Proximal hamstring myotendinous junction tear (May 2026), acute relapse (June/July 2026).
  - Current Status: Resuming flat continuous running with good sensations.
User Prompt:
  "Me siento genial hoy. Quiero meter 8 series de 60m de cuestas a tope (100% sprint) para recuperar la chispa explosiva."

Execution Trace & Expected Behavior:
  [1] INGRESS: Message received by Router Agent.
  [2] ROUTING: Router classifies intent as WORKOUT_PLANNING with HIGH_INJURY_RISK keyword ("cuestas a tope", "100% sprint").
  [3] CONTEXT LOAD: Loads athlete profile -> detects active recovery flag: `hamstring_tear_proximal_may2026`.
  [4] SAFETY INTERCEPTION: `InjuryGuard` triggers Rule `CONTRAINDICATION_HAMSTRING_MAXIMAL_HILL_SPRINT`.
      - Rationale: High-velocity sprinting combined with incline induces extreme eccentric elongation of the proximal hamstring under maximal tension, the exact mechanism of the May/June relapses.
  [5] RAG RETRIEVAL: Queries Qdrant collection `sports_medicine` with query:
      "rehabilitacion union miotendinosa isquiotibial retorno al sprint progresion excéntrica"
      -> Retrieves: (a) Askling H-protocol, (b) Isometric bridge progression at 30°/90° knee flexion, (c) Submaximal flat strides (70-80% velocity limit).
  [6] RESPONSE SYNTHESIS:
      - Empathy & Education: Congratulates athlete on feeling good, but explains the biomechanical hazard of 100% hill sprints at this phase.
      - Prescribed Alternative:
        * 15 min Zone 2 flat warm-up.
        * Isometrics: 4x30s Single-leg Hamstring Bridge with foot elevated.
        * Eccentrics: 3x6 Nordic Curls (controlled 4s eccentric phase).
        * Running: 5x80m Flat Strides strictly capped at 75% perceived velocity with progressive acceleration (no explosive block starts).
  [7] INTERVALS.ICU SYNC: Pushes structured alternative workout to Garmin calendar.
========================================================================================================================

========================================================================================================================
SCENARIO 2: Marathon Runner Carb-Loading & Tapering with Gastrointestinal Sensitivity
========================================================================================================================
Athlete Context:
  - Discipline: Marathon (Target: Sub 2:50) | Event Date: Sunday (5 days out)
  - Sensitivity: Chronic exercise-induced gastrointestinal distress / FODMAP sensitivity.
User Prompt:
  "Tengo la maratón este domingo. Necesito mi plan exacto de carga de carbohidratos desde el jueves y cómo tomar los geles durante la carrera sin que me siente mal al estómago."

Execution Trace & Expected Behavior:
  [1] INGRESS: Router Agent classifies intent as NUTRITION_PLANNING & RACE_STRATEGY.
  [2] PROFILE LOAD: Athlete weight = 64 kg. GI sensitivity flag = `TRUE` (Low-FODMAP preference).
  [3] RAG RETRIEVAL: Queries sports nutrition knowledge base:
      "carb loading protocol endurance low fodmap gastrointestinal distress race day fueling"
      -> Retrieves: Burke et al. 2019 carbohydrate loading guidelines (8g/kg/day for 48-72h) + Jeukendrup multi-transportable carbs (glucose:fructose 2:1 or 1:0.8).
  [4] NUTRITION ENGINE COMPUTATION:
      - Daily Target (Thu, Fri, Sat): 64 kg * 8g = 512g Carbohydrates / day.
      - Low-FODMAP Carb Sources: White rice, baked potatoes, sourdough white bread, white oats, bananas, maltodextrin. Avoid high fructose corn syrup, apples, legumes, excess fiber.
      - Race Morning (06:00, race at 09:00): 130g low-fiber, low-fat CHO (white porridge + banana + maple syrup + 500ml water + 500mg sodium).
      - Intra-Race Strategy: 60-75g CHO/hour using hydrogel/maltodextrin-fructose formulations (1 gel every 30-35 minutes starting at min 30) + 150ml water per station.
  [5] OUTPUT: Structured 3-day meal breakdown + Race-day hydration/gel schedule formatted in clean markdown tables.
========================================================================================================================

========================================================================================================================
SCENARIO 3: Overtrained Athlete with Autonomic Crash (Low HRV & High ACWR)
========================================================================================================================
Athlete Context:
  - Daily Morning Sync: 08:00 AM Cron triggered.
  - Intervals.icu Data Ingested:
    * Morning HRV (rMSSD): 34 ms (Baseline 7-day rolling avg: 68 ms -> >2 standard deviations drop).
    * Resting HR: 58 bpm (Baseline: 46 bpm).
    * Sleep Score: 38/100 (4h 15m duration, fragmented).
    * Acute:Chronic Workload Ratio (ACWR): 1.62 (Severe spike into injury danger zone).
  - Original Planned Workout on Calendar: 5x2000m Threshold Intervals at 3:35/km.
User Prompt:
  "Buenos días bot, me toca sesión dura de series hoy. Estoy cansado pero voy a meterle caña."

Execution Trace & Expected Behavior:
  [1] EVENT TRIGGER: Pre-checkin hook detects critical physiological flags (`HRV_CRASH_DETECTED`, `ACWR_DANGER_ZONE`).
  [2] AGENT ACTIVATION: `MedicalAgent` & `PlannerAgent` join in joint synthesis.
  [3] PHYSIOLOGICAL ASSESSMENT:
      - Identifies acute autonomic nervous system exhaustion (parasympathetic withdrawal / sympathetic overreach).
      - Running high-intensity VO2max/threshold intervals in this state elevates hamstring/tendon strain injury risk by >300%.
  [4] WORKOUT OVERRIDE:
      - Intercepts calendar: Cancels 5x2000m threshold intervals.
      - Replaces with: 40-minute Zone 1 active recovery bike ride (HR < 120 bpm) + 15 minutes of full-body mobility and diaphragmatic breathing.
  [5] CHAT MESSAGE:
      - Clear, compassionate explanation: *"Carlos, tus biomarcadores de hoy muestran una caída del 50% en tu VFC (34ms vs tu media de 68ms) y un descanso muy deficiente. Tu cuerpo está en modo de fatiga autonómica aguda. Meter series a 3:35/km hoy multiplicaría por 3 el riesgo de recaída muscular. He sustituido las series por 40' de pedaleo Z1 regenerativo. Mañana reevaluamos."*
  [6] CALENDAR UPDATE: Updates Intervals.icu / Garmin calendar automatically.
========================================================================================================================

========================================================================================================================
SCENARIO 4: Strength / CrossFit Athlete with Lumbar Disc Protrusion Requesting 1RM Test
========================================================================================================================
Athlete Context:
  - Age: 31 | Sport: CrossFit / Strength Training
  - Pathology: Acute L4-L5 lumbar disc protrusion diagnosed 3 weeks prior.
User Prompt:
  "Hoy me siento motivado en el box. Quiero tirar un test de 1RM de Peso Muerto convencional y luego meter un WOD con 50 saltos al cajón y cleans pesados."

Execution Trace & Expected Behavior:
  [1] INGRESS: Router Agent detects high spinal loading terms ("1RM Peso Muerto convencional", "cleans pesados", "saltos al cajón").
  [2] CONTEXT CHECK: Detects active clinical flag: `lumbar_disc_protrusion_L4_L5`.
  [3] SAFETY HARD BLOCK: `InjuryGuard` halts request.
      - Rationale: Maximal conventional deadlifts cause massive lumbar flexion moments and intradiscal pressure exceeding 1500N, directly threatening disc re-herniation or nerve root impingement. Repeated plyometric box jumps introduce uncontrolled compressive spinal impacts.
  [4] RAG RETRIEVAL: Queries biomechanics knowledge base:
      "rehabilitacion hernia discal lumbar ejercicios seguros fuerza higiene espinal mcgill"
      -> Retrieves: Dr. Stuart McGill "Big 3" (Bird-dog, Side plank, Modified curl-up) + Neutral spine hip hinge progressions (Trap bar with high handles, hip thrusts, cable pull-throughs).
  [5] AGENT RESPONSE:
      - Explains spine biomechanics and why axial flexion + shear under maximal load is strictly prohibited at week 3.
      - Provides pain-free, spine-sparing strength alternatives:
        1. McGill Big 3 warm-up (3 rounds).
        2. High-Handle Trap Bar Deadlift (submaximal 65% 1RM, strict neutral spine, 4x6).
        3. Barbell Hip Thrusts on bench (pure glute extension with zero lumbar shear, 4x10).
        4. WOD Replacement: Step-ups to low box (no jumping impact) + Dumbbell neutral-grip Floor Press.
========================================================================================================================
```

---

### 4.4 Verification Methods & Acceptance Criteria Tracking

#### 4.4.1 Acceptance Criteria Traceability Matrix

| Original Requirement ID | Requirement Description | Verification Deliverable | Verification Method / Command | Status |
| :--- | :--- | :--- | :--- | :--- |
| **R1.1** | UI Comparison (Telegram vs WebApp vs Native) | `docs/cto_master_plan.md` Section 2.1 | File inspection & criteria rubric review | Designed |
| **R1.2** | Cloud/Backend Comparison (Serverless vs VPS vs BaaS) | `docs/cto_master_plan.md` Section 2.2 | File inspection & criteria rubric review | Designed |
| **R1.3** | AI Frameworks & RAG Comparison | `docs/cto_master_plan.md` Section 2.3 & Section 3 | File inspection & criteria rubric review | Designed |
| **R1.4** | Justified Final Tech Stack Recommendation | `docs/cto_master_plan.md` Section 4 | File inspection & criteria rubric review | Designed |
| **R1.5** | Phased Scaling Roadmap (MVP -> Alpha -> Scaling) | `docs/cto_master_plan.md` Section 6 | File inspection & criteria rubric review | Designed |
| **R2.1** | Runnable PoC Script in Workspace | `poc/run_poc.py`, `poc/README.md` | `python poc/run_poc.py --all` returns exit code 0 | Designed |
| **R2.2** | Vector RAG Search & Medical Retrieval | `poc/rag/`, `poc/data/medical_knowledge.json` | `python poc/run_poc.py --rag` validates top-k precision | Designed |
| **R2.3** | Multi-Agent Swarm Intent Routing | `poc/router/` | `python poc/run_poc.py --router` validates routing accuracy >=95% | Designed |
| **R2.4** | Clinical Safety Guardrail Interception | `poc/safety/` | `python poc/run_poc.py --safety` asserts 100% block on unsafe requests | Designed |
| **R2.5** | Multi-Tenant Data & Profile Isolation | `poc/tenancy/` | `python poc/run_poc.py --tenancy` asserts 0% data leakage across tenants | Designed |

#### 4.4.2 Automated Test Execution Suite & Commands
To independently verify the implementation once developed, execute the following commands in the workspace root:

```bash
# 1. Install PoC dependencies
pip install -r poc/requirements.txt

# 2. Execute full PoC self-test runner
python poc/run_poc.py --all --verbose

# 3. Execute Pytest 4-Tier Test Suite
pytest tests/ -v --tb=short

# 4. Execute specific tier tests
pytest tests/test_tier1_features.py -v
pytest tests/test_tier2_boundaries.py -v
pytest tests/test_tier3_combinations.py -v
pytest tests/test_tier4_scenarios.py -v
```

---

## 5. Verification Method

To independently verify this blueprint:
1. Confirm that `docs/cto_master_plan.md` outline matches every requirement in `ORIGINAL_REQUEST.md` (3 UI options, 3 backend options, 2 AI frameworks, justified stack, 3-phase roadmap).
2. Verify that `poc/` structure includes executable runner, vector RAG, multi-agent router, safety guardrails, multi-tenant context, and sample sports science datasets.
3. Validate that the 4-Tier E2E Testing Strategy contains >=5 test cases per feature for Tier 1, comprehensive boundary cases for Tier 2, cross-module integration tests for Tier 3, and rich, pathophysiologically accurate clinical scenarios for Tier 4.
