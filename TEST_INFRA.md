# Aegis Coach: E2E Test Infrastructure & Methodology (`TEST_INFRA.md`)

## 1. Test Philosophy: Opaque-Box Requirement-Driven Testing

The Aegis Coach testing infrastructure adheres to the **Opaque-Box Requirement-Driven Testing** methodology. In a high-stakes AI personal training and clinical sports rehabilitation platform, testing internal implementation details is insufficient and brittle. Prescribing an inappropriate exercise to an injured athlete (e.g., maximal sprinting during acute hamstring remodeling or heavy spinal axial loading during an acute disc protrusion) carries severe clinical and legal liability.

Our testing paradigm enforces:
1. **Authoritative Specification Derivation**: Every test case derives its expected behavior and mathematical/clinical outputs directly from the project requirements (`ORIGINAL_REQUEST.md`), architectural contracts (`PROJECT.md`), and peer-reviewed sports science literature (e.g., Askling et al. for hamstring tendinopathy, Gabbett et al. for ACWR load management, Stuart McGill for spine biomechanics, Burke/Jeukendrup for endurance carb loading).
2. **Behavioral Contract Verification**: Tests treat subsystems as black/opaque boxes with strict interface contracts (Pydantic schemas, typed enums, and deterministic error propagation).
3. **No Facade or Trivial Tests**: All tests execute genuine computation, multi-tenant isolation assertions, vector math (cosine similarity & metadata pre-filtering), and clinical state transitions.
4. **Adversarial & Boundary Verification**: Systematic evaluation of malformed inputs, context overflows, malicious cross-tenant probes, and contradictory clinical claims.

---

## 2. The 4-Tier Test Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      TIER 4: REAL-WORLD SCENARIOS                       │
│  4 End-to-End Simulations (Carlos Hamstring, Marathon Low-FODMAP,       │
│  Autonomic Crash Overtraining, CrossFit Lumbar Disc Protrusion)         │
├─────────────────────────────────────────────────────────────────────────┤
│                   TIER 3: CROSS-FEATURE COMBINATIONS                    │
│  4 Combinatorial Workflows (Guard + Planner, Tenancy + RAG Partition,   │
│  Workout Parsing + ACWR Spike + Recalibration, Vegan Fueling + Cramps)  │
├─────────────────────────────────────────────────────────────────────────┤
│                     TIER 2: BOUNDARY & CORNER CASES                     │
│  7 Adversarial & Edge Cases (Empty Input, Token Overflow, Contradictory │
│  Injuries, Hallucinated Exercises, Missing Headers, Malformed Payloads) │
├─────────────────────────────────────────────────────────────────────────┤
│                       TIER 1: FEATURE COVERAGE                          │
│  24 Core Tests across 4 Features (Vector RAG, Multi-Agent Router,        │
│  Clinical Safety Guardrails, Multi-Tenant Data Isolation)               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Tier 1: Feature Coverage (Category-Partition Testing)
Covers all primary functional capabilities with at least 5 isolated test cases per feature (24 tests total):
- **Feature 1: Sports Science & Medical RAG Retrieval (`TC-RAG-01` to `TC-RAG-06`)**
  - Evaluates semantic search, cosine similarity metrics ($\ge 0.75$), metadata pre-filtering (`sport`, `pathology`, `rehab_phase`), and contraindication exclusion.
- **Feature 2: Multi-Agent Swarm Intent Routing (`TC-ROUT-01` to `TC-ROUT-06`)**
  - Evaluates intent classification into `WORKOUT_PLANNING`, `PHYSIO_REHAB`, `NUTRITION_RECOVERY`, `DATA_LOGGING`, `GENERAL_CHAT`, and compound intent dispatches.
- **Feature 3: Clinical Safety & Injury Guardrails (`TC-SAFE-01` to `TC-SAFE-06`)**
  - Verifies deterministic pre-flight and post-flight safety filters: Hard Rejection of contraindicated high-velocity sprints, lumbar spinal shear blocks, soft volume modifications for tendinopathies, autonomic fatigue overrides, cardiovascular emergency lockouts, and Low Energy Availability (LEA) interception.
