# src/eda_utils.py
import pandas as pd
import numpy as np

def load_and_clean_types(filepath):
    """Loads dataset and ensures correct data types for core columns."""
    df = pd.read_csv(filepath)
    
    # Date Conversions
    if 'TransactionMonth' in df.columns:
        df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'])
    if 'VehicleIntroDate' in df.columns:
        df['VehicleIntroDate'] = pd.to_datetime(df['VehicleIntroDate'])
        
    # Categorical Conversions
    cat_cols = ['Province', 'PostalCode', 'Gender', 'MaritalStatus', 'Make', 'Model', 'CoverType']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
            
    return df

def calculate_portfolio_metrics(df):
    """Computes fundamental insurance metrics at a portfolio level."""
    total_claims = df['TotalClaims'].sum()
    total_premium = df['TotalPremium'].sum()
    
    loss_ratio = total_claims / total_premium if total_premium > 0 else 0
    margin = total_premium - total_claims
    
    return {
        "Total Portfolio Premium": total_premium,
        "Total Portfolio Claims": total_claims,
        "Overall Loss Ratio": loss_ratio,
        "Net Portfolio Margin": margin
    }

def get_outlier_bounds(series):
    """Calculates Tukey's fences (IQR method) for outlier detection."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound