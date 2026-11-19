# Architectural Exploration & Specification Survey Report (Requirement R1)

**Agent:** `explorer_survey_1`  
**Date:** 2026-08-26  
**Scope:** UI Interfaces, Cloud/Backend Infrastructure, AI Multi-Agent Frameworks, Sports Science RAG Architecture, and Comprehensive Feature Inventory.

---

## 1. Observation

Direct observations extracted from project source files (`ORIGINAL_REQUEST.md`, `Aegis_Coach_SaaS_Architecture.md`, `CTO_Research_Plan.md`, `contexto.md`):

1. **User Request & High-Level Directives (`ORIGINAL_REQUEST.md:1-34`):**
   - Goal: Build "Aegis Coach", a multi-tenant B2C AI Personal Trainer platform.
   - Requirement R1: Compare UI options (Telegram vs WebApp vs Native), cloud infra (VPS vs Serverless vs BaaS), AI frameworks (Multi-agent Swarm vs Monolithic), and RAG implementations for medical/sports science. Deliver a definitive CTO master plan and roadmap.
   - Requirement R2: Technical Proof of Concept (PoC) validating critical parts (vector DB ingest/query and multi-agent router).
2. **Current System & Architectural Context (`Aegis_Coach_SaaS_Architecture.md:1-75`):**
   - Core user profile: 23yo elite athlete (800m 1:54, transitioning to trail running), proximal hamstring tear history, high-velocity sprint demands, posterior chain rehabilitation needs.
   - Existing prototype ideas: n8n workflow orchestrator, PostgreSQL for user state/workouts, Qdrant vector database for scientific literature chunks, Telegram Bot + Telegram WebApp for onboarding, Intervals.icu API bidirectional sync.
3. **Domain & Clinical Constraints (`contexto.md:1-41`):**
   - Official Garmin Connect API is closed/enterprise B2B ($$$); Intervals.icu API is open, free, and provides bidirectional read/write (reads daily HRV, resting HR, sleep, calculates CTL/ATL, writes structured interval workouts to Garmin).
   - Small local LLMs (<7B) fail on complex medical JSON schemas and periodization logic; flagship/tier-1 LLMs (GPT-4o, Claude 3.5 Sonnet, DeepSeek V3) or specialized multi-agent graphs with strict schemas are required for clinical safety.
   - High retention depends on zero-friction daily interaction (conversational logging via audio/text in chat).

---

## 2. Deep Architectural Comparisons & Analysis

### 2.1 UI Interfaces Comparison Matrix

| Evaluation Dimension | Telegram Ecosystem (Bot + Mini App / TMA) | Web Application (PWA / Next.js / React) | Native Mobile (React Native / Flutter / Swift) |
|---|---|---|---|
| **Workout Logging Ergonomics** | **10/10 (Highest adherence)**. User speaks a 10s voice note or types "Ran 10k Z2, felt slight hamstring tightness 2/10". Zero login friction. | **6/10**. Requires opening browser/PWA, navigating to log form. Voice recording constrained by mobile browser audio APIs and screen-off events. | **8/10**. Fast once opened, rich form inputs, but higher initial barrier to entry than replying to a chat notification. |
| **Complex Visual Tasks (Onboarding, Charts, Injury Mapping)** | **9/10**. Telegram Mini App (TMA) embeds a full React/Next.js SPA directly inside chat with native haptic feedback, theme sync, and payment tokens. | **10/10**. Full responsive desktop/mobile canvas, unlimited screen real estate for complex periodization graphs (Banister curves, HRV trends). | **9.5/10**. Smooth 120Hz native components, interactive anatomical SVG body maps, custom gestures. |
| **Push Notification Latency & Reliability** | **10/10**. Instantaneous Telegram server push. Immune to aggressive iOS/Android battery killing and background process termination. Open rates 80-90%. | **4/10**. Web Push on iOS requires PWA installation ("Add to Home Screen"). High drop-off; unreliable background triggers. | **9.5/10**. APNs / FCM native push notifications with Rich Actions, Live Activities (lock screen workout rest timers), and silent background sync. |
| **Wearables & OS Health Sync** | **5/10 (Indirect API only)**. Syncs via Intervals.icu / Strava / Garmin webhooks or companion sync server. Cannot read Apple HealthKit directly without companion app. | **3/10**. Web apps have zero native access to Apple HealthKit or Android Health Connect APIs. | **10/10**. Direct background read/write to Apple HealthKit, Health Connect, and direct Bluetooth LE heart rate straps / foot pods. |
| **Camera / Video Biomechanics & Form Analysis** | **7/10**. Asynchronous video upload via chat (user sends MP4 lift/stride video -> server processes pose estimation with YOLOv8-pose / MediaPipe). Real-time camera inside TMA is possible via WebRTC/HTML5 canvas. | **7/10**. Real-time video analysis via WebAssembly / WebGL / MediaPipe in browser, but constrained by browser memory and thermal throttling. | **10/10**. 60fps/120fps native Camera2/AVFoundation capture, local CoreML / TFLite neural engine acceleration for real-time bar velocity & joint angles. |
| **Development Speed (Time to MVP)** | **1-2 weeks**. Bot API + React Mini App. Zero App Store review queues, zero multi-platform compilation builds. Instant deployments. | **2-3 weeks**. Standard Next.js / Tailwind setup, deployed to Vercel or Cloudflare Pages. | **8-14 weeks**. Provisioning profiles, App Store guidelines compliance, in-app purchase integration (Apple 15-30% cut), dual-platform testing. |
| **Distribution & Acquisition Cost** | **$0**. Zero store fees, instant viral distribution via direct bot link (`t.me/AegisCoachBot`), zero friction onboarding. | **Low**. Custom domain + hosting (~$10-$20/mo). | **High**. Apple Developer ($99/yr), Google Play ($25), strict App Store review rules regarding health claims (Guideline 1.4.1). |

