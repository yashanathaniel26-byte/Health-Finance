"""
Loan Predictor Main Orchestrator
=================================
Purpose: Coordinate feature assembly, inference, and explanation.

Output:
- Default probability
- Risk category
- SHAP explanations

Key Principles:
- Pure prediction layer (NO decision making)
- Frozen model (NO training)
- Comprehensive explanations
- Production-ready
"""

from typing import Dict, Optional
import pandas as pd
from . import feature_assembly
from . import model_inference
from . import explainer


class LoanPredictor:
    """
    Main orchestrator for loan default prediction.
    
    Coordinates:
    1. Feature assembly
    2. Model inference
    3. Explanation generation
    
    Usage:
        predictor = LoanPredictor()
        result = predictor.predict({
            'jumlah_pinjaman': 30_000_000,
            'durasi_hari': 90,
            'jenis_pinjaman': 'Multiguna',
            'provinsi': 'DKI Jakarta',
            'status_peminjam': 'Baru',
            'sektor_usaha': 'Perdagangan',
            'pendidikan': 'S1',
            'jenis_jaminan': 'BPKB Motor'
        })
    """
    
    def __init__(self, model_path: Optional[str] = None, aggregation_maps: Optional[Dict] = None):
        """
        Initialize Loan Predictor.
        
        Args:
            model_path: Optional custom model path
            aggregation_maps: Optional pre-computed aggregation statistics
        """
        self.model_path = model_path
        self.aggregation_maps = aggregation_maps
        
        # Load model info on initialization
        try:
            self.model_info = model_inference.get_model_info()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize predictor: {str(e)}")
    
    def validate_input(self, loan_request: Dict) -> Dict[str, str]:
        """
        Validate loan request input.
        
        Args:
            loan_request: Loan request data
            
        Returns:
            Dictionary of validation errors (empty if valid)
        """
        errors = {}
        
        required_fields = ['jumlah_pinjaman', 'durasi_hari', 'jenis_pinjaman']
        
        # Check required fields
        for field in required_fields:
            if field not in loan_request:
                errors[field] = f"Missing required field: {field}"
            elif loan_request[field] is None:
                errors[field] = f"Field cannot be None: {field}"
        
        # Validate jumlah_pinjaman
        if 'jumlah_pinjaman' in loan_request:
            if not isinstance(loan_request['jumlah_pinjaman'], (int, float)):
                errors['jumlah_pinjaman'] = "Jumlah pinjaman must be numeric"
            elif loan_request['jumlah_pinjaman'] <= 0:
                errors['jumlah_pinjaman'] = "Jumlah pinjaman must be positive"
        
        # Validate durasi_hari
        if 'durasi_hari' in loan_request:
            if not isinstance(loan_request['durasi_hari'], (int, float)):
                errors['durasi_hari'] = "Durasi hari must be numeric"
            elif loan_request['durasi_hari'] <= 0:
                errors['durasi_hari'] = "Durasi hari must be positive"
        
        return errors
    
    def predict(
        self,
        loan_request: Dict,
        financial_metrics: Optional[Dict] = None,
        include_explanation: bool = True
    ) -> Dict:
        """
        Predict loan default probability.
        
        Args:
            loan_request: Loan request data (see class docstring)
            financial_metrics: Optional financial health metrics from Module 1
            include_explanation: Whether to include detailed explanation
            
        Returns:
            Dictionary containing:
                - default_prediction: Binary prediction (0 or 1)
                - default_probability: Probability of default (0.0 to 1.0)
                - risk_category: Risk level (low/medium/high)
                - confidence: Prediction confidence (low/medium/high)
                - explanation: Detailed explanation (if requested)
                - model_info: Model metadata
                
        Raises:
            ValueError: If input validation fails
            RuntimeError: If prediction fails
        """
        # Validate input
        validation_errors = self.validate_input(loan_request)
        if validation_errors:
            error_msg = "; ".join([f"{k}: {v}" for k, v in validation_errors.items()])
            raise ValueError(f"Input validation failed: {error_msg}")
        
        try:
            # Step 1: Assemble features
            features_df = feature_assembly.assemble_features(
                loan_request=loan_request,
                financial_metrics=financial_metrics,
                aggregation_maps=self.aggregation_maps
            )
            
            # DEBUG: Check if financial_metrics is passed
            print(f"🔍 LoanPredictor - financial_metrics received: {financial_metrics is not None}")
            if financial_metrics:
                print(f"   Metrics keys: {list(financial_metrics.keys())}")
            
            # IMPORTANT: Add loan amount to financial_metrics for adjustment
            if financial_metrics:
                financial_metrics['loan_amount'] = loan_request.get('jumlah_pinjaman', 0)
            
            # Step 2: Predict
            prediction, probability, risk_category = model_inference.predict_default_probability(
                features=features_df,
                model_path=self.model_path,
                financial_metrics=financial_metrics
            )
            
            # Step 3: Generate explanation (if requested)
            explanation = None
            if include_explanation:
                # Get model for explanation
                loader = model_inference.ModelLoader()
                model, _ = loader.load_model(self.model_path)
                
                explanation = explainer.explain_prediction(
                    features=features_df,
                    prediction=prediction,
                    probability=probability,
                    risk_category=risk_category,
                    model=model
                )
            
            # Compile result
            result = {
                "default_prediction": int(prediction),
                "default_probability": float(probability),
                "risk_category": risk_category,
                "confidence": explanation['confidence'] if explanation else self._calculate_confidence(probability),
                "model_info": {
                    "model_type": self.model_info['model_type'],
                    "version": self.model_info['version'],
                    "f1_score": self.model_info['performance']['average_f1_score']
                }
            }
            
            if explanation:
                result["explanation"] = explanation
            
            return result
            
        except ValueError as e:
            raise ValueError(f"Prediction error: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error during prediction: {str(e)}") from e
    
    def _calculate_confidence(self, probability: float) -> str:
        """
        Calculate prediction confidence based on probability.
        
        Args:
            probability: Prediction probability
            
        Returns:
            Confidence level string
        """
        distance_from_threshold = abs(probability - 0.5)
        if distance_from_threshold > 0.3:
            return "high"
        elif distance_from_threshold > 0.15:
            return "medium"
        else:
            return "low"
    
    def batch_predict(
        self,
        loan_requests: list[Dict],
        include_explanation: bool = False
    ) -> list[Dict]:
        """
        Predict default for multiple loan requests.
        
        Args:
            loan_requests: List of loan request dictionaries
            include_explanation: Whether to include explanations
            
        Returns:
            List of prediction results
        """
        results = []
        for request in loan_requests:
            try:
                result = self.predict(request, include_explanation=include_explanation)
                results.append(result)
            except Exception as e:
                results.append({
                    "error": str(e),
                    "default_prediction": None,
                    "default_probability": None,
                    "risk_category": "unknown"
                })
        
        return results
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Get feature importance from model.
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            DataFrame with feature importance
        """
        return model_inference.get_feature_importance(top_n=top_n)
