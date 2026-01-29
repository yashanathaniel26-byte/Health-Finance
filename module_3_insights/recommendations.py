"""
Recommendation Engine
======================
Purpose: Generate actionable recommendations.

Output:
- Priority actions
- Quick wins
- Long-term strategies

Key Principles:
- Actionable & specific
- Prioritized by impact
- Non-binding (advisory only)
- Based on root cause & scenarios
"""

from typing import Dict, List, Optional


def generate_health_recommendations(
    health_result: Dict,
    scenario_results: Optional[Dict] = None
) -> List[Dict]:
    """
    Generate recommendations to improve financial health.
    
    Args:
        health_result: Results from Module 1
        scenario_results: Optional scenario analysis results
        
    Returns:
        List of health improvement recommendations
    """
    recommendations = []
    
    health_score = health_result['score']
    status = health_result['status']
    risk_flags = health_result['risk_flags']
    metrics = health_result['metrics']
    
    # High Debt Burden
    if 'high_debt_burden' in risk_flags:
        dti = metrics['debt_to_income_ratio']
        recommendations.append({
            'category': 'Debt Management',
            'priority': 'high',
            'action': 'Fokus Pelunasan Debt',
            'detail': f'DTI ratio saat ini {dti:.2f}x. Target: < 3.0x',
            'steps': [
                'Prioritaskan pelunasan debt dengan bunga tertinggi',
                'Pertimbangkan debt consolidation',
                'Hindari tambahan debt baru',
                f'Target pengurangan debt minimal 30% (scenario analysis menunjukkan improvement signifikan)'
            ],
            'expected_impact': 'Mengurangi beban bulanan dan meningkatkan health score 15-25 poin',
            'timeframe': '6-12 bulan'
        })
    
    # Excessive Expenses
    if 'excessive_expenses' in risk_flags:
        expense_ratio = metrics['expense_ratio']
        recommendations.append({
            'category': 'Expense Optimization',
            'priority': 'high',
            'action': 'Kurangi Pengeluaran Non-Esensial',
            'detail': f'Expense ratio {expense_ratio:.1%}. Target: < 70%',
            'steps': [
                'Review dan kategorikan semua pengeluaran',
                'Identifikasi 3 area pengeluaran terbesar',
                'Target pengurangan 10-15% dari variable expenses',
                'Terapkan budgeting ketat selama 3 bulan pertama'
            ],
            'expected_impact': 'Meningkatkan disposable income dan health score 10-20 poin',
            'timeframe': '3-6 bulan'
        })
    
    # Insufficient Savings
    if 'insufficient_savings' in risk_flags:
        savings_ratio = metrics['savings_ratio']
        income = health_result.get('income', 0)  # If available
        recommendations.append({
            'category': 'Savings Building',
            'priority': 'medium',
            'action': 'Bangun Dana Darurat',
            'detail': f'Savings ratio {savings_ratio:.1f} bulan. Target: minimal 3-6 bulan',
            'steps': [
                'Set automatic transfer 10-15% income ke savings account',
                'Pisahkan rekening untuk dana darurat',
                'Target: akumulasi 3 bulan income dalam 12 bulan',
                'Gunakan windfall (bonus, THR) untuk accelerate savings'
            ],
            'expected_impact': 'Meningkatkan resilience dan health score 10-15 poin',
            'timeframe': '12-18 bulan'
        })
    
    # Negative Cashflow
    if 'negative_cashflow' in risk_flags:
        recommendations.append({
            'category': 'Cashflow Management',
            'priority': 'critical',
            'action': 'URGENT: Perbaiki Cashflow Negatif',
            'detail': 'Pengeluaran melebihi pendapatan - tidak sustainable',
            'steps': [
                'IMMEDIATE: Stop semua pengeluaran non-esensial',
                'Cari sumber income tambahan (side hustle, overtime)',
                'Negosiasi ulang biaya tetap (sewa, utilities)',
                'Pertimbangkan lifestyle downgrade sementara'
            ],
            'expected_impact': 'Critical untuk survival finansial',
            'timeframe': 'Immediate (1-3 bulan)'
        })
    
    # General health improvement (if no critical issues)
    if health_score >= 50 and health_score < 75:
        recommendations.append({
            'category': 'General Improvement',
            'priority': 'medium',
            'action': 'Optimasi Profil Finansial',
            'detail': 'Health score baik tapi ada ruang untuk improvement',
            'steps': [
                'Tingkatkan savings rate secara bertahap',
                'Diversifikasi income sources',
                'Review asuransi coverage',
                'Mulai financial planning jangka panjang'
            ],
            'expected_impact': 'Meningkatkan health score ke kategori "Healthy" (>75)',
            'timeframe': '6-12 bulan'
        })
    
    # Sort by priority
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
    
    return recommendations