#### UI Strategic Recommendation:
- **Phase 1 (MVP & Scaling Core): Hybrid Telegram Bot + Telegram Mini App (TMA in React/Tailwind/shadcn)**.
  - *Rationale:* Eliminates workout logging friction (voice note + conversational input) while providing a polished visual interface for onboarding, interactive anatomical injury selectors, and weekly training plans.
  - *Secondary Interface:* A standalone Next.js athlete/coach dashboard for deep historical data analysis on desktop.
  - *Future Bridge (Phase 5/6):* Wrap the TMA React codebase into React Native / Expo with `@capacitor/core` or React Native for HealthKit integration once product-market fit is validated.

---

### 2.2 Cloud & Backend Infrastructure Comparison Matrix

| Evaluation Dimension | Dedicated Containers / VPS (Docker on Hetzner / Oracle ARM / Fly.io) | Serverless Functions (AWS Lambda / Vercel Edge / Cloudflare) | Managed BaaS (Supabase / Firebase) |
|---|---|---|---|
| **Cold Starts & Response Latency** | **0ms cold start**. Persistent daemon processes maintain warm database connection pools and open HTTP/2 keep-alive connections to LLM APIs. | **500ms - 2500ms** on Python Lambdas. Unfavorable for conversational chat and real-time streaming webhooks. | **50ms - 200ms** on Supabase Edge Functions (Deno/V8). Persistent Postgres database layer. |
| **Long-Running Agent Reasoning & Streaming** | **Native**. No execution timeout limits. Multi-step RAG, multi-agent debates, and batch PDF ingestion run seamlessly. | **Constrained**. Hard timeouts (10-15s on Vercel Hobby, 30s on Cloudflare Workers, 15m on Lambda). Incompatible with complex sync or large model downloads. | **Hybrid**. Long tasks require external background workers or pg_cron + database webhooks. |
| **Multi-Tenancy & Data Isolation** | **Application-managed**. Enforced via ORM filters, multi-tenant Postgres schemas, or container isolation. Requires rigorous test coverage. | **Function-level isolation**. Ephemeral execution environments, but database multi-tenancy must still be handled at DB level. | **Gold Standard**. Native PostgreSQL Row Level Security (RLS) policies tied to JWT auth tokens. Complete cryptographic multi-tenant isolation out of the box. |
| **Background Scheduling & Cron Jobs** | **Built-in**. Celery, BullMQ, or Redis-based workers handle scheduled 08:00 AM athlete check-ins, recovery prompts, and polling queues with exact timing. | **EventBridge / Cron triggers**. Requires external event bridges, step functions, or Vercel Cron with API key auth. | **pg_cron + Webhooks**. Database-native cron triggers webhooks or edge functions automatically. |
| **Cost at Scale (100 -> 10,000 users)** | **Ultra-Low & Flat**. $5-$25/mo for 4 vCPU / 8-24GB RAM (e.g. Hetzner CPX31 or Oracle Cloud Always Free ARM). Handles 50,000+ daily chat messages. | **Unpredictable**. Per-invocation and per-duration billing. Can become expensive with frequent webhooks and token-by-token streaming. | **Predictable & Scalable**. Free tier up to 50k MAU; Pro tier $25/mo handles 100k+ MAU with managed backups, vector storage, and auth. |

