"""
Rule-Based Health Assessment
=============================
Purpose: Apply business rules to assess financial health.

Rules:
- DTI thresholds
- Savings adequacy
- Expense efficiency
- Risk flags

Key Principles:
- Explainable & deterministic
- Anti-bias (ratio-based, not absolute values)
- NO credit/default labels
- Transparent scoring logic
"""

from typing import Dict, List, Tuple


# Thresholds (configurable)
DTI_THRESHOLDS = {
    "excellent": 1.0,   # Debt < 1x monthly income
    "good": 3.0,        # Debt < 3x monthly income
    "warning": 6.0,     # Debt < 6x monthly income
    "critical": 12.0    # Debt >= 12x monthly income is critical
}

EXPENSE_RATIO_THRESHOLDS = {
    "excellent": 0.50,  # Expenses < 50% of income
    "good": 0.70,       # Expenses < 70% of income
    "warning": 0.85,    # Expenses < 85% of income
    "critical": 1.0     # Expenses >= 100% of income
}

SAVINGS_RATIO_THRESHOLDS = {
    "excellent": 6.0,   # Savings >= 6 months income
    "good": 3.0,        # Savings >= 3 months income
    "warning": 1.0,     # Savings >= 1 month income
    "critical": 0.0     # No savings
}

DISPOSABLE_INCOME_RATIO_THRESHOLDS = {
    "excellent": 0.30,  # 30%+ disposable income
    "good": 0.15,       # 15%+ disposable income
    "warning": 0.05,    # 5%+ disposable income
    "critical": 0.0     # Negative or zero disposable income
}


def assess_dti(dti_ratio: float) -> Tuple[int, str, str]:
    """
    Assess Debt-to-Income ratio.
    
    Args:
        dti_ratio: Debt-to-income ratio
        
    Returns:
        Tuple of (score, level, explanation)
    """
    if dti_ratio <= DTI_THRESHOLDS["excellent"]:
        return 100, "excellent", "Debt beban sangat rendah (< 1x pendapatan bulanan)"
    elif dti_ratio <= DTI_THRESHOLDS["good"]:
        return 80, "good", "Debt beban terkendali (1-3x pendapatan bulanan)"
    elif dti_ratio <= DTI_THRESHOLDS["warning"]:
        return 50, "warning", "Debt beban tinggi (3-6x pendapatan bulanan)"
    elif dti_ratio <= DTI_THRESHOLDS["critical"]:
        return 25, "at_risk", "Debt beban sangat tinggi (6-12x pendapatan bulanan)"
    else:
        return 0, "critical", "Debt beban kritis (>12x pendapatan bulanan)"


def assess_expense_ratio(expense_ratio: float) -> Tuple[int, str, str]:
    """
    Assess expense efficiency.
    
    Args:
        expense_ratio: Total expenses / income
        
    Returns:
        Tuple of (score, level, explanation)
    """
    if expense_ratio <= EXPENSE_RATIO_THRESHOLDS["excellent"]:
        return 100, "excellent", "Pengeluaran sangat efisien (<50% pendapatan)"
    elif expense_ratio <= EXPENSE_RATIO_THRESHOLDS["good"]:
        return 80, "good", "Pengeluaran terkendali (50-70% pendapatan)"
    elif expense_ratio <= EXPENSE_RATIO_THRESHOLDS["warning"]:
        return 50, "warning", "Pengeluaran tinggi (70-85% pendapatan)"
    elif expense_ratio < EXPENSE_RATIO_THRESHOLDS["critical"]:
        return 25, "at_risk", "Pengeluaran sangat tinggi (85-100% pendapatan)"
    else:
        return 0, "critical", "Pengeluaran melebihi pendapatan (>100%)"


