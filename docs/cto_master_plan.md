# Aegis Coach: CTO Master Architectural Blueprint & Scalability Roadmap
**Document Version:** 1.0.0-RELEASE  
**Classification:** Engineering & Clinical Architecture Specification  
**Author:** Technical Architecture & Sports Science Systems Engineering Group  
**Target Milestone:** Production Architecture Blueprint (Milestones M1–M5)  
**Date:** August 2026  

---

## 1. Executive Summary & Problem Formulation

### 1.1 Mission & Value Proposition: The Autonomous Athletic Brain
Aegis Coach is designed as an autonomous, multi-tenant AI personal training and clinical rehabilitation platform tailored for endurance athletes, track runners, and mountain/trail racers. Unlike conventional consumer fitness applications that deliver static PDF templates or basic algorithmic progression, Aegis Coach functions as an **Autonomous Athletic Brain**—synthesizing real-time physiological biometrics, biomechanical injury constraints, and sports science literature into adaptive daily training prescriptions.

The core objective is to eliminate the false dichotomy between *high performance* and *injury rehabilitation*. In competitive endurance and track disciplines (e.g., middle-distance track 800m/1500m, ultra-trail running, marathon), athletes routinely train on the boundary of tissue failure. Aegis Coach provides continuous closed-loop guidance, dynamically adjusting training intensity, volume, and neuromuscular loading while aggressively safeguarding injured kinetic chains.

```
       ┌────────────────────────────────────────────────────────┐
       │                AUTONOMOUS ATHLETIC BRAIN               │
       │                                                        │
       │   [Physiological Data]    [Clinical RAG Corpus]        │
       │   • Daily HRV & RHR       • Askling L-Protocol         │
       │   • Banister CTL/ATL/TSB  • Silbernagel Pain Model     │
       │   • Sleep & Soreness      • Seiler Polarized 80/20     │
       │             │                       │                  │
       │             ▼                       ▼                  │
       │     ┌───────────────────────────────────────┐          │
       │     │   Multi-Agent Swarm Orchestrator      │          │
       │     │   - Intent Classification             │          │
       │     │   - Biomechanical Safety Guard        │          │
       │     │   - Microcycle Periodization          │          │
       │     └──────────────────┬────────────────────┘          │
       │                        │                               │
       │                        ▼                               │
       │   [Zero-Friction UI]   [Deterministic Guardrails]      │
       │   • Telegram Audio/Text• Contraindication Filter       │
       │   • Telegram Mini App  • ACWR Volume Spike Gate        │
       │   • Intervals/Garmin   • Medical Red-Flag Triage       │
       └────────────────────────────────────────────────────────┘
```

---

### 1.2 The Core Triad of Fitness Technology Failures

Modern digital coaching tools and AI wrappers fail because of three systemic architectural shortcomings:

```
                      THE CORE TRIAD
                OF DIGITAL FITNESS FAILURES
                            ▲
                           / \
                          /   \
                         /     \
    1. Data Fragmentation ◄─────► 2. Lack of Clinical Reasoning
            \                         /
             \                       /
              \                     /
               ▼                   ▼
                  3. Friction in Daily
                        Logging
```

#### 1. Data Fragmentation Across Siloed Ecosystems
Athletes generate high-density physiological and kinetic data daily across disparate hardware platforms:
- **Wearables & GPS Devices:** Garmin Connect, Apple Watch, Coros, Suunto, Wahoo (recording HR, HRV rMSSD, cadence, elevation, power, sleep stages).
- **Analytics Platforms:** Intervals.icu, Strava, TrainingPeaks, GoldenCheetah (calculating Chronic Training Load [CTL], Acute Training Load [ATL], and Training Stress Balance [TSB]).
- **Manual Subjective Inputs:** WhatsApp/Telegram chats with human coaches, Notion injury logs, Apple Notes.

Because these data streams remain isolated, automated planning engines make decisions in a vacuum. A workout generator might prescribe a maximal $5 \times 1000\text{m}$ VO2max track session because the macrocycle calls for it, completely blind to the fact that the athlete's resting heart rate spiked by 8 bpm and nocturnal HRV dropped by 45% due to systemic autonomic fatigue.

#### 2. Lack of Clinical & Biomechanical Reasoning in AI Fitness Apps
Generic Large Language Model (LLM) wrappers treat exercise prescription as freeform creative writing. When an athlete discloses a *proximal hamstring myotendinous junction strain*, standard LLMs generate well-intentioned but biomechanically hazardous advice—recommending stretching, deep forward folds, or sprint drills. 

In sports medicine, tissue readaptation is governed by strict mechanical load principles:
- **Tendon and Myotendinous Junctions** require isometric stabilization and Heavy Slow Resistance (HSR) loading in mid-range muscle lengths, while completely avoiding maximal velocity sprint mechanics and deep hip flexion stretching in early phases (Askling et al., 2014).
- **Pain-Monitoring Protocols** (Silbernagel et al., 2007) allow transient discomfort up to $\le 3/10$ on a Visual Analog Scale (VAS) provided pain resolves within 24 hours and morning stiffness does not escalate.
- **Concurrent Training Interference** (Baar, 2014) dictates that high-intensity endurance running (activating AMPK and SIRT1) and heavy resistance training (activating mTORC1) must be separated by at least 6 to 8 hours to avoid dampening myofibrillar protein synthesis.

Standard AI fitness applications possess zero awareness of these kinetic constraints, risking catastrophic injury relapses.

#### 3. High Cognitive Friction in Daily Logging
The primary cause of churn in personal training software is logging fatigue. Requiring an athlete to open a heavy native application after a grueling 25 km mountain run, navigate through multi-step dropdown menus, select exercises, input load, and rate RPE leads to 60–80% drop-off within 14 days. 

Athletes demand zero-friction conversational interactions: sending a 10-second voice note via Telegram while walking home (*"Ran 12k easy at 4:50 pace, average HR 138, felt slight tightness in the left upper hamstring around 2/10, overall felt smooth"*), with the system automatically parsing biometrics, updating workload metrics, validating tissue safety, and providing instantaneous coaching feedback.

---

### 1.3 Key Architectural Directives & Non-Negotiables

To solve the Core Triad, Aegis Coach establishes five immutable architectural directives:

1. **Zero-Friction Conversational Ubiquity:** The primary athlete touchpoint must live inside messaging channels (Telegram Bot API paired with Telegram Mini Apps), enabling instantaneous voice-to-text logging, rich visual onboarding, and high-engagement push notifications with $>80\%$ open rates.
2. **Deterministic Safety-First Architecture:** AI agents must never possess unconstrained authority over workout generation. Every generated workout must pass through a hard deterministic **Biomechanical Safety Guard** and **ACWR Workload Gate** prior to delivery.
3. **Evidence-Based Clinical RAG Engine:** Clinical advice and rehabilitation protocols must be mathematically grounded via Hybrid Search (Dense Vectors + BM25 Sparse + Cross-Encoder Reranking) across a peer-reviewed sports science literature corpus.
4. **Bidirectional Hardware Synchronization:** Open integration with Intervals.icu REST API allows bi-directional data flow—extracting daily resting biometrics and pushing structured, step-by-step interval workouts directly to athlete Garmin devices without enterprise API paywalls.
5. **Multi-Tenant Cryptographic Isolation:** Strict multi-tenant security guarantees that athlete biometrics, injury records, and proprietary coaching knowledge are isolated at the database level via PostgreSQL Row-Level Security (RLS) and encrypted at rest with AES-256-GCM.

---

## 2. Comparative Technology Evaluation

To determine the production tech stack for Aegis Coach, we conducted a multidimensional comparative evaluation across the UI/Frontend, Cloud/Backend, and AI Orchestration layers.

---

### 2.1 UI / Frontend Architecture Comparison

