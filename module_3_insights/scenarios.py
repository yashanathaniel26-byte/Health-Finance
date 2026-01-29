"""
What-If Scenario Simulation
============================
Purpose: Simulate scenarios to improve financial health.

Scenarios:
- Increase income by X%
- Reduce debt by Y
- Increase savings rate
- Adjust loan parameters

Key Principles:
- Re-use Module 1 & 2 for predictions
- NO model modification
- Actionable what-if analysis
"""

from typing import Dict, List, Optional, Callable
import copy


def simulate_income_increase(
    health_analyzer,
    loan_predictor,
    current_profile: Dict,
    loan_request: Dict,
    increase_percentage: float
) -> Dict:
    """
    Simulate impact of income increase.
    
    Args:
        health_analyzer: Instance of HealthAnalyzer
        loan_predictor: Instance of LoanPredictor
        current_profile: Current financial profile
        loan_request: Loan request data
        increase_percentage: Income increase % (e.g., 0.20 for 20%)
        
    Returns:
        Scenario results with before/after comparison
    """
    # Create new profile with increased income
    new_profile = copy.deepcopy(current_profile)
    old_income = new_profile['income']
    new_income = old_income * (1 + increase_percentage)
    new_profile['income'] = new_income
    
    # Re-analyze health
    new_health = health_analyzer.analyze(new_profile)
    
    # Re-predict default risk
    new_loan_result = loan_predictor.predict(loan_request, include_explanation=False)
    
    return {
        'scenario': 'Income Increase',
        'change': f"+{increase_percentage*100:.0f}%",
        'old_value': old_income,
        'new_value': new_income,
        'health_impact': {
            'old_score': None,  # Will be filled by caller
            'new_score': new_health['score'],
            'improvement': None  # Will be calculated
        },
        'risk_impact': {
            'old_probability': None,  # Will be filled by caller
            'new_probability': new_loan_result['default_probability'],
            'reduction': None  # Will be calculated
        },
        'new_health': new_health,
        'new_loan_result': new_loan_result
    }


def simulate_debt_reduction(
    health_analyzer,
    current_profile: Dict,
    reduction_percentage: float
) -> Dict:
    """
    Simulate impact of debt reduction.
    
    Args:
        health_analyzer: Instance of HealthAnalyzer
        current_profile: Current financial profile
        reduction_percentage: Debt reduction % (e.g., 0.30 for 30%)
        
    Returns:
        Scenario results
    """
    new_profile = copy.deepcopy(current_profile)
    old_debt = new_profile['debt']
    new_debt = old_debt * (1 - reduction_percentage)
    new_profile['debt'] = new_debt
    
    # Re-analyze health
    new_health = health_analyzer.analyze(new_profile)
    
    return {
        'scenario': 'Debt Reduction',
        'change': f"-{reduction_percentage*100:.0f}%",
        'old_value': old_debt,
        'new_value': new_debt,
        'health_impact': {
            'new_score': new_health['score']
        },
        'new_health': new_health
    }


def simulate_expense_reduction(
    health_analyzer,
    loan_predictor,
    current_profile: Dict,
    loan_request: Dict,
    reduction_percentage: float
) -> Dict:
    """
    Simulate impact of expense reduction.
    
    Args:
        health_analyzer: Instance of HealthAnalyzer
        loan_predictor: Instance of LoanPredictor
        current_profile: Current financial profile
        loan_request: Loan request data
        reduction_percentage: Expense reduction % (e.g., 0.15 for 15%)
        
    Returns:
        Scenario results
    """
    new_profile = copy.deepcopy(current_profile)
    old_fixed = new_profile['fixed_expenses']
    old_variable = new_profile['variable_expenses']
    
    new_profile['fixed_expenses'] = old_fixed * (1 - reduction_percentage)
    new_profile['variable_expenses'] = old_variable * (1 - reduction_percentage)
    
    # Re-analyze health
    new_health = health_analyzer.analyze(new_profile)
    
    # Re-predict default risk
    new_loan_result = loan_predictor.predict(loan_request, include_explanation=False)
    
    return {
        'scenario': 'Expense Reduction',
        'change': f"-{reduction_percentage*100:.0f}%",
        'old_value': old_fixed + old_variable,
        'new_value': new_profile['fixed_expenses'] + new_profile['variable_expenses'],
        'health_impact': {
            'new_score': new_health['score']
        },
        'risk_impact': {
            'new_probability': new_loan_result['default_probability']
        },
        'new_health': new_health,
        'new_loan_result': new_loan_result
    }


