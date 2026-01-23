"""
Health Analyzer Main Orchestrator
==================================
Purpose: Coordinate metrics, rules, and clustering for health assessment.

Output:
- Health score (0-100)
- Financial metrics
- Risk flags
- Financial persona

Key Principles:
- Single public interface
- Input validation
- Comprehensive error handling
- Production-ready
"""

from typing import Dict, Optional
from . import metrics
from . import rules
from . import clustering


class HealthAnalyzer:
    """
    Main orchestrator for financial health analysis.
    
    Coordinates:
    1. Metrics calculation
    2. Rule-based assessment
    3. Persona assignment
    
    Usage:
        analyzer = HealthAnalyzer()
        result = analyzer.analyze({
            'income': 15_000_000,
            'fixed_expenses': 8_000_000,
            'variable_expenses': 3_000_000,
            'savings': 20_000_000,
            'debt': 50_000_000
        })
    """
    
    def __init__(self):
        """Initialize Health Analyzer."""
        pass
    
    def validate_input(self, data: Dict[str, float]) -> Dict[str, str]:
        """
        Validate input data.
        
        Args:
            data: Financial profile data
            
        Returns:
            Dictionary of validation errors (empty if valid)
        """
        errors = {}
        
        required_fields = ['income', 'fixed_expenses', 'variable_expenses', 'savings', 'debt']
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                errors[field] = f"Missing required field: {field}"
            elif data[field] is None:
                errors[field] = f"Field cannot be None: {field}"
            elif not isinstance(data[field], (int, float)):
                errors[field] = f"Field must be numeric: {field}"
            elif data[field] < 0:
                errors[field] = f"Field cannot be negative: {field}"
        
        # Validate income is not zero (would cause division errors)
        if 'income' in data and data['income'] == 0:
            errors['income'] = "Income cannot be zero"
        
        return errors
    
    def analyze(self, financial_profile: Dict[str, float]) -> Dict[str, any]:
        """
        Analyze financial health.
        
        Args:
            financial_profile: Dictionary containing:
                - income: Monthly income
                - fixed_expenses: Monthly fixed expenses
                - variable_expenses: Monthly variable expenses
                - savings: Total savings
                - debt: Total outstanding debt
                
        Returns:
            Dictionary containing:
                - score: Health score (0-100)
                - status: Health status (Healthy/Warning/At Risk)
                - metrics: All calculated financial metrics
                - risk_flags: List of identified risks
                - persona: Financial persona
                - persona_description: Description of persona
                - persona_insights: Actionable insights for persona
                - explanations: Detailed explanations for each component
                - component_scores: Individual component scores
                
        Raises:
            ValueError: If input validation fails
        """
        # Validate input
        validation_errors = self.validate_input(financial_profile)
        if validation_errors:
            error_msg = "; ".join([f"{k}: {v}" for k, v in validation_errors.items()])
            raise ValueError(f"Input validation failed: {error_msg}")
        
        try:
            # Step 1: Calculate metrics
            financial_metrics = metrics.calculate_all_metrics(
                income=financial_profile['income'],
                fixed_expenses=financial_profile['fixed_expenses'],
                variable_expenses=financial_profile['variable_expenses'],
                savings=financial_profile['savings'],
                debt=financial_profile['debt']
            )
            
            # Step 2: Calculate health score and assessment
            health_assessment = rules.calculate_health_score(financial_metrics)
            
            # Step 3: Assign financial persona
            persona = clustering.assign_financial_persona(financial_metrics, health_assessment)
            persona_description = clustering.get_persona_description(persona)
            persona_insights = clustering.get_persona_insights(persona)
            
            # Compile final result with enhanced persona including input profile
            result = {
                "score": health_assessment["score"],
                "status": health_assessment["status"],
                "metrics": financial_metrics,
                "risk_flags": health_assessment["risk_flags"],
                "persona": {
                    "name": persona,
                    "description": persona_description,
                    "insights": persona_insights,
                    "profile_summary": {
                        "monthly_income": financial_profile.get('income', 0),
                        "total_expenses": financial_profile.get('fixed_expenses', 0) + financial_profile.get('variable_expenses', 0),
                        "current_savings": financial_profile.get('savings', 0),
                        "current_debt": financial_profile.get('debt', 0),
                        "disposable_income": financial_metrics.get('disposable_income', 0)
                    }
                },
                "explanations": health_assessment["explanations"],
                "component_scores": health_assessment["component_scores"]
            }
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Error during health analysis: {str(e)}") from e
    
    def quick_check(self, financial_profile: Dict[str, float]) -> str:
        """
        Quick health status check without full analysis.
        
        Args:
            financial_profile: Financial profile data
            
        Returns:
            Quick status summary string
        """
        try:
            result = self.analyze(financial_profile)
            return f"Health Status: {result['status']} (Score: {result['score']}/100) - {result['persona']}"
        except Exception as e:
            return f"Error: {str(e)}"
