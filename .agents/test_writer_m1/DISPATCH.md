## 2026-08-26T20:04:17Z
You are test_writer_m1 for the Aegis Coach project.
Your working directory is: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\test_writer_m1

MANDATORY FIRST STEP: Read the authoritative user request at:
c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\ORIGINAL_REQUEST.md

Read the project blueprint and survey findings at:
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\PROJECT.md
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\explorer_survey_3\handoff.md
- c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\explorer_survey_2\handoff.md

Your task: Implement Milestone M1 — E2E Testing Track (Opaque-Box Requirement-Driven Test Suite).
Files you own exclusively:
- `TEST_INFRA.md`
- `TEST_READY.md`
- `tests/conftest.py`
- `tests/test_tier1_features.py`
- `tests/test_tier2_boundaries.py`
- `tests/test_tier3_combinations.py`
- `tests/test_tier4_scenarios.py`

Requirements:
1. `TEST_INFRA.md`: Document the test philosophy (Opaque-box, requirement-driven, 4-tier hierarchy: Category-Partition, BVA, Pairwise, Real-world workloads), feature inventory, test architecture, and coverage thresholds.
2. Implement 4-tier Pytest test suite in `tests/`:
   - **Tier 1: Feature Coverage (>=5 test cases per feature, total 24 tests)**:
     * Feature 1: Vector RAG Retrieval (`TC-RAG-01` to `TC-RAG-06`): Hamstring tendinopathy, Achilles load management, Patellar isometrics, Marathon carb loading, Altitude hydration, PAP 800m.
     * Feature 2: Multi-Agent Intent Routing (`TC-ROUT-01` to `TC-ROUT-06`): Medical injury, Workout planning, Natural language workout log, General chat, Compound query, Nutrition inquiry.
     * Feature 3: Clinical Safety & Injury Guardrails (`TC-SAFE-01` to `TC-SAFE-06`): High-risk sprint with hamstring tear (Hard Reject), Deadlift with lumbar herniation (Hard Reject), Patellar volume flare-up, Overtraining/Autonomic crash, Cardiovascular red flag emergency, Low energy availability (LEA).
     * Feature 4: Multi-Tenant Data Isolation (`TC-TEN-01` to `TC-TEN-06`): Cross-tenant profile rejection, Vector store payload isolation, Workout history isolation, API key scoping, Mismatched webhook rejection, Concurrent multi-tenant check-in isolation.
   - **Tier 2: Boundary & Corner Cases (7 tests)**:
     * `TC-BND-01`: Empty / Whitespace inputs.
     * `TC-BND-02`: Max token / Large payload handling.
     * `TC-BND-03`: Contradictory injury claims (user chat vs clinical DB record).
     * `TC-BND-04`: Unknown / Hallucinated exercise handling.
     * `TC-BND-05`: Missing / Tampered tenant header.
     * `TC-BND-06`: Malformed payload handling.
     * `TC-BND-07`: Ambiguous multi-intent parsing.
   - **Tier 3: Cross-Feature Combinations (4 tests)**:
     * `TC-COMB-01`: Injury Guard + Workout Generation.
     * `TC-COMB-02`: Multi-Tenant Isolation + RAG Domain Partition.
     * `TC-COMB-03`: Workout Parsing + ACWR Fatigue Calculation + Safety Recalibration.
     * `TC-COMB-04`: Nutrition Guidance + Caloric Calculation + Dietary Restrictions (Vegan).
   - **Tier 4: Real-World Coaching Scenarios (4 realistic end-to-end simulations)**:
     * Scenario 1: Injured elite 800m/trail runner (Carlos's profile) requesting 100% hill sprints -> Intercepted & substituted with Askling HSR / tempo.
     * Scenario 2: Marathon runner carb-loading & race fueling with low-FODMAP gastrointestinal sensitivity.
     * Scenario 3: Overtrained athlete with morning HRV autonomic crash -> Workout canceled & replaced with Zone 1 active recovery.
     * Scenario 4: CrossFit athlete with acute L4-L5 disc protrusion requesting 1RM conventional deadlift -> Intercepted & replaced with McGill Big 3 & neutral spine strength.
3. `TEST_READY.md`: Signal that the E2E test suite is published and ready, including the exact test runner commands and coverage checklist.