```
┌───────────────────────────────────────────────────────────────────────────┐
│                       UI / FRONTEND TRADEOFF MATRIX                       │
├──────────────────────┬──────────────────────┬─────────────────────────────┤
│  Telegram Ecosystem  │ Progressive Web App  │    Native Mobile App        │
│  (Bot + Mini App)    │  (PWA / Next.js 15)  │  (React Native / Flutter)   │
├──────────────────────┼──────────────────────┼─────────────────────────────┤
│ • Zero login friction│ • Rich desktop canvas│ • Direct Apple HealthKit    │
│ • 80%+ Push open rate│ • Complex data tables│ • 120Hz native animations   │
│ • Voice-to-log speed │ • Limited iOS push   │ • High App Store fees (30%) │
│ • MVP in 2 weeks     │ • High logging drop  │ • 12-week build cycle       │
└──────────────────────┴──────────────────────┴─────────────────────────────┘
```

#### Detailed Comparative Matrix: UI & Frontend

| Evaluation Dimension | Weight | Telegram Ecosystem (Bot + Mini App / TMA) | Progressive Web App (PWA / Next.js) | Native Mobile (React Native / Flutter / Swift) |
|---|:---:|---|---|---|
| **Workout Logging Ergonomics & Adherence** | 25% | **9.8/10** — Unmatched conversational ease. Athlete sends 10s voice note or text directly in chat. Zero login screens. | **5.5/10** — Requires opening browser/PWA, authenticating, navigating to form. High friction post-workout. | **7.5/10** — Fast once opened, rich form components, but friction is higher than replying to a chat notification. |
| **Complex Visual Tasks (Onboarding, Body Maps, Charts)** | 20% | **9.0/10** — Telegram Mini App (TMA) embeds full React/Tailwind SPAs inside chat with haptics, theme sync, and SVG body maps. | **10/10** — Full responsive canvas. Unlimited screen real estate for periodization graphs (Banister curves, HRV trends). | **9.5/10** — Smooth 120Hz native components, interactive anatomical SVG selectors, gesture navigation. |
| **Push Notification Latency & Reliability** | 15% | **10/10** — Instantaneous Telegram server push. Immune to aggressive Android/iOS battery management. Open rate >80%. | **4.0/10** — iOS requires PWA installation to Home Screen for Web Push. High user drop-off; unreliable background triggers. | **9.5/10** — APNs / FCM native push notifications with Rich Actions, Live Activities (lock-screen timers), and silent sync. |
| **Wearables & OS Health Sync** | 15% | **6.5/10** — Indirect sync via Intervals.icu / Strava webhooks. Cannot read Apple HealthKit background data directly. | **3.0/10** — Web apps have zero native access to Apple HealthKit or Android Health Connect APIs. | **10/10** — Direct background read/write to Apple HealthKit, Health Connect, and Bluetooth LE heart rate straps. |
| **Development Speed & Time to Market** | 15% | **9.5/10** — 1–2 weeks for functional MVP. Standard Bot API + React Mini App. Zero App Store review delays. | **8.0/10** — 2–3 weeks. Standard Next.js/Tailwind setup deployed to Vercel or Cloudflare. | **4.0/10** — 8–14 weeks. Dual-platform compilation, provisioning profiles, Apple Review Guidelines compliance. |
| **Distribution & App Store Fee Avoidance** | 10% | **10/10** — $0 store fees. Instant viral link distribution (`t.me/AegisCoachBot`). Direct Stripe/Telegram Stars billing. | **9.5/10** — Custom domain hosting (~$10/mo). Zero store cut; 100% web payment retention. | **4.0/10** — Apple Developer ($99/yr), Google Play ($25), mandatory 15–30% Apple In-App Purchase tax, Guideline 1.4.1 health scrutiny. |
| **Weighted Total Score** | **100%** | **9.08 / 10 (WINNER)** | **6.48 / 10** | **7.43 / 10** |

#### Strategic UI Decision
- **Primary Interface (Phase 1–4): Hybrid Telegram Bot + Telegram Mini App (TMA in React 19 / Tailwind / shadcn)**. Provides zero-friction conversational logging and instant push notifications, supplemented by embedded web apps for rich visual interactions (injury mapping, onboarding).
- **Secondary Desktop Hub (Phase 2–3): Next.js 15 Web Application**. Serves desktop users for deep historical analysis, long-term Banister fatigue graphs, and coach overview dashboards.
- **Future Native Bridge (Phase 5/6): React Native / Capacitor Companion**. Packaged native wrapper deployed solely if direct Apple HealthKit background polling is required.

---

### 2.2 Cloud & Backend Infrastructure Comparison

```
┌───────────────────────────────────────────────────────────────────────────┐
│                      BACKEND & CLOUD TRADEOFF MATRIX                      │
├──────────────────────┬──────────────────────┬─────────────────────────────┤
│ Dedicated Containers │ Serverless Functions │        Managed BaaS         │
│ (Docker on Hetzner)  │ (AWS Lambda / Vercel)│     (Supabase + FastAPI)    │
├──────────────────────┼──────────────────────┼─────────────────────────────┤
│ • 0ms cold starts    │ • 1500ms cold start  │ • Native PostgreSQL RLS     │
│ • Persistent memory  │ • Hard 15s timeouts  │ • Zero-ops Auth & Storage   │
│ • Flat $25/mo cost   │ • Unpredictable bill │ • Built-in pgvector support │
│ • Python AI runtime  │ • Brittle DB pools   │ • Production scale ready    │
└──────────────────────┴──────────────────────┴─────────────────────────────┘
```

#### Detailed Comparative Matrix: Cloud & Backend

| Evaluation Dimension | Weight | Dedicated Containers / VPS (Docker on Hetzner / Fly.io) | Serverless Functions (AWS Lambda / Vercel Edge) | Managed BaaS (Supabase + FastAPI Hybrid) |
|---|:---:|---|---|---|
| **Cold Starts & Response Latency** | 25% | **10/10** — 0ms cold start. Persistent Python daemons maintain warm connection pools and persistent HTTP/2 sessions to LLMs. | **4.0/10** — 800ms–2500ms cold starts on Python Lambdas. Unacceptable for interactive chat and webhook streaming. | **8.5/10** — Sub-50ms query latency on managed Postgres with persistent connection pooling (PgBouncer). |
| **Long-Running Agent Reasoning & Streaming** | 25% | **10/10** — No execution timeouts. Multi-step RAG, multi-agent debates, and batch PDF parsing execute reliably. | **3.5/10** — Strict execution timeouts (10–15s on Vercel Hobby, 30s Cloudflare, 15m Lambda). Fails on multi-agent loops. | **8.0/10** — FastAPI worker handles heavy reasoning; Supabase handles fast transactional queries. |
| **Multi-Tenancy & Data Isolation Security** | 20% | **7.0/10** — Application-level ORM filters. Requires rigorous engineering discipline to prevent cross-tenant leaks. | **6.5/10** — Ephemeral execution environments, but database isolation must still be enforced at the application layer. | **10/10** — Native PostgreSQL Row-Level Security (RLS) tied to JWT tokens. Cryptographic tenant isolation out of the box. |
| **Background Scheduling & Cron Jobs** | 15% | **9.5/10** — Built-in Redis + Celery / async workers. Reliable 08:00 AM athlete morning readiness checks with exact timing. | **5.0/10** — Requires AWS EventBridge, CloudWatch rules, or external webhook pingers with custom auth overhead. | **8.5/10** — `pg_cron` extension triggers scheduled database events, webhooks, and background workers natively. |
| **Cost at Scale (100 -> 10,000 MAU)** | 15% | **9.5/10** — $10–$40/mo for 4–8 vCPU / 16–32GB RAM (Hetzner CPX31/41). Handles millions of monthly chat requests flat. | **4.0/10** — Per-invocation, per-GB-second, and token streaming bandwidth billing scales aggressively at high volume. | **9.0/10** — $25/mo Pro tier handles up to 100k MAU with managed backups, auth, and vector indexing included. |
| **Weighted Total Score** | **100%** | **9.28 / 10** | **4.45 / 10** | **8.88 / 10 (HYBRID WINNER)** |

