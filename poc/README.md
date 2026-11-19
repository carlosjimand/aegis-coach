# Aegis Coach — Proof of Concept (PoC) Engine & CLI Runner

> **Multi-Agent Sports Science & Clinical Rehabilitation Intelligence Platform**  
> *Subacute Hamstring Rehabilitation, ACWR Workload Management, Metabolic Fueling & Deterministic Biomechanical Safety Guardrails.*

---

## 1. Overview & Architecture

**Aegis Coach** is a multi-tenant personal training and rehabilitation intelligence system designed for endurance, track, and mountain athletes. The Proof of Concept (PoC) implements a high-performance multi-agent architecture with deterministic clinical guardrails and vector-based sports science literature retrieval:

```
                                  [ Athlete Query / Webhook / Chat ]
                                                  │
                                                  ▼
                                     ┌─────────────────────────┐
                                     │   TenantContext (RLS)   │
                                     └────────────┬────────────┘
                                                  │
                                                  ▼
                                     ┌─────────────────────────┐
                                     │  InjuryGuard Pre-Flight │◄─── [ RedFlagDetector / Pain VAS / RED-S ]
                                     └────────────┬────────────┘
                                                  │
                                   ┌──────────────┴──────────────┐
                           [Safe]  │                             │ [Unsafe / Red Flag]
                                   ▼                             ▼
                        ┌────────────────────┐        ┌──────────────────────┐
                        │    AgentRouter     │        │ Safety Override Msg  │
                        └─────────┬──────────┘        └──────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┬──────────────────────┐
         ▼                        ▼                        ▼                      ▼
┌──────────────────┐    ┌───────────────────┐    ┌───────────────────┐  ┌───────────────────┐
│   MedicalAgent   │    │   PlannerAgent    │    │  NutritionAgent   │  │  DataEntryAgent   │
│  (Hybrid RAG)    │    │  (TRIMP / ACWR)   │    │  (Burke CHO/FODMAP)│  │ (Structured JSON) │
└────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘  └─────────┬─────────┘
         │                        │                        │                      │
         └────────────────────────┼────────────────────────┴──────────────────────┘
                                  │
                                  ▼
                     ┌───────────────────────────┐
                     │  InjuryGuard Post-Flight  │ ─── Scans & purges dangerous movement tokens
                     └────────────┬──────────────┘
                                  │
                                  ▼
                       [ Unified AgentResponse ]
```

---

## 2. Directory Layout & Components

```
poc/
├── README.md                      # Comprehensive PoC guide & architecture blueprint
├── requirements.txt               # Minimal dependencies (numpy, pydantic, pytest)
├── config.py                      # Global configuration, dataset paths, physiological constants
├── run_poc.py                     # Master executable test runner and CLI benchmark suite
├── data/
│   ├── medical_knowledge.json     # Sports medicine clinical literature corpus & protocols
│   ├── sample_workouts.json       # Benchmark periodized workout sessions
│   └── user_profiles.json         # Multi-tenant test athlete profiles
├── models/
│   ├── __init__.py
│   ├── athlete.py                 # AthleteProfile, InjuryRecord, RecoveryMetrics, BiometricState
│   └── conversation.py            # UserQuery, DomainIntent, SafetyViolation, ExecutionTrace, AgentResponse
├── rag/
│   ├── __init__.py
│   ├── embeddings.py              # Deterministic L2 normalized embedding generator & OpenAI adapter
│   ├── vector_store.py            # Vector store with Cosine Similarity, Metadata Filtering, Tenant namespaces
│   └── retriever.py               # HybridRetriever (Dense Cosine + Sparse BM25 + Citation Formatter)
├── safety/
│   ├── __init__.py
│   ├── rules.py                   # Clinical contraindication matrix, pain VAS policies, safe alternatives
│   ├── red_flags.py               # Acute cardiovascular & orthopedic trauma emergency detector
│   └── injury_guard.py            # Pre-flight query validator & post-flight response sanitizer
├── agents/
│   ├── __init__.py
│   ├── base_agent.py              # BaseAgent ABC with telemetry trace handling
│   ├── medical_agent.py           # Clinical Physio agent querying Sports Science RAG
│   ├── planner_agent.py           # Exercise Physiologist generating periodized workouts & ACWR
│   ├── nutrition_agent.py         # Nutrition specialist (Burke carb loading, Low-FODMAP, Collagen)
│   ├── data_entry_agent.py        # Natural language workout parser extracting structured JSON metrics
│   └── general_agent.py           # Conversational check-in, habit formation & clarification agent
├── router/
│   ├── __init__.py
│   └── agent_router.py            # Multi-agent swarm dispatcher & hierarchical intent classifier
└── tenancy/
    ├── __init__.py
    ├── context.py                 # Thread-safe/async-safe TenantContext manager (ContextVar)
    └── security.py                # TenantSecurityManager with HMAC-SHA256 token verification
```

