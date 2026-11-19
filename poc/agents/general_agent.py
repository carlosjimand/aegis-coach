"""
Aegis Coach — General Check-in, Motivation & Counseling Agent
============================================================
Handles athlete morning check-ins, motivation, adherence tracking,
habit formation, and conversational clarification.
"""

from __future__ import annotations

import time
import re
from typing import Dict, Any, Optional, List
from poc.agents.base_agent import BaseAgent
from poc.models.athlete import AthleteProfile
from poc.models.conversation import UserQuery, AgentResponse, DomainIntent


class GeneralAgent(BaseAgent):
    """
    General Conversational & Habit Adherence Agent.
    Maintains an empathetic, sports-science grounded tone for daily coaching interactions.
    """

    def __init__(self):
        super().__init__(agent_name="GeneralCoachingAgent", domain=DomainIntent.GENERAL_CHAT)

    def process(self, query: UserQuery, athlete: AthleteProfile) -> AgentResponse:
        start_time = time.time()
        text = query.raw_text.strip()
        norm_text = text.lower()

        # 1. Empty or whitespace prompt handling
        if not text:
            msg = f"¡Hola {athlete.name}! No he recibido ningún mensaje. ¿En qué puedo ayudarte hoy con tu entrenamiento o recuperación?"
            suggested_actions = ["Ver plan de hoy", "Registrar entreno", "Consultar molestia"]
            trace = self._create_trace(query=query, start_time=start_time)
            return self._build_response(
                query=query,
                athlete=athlete,
                message_markdown=msg,
                suggested_actions=suggested_actions,
                trace=trace
            )

        # 2. Morning Check-in / Readiness greeting
        is_greeting = bool(re.search(r"\b(buenos d[ií]as|check-in|hola|qu[eé] tal|c[oó]mo estamos|buenas)\b", norm_text))
        is_motivation = bool(re.search(r"\b(motiva|desmotiva|cansad|pereza|duro|cuesta|desánimo)\b", norm_text))

        if is_greeting:
            hrv_status = "Óptimo"
            if athlete.biometrics and athlete.biometrics.daily_metrics:
                latest = athlete.biometrics.daily_metrics[-1]
                if latest.is_autonomic_crash():
                    hrv_status = "Fatiga Elevada (Recuperación activa recomendada)"
                elif latest.hrv_drop_percentage() > 15.0:
                    hrv_status = "Ligeramente fatigado"

            msg = (
                f"¡Buenos días, {athlete.name}! 🌅\n\n"
                f"Tu estado fisiológico matutino:\n"
                f"- **Disciplina**: `{athlete.primary_discipline.value}`\n"
                f"- **Estado Autonómico**: `{hrv_status}`\n"
                f"- **Lesiones activas**: `{len(athlete.active_injuries)} activas`\n\n"
                f"¿Listo para la sesión de hoy o tienes alguna molestia que debamos revisar antes de arrancar?"
            )
            suggested_actions = ["Ver sesión de hoy", "Registrar dolor", "Ajustar descanso"]

        # 3. Motivation / Mindset / Consistency
        elif is_motivation:
            msg = (
                f"Recuerda {athlete.name}: el progreso atlético de alto nivel no se construye en los días en que todo sale perfecto, "
                f"sino en la consistencia inteligente. Escuchar a tu cuerpo cuando te pide bajar la intensidad no es rendirse, "
                f"es optimizar la supercompensación. ¡Vamos paso a paso!"
            )
            suggested_actions = ["Ajustar a sesión suave", "Ver progresión mensual", "Descansar hoy"]

        # 4. General fallback response
        else:
            msg = (
                f"¡Entendido, {athlete.name}! Estoy a tu disposición para planificar entrenamientos, "
                f"adaptar cargas por molestias musculares, calcular tu nutrición de carrera o registrar tus sesiones diarias. "
                f"¿En qué área nos enfocamos ahora?"
            )
            suggested_actions = ["Planificar entreno", "Registrar sesión", "Nutrición deportiva", "Revisión física"]

        trace = self._create_trace(query=query, start_time=start_time)
        return self._build_response(
            query=query,
            athlete=athlete,
            message_markdown=msg,
            suggested_actions=suggested_actions,
            trace=trace
        )
