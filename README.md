
# Procurement Projection & AI Planning
## Supply Chain AI Intern Assignment — Fast&Up (Aeronutrix Sports Products)
**Submitted by:** Arya Manjardekar | April 2026

---

## Project Overview
AI-driven procurement analysis for FY26 targeting 3× revenue growth 
(₹10.5 Cr → ₹31.5 Cr) using a ₹10.08 Cr procurement budget across 5 SKUs.

---

## Files Included

| File | Description |
|---|---|
| Procurement_Analysis.ipynb | Main Jupyter notebook (Tasks 1-5) |
| Procurement_Analysis_Outputs.xlsx | Excel outputs for all tasks |
| task1_forecast.png | FY26 demand forecast charts |
| task2_reorder.png | Reorder point normal vs stress |
| task3_optimization.png | Budget allocation + sensitivity |
| task4_supplier_risk.png | Supplier risk heatmap |

---

## Task Summary

### Task 1 — Demand Forecasting
- Built SKU-level revenue history (FY22-FY25)
- Applied growth multipliers based on product trajectory
- FY26 projection: ₹31.24 Cr across 5 SKUs (412,747 units)
- Libraries: pandas, numpy, matplotlib

### Task 2 — AI Reorder Point Calculator
- Formula: Reorder Point = (Daily Demand × Lead Time) + Safety Stock
- Safety Stock = Z × σ_LT × √LT (Z=1.65, 95% service level)
- Stress tested with 50% demand spike — all SKUs showed ~49% ROP increase
- Libraries: numpy, pandas

### Task 3 — Budget Optimization
- Linear programming using PuLP library
- Objective: Maximize revenue-weighted units within ₹10.08 Cr budget
- Constraints: Min 60% demand fulfillment per SKU, no overbuying
- Sensitivity: Tested at -20% (₹8.06 Cr) and +20% (₹12.10 Cr)
- Libraries: pulp, pandas, matplotlib

### Task 4 — Supplier Risk Assessment
- 15 suppliers assessed (3 per SKU) across 5 dimensions
- Scoring: Price, Lead Time, Reliability, MOQ Flexibility, Geo Risk
- 3 high-risk suppliers flagged (score < 7.0)
- Libraries: pandas, matplotlib

### Task 5 — Executive Report
- 5-slide PowerPoint deck
- 3-page PDF report with findings, risks, and 90-day action plan

---

## How to Run
1. Open Procurement_Analysis.ipynb in Google Colab or Jupyter
2. Run cells sequentially (Cell 1 through Cell 17)
3. All outputs auto-save as PNG and Excel files

## Dependencies
pip install prophet scikit-learn pulp openpyxl pandas numpy matplotlib

## AI Tools Disclosure
Code structuring and report drafting used Claude (Anthropic).
All analytical decisions, assumptions, and business interpretations 
were reviewed and validated by the author.