#### Strategic Backend Decision
- **The Optimal Hybrid Backend:** **Python FastAPI Core (Dockerized on high-performance VPS / Fly.io) + Supabase (Managed PostgreSQL 16 + pgvector + RLS + Auth + Storage) + Redis (Task Queue & Cache)**.
- *Rationale:* Combines the raw computational power, scientific Python libraries (NumPy, SciPy, LangGraph), and zero-timeout execution of FastAPI with Supabase’s bulletproof multi-tenant Row-Level Security and vector persistence.

---

### 2.3 AI Orchestration Frameworks Comparison

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    AI FRAMEWORK ORCHESTRATION MATRIX                      │
├──────────────────────┬──────────────────────┬─────────────────────────────┤
│  Multi-Agent Graph   │ Monolithic Single    │     CrewAI / AutoGen        │
│     (LangGraph)      │   Prompt Chains      │   Autonomous Frameworks     │
├──────────────────────┼──────────────────────┼─────────────────────────────┤
│ • Strict graph edges │ • Context saturation │ • Non-deterministic loops   │
│ • Deterministic safe │ • Hallucination risk │ • High token chatter waste  │
│ • Pydantic contracts │ • High token cost    │ • Fragile handoffs          │
│ • Fast/deep routing  │ • Brittle JSON schema│ • Hard to debug in prod     │
└──────────────────────┴──────────────────────┴─────────────────────────────┘
```

#### Detailed Comparative Matrix: AI Orchestration

| Evaluation Dimension | Weight | Multi-Agent State Graph (LangGraph / StateGraph) | Monolithic Single LLM Prompt Chains | CrewAI / AutoGen Frameworks | Visual Workflows (n8n Self-Hosted) |
|---|:---:|---|---|---|---|
| **Domain Specialization & Modularity** | 25% | **10/10** — Dedicated nodes for Intent Routing, Physio RAG, Periodization Planner, Safety Guard, and Data-Entry Parser. | **3.0/10** — One 5,000-token prompt attempting to hold medical rules, periodization math, and tone guidelines. | **7.5/10** — Autonomous role-playing agents, but prone to role confusion without explicit graph edge control. | **7.0/10** — Visual node separation; clean HTTP integrations, but limited programmatic state branch logic. |
| **Deterministic Guardrail Enforcement** | 25% | **10/10** — Hard graph edges enforce that the **Biometric Safety Guard** intercepts all generated workouts before user delivery. | **2.0/10** — Vulnerable to prompt injection, hallucination, and attention degradation ("lost in the middle"). | **4.5/10** — Autonomous handoffs make hard deterministic safety guarantees impossible to audit mathematically. | **8.0/10** — Code nodes can enforce conditional branching and schema validation deterministically. |
| **Token Efficiency & Operating Cost** | 20% | **9.5/10** — 80% of messages (logs, greetings) execute on ultra-fast $0.15/M token models with tiny prompts. Claude 3.5 used only for RAG. | **2.0/10** — Every trivial message ("Ran 5k") runs through the massive 5,000-token prompt on an expensive frontier model. | **3.5/10** — Heavy inter-agent conversational overhead and autonomous reflection loops multiply token burn. | **8.5/10** — Granular model selection per workflow node minimizes unnecessary frontier LLM invocations. |
| **State Persistence & Checkpointing** | 15% | **10/10** — Native state checkpointing to PostgreSQL/Redis. Asynchronous human-in-the-loop resumption. | **3.0/10** — Ephemeral chat memory buffer; context resets on server restart or long delays. | **6.0/10** — In-memory state tracking; custom persistence required for enterprise production. | **8.0/10** — Workflow execution state stored in Postgres; retries built-in. |
| **Structured Output Adherence** | 15% | **10/10** — Pydantic v2 / Instructor schema validation on every node with targeted self-healing retries. | **4.0/10** — Complex nested JSON schemas frequently suffer dropped keys or invalid syntax on long outputs. | **7.0/10** — Supports tool schemas, but recovery from malformed JSON can be brittle. | **8.0/10** — JSON schema validation in webhook response nodes. |
| **Weighted Total Score** | **100%** | **9.90 / 10 (WINNER)** | **2.75 / 10** | **5.75 / 10** | **7.80 / 10** |

#### Strategic AI Orchestration Decision
- **Definitive Choice:** **LangGraph / Custom Async State Graph in Python with Pydantic v2 & Instructor**.
- *Tiered Model Strategy:*
  - **Tier-2 Fast Path (80% of traffic):** `gpt-4o-mini` / `deepseek-v3` for intent routing, voice transcript extraction, workout data parsing, and conversational check-ins.
  - **Tier-1 Deep Clinical Path (20% of traffic):** `claude-3-5-sonnet` / `gpt-4o` for sports medicine RAG synthesis, acute injury assessments, and complex polarized periodization generation.

---

## 3. Sports Science & Clinical RAG Architecture

The intelligence core of Aegis Coach is its Sports Science & Clinical Retrieval-Augmented Generation (RAG) subsystem. Unlike generic fitness apps, Aegis Coach grounds every training modification in peer-reviewed sports medicine and exercise physiology literature.

---

### 3.1 Domain Knowledge Corpus & Clinical Models

The knowledge base contains structured protocols and validated scientific literature across five critical domains:

```
┌───────────────────────────────────────────────────────────────────────────┐
│                     SPORTS SCIENCE KNOWLEDGE DOMAINS                      │
├─────────────────────────┬─────────────────────────┬───────────────────────┤
│ 1. Tissue Mechanics     │ 2. Pain Monitoring      │ 3. Workload Modeling  │
│ • Askling L-Protocol    │ • Silbernagel Model     │ • Banister ACWR       │
│ • Heavy Slow Resistance │ • VAS <= 3/10 Rule      │ • Sweet Spot 0.8-1.3  │
│ • Tendinopathy Loading  │ • Morning Stiffness Gate│ • Danger Zone > 1.5   │
├─────────────────────────┴─────────────────────────┴───────────────────────┤
│ 4. Periodization & Energy Systems     │ 5. Molecular Signaling            │
│ • Seiler Polarized 80/20 Distribution │ • AMPK / mTOR Concurrent Training │
│ • Zone 1/2 vs Zone 4/5 Blood Lactate  │ • 6-8 Hour Separation Window      │
└───────────────────────────────────────┴───────────────────────────────────┘
```

#### 1. Askling L-Protocol & Hamstring Remodeling (Askling et al., 2013, 2014)
- **Pathology Target:** Proximal hamstring myotendinous junction strains (biceps femoris long head, semitendinosus).
- **Biomechanical Mechanism:** Sprint-type hamstring injuries occur during the terminal swing phase of high-speed running, where the hamstring undergoes maximal eccentric lengthening under peak tension.
- **The 3 Core Clinical Exercises ("L-Protocol"):**
  1. **The Extender:** Slow, active knee extensions while stabilizing the hip at $90^\circ$ flexion (neuromuscular control in lengthened position).
  2. **The Diver:** Single-leg hip hinge with thoracic spine extension and trailing leg extension (simulates terminal swing eccentric loading).
  3. **The Glider:** Backward gliding lunges on a low-friction slideboard with bodyweight (eccentric loading at long muscle lengths).
- **Heavy Slow Resistance (HSR):** Prone leg curls and seated leg curls performed at $3\text{s}$ concentric, $3\text{s}$ eccentric tempos at $70\text{–}85\%$ 1RM to stimulate collagen synthesis and fascicle length increase.
- **Contraindications (Acute & Subacute):** Maximal velocity sprinting ($>85\% v_{\max}$), explosive hill sprints, straight-leg deadlifts at maximal end-range of motion, ballistic kicking drills.

#### 2. Pain-Monitoring Model (Silbernagel et al., 2007)
- **Protocol:** Allows athletic activity and progressive loading during tendon and muscle rehabilitation under strict pain rules:
  1. Pain during or immediately after exercise must not exceed **$3/10$** on the Visual Analog Scale (VAS).
  2. Pain must return to pre-exercise baseline within **24 hours**.
  3. Morning stiffness and morning pain the day following loading must **not increase**.
- **Automated Gate:** If morning check-in reports VAS $>3/10$ or worsening morning stiffness, the system automatically cancels high-intensity workouts, downgrading to isometric analgesia (e.g., $5 \times 45\text{s}$ isometric leg extensions/bridges at $70\%$ MVC).

#### 3. Banister Impulse-Response Workload Model & ACWR
- **Mathematical Formulations:**
  $$\text{CTL}(t) = \text{CTL}(t-1) \cdot e^{-1/\tau_1} + \text{TRIMP}(t) \cdot (1 - e^{-1/\tau_1}) \quad (\tau_1 = 42 \text{ days, Fitness})$$
  $$\text{ATL}(t) = \text{ATL}(t-1) \cdot e^{-1/\tau_2} + \text{TRIMP}(t) \cdot (1 - e^{-1/\tau_2}) \quad (\tau_2 = 7 \text{ days, Fatigue})$$
  $$\text{TSB}(t) = \text{CTL}(t) - \text{ATL}(t) \quad (\text{Training Stress Balance / Freshness})$$
  $$\text{ACWR}(t) = \frac{\text{ATL}(t)}{\text{CTL}(t)} \quad (\text{Acute:Chronic Workload Ratio})$$
- **Safety Zones (Gabbett, 2016):**
  - $\text{ACWR} < 0.8$: Under-training / Detraining risk.
  - $0.8 \le \text{ACWR} \le 1.3$: **"The Sweet Spot"** (optimal progressive overload with lowest soft-tissue injury risk).
  - $1.3 < \text{ACWR} \le 1.5$: Caution Zone (elevated injury risk; flag for close biometric monitoring).
  - $\text{ACWR} > 1.5$: **"The Danger Zone"** (statistically $2\times\text{--}4\times$ increase in soft-tissue injury risk). Triggers automatic volume deload of $30\text{--}50\%$.

#### 4. Polarized 80/20 Periodization (Seiler, 2010)
- **Intensity Distribution:**
  - **Zone 1–2 (Low Intensity, below LT1 / $<2.0\text{ mmol/L}$ lactate):** $\sim 80\%$ of total training time. Focus on mitochondrial biogenesis, capillarization, and fat oxidation efficiency.
  - **Zone 4–5 (High Intensity, above LT2 / $>4.0\text{ mmol/L}$ lactate):** $\sim 20\%$ of total training time. Focus on stroke volume, $\text{VO}_2\max$, and neuromuscular power.
  - **Zone 3 ("Grey Zone" / Threshold):** Strictly minimized during base phases to prevent autonomic fatigue accumulation without proportional adaptive gains.

#### 5. Molecular Signaling & Concurrent Training Interference (Baar, 2014)
- **AMPK vs. mTOR Interference:** Endurance exercise activates $5'\text{-AMP-activated protein kinase (AMPK)}$, which phosphorylates and activates TSC2, inhibiting $mTORC1$ and blocking muscle protein synthesis for several hours.
- **Scheduling Rules:** Heavy strength and hypertrophy sessions must be separated from high-intensity endurance sessions by **$\ge 6\text{--}8\text{ hours}$** (or performed on alternate days). If performed on the same day, high-intensity endurance should be completed in the morning, followed by nutrition and evening strength training.

---

### 3.2 Ingestion, Semantic Chunking & Metadata Tagging

Scientific literature (PDFs, clinical guidelines, protocol papers) undergoes automated extraction and structured metadata tagging:

```
┌───────────────────────────────────────────────────────────────────────────┐
│                       DOCUMENT INGESTION PIPELINE                         │
│                                                                           │
│  [Scientific PDF] ──► [Marker / PyMuPDF] ──► [Markdown + Tables]          │
│                                                     │                     │
│                                                     ▼                     │
│                                          [Semantic Chunking]              │
│                                          • Parent: 800 tokens             │
│                                          • Child:  200 tokens             │
│                                                     │                     │
│                                                     ▼                     │
│                                          [Metadata Extraction]            │
│                                          • Anatomy & Pathology            │
│                                          • Contraindications              │
│                                          • Evidence Level                 │
│                                                     │                     │
│                                                     ▼                     │
│                                          [Dual Vector Index]              │
│                                          • Dense: text-embedding-3-small  │
│                                          • Sparse: BM25 / Qdrant Sparse   │
└───────────────────────────────────────────────────────────────────────────┘
```

#### Chunk Metadata JSON Schema
```json
{
  "chunk_id": "askling_2014_l_protocol_remodeling_01",
  "parent_doc_id": "askling_2014_acute_hamstring_guidelines",
  "title": "Acute Hamstring Muscle Injury: The L-Protocol for Lengthened Eccentric Loading",
  "source_doi": "10.1136/bjsports-2013-093218",
  "evidence_level": "Level_1_RCT",
  "anatomical_region": "hamstring",
  "tissue_type": "myotendinous_junction",
  "pathology": "proximal_hamstring_strain",
  "rehab_phase": "remodeling_eccentric",
  "indicated_exercises": [
    "the_extender",
    "the_diver",
    "the_glider",
    "single_leg_isometric_bridge",
    "nordic_hamstring_curl_regressed"
  ],
  "contraindicated_exercises": [
    "sprint_max_velocity",
    "ballistic_kicking",
    "stiff_leg_deadlift_end_rom",
    "deep_forward_fold_stretch"
  ],
  "pain_tolerance_rule": "VAS <= 3/10, resolve within 24h",
  "content_chunk": "The L-protocol focuses on eccentric loading of the hamstring at lengthened states. In a randomized controlled trial of 75 elite sprinters and track athletes, the L-protocol significantly shortened return-to-play time (28 days vs 51 days, p < 0.001) compared to conventional rehabilitation..."
}
```

---

### 3.3 Vector Database Benchmark & Selection

| Evaluation Dimension | Qdrant (Dedicated Vector DB) | pgvector (PostgreSQL Extension) | Pinecone (Managed Cloud) | Chroma (Embedded Vector DB) |
|---|:---:|:---:|:---:|:---:|
| **Hybrid Search Support (Dense + Sparse BM25)** | **10/10** — Native hybrid search with Reciprocal Rank Fusion (RRF) and sparse vector payloads. | **7.5/10** — Hybrid search requires combining pgvector cosine distance with Postgres `tsvector` full-text search. | **8.5/10** — Pinecone Serverless supports sparse-dense vectors, but vendor-locked. | **4.0/10** — Basic dense vector search only; sparse integration requires external libraries. |
| **Payload Metadata Pre-Filtering Speed** | **10/10** — Ultra-fast HNSW payload index filtering. Excludes contraindicated exercises in $<5\text{ms}$. | **8.5/10** — Fast using composite B-tree + HNSW/IVFFlat indexes inside Postgres. | **8.5/10** — Good filtering on string metadata; limited complex array operator filtering. | **5.0/10** — In-memory python metadata filtering; degrades rapidly $>50\text{k}$ vectors. |
| **Multi-Tenancy & Partitioning** | **10/10** — Native tenant payload namespaces and collection-level isolation. | **10/10** — Native PostgreSQL Row-Level Security (RLS) filters vectors per `tenant_id` automatically. | **7.0/10** — Namespace partitioning supported; per-tenant isolation costs scale with pod count. | **3.0/10** — No multi-tenant isolation primitives built-in. |
| **Deployment & Self-Hosting Flexibility** | **10/10** — Single lightweight Docker container (Rust-based, $<50\text{MB}$ RAM) or Qdrant Cloud. | **10/10** — Built directly into Supabase / PostgreSQL. Zero extra infrastructure. | **0/10** — Proprietary SaaS only. Cannot be run offline, in CI test runners, or on local VPS. | **8.5/10** — Embedded Python/SQLite; easy local development, but lacks production scale. |
| **Operational Overhead & Cost** | **9.5/10** — Open-source free self-hosted on VPS, or $25/mo managed. | **10/10** — $0 additional cost (included in Supabase / Postgres instance). | **4.0/10** — Minimum $50–$100/mo once scaling beyond free tier quotas. | **8.0/10** — Free local, but requires custom infrastructure for scaling. |
| **Final Recommendation** | **Tier 1 Recommendation** | **Tier 1 Co-Recommendation** | Not Recommended | Prototype Only |

#### Vector Database Architecture Decision
- **Production Architecture:** **Qdrant (Vector Engine)** paired with **pgvector in Supabase**.
- *Design:* In production, Qdrant handles high-performance hybrid dense+sparse vector queries with complex anatomical payload pre-filtering, while pgvector in Supabase provides transactional vector querying linked directly to user profile tables. For lightweight testing and CI, an embedded vector store with identical cosine+metadata interfaces runs deterministically in-memory.

---

### 3.4 Hybrid Search Pipeline & Medical Red-Flag Triage

```
                            ATHLETE QUERY
                                  │
                                  ▼
                   ┌──────────────────────────────┐
                   │  Medical Red-Flag Triage     │
                   │  (Heuristic + Regex Match)   │
                   └──────────────┬───────────────┘
                                  │
                    Is Acute Medical Emergency?
                     ├─── YES ───► [EMERGENCY LOCKOUT & CLINICAL REFERRAL]
                     │
                     └─── NO
                          │
                          ▼
            ┌─────────────────────────────┐
            │   Metadata Pre-Filter       │
            │   • Target Anatomy          │
            │   • Active Injury Status    │
            │   • Exclude Contraindicated │
            └─────────────┬───────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
  [Dense Vector Search]       [Sparse BM25 Search]
  (text-embedding-3-small)    (Exact Clinical Terms)
            │                           │
            └─────────────┬─────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │ Reciprocal Rank Fusion(RRF) │
            │ Score = 1 / (60 + Rank)     │
            └─────────────┬───────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │ Cross-Encoder Reranker      │
            │ (Cohere Rerank v3 / BGE)    │
            └─────────────┬───────────────┘
                          │
                          ▼
            [Top 3 Gold-Standard Chunks injected into LLM Context]
