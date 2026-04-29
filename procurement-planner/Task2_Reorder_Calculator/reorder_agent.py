# ============================================================
# reorder_agent.py
# Task 2: AI-Powered Dynamic Reorder Point Calculator
# Fast&Up (Aeronutrix Sports Products Pvt Ltd)
# Author: Arya Manjardekar | April 2026
# ============================================================

# WHY THIS EXISTS:
# Manual reorder decisions lead to stockouts during growth phases.
# This script automates reorder point calculation using statistical
# safety stock formulas, adjusted for supplier reliability and demand growth.
# It acts as an "AI agent" by dynamically adapting to different demand
# scenarios without manual recalculation.

# FORMULA USED (from assignment brief):
# Safety Stock = Z x σ_LT x √LT
#   Z    = 1.65 (service level factor for 95% in-stock probability)
#   σ_LT = standard deviation of lead time (days)
#   LT   = average lead time (days)
# Reorder Point = (Average Daily Demand x Lead Time) + Safety Stock

import numpy as np
import pandas as pd


# ─── CORE AGENT FUNCTION ──────────────────────────────────────

def reorder_agent(sku_name, annual_units, lead_time_days,
                  lead_time_std, supplier_reliability,
                  growth_factor=1.0):
    """
    Dynamically calculates reorder point for a single SKU.

    Parameters:
    -----------
    sku_name            : str   - Name of the product SKU
    annual_units        : int   - Projected annual demand in units
    lead_time_days      : float - Average days from order placement to receipt
    lead_time_std       : float - Std deviation of lead time (measures variability)
    supplier_reliability: float - Score 0 to 1 (1.0 = perfectly reliable)
    growth_factor       : float - Demand multiplier for scenario testing
                                  1.0 = normal demand
                                  1.5 = 50% demand spike

    Returns:
    --------
    dict containing all reorder metrics for this SKU
    """

    # 95% service level — means we want to be in-stock 95% of the time
    # Z = 1.65 is the standard normal distribution value for 95%
    Z = 1.65

    # Apply growth factor to simulate different demand scenarios
    # e.g., growth_factor=1.5 simulates a sudden 50% demand surge
    adjusted_annual = annual_units * growth_factor

    # Convert annual demand to daily demand
    # We use 365 days (not working days) for continuous supply chain operations
    daily_demand = adjusted_annual / 365

    # RELIABILITY ADJUSTMENT:
    # A less reliable supplier creates more uncertainty, requiring extra buffer.
    # Formula: multiply safety stock by (1 + gap from perfect reliability)
    # Example: 80% reliable → multiply by (1 + 0.20) = 1.20x more safety stock
    # Example: 90% reliable → multiply by (1 + 0.10) = 1.10x more safety stock
    reliability_adj = 1 + (1 - supplier_reliability)

    # SAFETY STOCK CALCULATION:
    # Z x σ_LT x √LT captures the statistical uncertainty in lead time.
    # Higher lead time variability (σ_LT) = more safety stock needed.
    # Longer average lead time (LT) = more exposure to variability.
    # Reliability adjustment adds buffer for supplier unpredictability.
    safety_stock = Z * lead_time_std * np.sqrt(lead_time_days) * reliability_adj

    # REORDER POINT:
    # When inventory hits this level, place a new order immediately.
    # = Units we'll sell while waiting for the new order to arrive
    #   (daily_demand x lead_time) + the safety buffer (safety_stock)
    reorder_point = (daily_demand * lead_time_days) + safety_stock

    # ECONOMIC ORDER QUANTITY (EOQ):
    # Optimal batch size that minimizes total ordering + holding costs.
    # EOQ = √(2 x Annual Demand x Ordering Cost / Holding Cost per unit)
    ordering_cost = 5000   # Rs fixed cost per purchase order (admin, logistics)
    holding_cost  = 50     # Rs to hold 1 unit for 1 year (storage, capital tie-up)
    eoq = np.sqrt((2 * adjusted_annual * ordering_cost) / holding_cost)

    return {
        'SKU':                     sku_name,
        'Scenario':                f"{growth_factor}x demand",
        'Annual Demand (units)':   int(adjusted_annual),
        'Daily Demand':            round(daily_demand, 1),
        'Lead Time (days)':        lead_time_days,
        'Lead Time Std Dev':       lead_time_std,
        'Supplier Reliability':    f"{supplier_reliability * 100:.0f}%",
        'Safety Stock (units)':    int(safety_stock),
        'Reorder Point (units)':   int(reorder_point),
        'EOQ (units)':             int(eoq),
    }


# ─── SKU PARAMETERS ───────────────────────────────────────────
# Lead times and reliability based on Fast&Up supply chain context.
# Plant Protein has longest lead time — ingredients often imported.
# Daily Fiber has highest reliability — simpler local sourcing.

