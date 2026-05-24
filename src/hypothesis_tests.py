import pandas as pd
import numpy as np
from scipy import stats

def find_balanced_segments(df, group_col, cat_a, cat_b, match_features=['Age', 'AnnualIncome', 'RiskScore']):
    """
    Isolates Group A and Group B for a given feature and verifies that their 
    background covariates are statistically equivalent (p > 0.05 on t-tests).
    Ensures any KPI divergence is due to the group variable itself.
    """
    group_a = df[df[group_col] == cat_a]
    group_b = df[df[group_col] == cat_b]
    
    print(f"\n--- Checking Feature Balance between Control [{cat_a}] & Test [{cat_b}] ---")
    is_balanced = True
    for feat in match_features:
        # T-test to see if background attributes differ significantly
        t_stat, p_val = stats.ttest_ind(group_a[feat].dropna(), group_b[feat].dropna(), equal_var=False)
        print(f"  - Covariate '{feat}' Balance Check: T-stat={t_stat:.3f}, p-value={p_val:.4f}")
        if p_val < 0.05:
            print(f"    ⚠️ Warning: '{feat}' is significantly unbalanced between these two categories.")
            is_balanced = False
            
    if is_balanced:
        print(f"  ✅ SUCCESS: Segments are statistically equivalent across attributes. Safe for A/B testing.")
    return group_a, group_b

def run_ab_frequency_test(group_a, group_b, label_a, label_b):
    """
    KPI: Claim Frequency (Proportion of policies with at least 1 claim)
    Methodology: Two-Sample Z-Test of Proportions / Chi-Square Contingency
    """
    successes_a = group_a['Claimed'].sum()
    trials_a = len(group_a)
    successes_b = group_b['Claimed'].sum()
    trials_b = len(group_b)
    
    contingency = [[successes_a, trials_a - successes_a], [successes_b, trials_b - successes_b]]
    chi2, p_val, _, _ = stats.chi2_contingency(contingency)
    
    print(f"\n📊 [KPI: Claim Frequency] A/B Test Results ({label_a} vs {label_b}):")
    print(f"  - {label_a} Freq: {successes_a/trials_a:.2%} ({successes_a}/{trials_a})")
    print(f"  - {label_b} Freq: {successes_b/trials_b:.2%} ({successes_b}/{trials_b})")
    print(f"  - Chi2 Stat: {chi2:.4f} | P-Value: {p_val:.4e}")
    print(f"  - Verdict: {'REJECT H0 - Significant Risk Difference' if p_val < 0.05 else 'FAIL TO REJECT H0 - No Significant Difference'}")
    return p_val

def run_ab_numeric_test(group_a, group_b, label_a, label_b, kpi_col, conditional_on_claim=False):
    """
    KPI: Claim Severity (conditional_on_claim=True) OR Margin (conditional_on_claim=False)
    Methodology: Two-Sample Independent t-Test (Welch's t-test)
    """
    if conditional_on_claim:
        # Isolate only instances where actual losses occurred
        vals_a = group_a[group_a[kpi_col] > 0][kpi_col].values
        vals_b = group_b[group_b[kpi_col] > 0][kpi_col].values
        kpi_name = "Claim Severity"
    else:
        vals_a = group_a[kpi_col].values
        vals_b = group_b[kpi_col].values
        kpi_name = "Net Premium Margin"
        
    t_stat, p_val = stats.ttest_ind(vals_a, vals_b, equal_var=False)
    
    print(f"\n💰 [KPI: {kpi_name}] A/B Test Results ({label_a} vs {label_b}):")
    print(f"  - {label_a} Mean: R {np.mean(vals_a):,.2f}")
    print(f"  - {label_b} Mean: R {np.mean(vals_b):,.2f}")
    print(f"  - T-Stat: {t_stat:.4f} | P-Value: {p_val:.4e}")
    print(f"  - Verdict: {'REJECT H0 - Significant Divergence' if p_val < 0.05 else 'FAIL TO REJECT H0 - Statistically Identical'}")
    return p_val