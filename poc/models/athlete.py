"""
Aegis Coach — Athlete & Physiological Data Models
==================================================
Defines typed models for athlete identity, clinical injury records, daily recovery metrics,
workout logs, and deterministic Banister TRIMP / ACWR / CTL / ATL biometric calculations.
"""

from __future__ import annotations

import math
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class SportDiscipline(str, Enum):
    TRACK_800M = "TRACK_800M"
    TRAIL_RUNNING = "TRAIL_RUNNING"
    MARATHON = "MARATHON"
    ROAD_RUNNING = "ROAD_RUNNING"
    HYBRID = "HYBRID"
    STRENGTH_CROSSFIT = "STRENGTH_CROSSFIT"
    CYCLING = "CYCLING"
    GENERAL_FITNESS = "GENERAL_FITNESS"


class RehabPhase(str, Enum):
    ACUTE = "ACUTE"                      # Phase 1: Protection, isometrics, pain control (VAS > 4)
    SUBACUTE = "SUBACUTE"                # Phase 2: Heavy Slow Resistance (HSR), controlled range (VAS <= 3)
    REMODELING = "REMODELING"            # Phase 3: Dynamic eccentric, energy storage, speed progression
    RETURN_TO_SPORT = "RETURN_TO_SPORT"  # Phase 4: High velocity sprint, sport-specific reactive agility
    MAINTENANCE = "MAINTENANCE"          # Prevention, post-rehab strength maintenance


class EvidenceLevel(str, Enum):
    SYSTEMATIC_REVIEW = "SYSTEMATIC_REVIEW"  # Level 1a / 1b
    RCT = "RCT"                              # Level 2a / 2b
    CLINICAL_GUIDELINE = "CLINICAL_GUIDELINE"
    EXPERT_CONSENSUS = "EXPERT_CONSENSUS"


class ActivityType(str, Enum):
    TRACK_INTERVALS = "TRACK_INTERVALS"
    TRAIL_RUN = "TRAIL_RUN"
    ROAD_RUN = "ROAD_RUN"
    LONG_RUN = "LONG_RUN"
    RECOVERY_RUN = "RECOVERY_RUN"
    CYCLING = "CYCLING"
    STRENGTH_HSR = "STRENGTH_HSR"
    MOBILITY_REHAB = "MOBILITY_REHAB"
    REST = "REST"


class InjuryRecord(BaseModel):
    """Clinical record of an athlete's acute or chronic pathology."""

    injury_id: str = Field(..., description="Unique injury identifier.")
    injury_name: str = Field(..., description="Pathology name (e.g., Proximal Hamstring Tendinopathy).")
    anatomical_region: str = Field(
        ...,
        description="Target anatomical zone (e.g. 'hamstring_proximal', 'achilles_tendon', 'patellar_tendon', 'lumbar_spine')."
    )
    date_onset: str = Field(..., description="ISO formatted date of injury onset (YYYY-MM-DD).")
    rehab_phase: RehabPhase = Field(default=RehabPhase.SUBACUTE, description="Current clinical rehabilitation phase.")
    current_pain_score: int = Field(
        default=0,
        ge=0,
        le=10,
        description="Visual Analog Scale (VAS) pain score from 0 (none) to 10 (emergency)."
    )
    contraindicated_movements: List[str] = Field(
        default_factory=list,
        description="List of forbidden movement patterns for this pathology."
    )
    safe_alternative_protocols: List[str] = Field(
        default_factory=list,
        description="Evidence-based exercise substitutes."
    )
    is_active: bool = Field(default=True, description="Whether the injury actively constrains training.")
    notes: Optional[str] = Field(default=None, description="Clinical physiotherapist notes.")

    @property
    def is_severe(self) -> bool:
        """Flags whether current pain level requires urgent clinical intervention."""
        return self.current_pain_score >= 7