```

#### Medical Red-Flag Triage Rules
Before any RAG retrieval or training generation occurs, incoming queries pass through the **Medical Red-Flag Triage Engine**. If any of the following clinical red-flag patterns are detected, the system immediately locks training generation and returns an emergency clinical referral:

| Red-Flag Category | Trigger Keywords & Semantic Patterns | Clinical Risk | Action / System Response |
|---|---|---|---|
| **Cardiovascular / Systemic** | *"Chest pain", "chest pressure", "radiating arm pain", "syncope", "fainted while running", "irregular heart flutter"* | Myocardial infarction, acute arrhythmia, hypertrophic cardiomyopathy. | **EMERGENCY LOCKOUT.** Halts workout planning; displays bold prompt instructing athlete to call emergency services (112/911). |
| **Neurological / Spinal** | *"Loss of bowel/bladder control", "saddle anesthesia", "numbness in groin", "bilateral progressive leg weakness"* | Cauda Equina Syndrome (neurosurgical emergency). | **EMERGENCY LOCKOUT.** Directs athlete to nearest emergency emergency department immediately. |
| **Structural / Fracture** | *"Audible bone snap", "inability to bear weight for 4 steps", "gross joint deformity", "rapid severe knee effusion within 2h"* | Acute bone fracture (Ottawa Rules), ACL/PCL ligamentous rupture. | **TRAINING SUSPENSION.** Recommends immediate orthopedic evaluation and imaging (X-ray/MRI). |

---

## 4. Target Architecture & Recommended Tech Stack

### 4.1 Definitive Tech Stack Specification

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AEGIS COACH TECH STACK                                      │
├─────────────────────────┬───────────────────────────────────┬───────────────────────────────┤
│ LAYER                   │ TECHNOLOGY                        │ PURPOSE / JUSTIFICATION       │
├─────────────────────────┼───────────────────────────────────┼───────────────────────────────┤
│ Conversational Ingress  │ Telegram Bot API                  │ Zero-friction voice & text    │
│ Visual App & Onboarding │ Telegram Mini App (React + Vite)  │ Interactive body map & forms  │
│ Desktop Analytics Hub   │ Next.js 15 (React 19 + Tailwind)  │ Long-term Banister/HRV charts │
│ Backend Core Engine     │ Python 3.11+ FastAPI (Async)      │ Scientific Python AI runtime  │
│ Database & Security     │ Supabase (PostgreSQL 16 + RLS)    │ Multi-tenant data isolation   │
│ Vector Database         │ Qdrant (Rust Vector DB)           │ Hybrid dense/sparse search    │
│ Task Queue & Crons      │ Redis 7 + Celery / Async Workers  │ 08:00 AM check-ins & webhooks │
│ AI Orchestrator         │ LangGraph / Async State Graph     │ Multi-agent graph execution   │
│ Fast LLM (Tier-2)       │ GPT-4o-mini / DeepSeek V3         │ 80% traffic (routing/parsing) │
│ Frontier LLM (Tier-1)   │ Claude 3.5 Sonnet / GPT-4o        │ 20% traffic (clinical RAG)    │
│ External Wearable Sync  │ Intervals.icu REST API + Strava   │ Bidirectional Garmin sync     │
│ Edge Ingress & SSL      │ Cloudflare Tunnels (Zero Trust)   │ Secure webhook ingestion      │
│ Observability           │ Sentry + Langfuse + Prometheus    │ LLM tracing & error telemetry │
└─────────────────────────┴───────────────────────────────────┴───────────────────────────────┘
```