def assess_savings_ratio(savings_ratio: float) -> Tuple[int, str, str]:
    """
    Assess savings adequacy.
    
    Args:
        savings_ratio: Savings / monthly income
        
    Returns:
        Tuple of (score, level, explanation)
    """
    if savings_ratio >= SAVINGS_RATIO_THRESHOLDS["excellent"]:
        return 100, "excellent", "Dana darurat sangat memadai (>=6 bulan pendapatan)"
    elif savings_ratio >= SAVINGS_RATIO_THRESHOLDS["good"]:
        return 80, "good", "Dana darurat memadai (3-6 bulan pendapatan)"
    elif savings_ratio >= SAVINGS_RATIO_THRESHOLDS["warning"]:
        return 50, "warning", "Dana darurat minimal (1-3 bulan pendapatan)"
    elif savings_ratio > SAVINGS_RATIO_THRESHOLDS["critical"]:
        return 25, "at_risk", "Dana darurat sangat terbatas (<1 bulan pendapatan)"
    else:
        return 0, "critical", "Tidak ada dana darurat"


def assess_disposable_income_ratio(disposable_ratio: float) -> Tuple[int, str, str]:
    """
    Assess cashflow health.
    
    Args:
        disposable_ratio: (Income - Expenses) / Income
        
    Returns:
        Tuple of (score, level, explanation)
    """
    if disposable_ratio >= DISPOSABLE_INCOME_RATIO_THRESHOLDS["excellent"]:
        return 100, "excellent", "Cashflow sangat sehat (>30% pendapatan bebas)"
    elif disposable_ratio >= DISPOSABLE_INCOME_RATIO_THRESHOLDS["good"]:
        return 80, "good", "Cashflow sehat (15-30% pendapatan bebas)"
    elif disposable_ratio >= DISPOSABLE_INCOME_RATIO_THRESHOLDS["warning"]:
        return 50, "warning", "Cashflow terbatas (5-15% pendapatan bebas)"
    elif disposable_ratio > DISPOSABLE_INCOME_RATIO_THRESHOLDS["critical"]:
        return 25, "at_risk", "Cashflow sangat terbatas (<5% pendapatan bebas)"
    else:
        return 0, "critical", "Cashflow negatif (pengeluaran > pendapatan)"


def calculate_health_score(metrics: Dict[str, float]) -> Dict[str, any]:
    """
    Calculate overall health score from metrics.
    
    Args:
        metrics: Dictionary of financial metrics
        
    Returns:
        Dictionary containing:
        - score: Overall health score (0-100)
        - status: Health status (Healthy/Warning/At Risk)
        - component_scores: Individual assessment scores
        - explanations: Explanations for each component
        - risk_flags: List of identified risks
    """
    # Assess each component
    dti_score, dti_level, dti_explanation = assess_dti(metrics["debt_to_income_ratio"])
    expense_score, expense_level, expense_explanation = assess_expense_ratio(metrics["expense_ratio"])
    savings_score, savings_level, savings_explanation = assess_savings_ratio(metrics["savings_ratio"])
    cashflow_score, cashflow_level, cashflow_explanation = assess_disposable_income_ratio(
        metrics["disposable_income_ratio"]
    )
    
    # Weighted average (cashflow and DTI are more critical)
    weights = {
        "dti": 0.30,
        "expense": 0.20,
        "savings": 0.20,
        "cashflow": 0.30
    }
    
    overall_score = (
        dti_score * weights["dti"] +
        expense_score * weights["expense"] +
        savings_score * weights["savings"] +
        cashflow_score * weights["cashflow"]
    )
    
    # Determine overall status
    if overall_score >= 75:
        status = "Healthy"
    elif overall_score >= 50:
        status = "Warning"
    else:
        status = "At Risk"
    
    # Identify risk flags
    risk_flags = []
    if dti_level in ["at_risk", "critical"]:
        risk_flags.append("high_debt_burden")
    if expense_level in ["at_risk", "critical"]:
        risk_flags.append("excessive_expenses")
    if savings_level in ["at_risk", "critical"]:
        risk_flags.append("insufficient_savings")
    if cashflow_level in ["at_risk", "critical"]:
        risk_flags.append("negative_cashflow")
    
    return {
        "score": round(overall_score, 1),
        "status": status,
        "component_scores": {
            "debt_to_income": dti_score,
            "expense_efficiency": expense_score,
            "savings_adequacy": savings_score,
            "cashflow_health": cashflow_score
        },
        "explanations": {
            "debt_to_income": dti_explanation,
            "expense_efficiency": expense_explanation,
            "savings_adequacy": savings_explanation,
            "cashflow_health": cashflow_explanation
        },
        "risk_flags": risk_flags
    }