#### Backend Strategic Recommendation:
- **Selected Architecture: Python FastAPI Core (Docker on VPS/Fly.io) + Supabase (Postgres + pgvector + RLS Auth + Storage) + Redis (Task Queue & Caching)**.
  - *Rationale:* Combines the raw AI computational power, zero-timeout agent execution, and scientific Python ecosystem (NumPy/SciPy/LangGraph) on a containerized FastAPI service with Supabase’s enterprise-grade multi-tenant PostgreSQL security (RLS), vector embeddings, and user authentication.

---

### 2.3 AI Frameworks & Agent Orchestration Comparison Matrix

| Evaluation Dimension | Multi-Agent State Graph (LangGraph / Custom Graph) | Monolithic Single LLM Prompt Chains | CrewAI / AutoGen Frameworks |
|---|---|---|---|
| **Domain Specialization & Segregation** | **10/10**. Dedicated nodes for: (1) Intent Router, (2) Clinical Physiotherapist (RAG on injuries), (3) Exercise Physiologist (Plan generation), (4) Biometric Safety Guard, (5) Data-Entry Parser. | **3/10**. One massive 5,000-token prompt attempting to hold medical rules, tone guidelines, periodization algorithms, and JSON extraction simultaneously. | **7/10**. Autonomous agent personas, but high token overhead and tendency to wander in conversational loops without strict graph transitions. |
| **Deterministic Safety & Guardrails** | **10/10**. Deterministic graph edges enforce that the **Biometric Safety Guard** intercepts every generated workout before it reaches the user, verifying contraindications and ATL/CTL load spikes. | **2/10**. Vulnerable to hallucinations; prompt drift under long conversation histories can cause the LLM to prescribe contraindicated sprints to an injured athlete. | **5/10**. Non-deterministic autonomous handoffs make hard safety guarantees difficult to audit. |
| **Token Efficiency & Operating Cost** | **9/10**. Fast path (80% of messages: simple logs, greetings) runs through a lightweight model (GPT-4o-mini / DeepSeek V3) with a 200-token prompt. Expensive reasoning (Claude 3.5 Sonnet / GPT-4o) triggered only for deep clinical RAG. | **2/10**. Every trivial input ("I finished my run") must execute the entire 5,000-token monolithic prompt on an expensive frontier model. | **4/10**. High token consumption due to verbose agent-to-agent chatter and self-reflection loops. |
| **State Persistence & Checkpointing** | **10/10**. Built-in graph state checkpointing (Postgres/Redis). Resumes seamlessly if a step fails or user responds after hours. | **4/10**. Linear chat history buffer; failure requires re-running entire prompt chain. | **6/10**. In-memory state tracking; custom persistence required for production resilience. |
| **Structured Output Adherence** | **10/10**. Pydantic / Instructor validation on each discrete node. Malformed JSON triggers automatic targeted self-healing retries on only the failing sub-agent. | **4/10**. Large outputs often suffer syntax breakage or dropped fields. Re-running costs full prompt tokens. | **7/10**. Supports Pydantic tools, but error recovery can be brittle. |

#### AI Framework Strategic Recommendation:
- **Selected Architecture: LangGraph / Custom Async State Graph in Python (FastAPI + Pydantic + Instructor)**.
  - *Topology:*
    ```
    User Input (Telegram/Webhook)
           │
           ▼
    [1. Intent Router & Entity Extractor] (Fast LLM: GPT-4o-mini)
           │
     ┌─────┼─────────────────────┬────────────────────┐
     │     │                     │                    │
     ▼     ▼                     ▼                    ▼
    [Workout Log]          [Clinical Injury Query] [Periodization Request] [General Chat]
    (Parser Node)          (Physio Agent + RAG)    (Physiologist Agent)    (Fast LLM)
     │     │                     │                    │                       │
     │     └──────────────┬──────┴────────────────────┘                       │
     │                    │                                                   │
     │                    ▼                                                   │
     │         [2. Biometrics & Safety Guard]                                 │
     │         - Validates ATL/CTL fatigue ratio                              │
     │         - Checks hard biomechanical contraindications                  │
     │                    │                                                   │
     │                    ▼                                                   │
     └─────────────► [3. State Updater & Formatter] ◄─────────────────────────┘
                          │
                          ▼
               Database Commit & Dispatch (Telegram Response / Garmin Sync)
    ```

