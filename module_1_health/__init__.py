"""
Module 1: Financial Health Analyzer
====================================
Purpose: Assess user's current financial health WITHOUT credit/default labels.

Key Principle: NO ML training, pure analysis and clustering.

Usage:
    from src.module_1_health import HealthAnalyzer
    
    analyzer = HealthAnalyzer()
    result = analyzer.analyze({
        'income': 15_000_000,
        'fixed_expenses': 8_000_000,
        'variable_expenses': 3_000_000,
        'savings': 20_000_000,
        'debt': 50_000_000
    })
"""

from .health_analyzer import HealthAnalyzer

__all__ = ['HealthAnalyzer']
