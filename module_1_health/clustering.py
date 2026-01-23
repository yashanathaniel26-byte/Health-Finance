"""
Financial Persona Clustering
=============================
Purpose: Cluster users into financial personas using unsupervised ML.

Output: Financial persona (e.g., "Conservative Saver", "High Risk Spender")

Key Principles:
- Rule-based (deterministic, no random state at runtime)
- Descriptive, NOT judgemental
- NO credit/default labels
- Focus on financial behavior patterns
"""

from typing import Dict


def assign_financial_persona(metrics: Dict[str, float], health_assessment: Dict[str, any]) -> str:
    """
    Assign financial persona based on metrics and health assessment.
    
    Uses deterministic rule-based logic to categorize users into
    financial behavior personas.
    
    Args:
        metrics: Financial metrics dictionary
        health_assessment: Health assessment results
        
    Returns:
        Financial persona string
    """
    dti_ratio = metrics["debt_to_income_ratio"]
    expense_ratio = metrics["expense_ratio"]
    savings_ratio = metrics["savings_ratio"]
    disposable_ratio = metrics["disposable_income_ratio"]
    
    # Pattern 1: Conservative Saver
    # Low debt, low expenses, high savings
    if (dti_ratio < 1.0 and 
        expense_ratio < 0.60 and 
        savings_ratio >= 6.0):
        return "Conservative Saver"
    
    # Pattern 2: Stable & Balanced
    # Moderate debt, controlled expenses, adequate savings
    if (dti_ratio < 3.0 and 
        expense_ratio < 0.75 and 
        savings_ratio >= 3.0 and 
        disposable_ratio >= 0.15):
        return "Stable & Balanced"
    
    # Pattern 3: High Earner - High Spender
    # Low debt ratio BUT high expense ratio with good savings
    if (dti_ratio < 2.0 and 
        expense_ratio >= 0.70 and 
        savings_ratio >= 2.0):
        return "High Earner - High Spender"
    
    # Pattern 4: Debt Pressured
    # High debt, any expense level
    if dti_ratio >= 6.0:
        return "Debt Pressured"
    
    # Pattern 5: Cashflow Challenged
    # Negative or very low disposable income
    if disposable_ratio <= 0.05:
        return "Cashflow Challenged"
    
    # Pattern 6: Building Financial Foundation
    # Low savings but managing expenses well
    if (savings_ratio < 3.0 and 
        expense_ratio < 0.75 and 
        disposable_ratio >= 0.10):
        return "Building Financial Foundation"
    
    # Pattern 7: Frugal & Low Savings
    # Very low expenses but also low savings (might be low income)
    if (expense_ratio < 0.50 and 
        savings_ratio < 2.0):
        return "Frugal & Low Savings"
    
    # Pattern 8: Needs Expense Optimization
    # High expenses, moderate debt
    if (expense_ratio >= 0.85 and 
        dti_ratio < 6.0):
        return "Needs Expense Optimization"
    
    # Default: General Financial Profile
    return "General Financial Profile"


def get_persona_description(persona: str) -> str:
    """
    Get detailed description for each persona.
    
    Args:
        persona: Financial persona name
        
    Returns:
        Description of the persona
    """
    descriptions = {
        "Conservative Saver": "Memiliki pola keuangan yang sangat konservatif dengan debt rendah, pengeluaran efisien, dan dana darurat yang kuat.",
        "Stable & Balanced": "Profil keuangan yang seimbang dengan debt terkendali, pengeluaran moderat, dan savings memadai.",
        "High Earner - High Spender": "Pendapatan tinggi dengan pola pengeluaran tinggi, namun tetap mampu menjaga savings.",
        "Debt Pressured": "Memiliki beban debt yang tinggi relatif terhadap pendapatan, perlu fokus pada pengurangan debt.",
        "Cashflow Challenged": "Menghadapi tantangan cashflow dengan disposable income yang sangat terbatas atau negatif.",
        "Building Financial Foundation": "Sedang membangun fondasi keuangan dengan fokus pada akumulasi savings.",
        "Frugal & Low Savings": "Pola hidup hemat namun belum memiliki savings yang memadai.",
        "Needs Expense Optimization": "Perlu optimasi pengeluaran untuk meningkatkan kesehatan finansial.",
        "General Financial Profile": "Profil keuangan umum tanpa pola khusus yang menonjol."
    }
    
    return descriptions.get(persona, "Profil keuangan yang perlu evaluasi lebih lanjut.")


def get_persona_insights(persona: str) -> Dict[str, any]:
    """
    Get actionable insights for each persona.
    
    Args:
        persona: Financial persona name
        
    Returns:
        Dictionary with strengths and focus_areas
    """
    insights = {
        "Conservative Saver": {
            "strengths": ["Disiplin menabung", "Debt rendah", "Pengeluaran terkendali"],
            "focus_areas": ["Pertimbangkan investasi untuk optimasi return", "Maintain current habits"]
        },
        "Stable & Balanced": {
            "strengths": ["Keuangan seimbang", "Savings memadai", "Cashflow sehat"],
            "focus_areas": ["Tingkatkan savings ratio secara bertahap", "Monitor debt levels"]
        },
        "High Earner - High Spender": {
            "strengths": ["Income tinggi", "Mampu maintain savings"],
            "focus_areas": ["Evaluasi efisiensi pengeluaran", "Optimalkan savings rate"]
        },
        "Debt Pressured": {
            "strengths": ["Awareness terhadap situasi keuangan"],
            "focus_areas": ["Prioritas: pelunasan debt", "Evaluasi ulang komitmen debt baru"]
        },
        "Cashflow Challenged": {
            "strengths": ["Awareness terhadap tantangan"],
            "focus_areas": ["Urgent: tingkatkan income atau kurangi expenses", "Review all expenses"]
        },
        "Building Financial Foundation": {
            "strengths": ["Pengeluaran terkendali", "Positive cashflow"],
            "focus_areas": ["Akselerasi pembangunan dana darurat", "Maintain expense discipline"]
        },
        "Frugal & Low Savings": {
            "strengths": ["Gaya hidup hemat", "Pengeluaran rendah"],
            "focus_areas": ["Cari peluang peningkatan income", "Alokasikan surplus untuk savings"]
        },
        "Needs Expense Optimization": {
            "strengths": ["Debt masih terkendali"],
            "focus_areas": ["Review dan kurangi pengeluaran non-esensial", "Buat budget yang ketat"]
        },
        "General Financial Profile": {
            "strengths": ["Kondisi keuangan netral"],
            "focus_areas": ["Identifikasi area improvement spesifik", "Set financial goals yang jelas"]
        }
    }
    
    return insights.get(persona, {
        "strengths": ["Perlu evaluasi mendalam"],
        "focus_areas": ["Konsultasi dengan financial advisor"]
    })