def generate_loan_recommendations(
    loan_result: Dict,
    loan_request: Dict,
    scenario_results: Optional[Dict] = None
) -> List[Dict]:
    """
    Generate recommendations for loan structure optimization.
    
    Args:
        loan_result: Results from Module 2
        loan_request: Original loan request
        scenario_results: Optional scenario analysis results
        
    Returns:
        List of loan optimization recommendations
    """
    recommendations = []
    
    default_probability = loan_result['default_probability']
    risk_category = loan_result['risk_category']
    
    # High default risk
    if default_probability > 0.6:
        recommendations.append({
            'category': 'Loan Structure',
            'priority': 'critical',
            'action': 'Restrukturisasi Pinjaman URGENT',
            'detail': f'Default probability {default_probability:.1%} sangat tinggi',
            'steps': [
                'Pertimbangkan MENUNDA aplikasi pinjaman',
                'Perbaiki financial health terlebih dahulu',
                f'Jika urgent: kurangi jumlah pinjaman minimal 25-30%',
                'Atau perpanjang tenor untuk mengurangi beban per periode'
            ],
            'expected_impact': 'Mengurangi default probability 15-25%',
            'timeframe': 'Immediate'
        })
    
    # Medium-high risk
    elif default_probability > 0.4:
        recommendations.append({
            'category': 'Loan Structure',
            'priority': 'high',
            'action': 'Optimasi Parameter Pinjaman',
            'detail': f'Default probability {default_probability:.1%} cukup tinggi',
            'steps': [
                'Kurangi jumlah pinjaman 15-20% jika memungkinkan',
                'Perpanjang durasi untuk menurunkan beban bulanan',
                'Tingkatkan down payment jika ada',
                'Pertimbangkan jaminan tambahan'
            ],
            'expected_impact': 'Mengurangi default probability 10-15%',
            'timeframe': '1-2 bulan'
        })
    
    # Scenario-based recommendations
    if scenario_results and scenario_results.get('best_scenario'):
        best = scenario_results['best_scenario']
        impact = best.get('impact_score', 0)
        
        if impact > 5:  # Significant improvement possible
            recommendations.append({
                'category': 'Scenario-Based',
                'priority': 'high',
                'action': f"Implement: {best['scenario']}",
                'detail': f"Change: {best['change']}",
                'steps': [
                    f"Scenario analysis menunjukkan {best['scenario']} paling efektif",
                    f"Expected improvement: {impact:.1f} points",
                    "Detail steps sesuai scenario recommendation"
                ],
                'expected_impact': f"Impact score: {impact:.1f}",
                'timeframe': 'As per scenario'
            })
    
    # Collateral recommendations
    jaminan = loan_request.get('jenis_jaminan', '')
    if jaminan in ['Tanpa Jaminan', 'Unknown', '']:
        recommendations.append({
            'category': 'Risk Mitigation',
            'priority': 'medium',
            'action': 'Pertimbangkan Penambahan Jaminan',
            'detail': 'Pinjaman tanpa jaminan memiliki risiko lebih tinggi',
            'steps': [
                'Evaluasi aset yang bisa dijadikan jaminan',
                'Jaminan dapat menurunkan risk assessment',
                'Potentially better terms and lower rates'
            ],
            'expected_impact': 'Moderate risk reduction',
            'timeframe': '1-2 bulan'
        })
    
    return recommendations


def generate_integrated_recommendations(
    health_result: Dict,
    loan_result: Dict,
    loan_request: Dict,
    root_cause: Dict,
    scenario_results: Optional[Dict] = None
) -> Dict:
    """
    Generate comprehensive integrated recommendations.
    
    Args:
        health_result: Results from Module 1
        loan_result: Results from Module 2
        loan_request: Original loan request
        root_cause: Root cause analysis results
        scenario_results: Optional scenario analysis
        
    Returns:
        Comprehensive recommendation package
    """
    # Generate recommendations from both dimensions
    health_recs = generate_health_recommendations(health_result, scenario_results)
    loan_recs = generate_loan_recommendations(loan_result, loan_request, scenario_results)
    
    # Combine and prioritize
    all_recommendations = health_recs + loan_recs
    
    # Sort by priority
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    all_recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
    
    # Identify quick wins (high impact, short timeframe)
    quick_wins = []
    for rec in all_recommendations:
        timeframe = rec.get('timeframe', '')
        priority = rec.get('priority', '')
        
        if priority in ['high', 'critical'] and any(word in timeframe.lower() for word in ['immediate', '1-3', '3-6']):
            quick_wins.append(rec)
    
    # Generate executive summary
    critical_count = len([r for r in all_recommendations if r['priority'] == 'critical'])
    high_count = len([r for r in all_recommendations if r['priority'] == 'high'])
    
    if critical_count > 0:
        summary = f"URGENT: {critical_count} tindakan kritis diperlukan. Fokus pada perbaikan cashflow dan debt management."
    elif high_count > 0:
        summary = f"{high_count} tindakan prioritas tinggi. Fokus pada optimasi struktur pinjaman dan pengeluaran."
    else:
        summary = "Profil relatif baik. Fokus pada optimasi dan pertumbuhan jangka panjang."
    
    # Generate action plan
    action_plan = {
        'phase_1_immediate': [r for r in all_recommendations if 'immediate' in r.get('timeframe', '').lower()][:3],
        'phase_2_short_term': [r for r in all_recommendations if any(w in r.get('timeframe', '').lower() for w in ['1-3', '3-6'])][:3],
        'phase_3_long_term': [r for r in all_recommendations if any(w in r.get('timeframe', '').lower() for w in ['6-12', '12-18'])][:3]
    }
    
    return {
        'summary': summary,
        'total_recommendations': len(all_recommendations),
        'by_priority': {
            'critical': critical_count,
            'high': high_count,
            'medium': len([r for r in all_recommendations if r['priority'] == 'medium']),
            'low': len([r for r in all_recommendations if r['priority'] == 'low'])
        },
        'all_recommendations': all_recommendations,
        'quick_wins': quick_wins[:5],
        'action_plan': action_plan,
        'top_3_priorities': all_recommendations[:3]
    }
