"""
Feature Assembly
================
Purpose: Prepare features for model inference.

Tasks:
- Combine loan request data with financial profile
- Engineer features following training pipeline
- Ensure feature order matches training schema
- Handle missing values

Key Principles:
- Stateless transformation
- Consistent with training pipeline
- NO data leakage
- Production-ready
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from datetime import datetime


def clean_loan_data(data: Dict) -> Dict:
    """
    Clean and fix loan data issues.
    
    Args:
        data: Raw loan request data
        
    Returns:
        Cleaned data dictionary
    """
    cleaned = data.copy()
    
    # Fix negative duration
    if 'durasi_hari' in cleaned and cleaned['durasi_hari'] < 0:
        cleaned['durasi_hari'] = abs(cleaned['durasi_hari'])
    
    # Handle tanggal_pencairan
    if 'tanggal_pencairan' in cleaned:
        if isinstance(cleaned['tanggal_pencairan'], str):
            cleaned['tanggal_pencairan'] = pd.to_datetime(cleaned['tanggal_pencairan'])
        # Fix future dates
        if cleaned['tanggal_pencairan'].year > 2024:
            cleaned['tanggal_pencairan'] = cleaned['tanggal_pencairan'] - pd.DateOffset(years=1)
    else:
        # If not provided, use current date
        cleaned['tanggal_pencairan'] = pd.Timestamp.now()
    
    return cleaned


def impute_missing_values(data: Dict) -> Dict:
    """
    Impute missing values following training methodology.
    
    Args:
        data: Data dictionary with potential missing values
        
    Returns:
        Data with imputed values
    """
    imputed = data.copy()
    
    # Median ratio from training: total_pengembalian / jumlah_pinjaman ≈ 1.15
    MEDIAN_RETURN_RATIO = 1.15
    # Median ratio from training: porsi_lender / total_pengembalian ≈ 0.95
    MEDIAN_LENDER_RATIO = 0.95
    # Median duration from training
    MEDIAN_DURATION = 90
    
    # Impute total_pengembalian if missing
    if 'total_pengembalian' not in imputed or imputed['total_pengembalian'] is None:
        imputed['total_pengembalian'] = imputed['jumlah_pinjaman'] * MEDIAN_RETURN_RATIO
    
    # Impute porsi_pengembalian_lender if missing
    if 'porsi_pengembalian_lender' not in imputed or imputed['porsi_pengembalian_lender'] is None:
        imputed['porsi_pengembalian_lender'] = imputed['total_pengembalian'] * MEDIAN_LENDER_RATIO
    
    # Impute durasi_hari if missing
    if 'durasi_hari' not in imputed or imputed['durasi_hari'] is None:
        imputed['durasi_hari'] = MEDIAN_DURATION
    
    # Fill categorical with 'Unknown'
    categorical_fields = ['provinsi', 'jenis_pinjaman', 'status_peminjam', 
                         'sektor_usaha', 'pendidikan', 'jenis_jaminan']
    for field in categorical_fields:
        if field not in imputed or imputed[field] is None or imputed[field] == '':
            imputed[field] = 'Unknown'
    
    return imputed


def engineer_features(data: Dict, aggregation_maps: Optional[Dict] = None) -> Dict:
    """
    Engineer features following training pipeline.
    
    Args:
        data: Cleaned and imputed data
        aggregation_maps: Optional pre-computed aggregation maps
        
    Returns:
        Data with engineered features
    """
    engineered = data.copy()
    
    # 1. Financial Ratios
    engineered['bunga'] = engineered['total_pengembalian'] - engineered['jumlah_pinjaman']
    engineered['ratio_bunga'] = engineered['bunga'] / engineered['jumlah_pinjaman']
    engineered['ratio_lender'] = engineered['porsi_pengembalian_lender'] / engineered['total_pengembalian']
    
    # 2. Date Features
    tanggal = pd.to_datetime(engineered['tanggal_pencairan'])
    engineered['month'] = tanggal.month
    engineered['day'] = tanggal.day
    engineered['dayofweek'] = tanggal.dayofweek
    engineered['is_weekend'] = 1 if tanggal.dayofweek in [5, 6] else 0
    
    # 3. Aggregation Features (use provided maps or defaults)
    if aggregation_maps is None:
        # Default values from training distribution
        aggregation_maps = {
            'mean_loan_provinsi': {},
            'mean_interest_sector': {}
        }
    
    # Mean loan by provinsi
    provinsi = engineered.get('provinsi', 'Unknown')
    engineered['mean_loan_provinsi'] = aggregation_maps['mean_loan_provinsi'].get(
        provinsi, 15_000_000  # Default median loan amount
    )
    engineered['loan_vs_prov_mean'] = engineered['jumlah_pinjaman'] / engineered['mean_loan_provinsi']
    
    # Mean interest by sector
    sektor = engineered.get('sektor_usaha', 'Unknown')
    engineered['mean_interest_sector'] = aggregation_maps['mean_interest_sector'].get(
        sektor, 0.15  # Default median interest ratio
    )
    
    # 4. Interaction Features
    engineered['beban_per_hari'] = engineered['total_pengembalian'] / (engineered['durasi_hari'] + 1)
    engineered['debt_pressure'] = engineered['ratio_bunga'] * engineered['durasi_hari']
    
    return engineered


def assemble_features(
    loan_request: Dict,
    financial_metrics: Optional[Dict] = None,
    aggregation_maps: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Assemble all features for model inference.
    
    Args:
        loan_request: Loan request data containing:
            - jumlah_pinjaman
            - durasi_hari
            - jenis_pinjaman
            - provinsi
            - status_peminjam
            - sektor_usaha
            - pendidikan
            - jenis_jaminan
            - tanggal_pencairan (optional)
            - total_pengembalian (optional)
            - porsi_pengembalian_lender (optional)
        financial_metrics: Optional financial health metrics from Module 1
        aggregation_maps: Optional pre-computed aggregation statistics
        
    Returns:
        DataFrame with single row containing all features in correct order
    """
    # Step 1: Clean data
    cleaned = clean_loan_data(loan_request)
    
    # Step 2: Impute missing values
    imputed = impute_missing_values(cleaned)
    
    # Step 3: Engineer features
    engineered = engineer_features(imputed, aggregation_maps)
    
    # Step 4: Create DataFrame with expected feature order
    feature_order = [
        'provinsi', 'jenis_pinjaman', 'status_peminjam', 'jumlah_pinjaman',
        'total_pengembalian', 'durasi_hari', 'porsi_pengembalian_lender',
        'sektor_usaha', 'pendidikan', 'jenis_jaminan',
        'bunga', 'ratio_bunga', 'ratio_lender',
        'month', 'day', 'dayofweek', 'is_weekend',
        'mean_loan_provinsi', 'loan_vs_prov_mean', 'mean_interest_sector',
        'beban_per_hari', 'debt_pressure'
    ]
    
    # Build features dict
    features = {col: engineered.get(col, 0) for col in feature_order}
    
    # Convert to DataFrame
    df = pd.DataFrame([features])
    
    # Convert categorical columns to category dtype (for LightGBM)
    categorical_cols = ['provinsi', 'jenis_pinjaman', 'status_peminjam', 
                       'sektor_usaha', 'pendidikan', 'jenis_jaminan']
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    
    return df


def load_aggregation_maps(train_data_path: Optional[str] = None) -> Dict:
    """
    Load or compute aggregation maps from training data.
    
    Args:
        train_data_path: Path to training data CSV
        
    Returns:
        Dictionary with aggregation statistics
    """
    if train_data_path is None:
        # Return default maps (could be loaded from saved JSON)
        return {
            'mean_loan_provinsi': {},
            'mean_interest_sector': {}
        }
    
    # Load and compute from training data
    import pandas as pd
    train = pd.read_csv(train_data_path)
    
    maps = {
        'mean_loan_provinsi': train.groupby('provinsi')['jumlah_pinjaman'].mean().to_dict(),
        'mean_interest_sector': {}
    }
    
    # Compute interest ratio first
    train['bunga'] = train['total_pengembalian'] - train['jumlah_pinjaman']
    train['ratio_bunga'] = train['bunga'] / train['jumlah_pinjaman']
    maps['mean_interest_sector'] = train.groupby('sektor_usaha')['ratio_bunga'].mean().to_dict()
    
    return maps
