import streamlit as st

st.set_page_config(
    page_title="Model & Data · Pula Watch",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Model & Data")
st.caption("Methodology, leakage audit, and performance metrics for Pula Watch.")

# MODEL 
st.header("Model")
st.markdown("""
**Ensemble classifier** — 50/50 average of Random Forest (300 trees, max_depth=15)
and XGBoost (300 estimators, max_depth=6, lr=0.1) probability outputs.

Trained on **16,360 dekads** across **10 rural districts** of Botswana, 1981–2026.

**Output:** probability of Severe/Extreme drought (SADC/FEWS NET thresholds: r3q < 60).
""")

# FEATURES 
st.header("Features (31)")
st.markdown("""
| Group | Count | Examples |
|---|---|---|
| Current-dekad measurements | 8 | `rfh`, `rfh_avg`, `r1h`, `r1h_avg`, `rfq`, `r1q`, `month`, `is_wet` |
| Lagged 3-month rainfall | 6 | `r3h_lag1` … `r3h_lag6` |
| Lagged 3-month ratios | 6 | `r3h_lag1_ratio` … `r3h_lag6_ratio` |
| Lagged 1-month rainfall | 3 | `r1h_lag1`, `r1h_lag2`, `r1h_lag3` |
| Spatial context | 2 | `neighbour_lag1_ratio`, `neighbour_lag2_ratio` |
| Cumulative deficit | 3 | `lagged_3mo_avg`, `lagged_3mo_ratio`, `recent_deficit_count` |
| **Climate index** | **1** | **`enso_oni`** (NOAA ONI) |
| Derived | 2 | `rfh_ratio`, `r1h_ratio` |

**No label leakage.** `r3q`, current `r3h`, and `anomaly` are excluded by design.
""")

# LEAKAGE AUDIT
st.header("🧪 Leakage Audit")
st.markdown("""
Three models were built and **rejected** before the final version:

| Version | Accuracy | Top Feature | Verdict |
|---|---|---|---|
| v1 | 98.5% | `anomaly` |  Linear transform of `r3q` (target) |
| v2 | 99.5% | `r3h_ratio` |  Mathematically equivalent to `r3q / 100` |
| v3 | 81.7% | `month` |  Worse than the 89.7% always-Normal baseline |
| **v4** | **96.2%** | `r3h_lag1_ratio` |  **Shipped** — lagged features only |

**Key insight:** drought is a 3-month accumulated deficit. Predicting drought
at dekad *t* requires rainfall from dekads *t-1, t-2, t-3* — not the current
dekad, which leaks the label. The final model uses **lagged rainfall only**,
which is how operational early-warning systems work.
""")

#  PERFORMANCE 
st.header("Performance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Random split (75/25)")
    st.markdown("""
| Metric | Value |
|---|---|
| Accuracy | **0.9647** |
| ROC-AUC | 0.9846 |
| Precision (drought) | **0.8442** |
| Recall (drought) | **0.8038** |
| F1 (drought) | **0.8235** |
| 5-fold CV accuracy | 0.9538 ± 0.0058 |
| 5-fold CV ROC-AUC | 0.9832 ± 0.0021 |
""")

with col2:
    st.subheader("Temporal holdout (train pre-2015, test 2015+)")
    st.markdown("""
| Metric | Value |
|---|---|
| Accuracy | 0.960 |
| ROC-AUC | 0.981 |
| Precision (drought) | 0.820 |
| Recall (drought) | 0.840 |
| Baseline (always-Normal) | 0.882 |
| **Improvement over baseline** | **+7.8 pp** |
""")

st.subheader("Model comparison")

st.markdown("""
| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Always-Normal baseline | 0.898 | 0.000 | 0.000 | 0.000 |
| Simple rule (`lagged_3mo_ratio < 0.7`) | 0.762 | 0.265 | 0.746 | 0.391 |
| Random Forest @ 0.50 | 0.951 | 0.721 | 0.842 | 0.777 |
| XGBoost @ 0.65 | 0.962 | 0.831 | 0.789 | 0.810 |
| **Ensemble @ 0.65 (shipped)** | **0.962** | **0.834** | **0.792** | **0.812** |
| Ensemble @ 0.80 + rule | ~0.94 | **0.906** | 0.646 | 0.754 |
""")

#  THRESHOLD TRADE-OFF 
st.header("Threshold trade-off")

st.markdown("""
The decision threshold controls the precision/recall balance. Higher threshold
= fewer false alarms, but more missed droughts.

| Threshold | Precision | Recall | F1 | Flagged |
|---|---|---|---|---|
| 0.50 | 0.721 | 0.842 | 0.777 | 488 |
| **0.65 (default)** | **0.834** | **0.792** | **0.812** | **397** |
| 0.80 | 0.872 | 0.734 | 0.797 | 352 |
| 0.80 + rule | 0.906 | 0.646 | 0.767 | 307 |
| 0.85 + rule | 0.930 | 0.605 | 0.733 | 272 |
""")

# DATA 
st.header("Data")
st.markdown("""
| Source | Purpose |
|---|---|
| [HDX / WFP CHIRPS v2](https://data.humdata.org/dataset/bwa-rainfall-subnat-full) | Rainfall (1981–2026) |
| [HDX COD-AB Botswana](https://data.humdata.org/dataset/cod-ab-bwa) | District boundaries |

**Coverage:** all 10 rural districts (Southern, South East, Kweneng, Kgatleng,
Central, North East, North West, Chobe, Ghanzi, Kgalagadi).
""")