---

### 4.2 End-to-End System Dataflow Sequence Diagrams

#### Sequence 1: Conversational Workout Logging via Telegram Voice/Text
```
Athlete                Telegram Bot         FastAPI Core        LangGraph / Router     PostgreSQL / RLS     Intervals.icu
   │                        │                     │                     │                     │                 │
   │── 1. Voice Note ──────►│                     │                     │                     │                 │
   │   ("12k Z2, 4:50 pace, │                     │                     │                     │                 │
   │    hamstring 2/10")    │                     │                     │                     │                 │
   │                        │── 2. Webhook Event ─►│                     │                     │                 │
   │                        │                      │── 3. Transcribe ───►│                     │                 │
   │                        │                      │      (Whisper API)  │                     │                 │
   │                        │                      │                     │                     │                 │
   │                        │                      │── 4. Route Intent ─►│                     │                 │
   │                        │                      │                     │── 5. Parse Workout ─│                 │
   │                        │                      │                     │   (Pydantic Schema) │                 │
   │                        │                      │                     │                     │                 │
   │                        │                      │                     │── 6. Update Metrics►│                 │
   │                        │                      │                     │   (Calculate TRIMP, │                 │
   │                        │                      │                     │    CTL, ATL, ACWR)  │                 │
   │                        │                      │                     │                     │                 │
   │                        │                      │                     │── 7. Recalculate ──►│                 │
   │                        │                      │                     │   Safety Thresholds │                 │
   │                        │                      │                     │                     │                 │
   │                        │                      │◄── 8. Formatted ────│                     │                 │
   │                        │                      │    Response Text    │                     │                 │
   │                        │◄── 9. Send Message ──│                     │                     │                 │
   │◄── 10. Chat Feedback ──│                      │                     │                     │                 │
   │   ("Logged! CTL: 54,   │                      │                     │                     │                 │
   │    ACWR: 1.05. Rest up")                      │── 11. Async Sync Completed Activity ─────┼────────────────►│
```

