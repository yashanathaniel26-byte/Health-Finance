"""
Module 3: Insight & Decision Intelligence
==========================================
Purpose: Integrate health + prediction for actionable insights.

Key Principle: This is where reasoning happens.

Exports:
- InsightEngine: Main orchestrator
- root_cause: Root cause analysis functions
- scenarios: What-if scenario functions
- recommendations: Recommendation generation functions
"""

from .insight_engine import InsightEngine
from . import root_cause
from . import scenarios
from . import recommendations

__all__ = [
    'InsightEngine',
    'root_cause',
    'scenarios',
    'recommendations'
]