def simulate_savings_increase(
    health_analyzer,
    current_profile: Dict,
    increase_amount: float
) -> Dict:
    """
    Simulate impact of increasing savings.
    
    Args:
        health_analyzer: Instance of HealthAnalyzer
        current_profile: Current financial profile
        increase_amount: Amount to add to savings
        
    Returns:
        Scenario results
    """
    new_profile = copy.deepcopy(current_profile)
    old_savings = new_profile['savings']
    new_savings = old_savings + increase_amount
    new_profile['savings'] = new_savings
    
    # Re-analyze health
    new_health = health_analyzer.analyze(new_profile)
    
    return {
        'scenario': 'Savings Increase',
        'change': f"+Rp {increase_amount:,.0f}",
        'old_value': old_savings,
        'new_value': new_savings,
        'health_impact': {
            'new_score': new_health['score']
        },
        'new_health': new_health
    }


def simulate_loan_amount_reduction(
    loan_predictor,
    loan_request: Dict,
    reduction_percentage: float
) -> Dict:
    """
    Simulate impact of reducing loan amount.
    
    Args:
        loan_predictor: Instance of LoanPredictor
        loan_request: Original loan request
        reduction_percentage: Loan amount reduction % (e.g., 0.25 for 25%)
        
    Returns:
        Scenario results
    """
    new_loan_request = copy.deepcopy(loan_request)
    old_amount = new_loan_request['jumlah_pinjaman']
    new_amount = old_amount * (1 - reduction_percentage)
    new_loan_request['jumlah_pinjaman'] = new_amount
    
    # Re-predict
    new_loan_result = loan_predictor.predict(new_loan_request, include_explanation=False)
    
    return {
        'scenario': 'Loan Amount Reduction',
        'change': f"-{reduction_percentage*100:.0f}%",
        'old_value': old_amount,
        'new_value': new_amount,
        'risk_impact': {
            'new_probability': new_loan_result['default_probability']
        },
        'new_loan_result': new_loan_result
    }


def simulate_duration_adjustment(
    loan_predictor,
    loan_request: Dict,
    new_duration_days: int
) -> Dict:
    """
    Simulate impact of adjusting loan duration.
    
    Args:
        loan_predictor: Instance of LoanPredictor
        loan_request: Original loan request
        new_duration_days: New duration in days
        
    Returns:
        Scenario results
    """
    new_loan_request = copy.deepcopy(loan_request)
    old_duration = new_loan_request['durasi_hari']
    new_loan_request['durasi_hari'] = new_duration_days
    
    # Re-predict
    new_loan_result = loan_predictor.predict(new_loan_request, include_explanation=False)
    
    return {
        'scenario': 'Duration Adjustment',
        'change': f"{old_duration} → {new_duration_days} hari",
        'old_value': old_duration,
        'new_value': new_duration_days,
        'risk_impact': {
            'new_probability': new_loan_result['default_probability']
        },
        'new_loan_result': new_loan_result
    }