#### Sequence 2: Clinical Injury Inquiry with Safety Guardrail Interception
```
Athlete                Telegram Bot         FastAPI Core        Medical Agent         Qdrant RAG        Biometric Safety Guard
   │                        │                     │                   │                   │                   │
   │── 1. "Hamstring hurts, ┼────────────────────►│                   │                   │                   │
   │   can I do 100m sprints│                     │                   │                   │                   │
   │   today?"              │                     │── 2. Route Query ─►│                   │                   │
   │                        │                     │   (PHYSIO_REHAB)  │                   │                   │
   │                        │                     │                   │── 3. Hybrid Search│                   │
   │                        │                     │                   │   (Anatomy: Hamst)│                   │
   │                        │                     │                   │──────────────────►│                   │
   │                        │                     │                   │◄── 4. Chunks ─────│                   │
   │                        │                     │                   │   (Askling L-Prot,│                   │
   │                        │                     │                   │    HSR Isometrics)│                   │
   │                        │                     │                   │                   │                   │
   │                        │                     │                   │── 5. Synthesize Draft Workout ───────►│
   │                        │                     │                   │   (Includes submaximal drills)        │── 6. Evaluate Rules
   │                        │                     │                   │                                       │   (Assert no sprints >80%,
   │                        │                     │                   │                                       │    check pain <= 3/10)
   │                        │                     │                   │◄── 7. APPROVED / MODIFIED WORKOUT ────│
   │                        │                     │◄── 8. Verified ───│
   │                        │                     │    Clinical Plan  │
   │                        │◄── 9. Send Message ─│
   │◄── 10. Prescribed ─────│
   │   Rehab Session        │
   │   (Isometrics + HSR)   │
```

#### Sequence 3: Proactive 08:00 AM Morning Check-in Cron
```
Redis / Cron           FastAPI Worker       Intervals.icu API     PostgreSQL DB        LangGraph Agent      Telegram Bot
   │                         │                     │                    │                     │                   │
   │── 1. 08:00 AM Trigger ─►│                     │                    │                     │                   │
   │   (All Active Athletes) │                     │                    │                     │                   │
   │                         │── 2. Fetch Daily ──►│                    │                     │                   │
   │                         │   Biometrics        │                    │                     │                   │
   │                         │   (HRV, RHR, Sleep) │                    │                     │                   │
   │                         │◄── 3. JSON Stream ──│                    │                     │                   │
   │                         │                                          │                     │                   │
   │                         │── 4. Query Athlete Profile & Baseline ──►│                     │                   │
   │                         │◄── 5. Stored 7-Day Rolling Baseline ─────│                     │                   │
   │                         │                                                                │                   │
   │                         │── 6. Evaluate Readiness ──────────────────────────────────────►│                   │
   │                         │   (Detect autonomic depression: HRV < -1.5 SD, sleep < 5h)     │                   │
   │                         │                                                                │                   │
   │                         │◄── 7. Synthesized Morning Briefing & Workout Adaptation ───────│                   │
   │                         │                                                                                    │
   │                         │── 8. Dispatch Telegram Notification ──────────────────────────────────────────────►│
   │                         │                                                                                    │── 9. Push to Athlete
```

---

## 5. Data Models, Multi-Tenancy & Security Architecture

### 5.1 Relational PostgreSQL Schema (Supabase)

```sql
-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. TENANTS TABLE (Supports Multi-Tenant Gyms, Coaches, and Direct B2C)
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    plan_tier VARCHAR(50) NOT NULL DEFAULT 'b2c_individual', -- 'b2c_individual', 'coach_pro', 'enterprise_club'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. USERS & ATHLETE PROFILES
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    telegram_chat_id BIGINT UNIQUE,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'athlete', -- 'athlete', 'coach', 'admin'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE athlete_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    height_cm NUMERIC(5,2) NOT NULL,
    weight_kg NUMERIC(5,2) NOT NULL,
    primary_sport VARCHAR(50) NOT NULL, -- 'track_800m', 'trail_running', 'marathon', 'triathlon'
    training_age_years INT NOT NULL DEFAULT 1,
    max_heart_rate INT NOT NULL,
    resting_heart_rate INT NOT NULL,
    lactate_threshold_hr INT,
    vVO2max_pace_sec_km INT, -- velocity at VO2max in seconds/km
    equipment_access JSONB NOT NULL DEFAULT '["gym", "track", "trail"]'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. INJURY HISTORY & ACTIVE CONTRAINDICATIONS
CREATE TABLE injury_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    anatomical_region VARCHAR(100) NOT NULL, -- 'hamstring_proximal', 'achilles_tendon', 'patellar_tendon'
    side VARCHAR(10) NOT NULL, -- 'left', 'right', 'bilateral'
    tissue_type VARCHAR(50) NOT NULL, -- 'myotendinous_junction', 'tendon_midportion', 'ligament'
    diagnosis_title VARCHAR(255) NOT NULL,
    diagnosis_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'rehab_remodeling', -- 'acute', 'rehab_isometrics', 'rehab_remodeling', 'return_to_sport', 'resolved'
    pain_vas_current INT NOT NULL CHECK (pain_vas_current BETWEEN 0 AND 10),
    active_contraindications TEXT[] NOT NULL DEFAULT '{}',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. DAILY BIOMETRICS & CHECK-INS
CREATE TABLE daily_checkins (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    checkin_date DATE NOT NULL,
    hrv_rmssd NUMERIC(5,2), -- Nocturnal HRV in milliseconds
    resting_hr INT,
    sleep_duration_hours NUMERIC(4,2),
    sleep_quality_score INT CHECK (sleep_quality_score BETWEEN 1 AND 100),
    subjective_soreness INT CHECK (subjective_soreness BETWEEN 1 AND 10),
    subjective_stress INT CHECK (subjective_stress BETWEEN 1 AND 10),
    injury_pain_vas INT CHECK (injury_pain_vas BETWEEN 0 AND 10),
    readiness_score INT CHECK (readiness_score BETWEEN 1 AND 100),
    morning_stiffness_present BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, checkin_date)
);

-- 5. WORKOUTS (PLANNED & EXECUTED)
CREATE TABLE workouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    scheduled_date DATE NOT NULL,
    sport VARCHAR(50) NOT NULL,
    workout_type VARCHAR(50) NOT NULL, -- 'easy_z2', 'vo2max_intervals', 'hsr_strength', 'recovery_spin'
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    structured_steps JSONB NOT NULL DEFAULT '[]'::jsonb, -- Structured steps for Garmin push
    planned_duration_minutes INT NOT NULL,
    planned_trimp NUMERIC(6,2) NOT NULL,
    
    -- Execution Data (Populated upon completion)
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    executed_duration_minutes INT,
    executed_distance_km NUMERIC(6,2),
    executed_elevation_gain_m INT,
    executed_avg_hr INT,
    executed_rpe INT CHECK (executed_rpe BETWEEN 1 AND 10),
    executed_trimp NUMERIC(6,2),
    intervals_icu_event_id VARCHAR(100),
    strava_activity_id VARCHAR(100),
    safety_override_applied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. THIRD-PARTY CREDENTIALS VAULT (ENCRYPTED AT REST)
CREATE TABLE external_integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL, -- 'intervals_icu', 'strava', 'garmin'
    athlete_external_id VARCHAR(100) NOT NULL,
    encrypted_api_key BYTEA, -- AES-256-GCM encrypted
    encrypted_access_token BYTEA,
    encrypted_refresh_token BYTEA,
    token_expires_at TIMESTAMPTZ,
    sync_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    last_sync_at TIMESTAMPTZ,
    UNIQUE(user_id, provider)
);
```

---

### 5.2 Multi-Tenant Data Isolation Strategy (PostgreSQL RLS)

To enforce strict multi-tenant isolation, every table enforces PostgreSQL Row-Level Security (RLS) policies. When a request hits the backend, the user's authenticated `tenant_id` and `user_id` are set in the database session context:

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE athlete_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE injury_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_checkins ENABLE ROW LEVEL SECURITY;
ALTER TABLE workouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE external_integrations ENABLE ROW LEVEL SECURITY;

-- Create RLS Policies for athlete data isolation
CREATE POLICY athlete_isolation_policy ON athlete_profiles
    FOR ALL
    USING (
        user_id = auth.uid() 
        OR 
        (tenant_id = current_setting('app.current_tenant_id', true)::uuid 
         AND current_setting('app.current_user_role', true) = 'coach')
    );

CREATE POLICY workout_isolation_policy ON workouts
    FOR ALL
    USING (
        user_id = auth.uid() 
        OR 
        (tenant_id = current_setting('app.current_tenant_id', true)::uuid 
         AND current_setting('app.current_user_role', true) = 'coach')
    );