class RecoveryMetrics(BaseModel):
    """Daily autonomic and recovery biometrics ingested from wearable or morning check-in."""

    date: str = Field(..., description="ISO formatted date (YYYY-MM-DD).")
    morning_hrv_rmssd: float = Field(..., description="Morning heart rate variability rMSSD in milliseconds.")
    hrv_baseline_7d: float = Field(..., description="7-day rolling average HRV baseline in milliseconds.")
    resting_heart_rate: int = Field(..., description="Morning resting heart rate in bpm.")
    rhr_baseline_7d: int = Field(..., description="7-day rolling average resting heart rate in bpm.")
    sleep_hours: float = Field(..., ge=0.0, le=24.0, description="Total sleep duration in hours.")
    sleep_quality_score: int = Field(default=75, ge=0, le=100, description="Sleep quality rating (0-100).")
    muscle_soreness_score: int = Field(default=0, ge=0, le=10, description="Perceived muscle soreness (0-10).")
    stress_level_score: int = Field(default=0, ge=0, le=10, description="Perceived mental/physical stress (0-10).")

    def hrv_drop_percentage(self) -> float:
        """Computes percentage drop in HRV relative to baseline."""
        if self.hrv_baseline_7d <= 0:
            return 0.0
        return ((self.hrv_baseline_7d - self.morning_hrv_rmssd) / self.hrv_baseline_7d) * 100.0

    def is_autonomic_crash(self) -> bool:
        """
        Detects acute autonomic nervous system exhaustion.
        Triggers if HRV drops >= 40% below baseline or sleep is severely deprived (< 4.5h) with high soreness.
        """
        drop = self.hrv_drop_percentage()
        if drop >= 40.0:
            return True
        if self.sleep_hours < 4.5 and drop >= 25.0:
            return True
        if self.resting_heart_rate >= (self.rhr_baseline_7d + 10) and drop >= 25.0:
            return True
        return False


class WorkoutLog(BaseModel):
    """Structured record of a single completed or planned training session."""

    workout_id: str = Field(..., description="Unique workout ID.")
    date: str = Field(..., description="ISO formatted date (YYYY-MM-DD).")
    activity_type: ActivityType = Field(..., description="Discipline/category of workout.")
    title: Optional[str] = Field(default=None, description="Short title/summary of session.")
    distance_km: Optional[float] = Field(default=None, ge=0.0, description="Distance covered in kilometers.")
    duration_minutes: float = Field(..., gt=0.0, description="Total duration in minutes.")
    avg_heart_rate: Optional[int] = Field(default=None, ge=30, le=240, description="Average heart rate in bpm.")
    max_heart_rate: Optional[int] = Field(default=None, ge=30, le=240, description="Maximum heart rate in bpm.")
    elevation_gain_m: Optional[int] = Field(default=0, ge=0, description="Positive elevation gain in meters.")
    pace_avg: Optional[str] = Field(default=None, description="Average pace string (e.g., '4:30/km').")
    rpe: int = Field(default=5, ge=1, le=10, description="Rate of Perceived Exertion (Borg CR10 scale 1-10).")
    trimp_score: Optional[float] = Field(default=None, ge=0.0, description="Calculated Banister TRIMP score.")
    soreness_reported: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Location and severity of pain/soreness post-workout."
    )
    notes: Optional[str] = Field(default=None, description="Athlete comments or qualitative feedback.")


