"""
Aegis Coach — Exercise Physiologist & Periodized Workout Planner Agent
=====================================================================
Generates polarized (80/20) and periodized training sessions, calculates Banister TRIMP/ACWR,
checks for autonomic fatigue crashes, and prevents molecular AMPK/mTOR interference.
"""

from __future__ import annotations

import time
import re
from typing import Dict, Any, Optional, List
from poc.agents.base_agent import BaseAgent
from poc.models.athlete import AthleteProfile, SportDiscipline, ActivityType, RehabPhase
from poc.models.conversation import UserQuery, AgentResponse, DomainIntent


class PlannerAgent(BaseAgent):
    """
    Exercise Physiologist & Workout Planning Agent.
    Synthesizes physiological state, recovery metrics, and periodization targets into structured workouts.
    """

    def __init__(self):
        super().__init__(agent_name="ExercisePhysiologistPlanner", domain=DomainIntent.WORKOUT_PLANNING)

    def process(self, query: UserQuery, athlete: AthleteProfile) -> AgentResponse:
        start_time = time.time()
        text = query.raw_text.strip()
        norm_text = text.lower()

        # 1. Evaluate Autonomic Fatigue & Recovery Status
        is_crashed = False
        hrv_drop = 0.0
        if athlete.biometrics and athlete.biometrics.daily_metrics:
            latest_metric = athlete.biometrics.daily_metrics[-1]
            hrv_drop = round(latest_metric.hrv_drop_percentage(), 1)
            is_crashed = latest_metric.is_autonomic_crash()

        # 2. Evaluate ACWR & Chronic Workload if workout history exists
        trimp_history = [
            w.trimp_score for w in athlete.biometrics.daily_workouts if w.trimp_score is not None
        ] if athlete.biometrics else []

        ctl = athlete.biometrics.calculate_ctl(trimp_history) if athlete.biometrics else 45.0
        atl = athlete.biometrics.calculate_atl(trimp_history) if athlete.biometrics else 50.0
        acwr_info = athlete.biometrics.get_acwr_risk_assessment(atl, ctl) if athlete.biometrics else {
            "acwr": 1.10,
            "zone": "SWEET_SPOT",
            "risk": "OPTIMAL_LOAD_LOW_INJURY_RISK",
            "recommendation": "Maintain progressive overload."
        }

        # 3. Handle Autonomic Crash State (Downgrade to Zone 1 Active Recovery)
        if is_crashed:
            markdown = (
                f"### ⚠️ Modificación por Fatiga Autonómica (Crash HRV -{hrv_drop}%)\n\n"
                f"Tus métricas de hoy indican una caída significativa en la variabilidad cardíaca rMSSD y déficit de recuperación. "
                f"Para evitar el sobreentrenamiento y proteger el sistema inmune, sustituimos el entrenamiento de alta intensidad por una sesión regenerativa.\n\n"
                f"#### 🚴 Sesión Regenerativa Prescrita:\n"
                f"- **Calentamiento**: 5 min de movilidad articular suave y respiración diafragmática.\n"
                f"- **Parte Principal**: 35-40 minutos de rodillo o bicicleta estática en **Zona 1** (FC < 120 ppm / RPE 2-3) con cadencia fluida (85-90 rpm).\n"
                f"- **Vuelta a la calma**: 10 min de estiramientos pasivos y descompresión espinal.\n"
                f"- **Objetivo Fisiológico**: Estimular el aclaramiento de lactato y restaurar el tono parasimpático sin generar estrés metabólico adicional."
            )
            structured_data = {
                "activity_type": ActivityType.RECOVERY_RUN.value,
                "target_duration_minutes": 40.0,
                "target_rpe": 2,
                "target_heart_rate_zone": "ZONE_1",
                "is_autonomic_override": True,
                "acwr_assessment": acwr_info
            }
            suggested_actions = ["Confirmar descanso activo", "Ver ejercicios de movilidad", "Registrar sueño de hoy"]
            trace = self._create_trace(query=query, start_time=start_time)
            return self._build_response(
                query=query,
                athlete=athlete,
                message_markdown=markdown,
                structured_data=structured_data,
                suggested_actions=suggested_actions,
                trace=trace,
                is_safety_override=False
            )

        # 4. Discipline-Specific Periodized Workout Generation
        discipline = athlete.primary_discipline
        lines: List[str] = []
        structured_data: Dict[str, Any] = {}

        has_hamstring_injury = any("hamstring" in inj.anatomical_region.lower() for inj in athlete.active_injuries)

        if discipline == SportDiscipline.TRACK_800M:
            if has_hamstring_injury:
                # Subacute running session: Flat progressive submaximal strides + HSR
                lines.append("### 🏃‍♂️ Planificación de Entrenamiento — Pista & Readaptación (800m)")
                lines.append(f"**Atleta**: {athlete.name} | **Fase**: Subaguda / Progresión de Velocidad Controlada")
                lines.append(f"**Carga Crónica (CTL)**: {ctl:.1f} | **Ratio ACWR**: {acwr_info['acwr']:.2f} ({acwr_info['zone']})")
                lines.append("")
                lines.append("#### 1. Calentamiento Dinámico (20 min)")
                lines.append("- 10 min carrera continua suave Z1 (ritmo 5:15/km).")
                lines.append("- Movilidad dinámica de cadera: leg swings frontales y laterales (2x10 cada pierna).")
                lines.append("- Isométricos de activación: Puentes de glúteo bipodales con pausa de 5s (3x8).")
                lines.append("- 3 progresivos controlados en recta llana (70m al 70-75% de velocidad máxima, sin salida explosiva).")
                lines.append("")
                lines.append("#### 2. Bloque Principal: Intervalos Subumbrales en Llano (30 min)")
                lines.append("- **4 x 800m** a ritmo umbral controlado (`3:30/km`, RPE 6-7).")
                lines.append("- **Recuperación**: 2 min de trote suave entre repeticiones.")
                lines.append("- *Nota biomecánica*: Mantén zancada compacta, cadencia alta (180 spm) y evita hiperextensión de rodilla en el impacto.")
                lines.append("")
                lines.append("#### 3. Vuelta a la Calma & Readaptación Neuromuscular (15 min)")
                lines.append("- 5 min trote regenerativo descalzo en césped.")
                lines.append("- Protocolo Askling L: *The Extender* (2x10 con control) + *The Diver* (2x6).")
                lines.append("")
                structured_data = {
                    "activity_type": ActivityType.TRACK_INTERVALS.value,
                    "target_duration_minutes": 65.0,
                    "target_distance_km": 8.5,
                    "target_rpe": 6,
                    "target_pace": "3:30/km",
                    "target_heart_rate_zone": "ZONE_3_4",
                    "acwr_assessment": acwr_info
                }
            else:
                # Full 800m track session
                lines.append("### 🏃‍♂️ Planificación de Entrenamiento — Series de Pista (800m)")
                lines.append(f"**Atleta**: {athlete.name} | **Objetivo**: Tolerancia al Lactato & Ritmo Específico")
                lines.append("")
                lines.append("#### 1. Calentamiento (20 min)")
                lines.append("- 12 min CC Z2 + técnica de carrera (skipping, talones, impulsiones) + 4 rectas progresivas.")
                lines.append("#### 2. Bloque Principal: Series Específicas")
                lines.append("- **2 bloques de (3 x 400m)** a ritmo de 800m objetivo (`1:02 - 1:04`), rec 90s entre series, 4 min entre bloques.")
                lines.append("#### 3. Vuelta a la Calma (10 min)")
                lines.append("- 10 min trote suave + movilidad articular.")
                structured_data = {
                    "activity_type": ActivityType.TRACK_INTERVALS.value,
                    "target_duration_minutes": 55.0,
                    "target_distance_km": 7.0,
                    "target_rpe": 8,
                    "acwr_assessment": acwr_info
                }

        elif discipline == SportDiscipline.TRAIL_RUNNING:
            lines.append("### ⛰️ Planificación de Entrenamiento — Trail Running & Cuestas")
            lines.append(f"**Atleta**: {athlete.name} | **Objetivo**: Eficiencia Aeróbica y Desnivel Positivo")
            lines.append("")
            lines.append("#### 1. Calentamiento (15 min)")
            lines.append("- 15 min CC llana Z1-Z2 activando tobillos y gemelos.")
            lines.append("#### 2. Bloque Principal: Subidas en Umbral Aeróbico")
            lines.append("- **10 km por montaña** acumulando **350-450m D+** continuos en subida progresiva.")
            lines.append("- En subidas pronunciadas (>12%): caminar con zancada rítmica apoyando manos en muslos (power hiking).")
            lines.append("- En bajadas: pisada técnica y relajada, evitando impactos de frenado brusco con el talón.")
            lines.append("#### 3. Vuelta a la Calma (10 min)")
            lines.append("- 10 min en llano a ritmo regenerativo.")
            structured_data = {
                "activity_type": ActivityType.TRAIL_RUN.value,
                "target_duration_minutes": 65.0,
                "target_distance_km": 10.0,
                "elevation_gain_m": 400,
                "target_rpe": 7,
                "acwr_assessment": acwr_info
            }

        elif discipline == SportDiscipline.MARATHON:
            lines.append("### 🏃‍♀️ Planificación de Entrenamiento — Tempo Maratón (Ritmo Específico)")
            lines.append(f"**Atleta**: {athlete.name} | **Objetivo**: Economía de Carrera y Eficiencia Glucolítica")
            lines.append("")
            lines.append("#### 1. Calentamiento (15 min)")
            lines.append("- 3 km progresivos de 4:45 a 4:15/km.")
            lines.append("#### 2. Bloque Principal: Tempo de Resistencia")
            lines.append("- **12 km a Ritmo Maratón Objetivo (3:55-4:00/km)** continuo en asfalto/terreno llano (RPE 6-7).")
            lines.append("- Pauta de hidratación: 150ml de agua/isotónico cada 4 km.")
            lines.append("#### 3. Vuelta a la Calma (10 min)")
            lines.append("- 2 km trote regenerativo a 5:00/km.")
            structured_data = {
                "activity_type": ActivityType.ROAD_RUN.value,
                "target_duration_minutes": 75.0,
                "target_distance_km": 17.0,
                "target_rpe": 7,
                "target_pace": "3:58/km",
                "acwr_assessment": acwr_info
            }

        else:
            # General / Hybrid / Strength
            lines.append("### 🏋️‍♂️ Planificación de Entrenamiento — Fuerza y Acondicionamiento Híbrido")
            lines.append(f"**Atleta**: {athlete.name} | **Objetivo**: Estabilidad Central y Fuerza Funcional")
            lines.append("")
            lines.append("#### 1. Calentamiento Dinámico (15 min)")
            lines.append("- McGill Big 3: Modified Curl-up (3x6), Side Plank (3x30s/lado), Bird-Dog (3x8/lado).")
            lines.append("#### 2. Bloque de Fuerza Funcional (35 min)")
            lines.append("- Trap Bar Deadlift (Agarre Alto, 65% 1RM, 4 series de 6 repeticiones).")
            lines.append("- Hip Thrusts con barra apoyada en banco (4x8 a 70% 1RM).")
            lines.append("- Split Squats búlgaros con mancuernas (3x8 cada pierna).")
            lines.append("#### 3. Vuelta a la Calma (10 min)")
            lines.append("- Movilidad de cadera y descompresión lumbar pasiva.")
            structured_data = {
                "activity_type": ActivityType.STRENGTH_HSR.value,
                "target_duration_minutes": 60.0,
                "target_rpe": 7,
                "acwr_assessment": acwr_info
            }

        # Add molecular pathway reminder (AMPK vs mTOR interference)
        lines.append("")
        lines.append("ℹ️ **Optimización Molecular (AMPK / mTOR)**: Si vas a combinar esta sesión con trabajo de fuerza máxima, asegúrate de separar ambas sesiones por un mínimo de **6 a 8 horas** para evitar la interferencia de la vía AMPK sobre la síntesis proteica muscular.")

        message_markdown = "\n".join(lines)
        suggested_actions = [
            "Exportar a Garmin / Intervals.icu",
            "Ver zonas de ritmo cardíaco",
            "Ajustar volumen semanal"
        ]

        trace = self._create_trace(query=query, start_time=start_time)
        return self._build_response(
            query=query,
            athlete=athlete,
            message_markdown=message_markdown,
            structured_data=structured_data,
            suggested_actions=suggested_actions,
            trace=trace
        )
