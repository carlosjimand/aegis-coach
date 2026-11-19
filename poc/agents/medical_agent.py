"""
Aegis Coach — Clinical Physiotherapist & Rehabilitation Agent
=============================================================
Specializes in sports injury assessment, pain monitoring (VAS 0-10),
biomechanical loading protocols, and Vector RAG scientific evidence retrieval.
"""

from __future__ import annotations

import time
import re
from typing import Dict, Any, Optional, List, Tuple
from poc.agents.base_agent import BaseAgent
from poc.models.athlete import AthleteProfile, RehabPhase
from poc.models.conversation import UserQuery, AgentResponse, DomainIntent
from poc.rag.retriever import HybridRetriever
from poc.rag.vector_store import VectorStore
from poc.safety.rules import evaluate_pain_vas, get_safe_alternatives_for_pathology


class MedicalAgent(BaseAgent):
    """
    Clinical Physio Agent backed by Hybrid Sports Science RAG.
    Applies evidence-based return-to-sport protocols (Askling, Silbernagel, Alfredson, McGill, Rio).
    """

    def __init__(self, retriever: Optional[HybridRetriever] = None, vector_store: Optional[VectorStore] = None):
        super().__init__(agent_name="ClinicalPhysioAgent", domain=DomainIntent.PHYSIO_REHAB)
        if retriever:
            self.retriever = retriever
        else:
            self.retriever = HybridRetriever(vector_store=vector_store)

    def process(self, query: UserQuery, athlete: AthleteProfile) -> AgentResponse:
        start_time = time.time()
        text = query.raw_text.strip()

        # 1. Extract reported pain score if present (VAS 0-10)
        pain_score = None
        pain_match = re.search(r"(\d{1,2})\s*/\s*10", text)
        if pain_match:
            pain_score = int(pain_match.group(1))
        elif athlete.active_injuries:
            pain_score = athlete.active_injuries[0].current_pain_score

        pain_eval = evaluate_pain_vas(pain_score if pain_score is not None else 0)

        # 2. Retrieve relevant sports science literature via Hybrid RAG
        rag_results = self.retriever.retrieve(
            query=text,
            athlete=athlete,
            top_k=3,
            tenant_id=query.tenant_id
        )

        citations_list: List[Dict[str, str]] = []
        for chunk, score in rag_results:
            if chunk.citations:
                citations_list.extend(chunk.citations)
            else:
                citations_list.append({
                    "title": chunk.title,
                    "evidence_level": chunk.evidence_level,
                    "source": "Aegis Sports Science Knowledge Base"
                })

        # 3. Synthesize Evidence-Based Clinical Response
        lines: List[str] = []
        lines.append("### 🩺 Evaluación Fisioterapéutica y Plan de Readaptación")
        lines.append("")

        if pain_score is not None:
            lines.append(f"**Nivel de dolor reportado**: `{pain_score}/10` (Escala Visual Analógica - VAS)")
            lines.append(f"- **Diagnóstico de carga**: *{pain_eval['category']}*")
            lines.append(f"- **Criterio clínico**: {pain_eval['guideline']}")
            lines.append("")

        # Mention athlete active injuries
        if athlete.active_injuries:
            injury = athlete.active_injuries[0]
            lines.append(f"**Patología activa**: {injury.injury_name} (Fase: `{injury.rehab_phase.value}`)")
            lines.append("")

        # RAG Context & Recommended Protocol
        if rag_results:
            top_chunk, top_score = rag_results[0]
            lines.append(f"#### 📋 Protocolo Clínico Basado en Evidencia: *{top_chunk.title}*")
            lines.append(f"*(Nivel de evidencia: {top_chunk.evidence_level} | Relevancia: {top_score:.2f})*")
            lines.append("")
            lines.append(top_chunk.content)
            lines.append("")

            if top_chunk.contraindications:
                lines.append(f"⚠️ **Movimientos estrictamente contraindicados en esta fase**: {', '.join(top_chunk.contraindications)}")
                lines.append("")
        else:
            # Fallback to deterministic safe alternatives from rules
            alts = get_safe_alternatives_for_pathology(athlete.active_injuries[0].anatomical_region if athlete.active_injuries else "general")
            lines.append("#### 📋 Protocolo de Protección e Isometría")
            for alt in alts:
                lines.append(f"- {alt}")
            lines.append("")

        lines.append("---")
        lines.append("**Regla de las 24 horas**: Cualquier molestia generada debe disiparse completamente antes de 24h. Si el dolor persiste o supera 3/10 al día siguiente, reduciremos el volumen un 30%.")

        message_markdown = "\n".join(lines)

        suggested_actions = [
            "Registrar dolor post-sesión",
            "Ver técnica de isométricos",
            "Ajustar entreno de mañana"
        ]

        structured_data = {
            "reported_pain_vas": pain_score,
            "pain_evaluation": pain_eval,
            "rehab_phase": athlete.active_injuries[0].rehab_phase.value if athlete.active_injuries else RehabPhase.MAINTENANCE.value,
            "retrieved_protocols": [chunk.chunk_id for chunk, _ in rag_results]
        }

        trace = self._create_trace(
            query=query,
            rag_queries=[text],
            rag_chunks_count=len(rag_results),
            safety_checks_count=1,
            start_time=start_time
        )

        return self._build_response(
            query=query,
            athlete=athlete,
            message_markdown=message_markdown,
            structured_data=structured_data,
            suggested_actions=suggested_actions,
            citations=citations_list,
            trace=trace
        )
