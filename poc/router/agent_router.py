"""
Aegis Coach — Multi-Agent Router & Intent Classifier
=====================================================
Classifies athlete intent into specialized domains (Medical/Rehab, Workout Planning,
Nutrition/Fueling, Data Logging, General Chat), coordinates pre-flight/post-flight
clinical safety guardrails, and manages agent swarm dispatching.
"""

from __future__ import annotations

import time
import re
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

from poc.models.athlete import AthleteProfile
from poc.models.conversation import (
    DomainIntent,
    UserQuery,
    AgentResponse,
    ExecutionTrace,
    SafetyViolation,
    RiskLevel
)
from poc.safety.injury_guard import InjuryGuard, SafetyCheckResult
from poc.rag.vector_store import VectorStore
from poc.rag.retriever import HybridRetriever
from poc.agents.medical_agent import MedicalAgent
from poc.agents.planner_agent import PlannerAgent
from poc.agents.nutrition_agent import NutritionAgent
from poc.agents.data_entry_agent import DataEntryAgent
from poc.agents.general_agent import GeneralAgent


class RoutingDecision(BaseModel):
    """Structured decision produced by the hierarchical intent classifier."""

    primary_intent: DomainIntent = Field(default=DomainIntent.GENERAL_CHAT)
    secondary_intents: List[DomainIntent] = Field(default_factory=list)
    extracted_entities: Dict[str, Any] = Field(default_factory=dict)
    requires_safety_override: bool = Field(default=False)
    rationale: str = Field(default="")


