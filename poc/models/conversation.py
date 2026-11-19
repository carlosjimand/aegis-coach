"""
Aegis Coach — Conversation & Multi-Agent Communication Models
=============================================================
Defines typed models for athlete query intake, domain intent classification,
clinical safety violation interception records, execution traces, and structured agent responses.
"""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DomainIntent(str, Enum):
    """Specialized agent domains for intent classification and routing."""
    WORKOUT_PLANNING = "WORKOUT_PLANNING"      # Workout generation, periodization, Intervals.icu updates
    PHYSIO_REHAB = "PHYSIO_REHAB"              # Pain inquiry, injury rehabilitation, RAG protocols
    NUTRITION_RECOVERY = "NUTRITION_RECOVERY"  # Nutrition, fueling, hydration, supplement strategies
    DATA_LOGGING = "DATA_LOGGING"              # Unstructured voice/text workout parsing & metric storage
    GENERAL_CHAT = "GENERAL_CHAT"              # Morning check-ins, motivation, athletic counseling


class RiskLevel(str, Enum):
    """Clinical risk classification for intercepted queries or workout recommendations."""
    CRITICAL = "CRITICAL"  # Acute medical emergency (chest pain, syncope, severe trauma) -> Doctor Referral
    HIGH = "HIGH"          # Direct contraindication to active injury (e.g. 100% sprints on acute hamstring)
    MODERATE = "MODERATE"  # Elevated volume/fatigue spike (ACWR > 1.5) -> Load modification required
    LOW = "LOW"            # Mild soreness, minor form advice -> Information only


class UserQuery(BaseModel):
    """Incoming user message payload from Telegram, WebApp, or API."""

    query_id: str = Field(default_factory=lambda: f"qry_{uuid.uuid4().hex[:10]}")
    tenant_id: str = Field(..., description="Tenant ID enforcing isolation.")
    athlete_id: str = Field(..., description="Athlete ID submitting query.")
    timestamp: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        description="ISO UTC timestamp of query."
    )
    raw_text: str = Field(..., description="Raw text or transcribed audio input.")
    context: Dict[str, Any] = Field(default_factory=dict, description="Session state, previous message history, etc.")


class SafetyViolation(BaseModel):
    """Details of a clinical or biomechanical safety rule violation intercepted by SafetyGuard."""

    violation_id: str = Field(default_factory=lambda: f"viol_{uuid.uuid4().hex[:8]}")
    violation_code: str = Field(..., description="Standardized error code (e.g. 'CONTRAINDICATION_HAMSTRING_MAX_SPRINT').")
    rule_name: str = Field(..., description="Human-readable rule name.")
    risk_level: RiskLevel = Field(default=RiskLevel.HIGH)
    blocked_content: str = Field(..., description="The dangerous exercise or advice that was intercepted.")
    safe_alternative: str = Field(..., description="The clinically approved replacement protocol.")
    rationale: str = Field(..., description="Biomechanical and physiological justification.")
    escalation_required: bool = Field(default=False, description="Whether immediate medical physician referral is triggered.")


class ExecutionTrace(BaseModel):
    """Telemetry, routing path, and performance metrics for a single agent transaction."""

    trace_id: str = Field(default_factory=lambda: f"trc_{uuid.uuid4().hex[:10]}")
    tenant_id: str = Field(..., description="Tenant ID context.")
    primary_intent: DomainIntent = Field(default=DomainIntent.GENERAL_CHAT)
    secondary_intents: List[DomainIntent] = Field(default_factory=list)
    agent_dispatched: str = Field(default="RouterAgent")
    rag_queries_executed: List[str] = Field(default_factory=list)
    rag_chunks_retrieved: int = Field(default=0)
    safety_checks_performed: int = Field(default=0)
    safety_violations: List[SafetyViolation] = Field(default_factory=list)
    latency_ms: float = Field(default=0.0)
    tokens_estimated: int = Field(default=0)


class AgentResponse(BaseModel):
    """Unified response object returned to the user interface layer."""

    response_id: str = Field(default_factory=lambda: f"resp_{uuid.uuid4().hex[:10]}")
    query_id: str = Field(..., description="Correlation ID matching the UserQuery.")
    tenant_id: str = Field(..., description="Tenant ID.")
    athlete_id: str = Field(..., description="Athlete ID.")
    primary_intent: DomainIntent = Field(...)
    message_markdown: str = Field(..., description="User-facing response in clean, empathetic Markdown.")
    structured_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional structured JSON (e.g. parsed workout metrics, workout calendar payload)."
    )
    suggested_actions: List[str] = Field(
        default_factory=list,
        description="Quick-reply chips or action buttons for Telegram/WebApp."
    )
    citations: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of scientific paper citations supporting this recommendation."
    )
    execution_trace: ExecutionTrace = Field(...)
    is_safety_override: bool = Field(
        default=False,
        description="True if dangerous content was blocked and replaced with safe protocols."
    )