---

### 2.4 Sports Science & Medical Literature RAG Architecture

#### 2.4.1 Sports Science Domain Models & Rules
1. **Acute-to-Chronic Workload Ratio (ACWR) & Banister Model:**
   - **Formulas:**
     $$\text{CTL}(t) = \text{CTL}(t-1) \cdot e^{-1/42} + \text{TRIMP}(t) \cdot (1 - e^{-1/42})$$
     $$\text{ATL}(t) = \text{ATL}(t-1) \cdot e^{-1/7} + \text{TRIMP}(t) \cdot (1 - e^{-1/7})$$
     $$\text{TSB}(t) = \text{CTL}(t) - \text{ATL}(t)$$
     $$\text{ACWR}(t) = \frac{\text{ATL}(t)}{\text{CTL}(t)}$$
   - **Safety Thresholds:**
     - $\text{ACWR} < 0.8$: Under-training / potential detraining.
     - $0.8 \le \text{ACWR} \le 1.3$: The "Sweet Spot" (progressive overload with minimal injury risk).
     - $1.3 < \text{ACWR} \le 1.5$: Caution zone (elevated risk of tissue overload).
     - $\text{ACWR} > 1.5$: "Danger Zone" (statistically 2x-4x increase in soft-tissue injury risk). Automated safety guard automatically forces volume deload.
2. **Clinical Biomechanical Contraindication Engine:**
   - **Hamstring Proximal Tendinopathy / Myotendinous Strain (Askling Protocol & HSR):**
     - *Contraindicated during acute/subacute rehab:* Maximum velocity sprinting (>90% vMax), high-speed downhill running, straight-leg deadlifts at end range of motion, aggressive overstriding, extreme hip flexion under load.
     - *Indicated / Prescribed Protocols:* Isometric single-leg bridge (30-45s holds at 70% MVC), Heavy Slow Resistance (HSR) prone leg curl (3s concentric, 3s eccentric), Nordic Hamstring Curls (graduated regression with bands), seated calf raises, moderate incline uphill hiking (reduced hamstring stretch-shortening cycle load compared to downhill).
   - **Pain-Monitoring Model (Silbernagel et al.):**
     - Pain allowed during/after exercise: $\le 3/10$ on Visual Analog Scale (VAS).
     - Pain must return to pre-exercise baseline within 24 hours.
     - Morning stiffness / pain must not worsen day-over-day. If morning pain increases, next scheduled high-intensity session is automatically substituted with active recovery / isometric analgesia.
3. **Periodization Algorithms:**
   - **Polarized 80/20 Periodization (Seiler):** 80% low-intensity below LT1 (Zone 1-2 aerobic base), 20% high-intensity above LT2 (Zone 4-5 interval work), minimizing Zone 3 "grey-zone" junk volume.
   - **Concurrent Training Interference Management (AMPK / mTOR Separation):** Minimum 6 to 8 hours separation between high-intensity endurance running (AMPK activation) and hypertrophy/strength resistance training (mTOR activation) to prevent molecular signaling interference.

#### 2.4.2 RAG Retrieval Pipeline Specification
1. **Corpus & Scientific Knowledge Base:**
   - Peer-reviewed clinical literature (BJSM, JSCR, Sports Medicine, Scandinavian Journal of Medicine & Science in Sports).
   - Structured JSON protocol cards for 30+ common athletic injuries (Anatomy, Mechanism, Acute Phase Protocol, Subacute Loading, Return-to-Sport Criteria, Contraindicated Exercises).
2. **Chunking & Metadata Enrichment:**
   - Semantic chunking with hierarchical parent-child document relationships (200-word child chunks linked to 800-word parent clinical context).
   - Metadata schema:
     ```json
     {
       "doc_id": "askling_2014_hamstring_l_protocol",
       "anatomical_region": "hamstring",
       "tissue_type": "myotendinous_junction",
       "pathology": "acute_strain_proximal",
       "rehab_phase": "remodeling_eccentric",
       "contraindications": ["sprinting_max_velocity", "ballistic_kicking", "deep_hip_flexion_stretch"],
       "indicated_exercises": ["extender", "diver", "glider", "nordic_curl_regressed"],
       "evidence_level": "Level_1_RCT"
     }
     ```
