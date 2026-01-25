"""
Module 2: Loan Default Prediction
==================================
Purpose: Predict loan default probability using FROZEN pre-trained model.

Key Principle: Pure inference layer, NO training/fitting.

Usage:
    from src.module_2_prediction import LoanPredictor
    
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

from .loan_predictor import LoanPredictor

__all__ = ['LoanPredictor']