def run_scenario_analysis(
    health_analyzer,
    loan_predictor,
    current_health: Dict,
    current_loan_result: Dict,
    financial_profile: Dict,
    loan_request: Dict,
    scenarios_to_run: Optional[List[str]] = None
) -> Dict:
    """
    Run comprehensive what-if scenario analysis.
    
    Args:
        health_analyzer: Instance of HealthAnalyzer
        loan_predictor: Instance of LoanPredictor
        current_health: Current health analysis results
        current_loan_result: Current loan prediction results
        financial_profile: Current financial profile
        loan_request: Loan request data
        scenarios_to_run: Optional list of specific scenarios
        
    Returns:
        Dictionary with all scenario results
    """
    current_health_score = current_health['score']
    current_default_prob = current_loan_result['default_probability']
    
    all_scenarios = []
    
    # Default scenarios to run
    if scenarios_to_run is None:
        scenarios_to_run = [
            'income_increase_20',
            'debt_reduction_30',
            'expense_reduction_15',
            'loan_reduction_25',
            'duration_extend_30'
        ]
    
    # Income increase scenarios
    if 'income_increase_20' in scenarios_to_run:
        result = simulate_income_increase(
            health_analyzer, loan_predictor, financial_profile, loan_request, 0.20
        )
        result['health_impact']['old_score'] = current_health_score
        result['health_impact']['improvement'] = result['health_impact']['new_score'] - current_health_score
        result['risk_impact']['old_probability'] = current_default_prob
        result['risk_impact']['reduction'] = current_default_prob - result['risk_impact']['new_probability']
        all_scenarios.append(result)
    
    # Debt reduction scenarios
    if 'debt_reduction_30' in scenarios_to_run:
        result = simulate_debt_reduction(health_analyzer, financial_profile, 0.30)
        result['health_impact']['old_score'] = current_health_score
        result['health_impact']['improvement'] = result['health_impact']['new_score'] - current_health_score
        all_scenarios.append(result)
    
    # Expense reduction scenarios
    if 'expense_reduction_15' in scenarios_to_run:
        result = simulate_expense_reduction(
            health_analyzer, loan_predictor, financial_profile, loan_request, 0.15
        )
        result['health_impact']['old_score'] = current_health_score
        result['health_impact']['improvement'] = result['health_impact']['new_score'] - current_health_score
        result['risk_impact']['old_probability'] = current_default_prob
        result['risk_impact']['reduction'] = current_default_prob - result['risk_impact']['new_probability']
        all_scenarios.append(result)
    
    # Loan amount reduction
    if 'loan_reduction_25' in scenarios_to_run:
        result = simulate_loan_amount_reduction(loan_predictor, loan_request, 0.25)
        result['risk_impact']['old_probability'] = current_default_prob
        result['risk_impact']['reduction'] = current_default_prob - result['risk_impact']['new_probability']
        all_scenarios.append(result)
    
    # Duration adjustment
    if 'duration_extend_30' in scenarios_to_run:
        current_duration = loan_request.get('durasi_hari', 90)
        new_duration = int(current_duration * 1.30)
        result = simulate_duration_adjustment(loan_predictor, loan_request, new_duration)
        result['risk_impact']['old_probability'] = current_default_prob
        result['risk_impact']['reduction'] = current_default_prob - result['risk_impact']['new_probability']
        all_scenarios.append(result)
    
    # Rank scenarios by impact
    for scenario in all_scenarios:
        # Calculate combined impact score
        health_improvement = scenario.get('health_impact', {}).get('improvement', 0)
        risk_reduction = scenario.get('risk_impact', {}).get('reduction', 0)
        
        # Weighted score (risk reduction is more important)
        scenario['impact_score'] = (health_improvement * 0.3) + (risk_reduction * 100 * 0.7)
    
    # Sort by impact
    all_scenarios.sort(key=lambda x: x.get('impact_score', 0), reverse=True)
    
    return {
        'current_state': {
            'health_score': current_health_score,
            'default_probability': current_default_prob
        },
        'scenarios': all_scenarios,
        'best_scenario': all_scenarios[0] if all_scenarios else None,
        'total_scenarios': len(all_scenarios)
    }