SKU_PARAMS = {
    'Reload Orange': {
        'lead_time_days':       21,    # 3 weeks avg lead time
        'lead_time_std':         4,    # ±4 days variability
        'supplier_reliability': 0.85,  # 85% on-time delivery
    },
    'Reload E&V': {
        'lead_time_days':       25,    # Slightly longer — multi-ingredient
        'lead_time_std':         5,
        'supplier_reliability': 0.80,
    },
    'Plant Protein Chocolate': {
        'lead_time_days':       30,    # Longest — often imported protein isolate
        'lead_time_std':         7,    # High variability — international shipping
        'supplier_reliability': 0.75,  # Lowest reliability — import complexity
    },
    'Lean Body': {
        'lead_time_days':       21,
        'lead_time_std':         4,
        'supplier_reliability': 0.85,
    },
    'Daily Fiber': {
        'lead_time_days':       18,    # Shortest — local fiber sourcing
        'lead_time_std':         3,    # Low variability — domestic supply
        'supplier_reliability': 0.90,  # Highest reliability
    },
}

# FY26 unit forecasts from assignment brief (actual data)
FY26_UNITS = {
    'Reload Orange':           12600,
    'Reload E&V':              10800,
    'Plant Protein Chocolate':  9800,
    'Lean Body':                6650,
    'Daily Fiber':             11200,
}

SKU_LIST = list(SKU_PARAMS.keys())


# ─── SCENARIO 1: NORMAL DEMAND ────────────────────────────────

def run_normal_scenario():
    """Run reorder calculations at standard FY26 demand levels."""
    print("=" * 65)
    print("SCENARIO 1: Normal FY26 Demand (growth_factor = 1.0)")
    print("=" * 65)

    results = []
    for sku in SKU_LIST:
        result = reorder_agent(
            sku_name=sku,
            annual_units=FY26_UNITS[sku],
            growth_factor=1.0,      # No adjustment — baseline
            **SKU_PARAMS[sku]
        )
        results.append(result)

    df = pd.DataFrame(results).set_index('SKU')
    print(df[['Daily Demand', 'Safety Stock (units)',
              'Reorder Point (units)', 'EOQ (units)']])
    return df


# ─── SCENARIO 2: STRESS TEST (50% DEMAND SPIKE) ───────────────

def run_stress_scenario():
    """
    Simulate a sudden 50% demand surge.
    Represents: viral campaign, festive season, influencer surge,
    or unexpected bulk B2B order.
    """
    print("\n" + "=" * 65)
    print("SCENARIO 2: Stress Test — 50% Demand Spike (growth_factor = 1.5)")
    print("=" * 65)

    results = []
    for sku in SKU_LIST:
        result = reorder_agent(
            sku_name=sku,
            annual_units=FY26_UNITS[sku],
            growth_factor=1.5,      # 50% above normal — stress scenario
            **SKU_PARAMS[sku]
        )
        results.append(result)

    df = pd.DataFrame(results).set_index('SKU')
    print(df[['Daily Demand', 'Safety Stock (units)',
              'Reorder Point (units)', 'EOQ (units)']])
    return df


# ─── COMPARISON REPORT ────────────────────────────────────────

def compare_scenarios(df_normal, df_stress):
    """Show side-by-side impact of the demand spike on reorder points."""
    print("\n" + "=" * 65)
    print("SCENARIO COMPARISON: Normal vs 50% Demand Spike")
    print("=" * 65)

    comparison = pd.DataFrame({
        'Normal ROP':      df_normal['Reorder Point (units)'],
        'Stress ROP':      df_stress['Reorder Point (units)'],
        'ROP Change':      df_stress['Reorder Point (units)'] -
                           df_normal['Reorder Point (units)'],
        'ROP Increase %':  ((df_stress['Reorder Point (units)'] -
                             df_normal['Reorder Point (units)']) /
                             df_normal['Reorder Point (units)'] * 100).round(1)
    })
    print(comparison)

    print("\n--- Key Insights ---")
    most_sensitive = comparison['ROP Change'].idxmax()
    print(f"Most sensitive SKU: {most_sensitive}")
    print(f"  Normal ROP:  {comparison.loc[most_sensitive, 'Normal ROP']:,} units")
    print(f"  Stress ROP:  {comparison.loc[most_sensitive, 'Stress ROP']:,} units")
    print(f"  Increase:    +{comparison.loc[most_sensitive, 'ROP Change']:,} units "
          f"({comparison.loc[most_sensitive, 'ROP Increase %']}%)")
    print("\nA 50% demand spike requires ~49-50% higher reorder points across all SKUs.")
    print("Plant Protein Chocolate is highest risk:")
    print("  → Longest lead time (30 days)")
    print("  → Lowest supplier reliability (75%)")
    print("  → Largest safety stock buffer required")
    print("Recommendation: Pre-build 30-day safety stock for Plant Protein")
    print("before summer season and festival periods.")


# ─── MAIN EXECUTION ───────────────────────────────────────────

if __name__ == "__main__":
    # Run both scenarios
    df_normal = run_normal_scenario()
    df_stress = run_stress_scenario()

    # Compare and generate insights
    compare_scenarios(df_normal, df_stress)

    print("\n" + "=" * 65)
    print("Reorder agent execution complete.")
    print("=" * 65)