- **Feature 4: Multi-Tenant Data & Profile Isolation (`TC-TEN-01` to `TC-TEN-06`)**
  - Verifies strict multi-tenant boundaries (`tenant_id` partitioning), preventing cross-tenant profile access, vector collection bleed, workout history leakage, API key misuse, mismatched webhook ingestion, and race conditions during concurrent check-ins.

### 2.2 Tier 2: Boundary & Corner Cases (Boundary Value Analysis)
Assesses system resilience under extreme and degraded conditions (7 tests):
- `TC-BND-01`: Empty / Whitespace Inputs (`""`, `"   "`, `"\n\t"`).
- `TC-BND-02`: Max Token / Context Overflow (>15,000 words payload).
- `TC-BND-03`: Contradictory Injury Claims (User chat claim vs. DB clinical record).
- `TC-BND-04`: Unknown / Hallucinated Exercises (Handling fabricated exercise nomenclature).
- `TC-BND-05`: Missing / Tampered Tenant Header (`X-Tenant-ID` validation failure).
- `TC-BND-06`: Malformed Third-Party Ingress Payloads (Corrupted JSON / schema mismatch).
- `TC-BND-07`: Ambiguous Multi-Intent Compound Query (Simultaneous Medical + Workout + Nutrition intents).

### 2.3 Tier 3: Cross-Feature Combinations (Pairwise & Integration Testing)
Evaluates state handoffs and complex multi-module interactions (4 tests):
- `TC-COMB-01`: **Injury Guard + Workout Generation**: Intercepts contraindicated exercises, queries RAG for evidence-based substitutes, and produces a safe periodized workout plan.
- `TC-COMB-02`: **Multi-Tenant Isolation + RAG Domain Partition**: Guarantees that different tenant sports domains (e.g. Trail Running vs. Powerlifting) receive tailored domain recovery protocols with zero cross-tenant contamination.
- `TC-COMB-03`: **Workout Parsing + ACWR Fatigue Calculation + Safety Recalibration**: Natural language workout extraction updates ATL/CTL; an acute spike ($\text{ACWR} \ge 1.5$) triggers an automatic safety downgrade of the next session.
- `TC-COMB-04`: **Nutrition Guidance + Caloric Calculation + Dietary Restrictions**: Computes exact macronutrient requirements (carbohydrates $g/\text{kg}$, sodium $\text{mg}/\text{hr}$) tailored to vegan constraints and muscle cramp prevention.

