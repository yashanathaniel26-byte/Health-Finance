"""
Insight Engine Main Orchestrator
=================================
Purpose: Coordinate root cause, scenarios, and recommendations.

Output:
- Integrated insights
- Prioritized recommendations
- Decision support

Key Principles:
- Reasoning layer (NOT prediction)
- Integrate Module 1 & 2 results
- Actionable intelligence
- NO model modification
"""

from typing import Dict, Optional, List
from . import root_cause
from . import scenarios
from . import recommendations


class InsightEngine:
    """
    Main orchestrator for insight generation and decision intelligence.
    
    Coordinates:
    1. Root cause analysis
    2. What-if scenario simulation
    3. Recommendation generation
    
    Usage:
        from src.module_1_health import HealthAnalyzer
        from src.module_2_prediction import LoanPredictor
        from src.module_3_insights import InsightEngine
        
        # Get results from Module 1 & 2
        health_result = health_analyzer.analyze(financial_profile)
        loan_result = loan_predictor.predict(loan_request)
        
        # Generate insights
        engine = InsightEngine()
        insights = engine.analyze(
            health_result=health_result,
            loan_result=loan_result,
            financial_profile=financial_profile,
            loan_request=loan_request
        )
    """
    
    def __init__(self):
        """Initialize Insight Engine."""
        pass
    
    def analyze(
        self,
        health_result: Dict,
        loan_result: Dict,
        financial_profile: Dict,
        loan_request: Dict,
        health_analyzer=None,
        loan_predictor=None,
        run_scenarios: bool = True,
        scenario_list: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate comprehensive insights and recommendations.
        
        Args:
            health_result: Results from Module 1 (HealthAnalyzer)
            loan_result: Results from Module 2 (LoanPredictor)
            financial_profile: Original financial profile data
            loan_request: Original loan request data
            health_analyzer: Optional HealthAnalyzer instance for scenarios
            loan_predictor: Optional LoanPredictor instance for scenarios
            run_scenarios: Whether to run scenario analysis
            scenario_list: Optional specific scenarios to run
            
        Returns:
            Comprehensive insight package containing:
                - root_cause_analysis: Root cause identification
                - scenario_analysis: What-if scenarios (if run)
                - recommendations: Actionable recommendations
                - decision_summary: Executive summary
                - risk_assessment: Integrated risk view
                
        Raises:
            ValueError: If required inputs are missing
        """
        # Validate inputs
        if not health_result or not loan_result:
            raise ValueError("Both health_result and loan_result are required")
        
        try:
            # Step 1: Root Cause Analysis
            root_cause_analysis = root_cause.generate_root_cause_summary(
                health_result=health_result,
                loan_result=loan_result,
                loan_request=loan_request
            )
            
            # Step 2: Scenario Analysis (optional, requires analyzer instances)
            scenario_analysis = None
            if run_scenarios and health_analyzer and loan_predictor:
                scenario_analysis = scenarios.run_scenario_analysis(
                    health_analyzer=health_analyzer,
                    loan_predictor=loan_predictor,
                    current_health=health_result,
                    current_loan_result=loan_result,
                    financial_profile=financial_profile,
                    loan_request=loan_request,
                    scenarios_to_run=scenario_list
                )
            
            # Step 3: Generate Recommendations
            recommendation_package = recommendations.generate_integrated_recommendations(
                health_result=health_result,
                loan_result=loan_result,
                loan_request=loan_request,
                root_cause=root_cause_analysis,
                scenario_results=scenario_analysis
            )
            
            # Step 4: Generate Decision Summary
            decision_summary = self._generate_decision_summary(
                health_result=health_result,
                loan_result=loan_result,
                root_cause_analysis=root_cause_analysis,
                recommendation_package=recommendation_package
            )
            
            # Step 5: Integrated Risk Assessment
            risk_assessment = self._generate_risk_assessment(
                health_result=health_result,
                loan_result=loan_result,
                root_cause_analysis=root_cause_analysis
            )
            
            # Compile comprehensive result
            insights = {
                "decision_summary": decision_summary,
                "risk_assessment": risk_assessment,
                "root_cause_analysis": root_cause_analysis,
                "recommendations": recommendation_package,
                "scenario_analysis": scenario_analysis,
                "metadata": {
                    "health_score": health_result['score'],
                    "default_probability": loan_result['default_probability'],
                    "risk_category": loan_result['risk_category'],
                    "scenarios_run": scenario_analysis is not None
                }
            }
            
            return insights
            
        except Exception as e:
            raise RuntimeError(f"Error generating insights: {str(e)}") from e
    
    def _generate_decision_summary(
        self,
        health_result: Dict,
        loan_result: Dict,
        root_cause_analysis: Dict,
        recommendation_package: Dict
    ) -> Dict:
        """
        Generate executive decision summary.
        
        Args:
            health_result: Health analysis results
            loan_result: Loan prediction results
            root_cause_analysis: Root cause analysis
            recommendation_package: Recommendation package
            
        Returns:
            Executive decision summary
        """
        health_score = health_result['score']
        default_prob = loan_result['default_probability']
        risk_category = loan_result['risk_category']
        
        # Determine overall recommendation
        if default_prob > 0.7 or health_score < 40:
            overall_decision = "TIDAK DIREKOMENDASIKAN"
            reasoning = "Risiko default sangat tinggi dan/atau kondisi finansial sangat lemah"
            confidence = "high"
        elif default_prob > 0.5 or health_score < 50:
            overall_decision = "PERLU RESTRUKTURISASI"
            reasoning = "Risiko default tinggi, memerlukan perbaikan struktur pinjaman atau kondisi finansial"
            confidence = "high"
        elif default_prob > 0.3 or health_score < 65:
            overall_decision = "DAPAT DIPERTIMBANGKAN DENGAN SYARAT"
            reasoning = "Risiko moderat, memerlukan beberapa improvement sebelum approval"
            confidence = "medium"
        else:
            overall_decision = "DIREKOMENDASIKAN"
            reasoning = "Profil finansial baik dan risiko default rendah"
            confidence = "high"
        
        # Key insights
        key_insights = [
            f"Health Score: {health_score:.1f}/100 ({health_result['status']})",
            f"Default Probability: {default_prob:.1%} ({risk_category} risk)",
            f"Total Risk Factors: {root_cause_analysis['total_risk_factors']}",
            f"Critical Issues: {root_cause_analysis['critical_factors']}"
        ]
        
        # Top 3 actions
        top_actions = [
            rec['action'] for rec in recommendation_package['top_3_priorities']
        ]
        
        return {
            "overall_decision": overall_decision,
            "reasoning": reasoning,
            "confidence": confidence,
            "key_insights": key_insights,
            "top_3_actions": top_actions,
            "summary": recommendation_package['summary'],
            "requires_immediate_action": root_cause_analysis['critical_factors'] > 0
        }
    
    def _generate_risk_assessment(
        self,
        health_result: Dict,
        loan_result: Dict,
        root_cause_analysis: Dict
    ) -> Dict:
        """
        Generate integrated risk assessment.
        
        Args:
            health_result: Health analysis results
            loan_result: Loan prediction results
            root_cause_analysis: Root cause analysis
            
        Returns:
            Integrated risk assessment
        """
        health_score = health_result['score']
        default_prob = loan_result['default_probability']
        
        # Risk matrix
        if health_score >= 75 and default_prob < 0.3:
            risk_level = "LOW"
            risk_description = "Profil finansial sangat baik dengan risiko default rendah"
        elif health_score >= 60 and default_prob < 0.4:
            risk_level = "MODERATE"
            risk_description = "Profil finansial baik dengan risiko default moderat"
        elif health_score >= 50 and default_prob < 0.5:
            risk_level = "MODERATE-HIGH"
            risk_description = "Profil finansial cukup dengan risiko default cukup tinggi"
        elif health_score >= 40 and default_prob < 0.6:
            risk_level = "HIGH"
            risk_description = "Profil finansial lemah dengan risiko default tinggi"
        else:
            risk_level = "VERY HIGH"
            risk_description = "Profil finansial sangat lemah dengan risiko default sangat tinggi"
        
        # Risk components
        risk_components = {
            "financial_health_risk": self._categorize_score(health_score),
            "default_risk": loan_result['risk_category'],
            "combined_risk": risk_level
        }
        
        # Risk drivers (from root cause)
        risk_drivers = [
            cause['cause'] for cause in root_cause_analysis['primary_causes'][:5]
        ]
        
        return {
            "risk_level": risk_level,
            "risk_description": risk_description,
            "risk_components": risk_components,
            "risk_drivers": risk_drivers,
            "health_score": health_score,
            "default_probability": default_prob,
            "risk_profile": root_cause_analysis['risk_profile']
        }
    
    def _categorize_score(self, score: float) -> str:
        """Categorize health score into risk level."""
        if score >= 75:
            return "low"
        elif score >= 60:
            return "moderate"
        elif score >= 50:
            return "moderate-high"
        else:
            return "high"
    
    def quick_insight(
        self,
        health_result: Dict,
        loan_result: Dict
    ) -> str:
        """
        Generate quick one-line insight.
        
        Args:
            health_result: Health analysis results
            loan_result: Loan prediction results
            
        Returns:
            Quick insight string
        """
        health_score = health_result['score']
        default_prob = loan_result['default_probability']
        
        if default_prob > 0.6:
            return f"⚠️ HIGH RISK: Default probability {default_prob:.1%}, Health score {health_score:.0f}/100 - Immediate action required"
        elif default_prob > 0.4:
            return f"⚡ MODERATE RISK: Default probability {default_prob:.1%}, Health score {health_score:.0f}/100 - Optimization recommended"
        else:
            return f"✅ LOW RISK: Default probability {default_prob:.1%}, Health score {health_score:.0f}/100 - Profile acceptable"