class BiometricState(BaseModel):
    """Stateful physiological engine calculating TRIMP, CTL, ATL, TSB, and ACWR."""

    daily_workouts: List[WorkoutLog] = Field(default_factory=list)
    daily_metrics: List[RecoveryMetrics] = Field(default_factory=list)

    @staticmethod
    def calculate_banister_trimp(
        duration_min: float,
        avg_hr: float,
        rest_hr: float,
        max_hr: float,
        sex: Sex = Sex.MALE
    ) -> float:
        """
        Calculates Banister Training Impulse (TRIMP) using heart rate reserve:
        TRIMP = Duration (min) * DeltaHR * y
        where DeltaHR = (avg_hr - rest_hr) / (max_hr - rest_hr)
        and y = 0.64 * exp(1.92 * DeltaHR) for males, 0.86 * exp(1.67 * DeltaHR) for females.
        """
        if max_hr <= rest_hr or duration_min <= 0:
            return 0.0

        # Heart Rate Reserve fraction
        delta_hr = (avg_hr - rest_hr) / (max_hr - rest_hr)
        delta_hr = max(0.0, min(1.0, delta_hr))

        if sex == Sex.FEMALE:
            y = 0.86 * math.exp(1.67 * delta_hr)
        elif sex == Sex.MALE:
            y = 0.64 * math.exp(1.92 * delta_hr)
        else:
            y = 0.75 * math.exp(1.80 * delta_hr)

        return round(duration_min * delta_hr * y, 2)

    @staticmethod
    def calculate_rpe_trimp(duration_min: float, rpe: int) -> float:
        """Fallback Foster Session-RPE load calculation: Load = Duration (min) * RPE."""
        return round(duration_min * float(rpe), 2)

    @staticmethod
    def calculate_ctl(
        trimp_history: List[float],
        time_constant: int = 42,
        initial_ctl: float = 0.0
    ) -> float:
        """
        Computes Chronic Training Load (CTL / Fitness) as an Exponential Weighted Moving Average (EWMA):
        CTL_t = CTL_{t-1} + (TRIMP_t - CTL_{t-1}) * (1 - exp(-1 / time_constant))
        """
        if not trimp_history:
            return round(initial_ctl, 2)

        decay_factor = 1.0 - math.exp(-1.0 / float(time_constant))
        current_ctl = initial_ctl

        for load in trimp_history:
            current_ctl = current_ctl + (load - current_ctl) * decay_factor

        return round(current_ctl, 2)

    @staticmethod
    def calculate_atl(
        trimp_history: List[float],
        time_constant: int = 7,
        initial_atl: float = 0.0
    ) -> float:
        """
        Computes Acute Training Load (ATL / Fatigue) as an EWMA:
        ATL_t = ATL_{t-1} + (TRIMP_t - ATL_{t-1}) * (1 - exp(-1 / time_constant))
        """
        if not trimp_history:
            return round(initial_atl, 2)

        decay_factor = 1.0 - math.exp(-1.0 / float(time_constant))
        current_atl = initial_atl

        for load in trimp_history:
            current_atl = current_atl + (load - current_atl) * decay_factor

        return round(current_atl, 2)

    @staticmethod
    def calculate_tsb(ctl: float, atl: float) -> float:
        """Calculates Training Stress Balance (TSB / Form): TSB = CTL - ATL."""
        return round(ctl - atl, 2)

    @staticmethod
    def calculate_acwr(atl: float, ctl: float) -> float:
        """
        Calculates Acute:Chronic Workload Ratio (ACWR): ACWR = ATL / CTL.
        If CTL is zero or near zero, returns safe bounded ratio.
        """
        if ctl <= 1.0:
            return round(atl / 1.0, 2) if atl > 0 else 1.0
        return round(atl / ctl, 2)

    def get_acwr_risk_assessment(self, atl: float, ctl: float) -> Dict[str, Any]:
        """Classifies the ACWR into clinical sports science risk categories (Gabbett 2016)."""
        acwr = self.calculate_acwr(atl, ctl)
        if acwr < 0.80:
            zone = "UNDER_TRAINING"
            risk = "LOW_FITNESS_DECAY"
            recommendation = "Gradually build chronic workload to avoid sudden loading spikes."
        elif 0.80 <= acwr <= 1.30:
            zone = "SWEET_SPOT"
            risk = "OPTIMAL_LOAD_LOW_INJURY_RISK"
            recommendation = "Maintain progressive overload; optimal adaptation zone."
        elif 1.30 < acwr <= 1.50:
            zone = "ELEVATED_RISK"
            risk = "MODERATE_INJURY_RISK"
            recommendation = "Monitor recovery closely; avoid adding additional high-intensity sessions."
        else:
            zone = "DANGER_ZONE"
            risk = "HIGH_INJURY_SPIKE_DANGER"
            recommendation = "Immediate load reduction required. Substitute high-velocity sessions with active recovery."

        return {
            "acwr": acwr,
            "ctl": ctl,
            "atl": atl,
            "tsb": self.calculate_tsb(ctl, atl),
            "zone": zone,
            "risk": risk,
            "recommendation": recommendation,
            "is_dangerous": acwr >= 1.50
        }


