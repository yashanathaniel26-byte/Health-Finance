"""
Root Cause Analysis
===================
Purpose: Identify root causes of high default risk.

Output:
- Primary risk factors
- Contributing factors
- Weakness areas

Key Principles:
- Integrate Module 1 (health) + Module 2 (prediction)
- Explainable reasoning
- Actionable insights
- NO model modification
"""

from typing import Dict, List, Optional


def analyze_financial_health_impact(
    health_result: Dict,
    loan_result: Dict
) -> Dict:
    """
    Analyze how financial health contributes to default risk.
    
    Args:
        health_result: Results from Module 1 (HealthAnalyzer)
        loan_result: Results from Module 2 (LoanPredictor)
        
    Returns:
        Dictionary with health impact analysis
    """
    health_score = health_result['score']
    health_status = health_result['status']
    risk_flags = health_result['risk_flags']
    default_probability = loan_result['default_probability']
    
    # Correlation analysis
    health_impact = {
        'health_score': health_score,
        'health_status': health_status,
        'default_probability': default_probability,
        'correlation': 'negative',  # Lower health = higher default risk
        'impact_level': 'high' if health_score < 50 else 'medium' if health_score < 75 else 'low'
    }
    
    # Identify which health metrics are problematic
    contributing_health_factors = []
    
    if 'high_debt_burden' in risk_flags:
        contributing_health_factors.append({
            'factor': 'High Debt Burden',
            'severity': 'critical',
            'explanation': 'DTI ratio tinggi menunjukkan beban debt yang berlebihan',
            'impact_on_default': 'Meningkatkan risiko gagal bayar secara signifikan'
        })
    
    if 'excessive_expenses' in risk_flags:
        contributing_health_factors.append({
            'factor': 'Excessive Expenses',
            'severity': 'high',
            'explanation': 'Pengeluaran tidak terkendali mengurangi kemampuan bayar',
            'impact_on_default': 'Mengurangi cashflow untuk cicilan pinjaman'
        })
    
    if 'insufficient_savings' in risk_flags:
        contributing_health_factors.append({
            'factor': 'Insufficient Emergency Fund',
            'severity': 'medium',
            'explanation': 'Dana darurat tidak memadai untuk shock finansial',
            'impact_on_default': 'Meningkatkan risiko default saat ada kejadian tak terduga'
        })
    
    if 'negative_cashflow' in risk_flags:
        contributing_health_factors.append({
            'factor': 'Negative Cashflow',
            'severity': 'critical',
            'explanation': 'Pengeluaran melebihi pendapatan',
            'impact_on_default': 'Tidak sustainable untuk membayar cicilan tambahan'
        })
    
    health_impact['contributing_factors'] = contributing_health_factors
    
    return health_impact


def analyze_loan_characteristics(loan_result: Dict, loan_request: Dict) -> Dict:
    """
    Analyze loan characteristics that contribute to risk.
    
    Args:
        loan_result: Prediction results from Module 2
        loan_request: Original loan request data
        
    Returns:
        Dictionary with loan characteristic analysis
    """
    explanation = loan_result.get('explanation', {})
    risk_factors = explanation.get('risk_factors', [])
    
    # Extract loan features
    jumlah_pinjaman = loan_request.get('jumlah_pinjaman', 0)
    durasi_hari = loan_request.get('durasi_hari', 0)
    
    loan_characteristics = {
        'loan_amount': jumlah_pinjaman,
        'duration_days': durasi_hari,
        'risk_factors': []
    }
    
    # Analyze loan structure
    if jumlah_pinjaman > 50_000_000:
        loan_characteristics['risk_factors'].append({
            'factor': 'Large Loan Amount',
            'severity': 'high',
            'explanation': f'Jumlah pinjaman Rp {jumlah_pinjaman:,.0f} tergolong besar',
            'impact': 'Beban pengembalian yang tinggi'
        })
    
    if durasi_hari > 180:
        loan_characteristics['risk_factors'].append({
            'factor': 'Long Duration',
            'severity': 'medium',
            'explanation': f'Durasi {durasi_hari} hari cukup panjang',
            'impact': 'Meningkatkan ketidakpastian dan exposure risiko'
        })
    
    if durasi_hari < 30:
        loan_characteristics['risk_factors'].append({
            'factor': 'Very Short Duration',
            'severity': 'high',
            'explanation': f'Durasi {durasi_hari} hari sangat pendek',
            'impact': 'Beban pembayaran per periode sangat tinggi'
        })
    
    # Add model-identified risk factors
    for risk in risk_factors:
        loan_characteristics['risk_factors'].append({
            'factor': risk['factor'],
            'severity': risk['severity'],
            'explanation': risk['detail'],
            'impact': 'Teridentifikasi oleh model sebagai risk driver'
        })
    
    return loan_characteristics