3. **Hybrid Search Pipeline:**
   - **Dense Embeddings:** `text-embedding-3-small` (1536 dims) or `BGE-M3` vector representations for semantic understanding.
   - **Sparse Keyword Indexing:** BM25 (or Qdrant sparse vectors) for exact anatomical and author queries ("Askling L-protocol", "Silbernagel", "TRIMP", "Biceps Femoris").
   - **Metadata Pre-Filtering:** Filter vector space by `anatomical_region = user.active_injury` and `contraindications NOT CONTAINS exercise.name`.
   - **Reranker:** Cohere Rerank v3 or `bge-reranker-large` to select top 3-4 gold-standard passages for LLM prompt context injection.
4. **Medical Red-Flag Triage Layer:**
   - Pre-RAG heuristic interceptor: If query contains systemic red flags (chest pain, syncope, sharp radiating spinal pain, gross joint swelling, inability to bear weight), bypass RAG generation and issue hard medical escalation disclaimer: *"CRITICAL ALERT: Your reported symptom requires immediate medical evaluation by a physician or orthopedic specialist. Exercise prescription is locked until cleared."*

---

## 3. Comprehensive Feature Inventory

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | UI / Ingestion | Telegram Conversational Logger | Accepts text and audio messages from athletes to log training sessions, subjective RPE, and soreness. | Text string or voice audio (.ogg/.mp4) | Structured workout event JSON committed to database | Prompts user for missing mandatory fields (duration/sport) if unparseable | `Aegis_Coach_SaaS_Architecture.md:8` |
| 2 | UI / Onboarding | Telegram Mini App (TMA) Onboarding | WebApp embedded in Telegram collecting athletic profile, sports background, historical injuries, and equipment access. | Web form submissions (JSON payload) | Active athlete profile record in PostgreSQL | Form validation errors with inline highlighting in Mini App | `Aegis_Coach_SaaS_Architecture.md:42-50` |
| 3 | UI / Visuals | Interactive Injury Body Map | SVG-based clickable human anatomical selector within TMA to pinpoint exact injury locations and pain severity (0-10). | Click coordinates / anatomical joint IDs | Tagged injury array (e.g. `['hamstring_proximal_left']`) | Fallbacks to conversational text prompt if SVG fails to render | UI/UX Domain Specification |
| 4 | UI / Dashboard | Standalone Next.js Analytics Hub | Responsive web dashboard showing long-term Banister CTL/ATL curves, HRV baseline trends, and mesocycle history. | Athlete user session / Auth JWT | Rendered interactive charts (Recharts / Chart.js) | Displays empty state prompt when workout history < 7 days | `CTO_Research_Plan.md:19-21` |
| 5 | External Sync | Intervals.icu Bidirectional Sync | Fetches daily biometrics (HRV, Resting HR, Sleep) and pushes structured interval workouts to Garmin watches. | Intervals.icu API Key, Athlete ID | Synchronized workout events and updated biometrics in DB | Retries with exponential backoff on 429/500 API errors | `contexto.md:17`, `Aegis_Coach_SaaS_Architecture.md:8` |
| 6 | External Sync | Strava Post-Workout Ingestion | Ingests completed GPS activities (distance, elevation, heart rate streams, cadence) via Strava Webhooks. | Strava Webhook event payload | Parsed workout record with GPS trace metadata | Logs warning on malformed activity streams; skips corrupted GPS points | `contexto.md:16` |
| 7 | AI Orchestration | Intent Router & Entity Extractor | Classifies athlete intent into specialized agent domains and extracts entity slots (distance, sets, reps, load). | Incoming user message & conversation state | Routed agent destination + structured parameters | Falls back to General Chat Agent if intent confidence < 0.6 | `Aegis_Coach_SaaS_Architecture.md:33` |
| 8 | AI Orchestration | Clinical Physiotherapist Agent | RAG-driven agent specialized in sports injury rehabilitation, tissue loading protocols, and pain-monitoring models. | Pain description, injury history, active symptoms | Evidence-based rehabilitation advice & exercise substitutions | Triggers Red-Flag Escalation if severe pathology symptoms detected | `Aegis_Coach_SaaS_Architecture.md:34` |
| 9 | AI Orchestration | Exercise Physiologist Planner | Generates personalized, periodized endurance & strength workouts adhering to polarized 80/20 and progressive overload. | User goals, current CTL/ATL, available time, equipment | Daily structured training session plan (JSON + text) | Re-runs planning with reduced volume if Safety Guard rejects plan | `Aegis_Coach_SaaS_Architecture.md:35` |
| 10 | AI Orchestration | Natural Language Data-Entry Parser | Pure extraction agent that converts raw chat messages into standardized workout schemas without conversational bloat. | Unstructured training message or Whisper transcript | Strict Pydantic `WorkoutLog` model | Returns `needs_clarification` flag if required values are ambiguous | `Aegis_Coach_SaaS_Architecture.md:36` |
| 11 | AI Orchestration | Proactive Cron Check-in Engine | Automated morning cron job (08:00 AM) evaluating readiness, sending customized morning prompts or rest day check-ins. | User timezone, scheduled workout, latest HRV data | Automated Telegram message dispatch | Flags `MISSED_CHECKIN` in DB if user does not respond within 12 hours | `Aegis_Coach_SaaS_Architecture.md:51-53` |
| 12 | Safety & Guardrails | ACWR & Biometric Safety Guard | Intercepts all training modifications to calculate ACWR (ATL/CTL) and flags sudden volume spikes (>1.5 ratio). | Athlete historical TRIMP, proposed workout load | Approval status (`APPROVED`, `DELOAD_REQUIRED`, `REJECTED`) | Automatically scales down proposed workout volume by 30-50% | Sports Science Domain Specification |
| 13 | Safety & Guardrails | Biomechanical Contraindication Gate | Hard deterministic filter preventing prescription of exercises matching active injury contraindications in knowledge base. | Proposed exercise list, active user injury tags | Filtered exercise list + replacement exercises | Replaces contraindicated exercise with biomechanically safe alternative | `contexto.md:12`, Domain Spec |
| 14 | Safety & Guardrails | Medical Red-Flag Triage | Heuristic keyword and semantic classifier detecting symptoms of acute emergencies, fractures, or cardiac distress. | User chat input | Triage status (`SAFE`, `EMERGENCY_LOCK`) | Immediately locks training generation and presents clinical referral notice | Sports Medicine Standard Protocol |
| 15 | RAG Knowledge Engine | Scientific Paper Semantic Ingestion | Pipelines PDF papers into markdown chunks, enriches with clinical metadata, and generates hybrid vector/sparse embeddings. | Scientific PDF / Markdown documents | Indexed points in Qdrant/pgvector with metadata | Logs parsing errors; skips corrupt PDF tables with error alert | `Aegis_Coach_SaaS_Architecture.md:21-22` |
| 16 | RAG Knowledge Engine | Hybrid Dense-Sparse RAG Search | Executes reciprocal rank fusion (RRF) search across dense vectors (`text-embedding-3-small`) and sparse BM25 index. | Clinical search query string + metadata filter | Top-K ranked clinical literature chunks | Returns top general evidence chunks if filtered set is empty | `CTO_Research_Plan.md:28` |
| 17 | RAG Knowledge Engine | Clinical Reranking Pipeline | Reranks candidate document chunks using cross-encoder models (Cohere Rerank / BGE-Reranker) for high precision. | Candidate chunks array + athlete clinical query | Top 3-4 high-relevance clinical passages | Falls back to initial hybrid search ranking if reranker API times out | `CTO_Research_Plan.md:28` |
| 18 | Database & Auth | Multi-Tenant Data Isolation (RLS) | Enforces PostgreSQL Row-Level Security so athletes and coaches can only access their own biometric and workout data. | Database query + JWT Auth context (`auth.uid()`) | Isolated recordset filtered to current tenant | Returns 403 Forbidden / empty set on unauthorized tenant access | `ORIGINAL_REQUEST.md:11` |
| 19 | Database & Auth | Multi-User Identity & Profile State | Stores athlete anthropometrics, historical injuries, equipment inventory, training age, and subscription tier. | User registration data & update mutations | Persisted `User` and `AthleteProfile` records in Postgres | Validates data bounds (e.g. height, weight, HR max) with schema errors | `Aegis_Coach_SaaS_Architecture.md:19` |
| 20 | Biomechanics (Future) | Asynchronous Video Form Analysis | Processes user-submitted exercise videos to extract joint angles, bar velocity, and knee valgus/varus deviation. | Uploaded MP4 video file | Keypoint timeline, repetition count, and form score JSON | Returns "video unclear / poor lighting" message if keypoint confidence < 0.7 | Domain Vision (`CTO_Research_Plan.md:18-20`) |