### 2.4 Tier 4: Real-World Coaching Scenarios (Realistic End-to-End Simulations)
Simulates end-to-end user journeys modeled on authentic athletic profiles (4 tests):
- **Scenario 1: Injured Elite 800m/Trail Runner (Carlos's Pathophysiological Profile)**: 23yo, 800m specialist with proximal hamstring tear recurrence requesting 100% hill sprints $\rightarrow$ Intercepted, blocked, and substituted with Askling HSR protocols and 75% submaximal flat strides.
- **Scenario 2: Marathon Runner Carb-Loading with Low-FODMAP Sensitivity**: 64kg athlete requesting race-week carb-loading and in-race fueling $\rightarrow$ Computes 512g CHO/day, low-FODMAP sources, race morning breakfast (130g CHO), and intra-race 60-75g CHO/hr hydrogel schedule.
- **Scenario 3: Overtrained Athlete with Autonomic Crash**: Morning biometrics indicate 50% HRV drop (34ms vs 68ms baseline) and sleep deprivation $\rightarrow$ Scheduled 5x2000m threshold intervals intercepted and replaced with 40min Zone 1 active recovery.
- **Scenario 4: Strength Athlete with Acute Lumbar Disc Protrusion (L4-L5)**: Athlete requests 1RM conventional deadlift test and heavy cleans $\rightarrow$ Hard block due to spinal shear forces; substituted with McGill Big 3 and high-handle Trap Bar / Belt Squats.

---

## 3. Feature Inventory & Traceability Matrix

| Feature ID | Feature Name | Mapped Test Cases | Target Subsystem | Milestone |
| :--- | :--- | :--- | :--- | :--- |
| **F-01** | Vector RAG Retrieval & Ingestion | `TC-RAG-01` .. `TC-RAG-06`, `TC-COMB-02` | `poc/rag/` | M1, M3 |
| **F-02** | Multi-Agent Swarm Intent Routing | `TC-ROUT-01` .. `TC-ROUT-06`, `TC-BND-07` | `poc/router/` | M1, M4 |
| **F-03** | Clinical Safety & Injury Guardrails | `TC-SAFE-01` .. `TC-SAFE-06`, `TC-COMB-01`, `TC-BND-03` | `poc/safety/` | M1, M4 |
| **F-04** | Multi-Tenant Data & Security Isolation | `TC-TEN-01` .. `TC-TEN-06`, `TC-BND-05`, `TC-COMB-02` | `poc/tenancy/` | M1, M3, M4 |
| **F-05** | Natural Language Workout Parser | `TC-ROUT-03`, `TC-COMB-03`, `TC-BND-04` | `poc/agents/` | M1, M4 |
| **F-06** | Biometric Load & ACWR Engine | `TC-SAFE-04`, `TC-COMB-03`, `Scenario 3` | `poc/models/athlete.py` | M1, M3 |
| **F-07** | Nutrition & Periodization Planner | `TC-RAG-04`, `TC-ROUT-06`, `TC-COMB-04`, `Scenario 2` | `poc/agents/` | M1, M4 |
| **F-08** | Clinical Red-Flag Triage | `TC-SAFE-05`, `TC-SAFE-06`, `Scenario 4` | `poc/safety/` | M1, M4 |

---

## 4. Test Architecture & Fixtures Design

The test suite is built on top of **Pytest 9.x** with zero external network or billing dependencies. It uses clean, deterministic fixtures defined in `tests/conftest.py`:

1. **`knowledge_corpus`**: Pre-seeded domain sports medicine and exercise physiology corpus containing clinically verified protocols (Hamstring HSR, Achilles Silbernagel, Patellar Spanish Squat, Marathon Burke CHO, Altitude Acclimatization, PAP Sprint, McGill Big 3).
2. **`mock_vector_store`**: In-memory vector store computing exact cosine similarity metrics and executing pre-filtering and contraindication pruning.
3. **`athlete_factory`**: Factory producing customized `AthleteProfile` instances across distinct tenants (`tenant_carlos`, `tenant_marathon`, `tenant_crossfit`, `tenant_beta`).
4. **`safety_guard`**: Clinical rule engine validating input queries and output responses against active injury profiles.
5. **`agent_router`**: Intent classifier and multi-agent dispatcher orchestrating domain handlers.
6. **`tenant_context_manager`**: Scoped multi-tenant context manager asserting security boundary enforcement.

---

## 5. Coverage Thresholds & Quality Gates

To achieve production certification, the Aegis Coach test suite enforces the following non-negotiable quality gates:

| Metric | Target Threshold | Rationale |
| :--- | :--- | :--- |
| **Test Suite Pass Rate** | **100% (39/39 Tests)** | Zero tolerance for failing tests in clinical sports intelligence. |
| **Safety Interception Rate** | **100% on Critical/High Risk** | Every contraindicated movement must be intercepted without exception. |
| **Cross-Tenant Data Leakage** | **0% (Zero cross-tenant bleed)** | Strict database and vector payload isolation across tenant IDs. |
| **RAG Top-3 Clinical Precision** | **$\ge 90\%$ relevance** | Chunks returned must match target anatomy and active rehabilitation phase. |
| **Execution Latency** | **$< 5.0$ seconds for full suite** | Fast, local, deterministic execution without network blocking. |

---

## 6. Test Runner Execution Commands

```powershell
# 1. Run the entire test suite with verbose output
python -m pytest tests/ -v

# 2. Run Tier 1 Feature Coverage tests only
python -m pytest tests/test_tier1_features.py -v

# 3. Run Tier 2 Boundary & Corner Case tests only
python -m pytest tests/test_tier2_boundaries.py -v

# 4. Run Tier 3 Cross-Feature Combination tests only
python -m pytest tests/test_tier3_combinations.py -v

# 5. Run Tier 4 Real-World Coaching Scenarios only
python -m pytest tests/test_tier4_scenarios.py -v

# 6. Run with short traceback and summary
python -m pytest tests/ --tb=short -q
```
