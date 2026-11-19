"""
Aegis Coach — Base Agent Abstract Interface
===========================================
Defines the standardized contract for all domain-specific micro-agents,
including execution telemetry, context memory management, and structured response building.
"""

from __future__ import annotations

import time
import abc
from typing import Dict, Any, Optional, List
from poc.models.athlete import AthleteProfile
from poc.models.conversation import UserQuery, AgentResponse, ExecutionTrace, DomainIntent, SafetyViolation


class BaseAgent(abc.ABC):
    """
    Abstract Base Class for specialized Aegis Coach domain agents.
    Enforces standardized execution traces, timing telemetry, and response schemas.
    """

    def __init__(self, agent_name: str, domain: DomainIntent):
        self.agent_name = agent_name
        self.domain = domain
        self._memory_context: Dict[str, Any] = {}

    @abc.abstractmethod
    def process(self, query: UserQuery, athlete: AthleteProfile) -> AgentResponse:
        """
        Executes domain logic for an incoming athlete query.

        Args:
            query: Typed user query with tenant and athlete identifiers.
            athlete: Complete physiological profile, injury status, and biometrics.

        Returns:
            AgentResponse: Standardized response object with markdown, structured data, and telemetry.
        """
        pass

    def _create_trace(
        self,
        query: UserQuery,
        secondary_intents: Optional[List[DomainIntent]] = None,
        rag_queries: Optional[List[str]] = None,
        rag_chunks_count: int = 0,
        safety_checks_count: int = 0,
        safety_violations: Optional[List[SafetyViolation]] = None,
        start_time: Optional[float] = None
    ) -> ExecutionTrace:
        """Helper to construct an ExecutionTrace with calculated latency."""
        latency = 0.0
        if start_time is not None:
            latency = round((time.time() - start_time) * 1000.0, 2)

        return ExecutionTrace(
            tenant_id=query.tenant_id,
            primary_intent=self.domain,
            secondary_intents=secondary_intents or [],
            agent_dispatched=self.agent_name,
            rag_queries_executed=rag_queries or [],
            rag_chunks_retrieved=rag_chunks_count,
            safety_checks_performed=safety_checks_count,
            safety_violations=safety_violations or [],
            latency_ms=latency,
            tokens_estimated=max(50, len(query.raw_text.split()) * 4)
        )

    def _build_response(
        self,
        query: UserQuery,
        athlete: AthleteProfile,
        message_markdown: str,
        structured_data: Optional[Dict[str, Any]] = None,
        suggested_actions: Optional[List[str]] = None,
        citations: Optional[List[Dict[str, str]]] = None,
        trace: Optional[ExecutionTrace] = None,
        is_safety_override: bool = False
    ) -> AgentResponse:
        """Helper to construct a typed AgentResponse."""
        if trace is None:
            trace = self._create_trace(query)

        return AgentResponse(
            query_id=query.query_id,
            tenant_id=query.tenant_id,
            athlete_id=athlete.athlete_id,
            primary_intent=self.domain,
            message_markdown=message_markdown,
            structured_data=structured_data,
            suggested_actions=suggested_actions or [],
            citations=citations or [],
            execution_trace=trace,
            is_safety_override=is_safety_override
        )