CREATE POLICY credentials_vault_policy ON external_integrations
    FOR ALL
    USING (user_id = auth.uid()); -- Coaches NEVER have access to athlete private OAuth tokens
```

---

### 5.3 Sensitive Data Protection & GDPR / Health Data Compliance

Biometric, physiological, and injury records constitute **Special Category Health Data** under GDPR Article 9. Aegis Coach implements the following security protocols:

1. **AES-256-GCM Token Encryption at Rest:**
   - Third-party API keys and OAuth tokens (Intervals.icu, Strava) are encrypted using authenticated `AES-256-GCM` before database insertion. The encryption key is managed via AWS Secrets Manager / Doppler and rotated every 90 days.
2. **Pseudonymization of AI Telemetry:**
   - All prompts sent to external LLM providers (OpenAI, Anthropic) are stripped of PII (names, emails, Telegram chat IDs, exact GPS coordinates). Only sanitized numeric biometrics and anatomical tags (`athlete_58kg_male_23yo`, `proximal_hamstring_strain`) are transmitted.
3. **Right to Be Forgotten (GDPR Article 17):**
   - Executing an account deletion cascades through foreign keys, permanently purging all biometric check-ins, injury logs, workout traces, and vector embeddings within 60 seconds.
4. **Data Portability (GDPR Article 20):**
   - Athletes can export their complete training and biometric history in open standard formats (`.fit`, `.tcx`, `.json`, `.csv`) with a single command (`/export_data`).

---

## 6. Phased Implementation Roadmap

```
┌───────────────────────────────────────────────────────────────────────────┐
│                     6-MONTH IMPLEMENTATION ROADMAP                        │
├──────────────────────┬──────────────────────┬─────────────────────────────┤
│   PHASE 1 (M1–M2)    │   PHASE 2 (M3–M4)    │       PHASE 3 (M5–M6)       │
│ MVP & Core Validation│ Alpha & Hardening    │ Scale & Multi-Tenancy       │
├──────────────────────┼──────────────────────┼─────────────────────────────┤
│ • Telegram Bot MVP   │ • Telegram Mini App  │ • Stripe Subscription SaaS  │
│ • Intervals.icu Sync │ • 50-Athlete Alpha   │ • Multi-Sport Expansion     │
│ • Hamstring RAG      │ • Interactive BodyMap│ • Coach Portal & Multi-Ten  │
│ • ACWR Safety Gate   │ • Automated Crons    │ • Direct HealthKit Bridge   │
│ • Fast/Deep LLM Tier │ • Latency & Caching  │ • PostHog / Langfuse Stack  │
└──────────────────────┴──────────────────────┴─────────────────────────────┘
```

---

### Phase 1: MVP & Core Validation (Months 1–2)
- **Core Focus:** Functional validation of conversational logging, Intervals.icu sync, and the clinical hamstring rehabilitation RAG engine.
- **Deliverables:**
  - Telegram Bot interface supporting audio/voice note transcription (Whisper API) and text logging.
  - Python FastAPI asynchronous backend containerized on Docker VPS.
  - Intervals.icu bidirectional integration (reading daily HRV/RHR/sleep; pushing structured interval workouts to Garmin).
  - Qdrant Vector RAG corpus with initial sports science literature (Askling L-Protocol, Silbernagel Pain Model, Banister ACWR).
  - Deterministic Biomechanical Safety Guard intercepting contraindicated sprint/loading requests.
  - Dual-mode provider architecture (Offline Mock deterministic testing + Live API adapters).
- **Target Milestone Gate:** Single-athlete end-to-end verification (Carlos's 800m hamstring rehabilitation protocol).

---

### Phase 2: Alpha Testing & Clinical Hardening (Months 3–4)
- **Core Focus:** User experience refinement, rich visual onboarding, proactive morning check-in automation, and closed beta testing with 50 athletes.
- **Deliverables:**
  - Telegram Mini App (TMA in React 19 / Tailwind / Vite) featuring an interactive clickable SVG body injury selector.
  - Proactive 08:00 AM morning check-in cron evaluating daily HRV/sleep readiness and dispatching personalized check-in messages.
  - Next.js 15 desktop analytics dashboard rendering interactive Banister CTL/ATL/TSB curves and mesocycle volume tables.
  - Strava Webhook connector for automatic GPS activity ingestion.
  - Prompt caching, semantic response caching with Redis, and latency optimization ($<1.2\text{s}$ average response time).
  - Closed Alpha rollout to 50 competitive track, road, and trail athletes.
- **Target Milestone Gate:** $>70\%$ 30-day conversational logging retention across 50 alpha athletes with zero clinical safety violations.

---

### Phase 3: Production, Multi-Tenancy & Commercial Scaling (Months 5–6)
- **Core Focus:** Commercial SaaS launch, enterprise multi-tenant coach portals, multi-sport expansion, and automated subscription billing.
- **Deliverables:**
  - Stripe Billing integration supporting monthly ($14.99/mo) and annual ($129/mo) subscription tiers via Telegram Mini App checkout.
  - Multi-tenant Coach Portal allowing human coaches to manage rosters of 20–100 athletes with shared team dashboards and custom training template libraries.
  - Multi-Sport Clinical RAG expansion: Cycling (power profiling, FTP, knee patellofemoral tracking), Strength/CrossFit (lumbar disc protection, rotator cuff rehabilitation), and Triathlon.
  - Native Mobile Companion wrapper (React Native / Capacitor) for direct background Apple HealthKit and Android Health Connect syncing.
  - Full observability stack: Langfuse for LLM token tracing, Sentry for exception tracking, and Prometheus/Grafana for infrastructure metrics.
- **Target Milestone Gate:** Public commercial launch, scaling to 1,000+ paying active subscribers with $>85\%$ gross margin.

---

## 7. Operational Cost Modeling & Unit Economics

### 7.1 Detailed LLM Token Cost Analysis per User per Month

To achieve high gross margins, Aegis Coach implements an intelligent **Tiered Multi-Model Router**:
- **Tier-2 Fast Path (`gpt-4o-mini` / `deepseek-v3`):** Handles $80\%$ of all user interactions (intent classification, voice transcription extraction, structured workout parsing, motivational check-ins).
- **Tier-1 Deep Path (`claude-3-5-sonnet` / `gpt-4o`):** Reserved for the $20\%$ of computationally heavy tasks (clinical RAG reasoning, acute injury diagnostics, weekly periodization plan generation).

#### Monthly User Interaction Profile & Token Breakdown

| Interaction Type | Frequency / Mo | Model Tier | Input Tokens / Call | Output Tokens / Call | Prompt Caching Discount | Net Monthly Cost / User |
|---|:---:|---|:---:|:---:|:---:|:---:|
| **Daily Morning Readiness Check-in** | 30 | `gpt-4o-mini` | 400 | 150 | 50% Cached | **$0.0022** |
| **Conversational Workout Logging (Voice/Text)** | 22 | `gpt-4o-mini` + Whisper | 600 | 200 | 50% Cached | **$0.0132** (incl. Whisper) |
| **Conversational Chat & Queries** | 15 | `gpt-4o-mini` | 500 | 250 | 50% Cached | **$0.0028** |
| **Clinical RAG Injury Inquiry** | 4 | `claude-3-5-sonnet` | 2,500 (incl. RAG) | 600 | 60% Cached | **$0.0420** |
| **Weekly Periodization Plan Generation** | 4 | `claude-3-5-sonnet` | 3,500 | 1,200 | 70% Cached | **$0.0880** |
| **Total Monthly LLM Cost per Active User** | — | — | — | — | — | **$0.1482 / month** |

*Note on Safety Margin:* Even assuming heavy conversational volume ($3\times$ base usage), monthly LLM costs remain below **$0.45 / user / month**.

---

### 7.2 Cloud Infrastructure Scaling Projections

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                             INFRASTRUCTURE COST AT SCALE                                  │
├───────────────────────────────┬───────────────────┬───────────────────┬───────────────────┤
│ INFRASTRUCTURE COMPONENT      │ 100 USERS (MVP)   │ 1,000 USERS       │ 10,000 USERS      │
├───────────────────────────────┼───────────────────┼───────────────────┼───────────────────┤
│ Compute VPS (FastAPI/Docker)  │ $10.00 / mo       │ $40.00 / mo       │ $240.00 / mo      │
│ Database (Supabase Postgres)  │ $0.00 (Free Tier) │ $25.00 (Pro Tier) │ $599.00 (Team DB) │
│ Vector Database (Qdrant)      │ $0.00 (Local VPS) │ $25.00 / mo       │ $180.00 / mo      │
│ Redis Task Queue & Caching    │ $0.00 (Local VPS) │ $15.00 / mo       │ $75.00 / mo       │
│ Ingress & CDN (Cloudflare)    │ $0.00 (Free)      │ $20.00 (Pro)      │ $200.00 (Business)│
│ Telemetry & Logging           │ $0.00             │ $29.00 / mo       │ $180.00 / mo      │
│ Total Monthly LLM Token Costs │ $14.82            │ $148.20           │ $1,482.00         │
├───────────────────────────────┼───────────────────┼───────────────────┼───────────────────┤
│ TOTAL MONTHLY OPEX            │ $24.82 / mo       │ $302.20 / mo      │ $2,956.00 / mo    │
│ BLENDED COST PER USER / MONTH │ $0.25 / user      │ $0.30 / user      │ $0.29 / user      │
└───────────────────────────────┴───────────────────┴───────────────────┴───────────────────┘
```