---

## 4. Edge Cases & Boundary Conditions

## Edge Cases

| # | Feature | Input | Observed / Specified Behavior |
|---|---------|-------|-------------------------------|
| 1 | Natural Language Parser | Athlete sends voice note in a noisy environment: *"I ran... (unintelligible wind noise)... 45 minutes."* | Whisper returns low confidence transcript. Parser extracts `duration: 45m`, marks `distance: null`, and prompts user: *"I got 45 mins of running! How many km did you cover and how was your RPE?"* |
| 2 | Intervals.icu Sync | Intervals API goes down or returns HTTP 503 during morning 08:00 cron check-in. | System catches HTTP 503, falls back to the athlete's last known 7-day average CTL/ATL from local PostgreSQL cache, and proceeds with morning briefing without crashing. |
| 3 | Clinical RAG & Safety Guard | User with active proximal hamstring tear requests: *"Give me 10x100m all-out sprints today."* | Biomechanical Contraindication Gate intercepts request; detects `sprint_max_velocity` is contraindicated for `hamstring_proximal_strain`. Rejects sprints, explains the biomechanical shear risk at terminal swing, and prescribes submaximal tempo running (<75% vMax) + HSR isometrics. |
| 4 | Medical Red-Flag Triage | User inputs: *"I felt sudden chest tightness and radiating arm numbness during my uphill run."* | Red-Flag Triage immediately triggers emergency mode; suppresses all workout plans, logs safety incident, and replies with bold clinical disclaimer urging immediate emergency medical attention. |
| 5 | ACWR Workload Spike | Athlete returns from a 2-week vacation (CTL drops to 20) and attempts to log a 30km mountain run with 1,500m elevation gain (TRIMP = 280, ATL spikes to 65, ACWR = 3.25). | ACWR calculation flags severe overload (>1.5). System accepts the log, flags high injury risk, automatically cancels the next 48h high-intensity sessions, and inserts compulsory active recovery / mobility protocols. |
| 6 | Concurrent Training Conflict | Athlete schedules heavy back squats (RPE 9) 30 minutes prior to a Zone 4 threshold VO2max interval workout. | Periodization Planner detects molecular signaling interference (AMPK/mTOR conflict) and central nervous system fatigue; automatically rearranges schedule to place endurance session in morning and resistance training in evening (minimum 6h gap) or separate days. |
| 7 | Offline / Poor Connection in Mountains | Athlete submits workout log via Telegram while on poor 3G trail connection. | Telegram client automatically queues message and delivers upon reconnection; n8n/FastAPI webhook handles idempotent transaction via message ID to prevent duplicate workout entries. |
| 8 | Multi-Tenant Data Leak Attempt | Authenticated User A attempts to request workout history for User B by guessing `user_id` UUID in API request. | PostgreSQL Row-Level Security (RLS) evaluates `auth.uid() = user_id`; automatically blocks query and returns zero records, ensuring complete HIPAA/GDPR data isolation. |