def identify_primary_causes(
    health_result: Dict,
    loan_result: Dict,
    loan_request: Dict
) -> List[Dict]:
    """
    Identify primary root causes of high default risk.
    
    Args:
        health_result: Results from Module 1
        loan_result: Results from Module 2
        loan_request: Original loan request
        
    Returns:
        List of primary root causes, sorted by severity
    """
    # Analyze both dimensions
    health_impact = analyze_financial_health_impact(health_result, loan_result)
    loan_characteristics = analyze_loan_characteristics(loan_result, loan_request)
    
    # Combine all factors
    all_causes = []
    
    # Add health factors
    for factor in health_impact.get('contributing_factors', []):
        all_causes.append({
            'category': 'Financial Health',
            'cause': factor['factor'],
            'severity': factor['severity'],
            'explanation': factor['explanation'],
            'impact': factor['impact_on_default']
        })
    
    # Add loan factors
    for factor in loan_characteristics.get('risk_factors', []):
        all_causes.append({
            'category': 'Loan Characteristics',
            'cause': factor['factor'],
            'severity': factor['severity'],
            'explanation': factor['explanation'],
            'impact': factor['impact']
        })
    
    # Sort by severity
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    all_causes.sort(key=lambda x: severity_order.get(x['severity'], 4))
    
    return all_causes


def generate_root_cause_summary(
    health_result: Dict,
    loan_result: Dict,
    loan_request: Dict
) -> Dict:
    """
    Generate comprehensive root cause summary.
    
    Args:
        health_result: Results from Module 1
        loan_result: Results from Module 2
        loan_request: Original loan request
        
    Returns:
        Comprehensive root cause analysis
    """
    primary_causes = identify_primary_causes(health_result, loan_result, loan_request)
    health_impact = analyze_financial_health_impact(health_result, loan_result)
    loan_characteristics = analyze_loan_characteristics(loan_result, loan_request)
    
    # Determine overall risk profile
    default_probability = loan_result['default_probability']
    health_score = health_result['score']
    
    if default_probability > 0.6 and health_score < 50:
        risk_profile = 'Critical - Both poor health and high loan risk'
    elif default_probability > 0.6:
        risk_profile = 'High - Loan structure issues despite okay health'
    elif health_score < 50:
        risk_profile = 'High - Poor financial health driving risk'
    elif default_probability > 0.4:
        risk_profile = 'Moderate - Some concerns in both areas'
    else:
        risk_profile = 'Low - Acceptable health and loan risk'
    
    # Generate executive summary
    if len(primary_causes) == 0:
        summary = "Tidak ada faktor risiko signifikan yang teridentifikasi. Profil baik secara kesehatan finansial maupun struktur pinjaman."
    else:
        top_cause = primary_causes[0]
        summary = f"Risiko utama: {top_cause['cause']}. {top_cause['explanation']}"
    
    return {
        'summary': summary,
        'risk_profile': risk_profile,
        'default_probability': default_probability,
        'health_score': health_score,
        'primary_causes': primary_causes[:5],  # Top 5
        'health_impact': health_impact,
        'loan_characteristics': loan_characteristics,
        'total_risk_factors': len(primary_causes),
        'critical_factors': len([c for c in primary_causes if c['severity'] == 'critical']),
        'high_factors': len([c for c in primary_causes if c['severity'] == 'high'])
    }
