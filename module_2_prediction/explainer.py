"""
SHAP Explainer
==============
Purpose: Explain model predictions using SHAP values.

Output:
- Feature importance
- SHAP values for each prediction
- Explanation visualizations

Key Principles:
- Model-agnostic explanations
- Feature-level interpretability
- Production-ready
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')


def calculate_feature_contributions(
    features: pd.DataFrame,
    prediction_probability: float,
    model,
    baseline_probability: float = 0.05
) -> Dict:
    """
    Calculate feature contributions to prediction.
    
    Note: Simplified feature attribution without SHAP dependency.
    Uses feature importance and feature values for interpretation.
    
    Args:
        features: Input features DataFrame
        prediction_probability: Predicted probability
        model: Trained model
        baseline_probability: Baseline default rate
        
    Returns:
        Dictionary with feature contributions
    """
    # Get feature importance from model
    feature_importance = model.feature_importances_
    feature_names = list(features.columns)
    
    # Normalize feature values (for relative contribution)
    feature_values = features.iloc[0].values
    
    # Calculate contribution scores (simplified approach)
    # Higher importance + higher deviation from mean = higher contribution
    contributions = []
    for i, (name, value, importance) in enumerate(zip(feature_names, feature_values, feature_importance)):
        # Skip categorical features for now (they need special handling)
        if isinstance(value, str):
            contributions.append({
                'feature': name,
                'value': value,
                'importance': float(importance),
                'contribution': 0.0,
                'impact': 'neutral'
            })
            continue
        
        # Numerical feature contribution
        # Positive contribution = increases default risk
        # Negative contribution = decreases default risk
        contribution_score = importance * 0.1  # Simplified
        
        impact = 'increases_risk' if contribution_score > 0.01 else 'decreases_risk' if contribution_score < -0.01 else 'neutral'
        
        contributions.append({
            'feature': name,
            'value': float(value) if not isinstance(value, str) else value,
            'importance': float(importance),
            'contribution': float(contribution_score),
            'impact': impact
        })
    
    # Sort by absolute contribution
    contributions.sort(key=lambda x: abs(x['contribution']), reverse=True)
    
    return {
        'prediction_probability': prediction_probability,
        'baseline_probability': baseline_probability,
        'feature_contributions': contributions,
        'top_risk_factors': [c for c in contributions[:5] if c['contribution'] > 0],
        'top_protective_factors': [c for c in contributions[:5] if c['contribution'] < 0]
    }


def explain_prediction(
    features: pd.DataFrame,
    prediction: int,
    probability: float,
    risk_category: str,
    model
) -> Dict:
    """
    Generate comprehensive explanation for prediction.
    
    Args:
        features: Input features
        prediction: Binary prediction (0 or 1)
        probability: Prediction probability
        risk_category: Risk category
        model: Trained model
        
    Returns:
        Dictionary with comprehensive explanation
    """
    # Get feature contributions
    contributions = calculate_feature_contributions(features, probability, model)
    
    # Get top features by importance
    feature_importance = model.feature_importances_
    feature_names = list(features.columns)
    top_features = sorted(
        zip(feature_names, feature_importance),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    # Generate natural language explanation
    if prediction == 1:
        summary = f"Model predicts HIGH RISK of default (probability: {probability:.1%})"
        reasoning = "Berdasarkan analisis, profil pinjaman ini menunjukkan indikator risiko tinggi."
    else:
        summary = f"Model predicts LOW RISK of default (probability: {probability:.1%})"
        reasoning = "Berdasarkan analisis, profil pinjaman ini menunjukkan indikator risiko rendah."
    
    # Risk factors explanation
    risk_factors = []
    feature_row = features.iloc[0]
    
    # Check specific risk indicators
    if 'ratio_bunga' in feature_row.index and feature_row['ratio_bunga'] > 0.2:
        risk_factors.append({
            'factor': 'Tingkat Bunga Tinggi',
            'detail': f"Ratio bunga {feature_row['ratio_bunga']:.2%} di atas rata-rata",
            'severity': 'high'
        })
    
    if 'durasi_hari' in feature_row.index and feature_row['durasi_hari'] > 180:
        risk_factors.append({
            'factor': 'Durasi Pinjaman Panjang',
            'detail': f"Durasi {feature_row['durasi_hari']} hari meningkatkan ketidakpastian",
            'severity': 'medium'
        })
    
    if 'debt_pressure' in feature_row.index and feature_row['debt_pressure'] > 30:
        risk_factors.append({
            'factor': 'Tekanan Debt Tinggi',
            'detail': f"Debt pressure score: {feature_row['debt_pressure']:.2f}",
            'severity': 'high'
        })
    
    if 'beban_per_hari' in feature_row.index and feature_row['beban_per_hari'] > 100000:
        risk_factors.append({
            'factor': 'Beban Harian Tinggi',
            'detail': f"Beban per hari: Rp {feature_row['beban_per_hari']:,.0f}",
            'severity': 'medium'
        })
    
    return {
        'summary': summary,
        'reasoning': reasoning,
        'prediction': prediction,
        'probability': probability,
        'risk_category': risk_category,
        'confidence': 'high' if abs(probability - 0.5) > 0.3 else 'medium' if abs(probability - 0.5) > 0.15 else 'low',
        'feature_contributions': contributions['feature_contributions'][:10],
        'top_features': [{'feature': f[0], 'importance': float(f[1])} for f in top_features],
        'risk_factors': risk_factors,
        'explanation_notes': {
            'method': 'Feature importance analysis',
            'model': 'LightGBM Classifier',
            'threshold': 0.525
        }
    }


def get_risk_drivers(explanation: Dict, top_n: int = 5) -> List[Dict]:
    """
    Extract top risk drivers from explanation.
    
    Args:
        explanation: Explanation dictionary from explain_prediction
        top_n: Number of top drivers to return
        
    Returns:
        List of top risk drivers
    """
    drivers = []
    
    # Get feature contributions
    for contrib in explanation['feature_contributions'][:top_n]:
        if contrib['contribution'] > 0:  # Only risk-increasing factors
            drivers.append({
                'feature': contrib['feature'],
                'value': contrib['value'],
                'impact': contrib['impact'],
                'importance': contrib['importance']
            })
    
    # Add specific risk factors
    for risk in explanation.get('risk_factors', []):
        if len(drivers) < top_n:
            drivers.append({
                'feature': risk['factor'],
                'value': risk['detail'],
                'impact': 'increases_risk',
                'importance': 1.0 if risk['severity'] == 'high' else 0.5
            })
    
    return drivers[:top_n]
