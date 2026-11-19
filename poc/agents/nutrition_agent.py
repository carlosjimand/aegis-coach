"""
Aegis Coach — Nutrition, Fueling & Recovery Specialist Agent
============================================================
Calculates carbohydrate loading protocols (Burke et al.), post-workout glycogen replenishment,
Low-FODMAP dietary adjustments, tendon collagen synthesis, and hydration/electrolyte targets.
"""

from __future__ import annotations

import time
import re
from typing import Dict, Any, Optional, List
from poc.agents.base_agent import BaseAgent
from poc.models.athlete import AthleteProfile
from poc.models.conversation import UserQuery, AgentResponse, DomainIntent


class NutritionAgent(BaseAgent):
    """
    Nutrition and Recovery Specialist Agent.
    Generates evidence-backed macronutrient targets, race fueling strategies, and gastrointestinal protocols.
    """

    def __init__(self):
        super().__init__(agent_name="NutritionRecoverySpecialist", domain=DomainIntent.NUTRITION_RECOVERY)

    def process(self, query: UserQuery, athlete: AthleteProfile) -> AgentResponse:
        start_time = time.time()
        text = query.raw_text.strip()
        norm_text = text.lower()

        weight = athlete.weight_kg
        is_low_fodmap = "low_fodmap" in [d.lower() for d in athlete.dietary_restrictions] or "fodmap" in norm_text or "sensitive_gut" in [d.lower() for d in athlete.dietary_restrictions]
        is_vegan = "vegan" in [d.lower() for d in athlete.dietary_restrictions] or "vegano" in norm_text

        lines: List[str] = []
        structured_data: Dict[str, Any] = {}

        # ----------------------------------------------------------------------
        # Case A: Marathon Carb Loading / Pre-Race Fueling (Burke et al.)
        # ----------------------------------------------------------------------
        if any(w in norm_text for w in ["carga", "carbohidratos", "marat[oó]n", "carrera", "competi", "42k", "21k", "pre-race"]):
            target_cho_min = round(weight * 8.0, 0)
            target_cho_max = round(weight * 10.0, 0)
            pre_race_meal_cho = round(weight * 2.5, 0)
            in_race_cho_per_hr = "60-90g CHO/hora"
            fluid_target_ml = "500-750 ml/hora"
            sodium_target_mg = "500-700 mg/hora"

            lines.append("### 🍌 Protocolo de Carga de Carbohidratos y Nutrición de Carrera")
            lines.append(f"**Atleta**: {athlete.name} | **Peso Corporal**: {weight:.1f} kg | **Evidencia**: Burke et al. 2019 / Jeukendrup 2014")
            lines.append("")
            lines.append(f"#### 1. Carga de Glucógeno (36-48h previas)")
            lines.append(f"- **Objetivo Diario de Carbohidratos**: **{int(target_cho_min)} - {int(target_cho_max)} g CHO/día** (8-10 g/kg/día).")
            lines.append(f"- **Estrategia**: Priorizar carbohidratos simples y refinados con **baja fibra (<15g/día)** y bajo contenido graso para maximizar saturación de glucógeno y evitar molestias gastrointestinales.")

            if is_low_fodmap:
                lines.append("")
                lines.append("🛡️ **Adaptación Estricta Low-FODMAP (Sensibilidad Gastrointestinal)**:")
                lines.append("- **Fuentes Recomendadas**: Arroz blanco, harina de avena sin gluten, patata cocida/asada sin piel, plátano maduro, jarabe de arce, maltodextrina.")
                lines.append("- **Alimentos a Evitar**: Trigo/centeno, manzanas, miel, cebolla, ajo, legumbres, edulcorantes polialcoholes (sorbitol, xilitol).")

            lines.append("")
            lines.append(f"#### 2. Desayuno Pre-Competición (3-4h antes de la salida)")
            lines.append(f"- **Ingesta Objetivo**: **~{int(pre_race_meal_cho)} g CHO** (2.0-3.0 g/kg).")
            lines.append("- Ejemplo: Gachas de harina de arroz con plátano y miel/sirope de arce + 300ml de agua/isotónico isotónico.")
            lines.append("")
            lines.append("#### 3. Pauta de Avituallamiento en Carrera")
            lines.append(f"- **Carbohidratos**: **{in_race_cho_per_hr}** (ratio 2:1 o 1:0.8 glucosa:fructosa para optimizar transportadores SGLT1 y GLUT5).")
            lines.append(f"- **Líquidos y Electrolitos**: **{fluid_target_ml}** con **{sodium_target_mg} de sodio** por hora.")

            structured_data = {
                "protocol": "BURKE_CARBOHYDRATE_LOADING",
                "daily_carbs_target_g": [int(target_cho_min), int(target_cho_max)],
                "pre_race_meal_carbs_g": int(pre_race_meal_cho),
                "in_race_carbs_per_hour_g": 75,
                "hourly_sodium_mg": 600,
                "is_low_fodmap_adapted": is_low_fodmap
            }

        # ----------------------------------------------------------------------
        # Case B: Post-Workout Glycogen & Tendon Collagen Recovery
        # ----------------------------------------------------------------------
        elif any(w in norm_text for w in ["recuperar", "post-entreno", "isquio", "isquiotibial", "despu[eé]s de", "comer tras"]):
            post_cho = round(weight * 1.2, 0)
            post_protein = round(max(25.0, weight * 0.35), 0)

            lines.append("### 🥗 Nutrición de Recuperación Post-Entrenamiento & Síntesis de Colágeno")
            lines.append(f"**Atleta**: {athlete.name} | **Peso**: {weight:.1f} kg")
            lines.append("")
            lines.append("#### 1. Ventana de Resíntesis de Glucógeno (Primeros 30-45 min)")
            lines.append(f"- **Carbohidratos**: **{int(post_cho)} g CHO** (1.2 g/kg) de alto índice glucémico (arroz blanco, zumo de fruta, plátano, copos de maíz).")
            lines.append(f"- **Proteína de Alta Calidad**: **{int(post_protein)} g** (0.35 g/kg) con al menos 3g de Leucina para activar la vía mTOR.")
            lines.append("")
            lines.append("#### 2. Protocolo Específico para Tendón y Tejido Conectivo (Baar et al.)")
            lines.append("- **Colágeno Hidrolizado / Gelatina**: 15g de colágeno + 50mg de Vitamina C consumidos **45-60 min antes** del trabajo de fuerza/isométricos.")
            lines.append("- *Mecanismo*: Incrementa la concentración plasmática de prolina y glicina en el tendón durante el estímulo mecánico.")
            lines.append("")
            lines.append("#### 3. Rehidratación & Sodio")
            lines.append("- Bebe 1.25 a 1.5 L de líquido por cada kg de peso perdido durante la sesión, añadiendo 500mg de sales electrolíticas.")

            structured_data = {
                "protocol": "POST_WORKOUT_GLYCOGEN_COLLAGEN_RECOVERY",
                "post_workout_carbs_g": int(post_cho),
                "post_workout_protein_g": int(post_protein),
                "collagen_target_g": 15,
                "vitamin_c_mg": 50
            }

        # ----------------------------------------------------------------------
        # Case C: General Daily Macronutrients & Energy Balance
        # ----------------------------------------------------------------------
        else:
            base_protein = round(weight * 1.8, 0)
            base_carbs = round(weight * 5.5, 0)
            base_fat = round(weight * 1.0, 0)
            daily_cals = int(base_protein * 4 + base_carbs * 4 + base_fat * 9)

            lines.append("### 🥑 Distribución Nutricional Diaria y Balance Energético")
            lines.append(f"**Atleta**: {athlete.name} | **Peso**: {weight:.1f} kg | **Disciplina**: {athlete.primary_discipline.value}")
            lines.append("")
            lines.append(f"- **Calorías Totales de Mantenimiento / Rendimiento**: **~{daily_cals} kcal/día**.")
            lines.append(f"- **Proteínas**: **{int(base_protein)} g/día** (1.8 g/kg) para soporte estructural.")
            lines.append(f"- **Carbohidratos**: **{int(base_carbs)} g/día** (5.5 g/kg) como combustible glucolítico.")
            lines.append(f"- **Grasas Saludables**: **{int(base_fat)} g/día** (1.0 g/kg) para soporte hormonal y absorción de vitaminas liposolubles.")

            structured_data = {
                "daily_calories": daily_cals,
                "daily_protein_g": int(base_protein),
                "daily_carbs_g": int(base_carbs),
                "daily_fat_g": int(base_fat)
            }

        message_markdown = "\n".join(lines)
        suggested_actions = [
            "Descargar lista de compra",
            "Ajustar por peso actual",
            "Ver timing de suplementación"
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
