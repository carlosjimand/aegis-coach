"""
Aegis Coach — Specialized Multi-Agent Swarm Modules
"""

from poc.agents.base_agent import BaseAgent
from poc.agents.medical_agent import MedicalAgent
from poc.agents.planner_agent import PlannerAgent
from poc.agents.nutrition_agent import NutritionAgent
from poc.agents.data_entry_agent import DataEntryAgent
from poc.agents.general_agent import GeneralAgent

__all__ = [
    "BaseAgent",
    "MedicalAgent",
    "PlannerAgent",
    "NutritionAgent",
    "DataEntryAgent",
    "GeneralAgent",
]