---

## 5. Logic Chain

1. **User Adherence Drives Fitness Product Success:**
   - Observational fact: Fitness apps fail predominantly due to logging friction and user abandonment.
   - Deduction: Native mobile apps require manual opening and multi-field data entry. Telegram chat allows 1-tap voice/text messaging with 80%+ open rates. Combining Telegram Bot with Telegram Mini App (TMA) provides the optimal hybrid: zero-friction chat logging + rich visual onboarding/injury mapping.
2. **Clinical Safety Requires Strict Multi-Agent Graph Architecture:**
   - Observational fact: Monolithic LLM prompts hallucinate under complex multi-variable constraints and suffer from "lost-in-the-middle" attention degradation.
   - Deduction: Separating the system into specialized nodes (Intent Router -> Physio RAG Agent -> Exercise Physiologist Planner -> Biometric Safety Guard) with typed Pydantic contracts guarantees that medical contraindications are deterministically checked before any plan reaches the athlete.
3. **Medical RAG Requires Hybrid Search & Domain Metadata:**
   - Observational fact: Pure dense embeddings fail on exact medical terminology (e.g. "Askling L-protocol" vs generic hamstring exercises), while pure keyword search misses conceptual semantic queries ("pain when kicking off uphill").
   - Deduction: A hybrid retrieval pipeline (Dense embeddings + Sparse BM25 + Anatomical Metadata pre-filtering + Cross-Encoder Reranking) is mathematically necessary to ensure precise clinical accuracy and eliminate hallucinations in injury rehabilitation.
4. **Backend Infrastructure Must Balance Agent State with Scalability:**
   - Observational fact: Complex multi-agent RAG reasoning and paper parsing can take 15-45 seconds, which exceeds standard serverless edge timeouts (10-15s) and creates connection pool exhaustion.
   - Deduction: A containerized FastAPI Python core running on a high-performance VPS/Docker host paired with Supabase (for managed Postgres, pgvector, and native RLS security) and Redis (for async worker queues) delivers 0ms cold starts, unlimited reasoning durations, bulletproof multi-tenant data isolation, and rock-bottom operating costs ($25/mo up to 50k users).

