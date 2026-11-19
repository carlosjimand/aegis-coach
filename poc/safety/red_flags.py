"""
Aegis Coach — Acute Medical Red-Flag Detector
==============================================
Identifies critical medical emergencies, acute trauma, and high-risk physiological signs.
Enforces immediate lockout of training prescriptions and formats structured clinical referral notices.
"""

from __future__ import annotations

import re
from typing import Optional, List, Tuple
from poc.models.athlete import AthleteProfile
from poc.models.conversation import SafetyViolation, RiskLevel


class RedFlagDetector:
    """
    Scans user input and athlete biometrics for acute medical red flags requiring
    immediate cessation of exercise and certified sports physician / emergency referral.
    """

    # Comprehensive emergency pattern dictionary: (Regex Pattern, Violation Code, Rule Name, Rationale)
    RED_FLAG_PATTERNS: List[Tuple[str, str, str, str]] = [
        (
            r"\b(dolor en el pecho|opresi[oó]n en el pecho|dolor tor[aá]cico|chest pain|chest tightness|falta de aire aguda|dificultad para respirar severa|desmayo|p[eé]rdida de conocimiento|syncope|fainting|mareo severo|sensaci[oó]n de desmayo|palpitaciones irregulares en reposo|dolor que irradia al brazo izquierdo)\b",
            "RED_FLAG_CARDIOVASCULAR_EMERGENCY",
            "Cardiovascular Emergency / Acute Chest Distress",
            "Reported symptoms indicate a potential acute cardiovascular event or serious hemodynamic compromise. Any physical exertion is strictly contraindicated."
        ),
        (
            r"\b(rotura total|avulsi[oó]n|avulsion|chasquido fuerte|son[oó] un chasquido|imposible apoyar|incapaz de apoyar el pie|incapaz de caminar|deformidad [oó]sea|sospecha de fractura|fractura|hematoma masivo|hinchaz[oó]n instant[aá]nea masiva|no puedo apoyar)\b",
            "RED_FLAG_ACUTE_TRAUMA_RUPTURE",
            "Acute Musculoskeletal Trauma / Complete Rupture / Fracture",
            "Reported mechanical trauma, audible tendon snapping with functional loss, or inability to bear weight suggests acute structural disruption requiring urgent radiological imaging and orthopedic evaluation."
        ),
        (
            r"\b(p[eé]rdida de sensibilidad en la pelvis|anestesia en silla de montar|incontinencia|p[eé]rdida de control de esf[ií]nteres|pie ca[ií]do repentino|p[eé]rdida repentina de fuerza en la pierna|saddle anesthesia)\b",
            "RED_FLAG_NEUROLOGICAL_CAUDA_EQUINA",
            "Acute Neurological Compromise / Suspected Cauda Equina Syndrome",
            "Symptoms of saddle anesthesia, acute progressive motor deficit, or sphincter disturbance represent a neurosurgical emergency."
        ),
        (
            r"\b(golpe de calor|confusi[oó]n severa y no sudo|deje de sudar con 40 grados|calambres en todo el cuerpo con confusi[oó]n|desorientaci[oó]n extrema por calor)\b",
            "RED_FLAG_EXERTIONAL_HEAT_STROKE",
            "Exertional Heat Stroke / Severe Hyperthermia",
            "Central nervous system dysfunction coupled with elevated thermal load is life-threatening and requires immediate external cooling and emergency medical dispatch."
        )
    ]

    def detect_red_flags(
        self,
        query_text: str,
        athlete: Optional[AthleteProfile] = None
    ) -> Optional[SafetyViolation]:
        """
        Scans query text and athlete state for clinical red flags.
        Returns a SafetyViolation if an emergency is detected; otherwise None.
        """
        norm_text = query_text.lower().strip()

        # 1. Regex pattern scanning for emergency conditions
        for pattern, code, rule_name, rationale in self.RED_FLAG_PATTERNS:
            match = re.search(pattern, norm_text, flags=re.IGNORECASE)
            if match:
                matched_str = match.group(0)
                return SafetyViolation(
                    violation_code=code,
                    rule_name=f"Medical Red Flag: {rule_name}",
                    risk_level=RiskLevel.CRITICAL,
                    blocked_content=matched_str,
                    safe_alternative="Immediate medical evaluation at an emergency clinic or consultation with a certified sports physician.",
                    rationale=rationale,
                    escalation_required=True
                )

        # 2. Severe Pain VAS >= 7 reported in text or profile
        vas_match = re.search(r"\b([789]|10)\s*/\s*10\b", norm_text)
        if vas_match:
            pain_score = int(vas_match.group(1))
            return SafetyViolation(
                violation_code="RED_FLAG_SEVERE_PAIN_VAS_CRITICAL",
                rule_name="Acute Pain Flare: VAS >= 7/10 Medical Referral Trigger",
                risk_level=RiskLevel.CRITICAL,
                blocked_content=f"Reported pain level {pain_score}/10",
                safe_alternative="Complete cessation of provocative loading; clinical examination and diagnostic ultrasound/MRI.",
                rationale=f"Reported pain intensity of {pain_score}/10 surpasses safe athletic thresholds and indicates acute tissue injury.",
                escalation_required=True
            )

        # 3. Check athlete profile active injury severity
        if athlete:
            for injury in athlete.active_injuries:
                if injury.is_severe:
                    return SafetyViolation(
                        violation_code="RED_FLAG_ATHLETE_INJURY_SEVERE",
                        rule_name=f"Severe Active Injury: {injury.injury_name} (VAS {injury.current_pain_score}/10)",
                        risk_level=RiskLevel.CRITICAL,
                        blocked_content=injury.injury_name,
                        safe_alternative="Sports medicine medical evaluation before resuming any structured physical training.",
                        rationale="Athlete profile contains an active pathology with severe clinical pain score (>= 7/10).",
                        escalation_required=True
                    )

        return None

    @staticmethod
    def format_medical_referral_notice(violation: SafetyViolation) -> str:
        """
        Generates an authoritative, compassionate, and clear medical referral notice
        explaining why training is locked down and directing the athlete to proper medical care.
        """
        return (
            f"🚨 **AVISO MÉDICO DE SEGURIDAD CLÍNICA — ATENCIÓN INMEDIATA** 🚨\n\n"
            f"Hemos detectado un síntoma o indicador de **alerta médica crítica ({violation.rule_name})**.\n\n"
            f"**Motivo de Interrupción de Entrenamiento:**\n"
            f"{violation.rationale}\n\n"
            f"**Protocolo de Actuación Recomendado:**\n"
            f"1. **Detén cualquier actividad física o entrenamiento de inmediato.** No intentes 'probarte' ni forzar la zona.\n"
            f"2. **Consulta a un profesional sanitario colegiado**: Acude a un centro de urgencias médicas o solicita cita prioritaria con un médico especialista en medicina del deporte / traumatólogo.\n"
            f"3. Aplica los principios iniciales de protección (**PEACE & LOVE**): Protección, Elevación, Evitar antiinflamatorios innecesarios en fase hiperaguda sin prescripción, Compresión suave.\n\n"
            f"*(Aegis Coach ha bloqueado temporalmente la generación de planes de entrenamiento para proteger tu salud y evitar lesiones graves.)*"
        )