---

## 3. Prerequisites & Installation

Aegis Coach PoC runs **100% offline and deterministically** with zero external cloud dependencies or C++ build tools required.

### Requirements:
- Python 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.14 on Windows, macOS, Linux)
- Standard packages: `pydantic>=2.5.0`, `numpy>=1.24.0`, `pytest>=8.0.0`

### Setup:
```bash
# Clone or navigate to the repository
cd aegis-coach

# Install dependencies
pip install -r poc/requirements.txt
```

---

## 4. CLI Execution & Benchmark Switches

The master runner `poc/run_poc.py` validates all subsystems:

```bash
# Run all benchmark suites and coaching demonstrations
python poc/run_poc.py --all

# Run individual subsystems
python poc/run_poc.py --rag       # Sports science vector search & metadata filtering
python poc/run_poc.py --router    # Intent classification & entity extraction
python poc/run_poc.py --safety    # Clinical guardrails, 100% sprint block, red flags
python poc/run_poc.py --tenancy   # Multi-tenant context scoping & token validation
python poc/run_poc.py --demo      # End-to-end walkthrough of 4 core coaching scenarios

# Enable verbose execution traces and telemetry
python poc/run_poc.py --all --verbose
```

---

## 5. Core Coaching Scenarios Demonstrated

| Scenario ID | Athlete Persona | Challenge / Pathology | Expected System Behavior |
|---|---|---|---|
| **SCENARIO_1** | **Carlos** (23yo 800m/Trail runner) | Proximal hamstring strain recurrence (Subacute, VAS 2/10). Requests 100% maximal hill sprints. | **HARD BLOCK by InjuryGuard.** Blocks explosive sprints, substitutes with Askling L-Protocol + prone isometrics (5x45s) + flat submaximal strides (70-75%). |
| **SCENARIO_2** | **Elena** (28yo Sub-2:50 Marathoner) | Marathon carbohydrate loading with Low-FODMAP gut sensitivity. | **NutritionAgent Dispatch.** Generates Burke et al. carbohydrate loading (8-10g/kg/day, 512g/day) with white rice, oats, maltodextrin; restricts high-FODMAP foods. |
| **SCENARIO_3** | **Sofia** (26yo Ultra-Trail Runner) | Severe autonomic crash (Morning HRV rMSSD drops 50% from 68ms to 34ms, 4h sleep). Requests hard intervals. | **AUTONOMIC OVERRIDE.** Intercepts threshold session, substitutes with 40-min Zone 1 active recovery spin (HR < 120 bpm) + diaphragmatic mobility. |
| **SCENARIO_4** | **Marcus** (31yo CrossFit Athlete) | Acute L4-L5 lumbar disc herniation. Requests 1RM conventional deadlifts. | **HARD BLOCK.** Drops maximal spinal flexion deadlifts, prescribes Dr. Stuart McGill Big 3 (Curl-up, Side Plank, Bird-Dog) + High-Handle Trap Bar (65% 1RM). |

---

## 6. Scientific References & Clinical Evidence

The Aegis Coach PoC implements peer-reviewed evidence across sports science:

1. **Hamstring Rehabilitation**: Askling CM, et al. (2013, 2014) *Br J Sports Med*. Askling L/H-protocols and lengthened eccentric loading.
2. **Achilles Tendinopathy**: Silbernagel KG, et al. (2007) *Am J Sports Med*; Alfredson H, et al. (1998). Pain-monitoring model and heavy eccentric heel drops.
3. **Patellar Analgesia**: Rio E, et al. (2015) *Br J Sports Med*. Isometric Spanish squats (5x45s at 60-70° knee flexion) inducing immediate pain relief.
4. **Spine Mechanics**: McGill SM. (2010, 2015). Core stability, neutral lordosis, and modified curl-up / side bridge / bird-dog.
5. **Endurance Fueling**: Burke LM, et al. (2019) *Int J Sport Nutr Exerc Metab*. Glycogen loading protocols and Low-FODMAP gastrointestinal management.
6. **Workload Modeling**: Banister EW. (1991); Gabbett TJ. (2016) *Br J Sports Med*. Acute:Chronic Workload Ratio (ACWR) and injury spike thresholds (>1.50).
7. **Tendon Collagen Synthesis**: Baar K. (2017) *Sports Med*. Gelatin/Vitamin C timing 45-60 min prior to loading.
