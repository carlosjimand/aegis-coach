"""
Aegis Coach — Natural Language Workout Data-Entry Parser Agent
==============================================================
Parses conversational workout reports (text/voice transcripts) into standardized,
structured JSON metrics (distance, duration, elevation, pace, heart rate, RPE, soreness).
"""

from __future__ import annotations

import time
import re
from typing import Dict, Any, Optional, List
from poc.agents.base_agent import BaseAgent
from poc.models.athlete import AthleteProfile, ActivityType, WorkoutLog
from poc.models.conversation import UserQuery, AgentResponse, DomainIntent


class DataEntryAgent(BaseAgent):
    """
    Data Entry Parser Agent.
    Converts informal conversational athlete messages into structured physiological workout logs.
    """

    def __init__(self):
        super().__init__(agent_name="NaturalLanguageWorkoutParser", domain=DomainIntent.DATA_LOGGING)

    def parse_workout_text(self, text: str, athlete: AthleteProfile) -> Dict[str, Any]:
        """Extracts structured workout fields from natural language text."""
        norm_text = text.lower().strip()

        # 1. Determine Activity Type
        activity_type = ActivityType.ROAD_RUN
        if any(w in norm_text for w in ["trail", "montaña", "sendero", "desnivel", "vert"]):
            activity_type = ActivityType.TRAIL_RUN
        elif any(w in norm_text for w in ["pista", "series", "intervalos", "tacos", "800m", "400m"]):
            activity_type = ActivityType.TRACK_INTERVALS
        elif any(w in norm_text for w in ["bici", "ciclismo", "rodillo", "pedalear", "bike"]):
            activity_type = ActivityType.CYCLING
        elif any(w in norm_text for w in ["pesas", "gimnasio", "fuerza", "deadlift", "hsr", "sentadilla"]):
            activity_type = ActivityType.STRENGTH_HSR
        elif any(w in norm_text for w in ["regenerativo", "suave", "recuperacion"]):
            activity_type = ActivityType.RECOVERY_RUN
        elif any(w in norm_text for w in ["tirada larga", "long run"]):
            activity_type = ActivityType.LONG_RUN

        # 2. Extract Distance (km)
        distance_km = None
        dist_match = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:km|kilometros|k\b)", norm_text)
        if dist_match:
            distance_km = float(dist_match.group(1).replace(",", "."))

        # 3. Extract Duration (minutes)
        duration_minutes = None
        # Format: 1h 15m, 1h15min, 1 hora 20 min
        hour_min_match = re.search(r"(\d+)\s*(?:h|hora|horas)\s*(\d+)?\s*(?:m|min|minutos)?", norm_text)
        if hour_min_match:
            hours = int(hour_min_match.group(1))
            mins = int(hour_min_match.group(2)) if hour_min_match.group(2) else 0
            duration_minutes = float(hours * 60 + mins)
        else:
            # Format: 48 minutos, 48min, 35m
            min_match = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:min|minutos|m\b)", norm_text)
            if min_match:
                duration_minutes = float(min_match.group(1).replace(",", "."))

        if duration_minutes is None:
            # Default fallback estimation if only distance is given
            duration_minutes = (distance_km * 5.0) if distance_km else 45.0

        # 4. Extract Elevation Gain (m D+)
        elevation_gain_m = 0
        elev_match = re.search(r"(\d+)\s*(?:m|metros)?\s*(?:de\s+desnivel|vert|\+|d\+|m\+|desnivel|positivo|de\s+desnivel\s+positivo)", norm_text)
        if elev_match:
            elevation_gain_m = int(elev_match.group(1))

        # 5. Extract Heart Rate (avg & max)
        avg_hr = None
        max_hr = None
        hr_match = re.search(r"(\d{2,3})\s*(?:ppm|bpm|pulsaciones)", norm_text)
        if hr_match:
            avg_hr = int(hr_match.group(1))

        max_hr_match = re.search(r"(?:max|pico)\s*(?:de\s*)?(\d{2,3})\s*(?:ppm|bpm)?", norm_text)
        if max_hr_match:
            max_hr = int(max_hr_match.group(1))

        # 6. Extract RPE (Rating of Perceived Exertion 1-10)
        rpe = 5
        rpe_match = re.search(r"rpe\s*(\d{1,2})", norm_text)
        if rpe_match:
            rpe = max(1, min(10, int(rpe_match.group(1))))

        # 7. Extract Soreness / Pain Location and Score
        soreness_reported = None
        pain_match = re.search(r"(\d{1,2})\s*/\s*10", norm_text)
        soreness_loc = None
        for loc in ["isquio", "isquiotibial", "hamstring", "aquiles", "rodilla", "soleo", "gemelo", "lumbar", "espalda"]:
            if loc in norm_text:
                soreness_loc = loc
                break

        if pain_match or soreness_loc:
            pain_val = int(pain_match.group(1)) if pain_match else 2
            soreness_reported = {
                "location": soreness_loc or "general_lower_limb",
                "pain_score": pain_val
            }

        # 8. Compute Pace Average
        pace_avg = None
        pace_match = re.search(r"(\d+:\d+)\s*(?:/km|min/km|el km)?", norm_text)
        if pace_match:
            pace_avg = f"{pace_match.group(1)}/km"
        elif distance_km and distance_km > 0 and duration_minutes:
            pace_dec = duration_minutes / distance_km
            p_min = int(pace_dec)
            p_sec = int((pace_dec - p_min) * 60)
            pace_avg = f"{p_min}:{p_sec:02d}/km"

        # 9. Compute TRIMP Score
        if avg_hr and athlete.max_heart_rate and athlete.resting_heart_rate:
            trimp = athlete.biometrics.calculate_banister_trimp(
                duration_min=duration_minutes,
                avg_hr=float(avg_hr),
                rest_hr=float(athlete.resting_heart_rate),
                max_hr=float(athlete.max_heart_rate),
                sex=athlete.gender
            )
        else:
            trimp = athlete.biometrics.calculate_rpe_trimp(
                duration_min=duration_minutes,
                rpe=rpe
            )

        return {
            "activity_type": activity_type.value,
            "distance_km": distance_km,
            "duration_minutes": duration_minutes,
            "elevation_gain_m": elevation_gain_m,
            "pace_avg": pace_avg,
            "avg_heart_rate": avg_hr,
            "max_heart_rate": max_hr,
            "rpe": rpe,
            "soreness_reported": soreness_reported,
            "trimp_score": trimp,
            "status": "PARSED_SUCCESS"
        }

    def process(self, query: UserQuery, athlete: AthleteProfile) -> AgentResponse:
        start_time = time.time()
        parsed = self.parse_workout_text(query.raw_text, athlete)

        dist_str = f"{parsed['distance_km']} km" if parsed.get("distance_km") else "Sin distancia"
        dur_str = f"{int(parsed['duration_minutes'])} min"
        pace_str = f" | Ritmo: `{parsed['pace_avg']}`" if parsed.get("pace_avg") else ""
        elev_str = f" | Desnivel: `+{parsed['elevation_gain_m']}m`" if parsed.get("elevation_gain_m") else ""
        hr_str = f" | FC Media: `{parsed['avg_heart_rate']} ppm`" if parsed.get("avg_heart_rate") else ""
        rpe_str = f" | RPE: `{parsed['rpe']}/10`"

        lines = [
            "### ✅ Entrenamiento Registrado en Base de Datos",
            f"- **Tipo de Actividad**: `{parsed['activity_type']}`",
            f"- **Métricas Principales**: {dist_str} en {dur_str}{pace_str}{elev_str}{hr_str}{rpe_str}",
            f"- **Carga TRIMP Calculada**: `{parsed['trimp_score']:.1f} puntos`"
        ]

        if parsed.get("soreness_reported"):
            s = parsed["soreness_reported"]
            lines.append(f"- ⚠️ **Molestia Registrada**: `{s['location']}` con nivel de dolor `{s['pain_score']}/10` (derivado al módulo de fisioterapia).")

        message_markdown = "\n".join(lines)
        suggested_actions = ["Ver curva CTL/ATL", "Añadir notas de sensaciones", "Registrar nutrición post-sesión"]

        trace = self._create_trace(query=query, start_time=start_time)
        return self._build_response(
            query=query,
            athlete=athlete,
            message_markdown=message_markdown,
            structured_data=parsed,
            suggested_actions=suggested_actions,
            trace=trace
        )