class AgentRouter:
    """
    Central Multi-Agent Swarm Orchestrator.
    Evaluates incoming queries, enforces pre-flight & post-flight clinical safety checks,
    and dispatches execution to domain micro-agents.
    """

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        retriever: Optional[HybridRetriever] = None,
        safety_guard: Optional[InjuryGuard] = None
    ):
        self.vector_store = vector_store or VectorStore()
        self.retriever = retriever or HybridRetriever(vector_store=self.vector_store)
        self.safety_guard = safety_guard or InjuryGuard()

        # Initialize specialized domain micro-agents
        self.medical_agent = MedicalAgent(retriever=self.retriever)
        self.planner_agent = PlannerAgent()
        self.nutrition_agent = NutritionAgent()
        self.data_entry_agent = DataEntryAgent()
        self.general_agent = GeneralAgent()

    def classify_intent(self, raw_text: str) -> RoutingDecision:
        """
        Classifies athlete input text into primary and secondary domains and extracts entity slots.
        """
        text = raw_text.lower().strip()

        # 1. Handle empty / whitespace input
        if not text:
            return RoutingDecision(
                primary_intent=DomainIntent.GENERAL_CHAT,
                rationale="Empty payload routed to GeneralAgent clarification."
            )

        # 2. Heuristic domain keyword patterns
        is_medical = bool(re.search(
            r"\b(dolor|molestia|pinchazo|isquio|isquiotibial|aquiles|rodilla|tend[oó]n|lesi[oó]n|rehabilitaci[oó]n|inflamaci[oó]n|s[oó]leo|gemelo|hernia|disc|opresi[oó]n|mareo|duele|duelen|contractura|sobrecarga|rotura|fisio|fisioterapia|vas|articulaci[oó]n|inflamado)\b",
            text
        ))

        is_planning = bool(re.search(
            r"\b(planif[ií]came|microciclo|entreno|entrenar|semana|series|cuestas|sesi[oó]n|tirada|kilometros|km|1rm|deadlift|wod|threshold|intervalos|quiero hacer|\d+x\d+|mancuernas|pesas|ejercicio|ejercicios|rutina|fuerza|lunges|sentadillas|volumen|ritmo objetivo|que hago hoy|que me toca hoy)\b",
            text
        ))

        is_logging = bool(re.search(
            r"\b(hoy hice|corr[ií]|hice \d+|complet[eé]|ppm|rpe \d+|ritmo \d+:\d+|desnivel|pulsaciones|duraci[oó]n|entren[eé]|acabo de terminar|sesion completada)\b",
            text
        ))

        is_nutrition = bool(re.search(
            r"\b(carbohidratos|hidratos|comer|carga|geles|nutrici[oó]n|calor[ií]as|kcal|suplementaci[oó]n|prote[ií]na|sodio|agua|hidrataci[oó]n|fodmap|vegano|arroz|comida|dieta|como hoy|que comer|post-entreno|col[aá]geno|electrolitos)\b",
            text
        ))

        # 3. Intent Priority & Arbitration
        detected_intents: List[DomainIntent] = []
        if is_logging:
            detected_intents.append(DomainIntent.DATA_LOGGING)
        if is_medical:
            detected_intents.append(DomainIntent.PHYSIO_REHAB)
        if is_planning:
            if DomainIntent.WORKOUT_PLANNING not in detected_intents:
                detected_intents.append(DomainIntent.WORKOUT_PLANNING)
        if is_nutrition:
            detected_intents.append(DomainIntent.NUTRITION_RECOVERY)

        if not detected_intents:
            primary = DomainIntent.GENERAL_CHAT
            secondary = []
        else:
            primary = detected_intents[0]
            secondary = detected_intents[1:]

        # 4. Entity Extraction
        entities: Dict[str, Any] = {}

        dist_match = re.search(r"(\d+(?:[.,]\d+)?)\s*km", text)
        if dist_match:
            entities["distance_km"] = float(dist_match.group(1).replace(",", "."))

        pace_match = re.search(r"(\d+:\d+)\s*/?km", text)
        if pace_match:
            entities["pace_avg"] = f"{pace_match.group(1)}/km"

        hr_match = re.search(r"(\d{2,3})\s*(?:ppm|bpm)", text)
        if hr_match:
            entities["avg_heart_rate"] = int(hr_match.group(1))

        rpe_match = re.search(r"rpe\s*(\d{1,2})", text)
        if rpe_match:
            entities["rpe"] = int(rpe_match.group(1))

        vert_match = re.search(r"(\d+)\s*(?:m|metros)?\s*(?:de\s+desnivel|vert|\+|d\+)", text)
        if vert_match:
            entities["elevation_gain_m"] = int(vert_match.group(1))

        pain_match = re.search(r"(\d{1,2})\s*/\s*10", text)
        if pain_match:
            entities["pain_score"] = int(pain_match.group(1))

        return RoutingDecision(
            primary_intent=primary,
            secondary_intents=secondary,
            extracted_entities=entities,
            rationale=f"Classified as primary '{primary.value}' with {len(secondary)} secondary intent(s)."
        )

    def route_and_execute(self, query: UserQuery, athlete: AthleteProfile) -> AgentResponse:
        """
        Main multi-agent swarm execution pipeline:
        1. Classify intent.
        2. Pre-flight SafetyGuard validation (blocking acute contraindications and red flags).
        3. Dispatch to specialized domain agent.
        4. Post-flight SafetyGuard interception of agent response.
        5. Package unified AgentResponse with comprehensive telemetry trace.
        """
        start_time = time.time()
        decision = self.classify_intent(query.raw_text)

        # ----------------------------------------------------------------------
        # Step 1: Pre-Flight Safety Validation
        # ----------------------------------------------------------------------
        safety_check = self.safety_guard.check_query_safety(query.raw_text, athlete)

        # Handle empty/whitespace edge case
        if not query.raw_text.strip():
            trace = ExecutionTrace(
                tenant_id=query.tenant_id,
                primary_intent=DomainIntent.GENERAL_CHAT,
                agent_dispatched="GeneralAgent",
                safety_checks_performed=1,
                latency_ms=round((time.time() - start_time) * 1000.0, 2)
            )
            return self.general_agent.process(query, athlete)

        # Pre-Flight Safety Interception (Hard Stop / Override)
        if not safety_check.is_safe:
            primary_violation = safety_check.violations[0] if safety_check.violations else None
            trace = ExecutionTrace(
                tenant_id=query.tenant_id,
                primary_intent=decision.primary_intent,
                secondary_intents=decision.secondary_intents,
                agent_dispatched="SafetyGuardrailInterceptor",
                safety_checks_performed=1,
                safety_violations=safety_check.violations,
                latency_ms=round((time.time() - start_time) * 1000.0, 2)
            )

            # Format user-facing safety message
            if safety_check.action_taken == "EMERGENCY_LOCKOUT":
                msg = safety_check.safe_alternative or "⚠️ **Alerta Médica**: Consulta médica urgente requerida."
            else:
                rationale_text = primary_violation.rationale if primary_violation else "Prescripción no recomendada por biomecánica de la lesión."
                safe_alt_text = safety_check.safe_alternative or "Trabajo isométrico controlado en rango no doloroso."
                msg = (
                    f"⚠️ **Aviso de Seguridad Biomecánica**: {rationale_text}\n\n"
                    f"**Propuesta Segura Alternativa**: {safe_alt_text}"
                )

            return AgentResponse(
                query_id=query.query_id,
                tenant_id=query.tenant_id,
                athlete_id=athlete.athlete_id,
                primary_intent=decision.primary_intent,
                message_markdown=msg,
                structured_data={"safety_check": safety_check.model_dump()},
                suggested_actions=["Ver ejercicios seguros", "Consultar fisioterapeuta"],
                execution_trace=trace,
                is_safety_override=True
            )

        # ----------------------------------------------------------------------
        # Step 2: Domain Agent Swarm Dispatch
        # ----------------------------------------------------------------------
        if decision.primary_intent == DomainIntent.DATA_LOGGING:
            response = self.data_entry_agent.process(query, athlete)
        elif decision.primary_intent == DomainIntent.PHYSIO_REHAB:
            response = self.medical_agent.process(query, athlete)
        elif decision.primary_intent == DomainIntent.WORKOUT_PLANNING:
            response = self.planner_agent.process(query, athlete)
        elif decision.primary_intent == DomainIntent.NUTRITION_RECOVERY:
            response = self.nutrition_agent.process(query, athlete)
        else:
            response = self.general_agent.process(query, athlete)

        # ----------------------------------------------------------------------
        # Step 3: Post-Flight Response Sanitization & Guardrail Check
        # ----------------------------------------------------------------------
        sanitized_markdown, post_check = self.safety_guard.intercept_agent_response(
            response.message_markdown,
            athlete
        )

        response.message_markdown = sanitized_markdown
        if not post_check.is_safe:
            response.is_safety_override = True
            response.execution_trace.safety_violations.extend(post_check.violations)

        # Update trace with routing metadata
        response.execution_trace.secondary_intents = decision.secondary_intents
        response.execution_trace.latency_ms = round((time.time() - start_time) * 1000.0, 2)

        return response