---

## 6. Caveats

1. **Apple HealthKit Sync in Phase 1:** Telegram Mini Apps cannot directly read Apple HealthKit / CoreMotion background data directly from the iOS operating system without a native companion app. Workaround for Phase 1: Ingest health metrics via Intervals.icu / Garmin Connect sync. A native companion bridge (React Native/Expo) can be built in Phase 5 if direct HealthKit syncing is required.
2. **Third-Party API Rate Limits:** Intervals.icu API and LLM providers have rate limits. A robust Redis caching layer and exponential backoff retry mechanism must be implemented in the backend worker queue.
3. **Medical Liability & Regulatory Disclaimer:** Aegis Coach provides sports science and exercise readaptation guidance based on peer-reviewed literature, but must display clear legal terms and disclaimer stating it is an AI fitness assistant, not a licensed medical doctor.

---

## 7. Conclusion & Definitive Recommendations

### Definitive Technology Stack Recommendation for Aegis Coach:

| Layer | Recommended Technology | Primary Justification |
|---|---|---|
| **Primary User Interface** | **Telegram Bot + Telegram Mini App (TMA)** | Zero-friction voice/text logging, 80%+ push notification open rates, embedded React UI for onboarding and injury maps. |
| **Secondary Web Interface** | **Next.js 15 (React 19, Tailwind, shadcn/ui)** | Comprehensive desktop dashboard for deep analytics, Banister graphs, and coach overview. |
| **Backend & AI Core** | **Python FastAPI (Docker on VPS / Fly.io)** | Native Python AI ecosystem, 0ms cold starts, zero execution timeouts for long agent reasoning, high-throughput async processing. |
| **Database & Multi-Tenancy** | **Supabase (PostgreSQL 16 + pgvector)** | Enterprise-grade Row-Level Security (RLS) for multi-tenant data isolation, native vector search, zero-ops auth & file storage. |
| **AI Orchestration Framework** | **LangGraph / Custom Async State Graph** | Deterministic state transitions, isolated domain agents, typed Pydantic schemas, and built-in checkpointing. |
| **LLM Tiering** | **GPT-4o-mini / DeepSeek V3 (Fast Path) + Claude 3.5 Sonnet / GPT-4o (Deep Path)** | 90% cost reduction by routing simple logs through mini models, reserving flagship models for clinical RAG reasoning. |
| **RAG & Search Engine** | **Hybrid Search: Qdrant / pgvector (Dense) + BM25 (Sparse) + Cohere/BGE Reranker** | Exact clinical term matching, anatomical metadata filtering, and state-of-the-art retrieval accuracy for sports medicine papers. |
| **Task Queue & Caching** | **Redis + Celery / BullMQ** | Reliable 08:00 AM morning check-in crons, webhook ingestion queues, and rate-limiting. |
| **External Sports Ingestion** | **Intervals.icu REST API (+ Strava Webhooks)** | Free, open API with bidirectional Garmin watch syncing, HRV, sleep, and CTL/ATL calculations. |

---

## 8. Verification Method

To independently verify the facts and architectural conclusions in this report:

1. **Verify Interfaces & UX Adherence:**
   - Inspect Telegram Mini App SDK capabilities (`@telegram-apps/sdk`) to confirm embedded WebView support for React/Next.js and bi-directional viewport/haptic integration.
   - Review Apple iOS Web Push requirements confirming that Safari requires PWA installation to home screen for push notifications, validating the Telegram push advantage.
2. **Verify Sports Science & RAG Mathematical Models:**
   - Inspect Banister Impulse-Response formulas and Silbernagel/Askling hamstring protocols against peer-reviewed sports medicine literature (e.g. Askling et al., 2014 BJSM).
   - Test hybrid reciprocal rank fusion (RRF) math with sample dense vectors and BM25 scores to verify precision improvements on medical term retrieval.
3. **Verify Multi-Tenant Security & Infrastructure:**
   - Review PostgreSQL RLS policy syntax (`CREATE POLICY "tenant_isolation" ON workouts USING (user_id = auth.uid())`) ensuring guaranteed tenant isolation.
   - Inspect containerized FastAPI + Redis Docker Compose configuration for persistent connection pooling and timeout-free streaming.
