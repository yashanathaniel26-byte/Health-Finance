"""
Financial Metrics Calculator
=============================
Purpose: Calculate key financial health metrics.

Metrics:
- DTI (Debt-to-Income Ratio)
- Savings Ratio
- Expense Ratio
- Disposable Income & Ratio
- Net Cash Flow

Key Principles:
- Scale-invariant (ratio-based, anti-bias)
- Safe division (no zero division errors)
- Pure functions (stateless, reusable)
- NO business decisions here
"""

from typing import Dict, Union


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Number to be divided
        denominator: Number to divide by
        default: Value to return if denominator is zero
        
    Returns:
        Result of division or default value
    """
    if denominator == 0 or denominator is None:
        return default
    return numerator / denominator


def calculate_debt_to_income_ratio(debt: float, income: float) -> float:
    """
    Calculate Debt-to-Income (DTI) ratio.
    
    DTI = Total Debt / Monthly Income
    
    Args:
        debt: Total outstanding debt
        income: Monthly income
        
    Returns:
        DTI ratio (e.g., 3.33 means debt is 3.33x monthly income)
    """
    return safe_divide(debt, income, default=0.0)


def calculate_expense_ratio(fixed_expenses: float, variable_expenses: float, income: float) -> float:
    """
    Calculate total expense ratio against income.
    
    Expense Ratio = (Fixed + Variable Expenses) / Income
    
    Args:
        fixed_expenses: Monthly fixed expenses
        variable_expenses: Monthly variable expenses
        income: Monthly income
        
    Returns:
        Expense ratio (e.g., 0.75 means 75% of income goes to expenses)
    """
    total_expenses = fixed_expenses + variable_expenses
    return safe_divide(total_expenses, income, default=0.0)


def calculate_savings_ratio(savings: float, income: float) -> float:
    """
    Calculate savings ratio against income.
    
    Savings Ratio = Total Savings / Monthly Income
    
    Args:
        savings: Total savings amount
        income: Monthly income
        
    Returns:
        Savings ratio (e.g., 2.0 means savings = 2 months of income)
    """
    return safe_divide(savings, income, default=0.0)


def calculate_disposable_income(income: float, fixed_expenses: float, variable_expenses: float) -> float:
    """
    Calculate disposable income (cashflow).
    
    Disposable Income = Income - Fixed Expenses - Variable Expenses
    
    Args:
        income: Monthly income
        fixed_expenses: Monthly fixed expenses
        variable_expenses: Monthly variable expenses
        
    Returns:
        Disposable income amount
    """
    return income - fixed_expenses - variable_expenses


def calculate_disposable_income_ratio(income: float, fixed_expenses: float, variable_expenses: float) -> float:
    """
    Calculate disposable income as ratio of income.
    
    Disposable Income Ratio = (Income - Expenses) / Income
    
    Args:
        income: Monthly income
        fixed_expenses: Monthly fixed expenses
        variable_expenses: Monthly variable expenses
        
    Returns:
        Disposable income ratio (e.g., 0.25 means 25% of income is free)
    """
    disposable = calculate_disposable_income(income, fixed_expenses, variable_expenses)
    return safe_divide(disposable, income, default=0.0)


def calculate_all_metrics(
    income: float,
    fixed_expenses: float,
    variable_expenses: float,
    savings: float,
    debt: float
) -> Dict[str, Union[float, int]]:
    """
    Calculate all financial health metrics.
    
    Args:
        income: Monthly income
        fixed_expenses: Monthly fixed expenses
        variable_expenses: Monthly variable expenses
        savings: Total savings
        debt: Total outstanding debt
        
    Returns:
        Dictionary containing all calculated metrics:
        - debt_to_income_ratio: DTI ratio
        - expense_ratio: Total expenses / income
        - savings_ratio: Savings / income
        - disposable_income: Absolute disposable income
        - disposable_income_ratio: Disposable income / income
        - total_expenses: Sum of fixed and variable expenses
        - net_cashflow: Same as disposable_income
    """
    total_expenses = fixed_expenses + variable_expenses
    disposable = calculate_disposable_income(income, fixed_expenses, variable_expenses)
    
    return {
        "debt_to_income_ratio": calculate_debt_to_income_ratio(debt, income),
        "expense_ratio": calculate_expense_ratio(fixed_expenses, variable_expenses, income),
        "savings_ratio": calculate_savings_ratio(savings, income),
        "disposable_income": disposable,
        "disposable_income_ratio": calculate_disposable_income_ratio(income, fixed_expenses, variable_expenses),
        "total_expenses": total_expenses,
        "net_cashflow": disposable,
    }