class AthleteProfile(BaseModel):
    """Complete profile and physiological identity of an athlete in a tenant domain."""

    athlete_id: str = Field(..., description="Unique athlete ID.")
    tenant_id: str = Field(..., description="Tenant ID enforcing isolation boundary.")
    name: str = Field(..., description="Full name or alias of the athlete.")
    age: int = Field(..., ge=10, le=120, description="Age in years.")
    gender: Sex = Field(default=Sex.MALE, description="Biological sex for physiological calculations.")
    height_cm: float = Field(..., ge=100.0, le=250.0, description="Height in centimeters.")
    weight_kg: float = Field(..., ge=30.0, le=250.0, description="Weight in kilograms.")
    primary_discipline: SportDiscipline = Field(default=SportDiscipline.TRAIL_RUNNING)
    secondary_disciplines: List[SportDiscipline] = Field(default_factory=list)
    training_age_years: float = Field(default=1.0, ge=0.0, description="Years of structured training history.")
    vo2max_estimate: Optional[float] = Field(default=None, description="Estimated VO2max in ml/kg/min.")
    threshold_pace_min_km: Optional[str] = Field(default=None, description="Lactate threshold pace (e.g., '3:45/km').")
    max_heart_rate: int = Field(default=195, ge=100, le=240, description="Maximal heart rate in bpm.")
    resting_heart_rate: int = Field(default=50, ge=30, le=120, description="Resting heart rate in bpm.")
    injuries: List[InjuryRecord] = Field(default_factory=list, description="Historical and active injury records.")
    biometrics: BiometricState = Field(default_factory=BiometricState, description="Biometric state and history.")
    dietary_restrictions: List[str] = Field(
        default_factory=list,
        description="Dietary requirements (e.g. 'vegan', 'low_fodmap', 'celiac', 'dairy_free')."
    )
    equipment_access: List[str] = Field(
        default_factory=lambda: ["running_shoes", "gym_dumbbells", "resistance_bands"],
        description="Available training equipment."
    )
    intervals_icu_connected: bool = Field(default=False, description="Whether Intervals.icu sync is active.")
    strava_connected: bool = Field(default=False, description="Whether Strava sync is active.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary custom tenant metadata.")

    @property
    def active_injuries(self) -> List[InjuryRecord]:
        """Returns list of currently active injuries."""
        return [inj for inj in self.injuries if inj.is_active]

    @property
    def active_contraindications(self) -> List[str]:
        """Aggregates all active contraindicated movement strings across all active injuries."""
        contra = []
        for inj in self.active_injuries:
            contra.extend(inj.contraindicated_movements)
        return list(set(contra))

    def has_contraindication_for(self, exercise_or_movement: str) -> bool:
        """Checks if a given exercise or movement pattern is contraindicated."""
        normalized = exercise_or_movement.lower().strip()
        for c in self.active_contraindications:
            if c.lower() in normalized or normalized in c.lower():
                return True
        return False

    def add_injury(self, injury: InjuryRecord) -> None:
        """Adds or updates an injury record."""
        self.injuries = [inj for inj in self.injuries if inj.injury_id != injury.injury_id]
        self.injuries.append(injury)

    def resolve_injury(self, injury_id: str) -> bool:
        """Marks an active injury as resolved / inactive."""
        for inj in self.injuries:
            if inj.injury_id == injury_id:
                inj.is_active = False
                inj.rehab_phase = RehabPhase.MAINTENANCE
                inj.current_pain_score = 0
                return True
        return False