---

### 7.3 Unit Economics & Financial Margin Analysis

```
┌───────────────────────────────────────────────────────────────────────────┐
│                     B2C SUBSCRIPTION UNIT ECONOMICS                       │
│                     (Target Price: $14.99 / Month)                        │
├───────────────────────────────────────────────────────────────────────────┤
│  Gross Subscription Revenue:                    $14.99                    │
│                                                                           │
│  Direct Marginal COGS per User:                                           │
│  • Stripe Payment Processing Fee (2.9% + $0.30): -$0.73                   │
│  • Tiered LLM Token Costs (Fast + Deep Paths):   -$0.15                   │
│  • Whisper Audio Transcription Ingestion:        -$0.02                   │
│  • Infrastructure Share (Compute, DB, Vector):   -$0.15                   │
│  • Third-Party API Sync Allotment:               -$0.05                   │
│  ────────────────────────────────────────────────────────                 │
│  Total Blended Marginal Cost per User:           -$1.10 / month           │
│                                                                           │
│  NET CONTRIBUTION MARGIN PER SUBSCRIBER:         $13.89 (92.6% MARGIN)    │
└───────────────────────────────────────────────────────────────────────────┘
```

#### Key Financial Metrics
- **Average Revenue Per User (ARPU):** $\$14.99\text{ / month}$ (or $\$129.00\text{ / year} = \$10.75\text{/mo}$).
- **Marginal Cost of Goods Sold (COGS):** $\$1.10\text{ / user / month}$.
- **Gross Profit Margin:** **$92.6\%$**.
- **Customer Lifetime Value (LTV):** Assuming a conservative $5\%$ monthly churn rate ($20\text{-month}$ average lifespan):
  $$\text{LTV} = 20 \text{ months} \times \$13.89 \text{ net margin} = \mathbf{\$277.80}$$
- **Target Customer Acquisition Cost (CAC):** Paid digital acquisition (Meta, Strava running clubs, organic influencer partnerships) target of $\$35.00\text{--}\$50.00$.
- **LTV / CAC Ratio:** $\mathbf{5.5 : 1 \text{ to } 7.9 : 1}$ (Indicating exceptional venture-scale capital efficiency).

---

## 8. Risk Management & Fallback Matrix

```
┌───────────────────────────────────────────────────────────────────────────┐
│                     COMPREHENSIVE RISK & FALLBACK MATRIX                  │
├─────────────────────────┬─────────────────────────┬───────────────────────┤
│ 1. API Dependency Risk  │ 2. Clinical Drift Risk  │ 3. LLM Latency Spike  │
│ • Intervals.icu 503     │ • Hallucinated Exercises│ • Provider Outage     │
│ • Local DB Cache fallback│ • Deterministic Gate   │ • Multi-Provider Fail │
└─────────────────────────┴─────────────────────────┴───────────────────────┘
```

| Risk Domain | Risk Event | Severity | Probability | Automated Detection | Fallback & Mitigation Strategy |
|---|---|:---:|:---:|---|---|
| **External API** | Intervals.icu API downtime or HTTP 503 during 08:00 AM morning check-in cron. | HIGH | MEDIUM | Health-check probe returns non-200 status code. | **Local Database Fallback:** System automatically reads the athlete's 7-day cached rolling average CTL/ATL/HRV from PostgreSQL and proceeds with morning check-in without failure. |
| **Clinical Safety** | LLM generates a contraindicated exercise (e.g., maximal sprint with acute hamstring tear). | CRITICAL | LOW | **Biomechanical Safety Guard** string & token contraindication scanner. | **Deterministic Interception:** Hard safety guard catches contraindicated exercise name, purges it from the response, and substitutes it with the knowledge base gold-standard alternative (e.g., Askling isometrics) before the athlete sees the message. |
| **Clinical Liability** | Athlete experiences acute cardiac distress or spinal emergency symptoms during workout. | CRITICAL | LOW | **Medical Red-Flag Triage** keyword and semantic regex scanner. | **Immediate Emergency Lockout:** Instantly terminates all workout generation, locks account into Medical Hold, and returns clear emergency medical referral prompts. |
| **LLM Infrastructure** | Anthropic / OpenAI API experiences major outage or latency spike $>15\text{s}$. | HIGH | MEDIUM | Circuit breaker detects 3 consecutive request timeouts. | **Multi-Provider Failover:** LangGraph dynamically reroutes requests: `claude-3-5-sonnet` $\rightarrow$ `gpt-4o` $\rightarrow$ `deepseek-v3` $\rightarrow$ Local Ollama / vLLM fallback. |
| **Data Integrity** | Athlete submits corrupt voice note or incomprehensible background noise. | LOW | HIGH | Whisper API returns low confidence score ($<0.4$). | **Conversational Clarification:** System responds politely: *"I couldn't quite catch the workout details due to wind noise. Did you run or cycle, and what was your time and RPE?"* |
| **Multi-Tenancy** | Cross-tenant data leak attempt via parameter tampering. | CRITICAL | LOW | PostgreSQL RLS policy violation logs 403 Forbidden. | **Cryptographic RLS Rejection:** Query returns empty recordset automatically; security event logged to Sentry; tenant access suspended pending audit. |

---

## 9. Conclusion & Execution Directives

The architectural research conducted in this CTO Master Plan demonstrates that Aegis Coach's competitive advantage lies at the intersection of **Zero-Friction Conversational UX (Telegram Ecosystem)**, **Deterministic Clinical Safety Guardrails**, and **Sports Science Literature RAG**.

By bypassing the friction of native app installs and the high cost of enterprise wearable APIs, Aegis Coach achieves an industry-leading **$92.6\%$ gross margin** with a marginal operating cost of **$1.10 / user / month**. The hybrid technology stack—FastAPI, Supabase PostgreSQL with Row-Level Security, Qdrant vector retrieval, and LangGraph multi-agent orchestration—provides the foundation required to scale from a single-athlete MVP to 100,000+ active subscribers.

**Immediate Next Directives:**
1. Proceed with **Milestone M3**: Implementation of sports science data models, RAG vector corpus, and multi-tenant context manager in `poc/`.
2. Proceed with **Milestone M4**: Implementation of multi-agent intent router, clinical physio agents, and deterministic biometric safety guards.
3. Validate entire system against the **4-Tier E2E Testing Suite** in `tests/` to guarantee $100\%$ pass rates with zero clinical regressions.

---
*End of CTO Master Architectural Blueprint — Aegis Coach Systems Engineering.*
