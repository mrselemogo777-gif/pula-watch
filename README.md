# Pula Watch — Botswana Drought Early-Warning System

Ensemble (Random Forest + XGBoost) trained on 31 features — 30 lagged
rainfall measurements plus the NOAA ONI climate index — from 16,360 dekads
of WFP CHIRPS v2 data (1981–2026).

**Live demo:** https://pula-watch.streamlit.app

##  Scope

Pula Watch is a **decision-support tool**, not an autonomous warning system.
It classifies historical dekads as drought or not-drought, with confidence
tiers for human review by extension officers, NGOs, or researchers. It is
not designed to trigger aid disbursement, livestock movement, or water
rationing without confirmation from a qualified officer.

## 📓 Notebook

The full methodology is in `pula_watch.ipynb`:

- Data loading & district mapping (HDX / WFP CHIRPS v2)
- Drought definition (SADC / FEWS NET thresholds)
- Historical analysis (2023 = worst year on record)
- Feature engineering with leakage audit (v1–v3 rejected)
- Random Forest + XGBoost training
- 5-fold cross-validation
- Temporal holdout (train pre-2015, test 2015+)
- ENSO climate feature extension

## 📊 Model Performance

Final model (with ENSO, 31 features):

| Metric | Value |
|---|---|
| Accuracy (random split) | 96.47% |
| F1 (balanced, threshold 0.65) | 82.35% |
| Precision (drought) | 84.42% |
| Recall (drought) | 80.38% |
| ROC-AUC | 98.46% |
| Accuracy (temporal holdout) | 96.0% |
| 5-fold CV accuracy | 0.9538 ± 0.0058 |

## 🌡️ Climate Feature (ENSO)

The model incorporates the NOAA Oceanic Niño Index (ONI) as a 31st feature.
Botswana's rainfall is teleconnected to ENSO — El Niño years correlate with
reduced rainfall and elevated drought risk.

Impact of adding ENSO:

| Metric | Without ENSO | With ENSO | Delta |
|---|---|---|---|
| Accuracy | 96.20% | 96.47% | +0.27% |
| Precision | 83.40% | 84.42% | +1.02% |
| Recall | 79.20% | 80.38% | +1.18% |
| F1 | 81.20% | 82.35% | +1.15% |
| ROC-AUC | 98.50% | 98.46% | -0.04% |

ENSO contributes a small but consistent signal (RF 0.6%, XGB 1.1% importance).
The +1.18 pp recall improvement is the most important change.

Data source: NOAA CPC ONI (cpc.ncep.noaa.gov)

##  Leakage Audit

Three models were built and rejected before the final version:

| Version | Accuracy | Top Feature | Verdict |
|---|---|---|---|
| v1 | 98.5% | anomaly | Linear transform of r3q (target) |
| v2 | 99.5% | r3h_ratio | Mathematically equivalent to r3q / 100 |
| v3 | 81.7% | month | Worse than the 89.7% always-Normal baseline |
| v4 | 96.2% | r3h_lag1_ratio | Shipped — lagged features only |
| v5 | 96.47% | r3h_lag1_ratio | Current — ENSO-enhanced |

Key insight: drought is a 3-month accumulated deficit. Predicting drought at
dekad t requires rainfall from dekads t-1, t-2, t-3 — not the current dekad,
which leaks the label. The final model uses lagged rainfall only.

## 🎯 Operating Points

| Persona | Threshold | Precision | Recall | Use case |
|---|---|---|---|---|
| Farmer / community alert | 0.50 | 0.721 | 0.842 | Never miss a drought |
| Balanced (default) | 0.65 | 0.844 | 0.804 | General purpose |
| Budget-constrained | 0.80 + rule | 0.906 | 0.646 | Only high-confidence flags |
| Highest confidence | 0.85 + rule | 0.930 | 0.605 | Minimal false alarms |

## 🌍 Districts Covered

All 10 rural districts of Botswana: Southern, South East, Kweneng, Kgatleng,
Central, North East, North West, Chobe, Ghanzi, Kgalagadi.

## 📈 Worst Drought Years on Record

| Rank | Year | Drought dekads |
|---|---|---|
| 1 | 2023 | 121 |
| 2 | 1992 | 108 |
| 3 | 1994 | 99 |
| 4 | 2019 | 82 |
| 5 | 1987 | 79 |

## 🖥️ Technology Stack

- Python 3.11
- scikit-learn (Random Forest)
- XGBoost (gradient boosting)
- Streamlit (web app)
- Geopandas + Plotly (choropleth map)
- HDX / WFP CHIRPS v2 + NOAA ONI (data)

## 📦 Installation

git clone https://github.com/mrselemogo777-gif/pula-watch.git
cd pula-watch
pip install -r requirements.txt
streamlit run app.py

## 🔬 Future Work

- Extend to IOD (Indian Ocean Dipole) index
- Live CHIRPS API integration
- Satellite vegetation indices (NDVI, EVI)
- Soil moisture integration
- Forecasting mode using seasonal forecasts

## 👤 Author

Legakwa Selemogo · github.com/mrselemogo777-gif

## License

MIT