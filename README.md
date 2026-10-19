# Pula Watch — Botswana Drought Classification Tool

Ensemble (Random Forest + XGBoost) trained on 31 features — 30 lagged
rainfall measurements plus the NOAA Oceanic Niño Index (ENSO) — from 16,360
dekads of WFP CHIRPS v2 data (1981–2026).

**Live demo:** https://pula-watch.streamlit.app

## ⚠️ Scope

Pula Watch is a **decision-support tool**, not an autonomous warning system.
It classifies historical dekads as drought or not-drought, with confidence
tiers for human review by extension officers, NGOs, or researchers. It is
not designed to trigger aid disbursement, livestock movement, or water
rationing without confirmation from a qualified officer.

## 🌍 Climate Justice Context

Drought is not just a physical phenomenon. The people who bear its burden
are not distributed evenly.

- **Eriksen et al. (2021)** show that adaptation limits in southern Africa
  are shaped by unequal access to resources, not just rainfall variability.
- **Tschakert et al. (2019)** document how vulnerability to climate stress
  in southern Africa is produced by intersecting factors — gender, land
  tenure, and access to water infrastructure — that a rainfall classifier
  cannot see.
- **Niang et al. (2014)**, in the IPCC's Africa chapter, note that drought
  monitoring is a necessary but insufficient condition for effective relief
  targeting.

Pula Watch classifies the physical signal. It does not, and cannot, capture
the social dimensions of drought vulnerability.

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

| Metric | Without ENSO | With ENSO | Delta |
|---|---|---|---|
| Accuracy | 96.20% | 96.47% | +0.27% |
| Precision | 83.40% | 84.42% | +1.02% |
| Recall | 79.20% | 80.38% | +1.18% |
| F1 | 81.20% | 82.35% | +1.15% |
| ROC-AUC | 98.50% | 98.46% | -0.04% |

## 🧪 Leakage Audit

| Version | Accuracy | Top Feature | Verdict |
|---|---|---|---|
| v1 | 98.5% | anomaly | Linear transform of r3q |
| v2 | 99.5% | r3h_ratio | Mathematically = r3q / 100 |
| v3 | 81.7% | month | Worse than baseline |
| v4 | 96.2% | r3h_lag1_ratio | Shipped — lagged only |
| v5 | 96.47% | r3h_lag1_ratio | Current — ENSO-enhanced |

## 🎯 Operating Points

| Persona | Threshold | Precision | Recall |
|---|---|---|---|
| Farmer | 0.50 | 0.721 | 0.842 |
| Balanced (default) | 0.65 | 0.844 | 0.804 |
| Budget-constrained | 0.80 + rule | 0.906 | 0.646 |
| Highest confidence | 0.85 + rule | 0.930 | 0.605 |

## 🌍 Districts Covered

All 10 rural districts of Botswana: Southern · South East · Kweneng ·
Kgatleng · Central · North East · North West · Chobe · Ghanzi · Kgalagadi

## 📈 Worst Drought Years on Record

| Rank | Year | Drought dekads |
|---|---|---|
| 1 | 2023 | 121 |
| 2 | 1992 | 108 |
| 3 | 1994 | 99 |
| 4 | 2019 | 82 |
| 5 | 1987 | 79 |

## 🖥️ Technology Stack

Python 3.11 · scikit-learn · XGBoost · Streamlit · Geopandas · Plotly ·
HDX / WFP CHIRPS v2 · NOAA ONI

## 📦 Installation

git clone https://github.com/mrselemogo777-gif/pula-watch.git
cd pula-watch
pip install -r requirements.txt
streamlit run app.py

## 🔬 Future Work

Pula Watch is a **historical drought classifier**, not a forecaster. It
answers "Was this dekad a drought?" with high confidence, but not "Will the
next dekad be a drought?"

This is a deliberate design choice. The classifier provides the validation
layer that any forecasting system needs. Once "what counts as a drought" is
answered reliably, the next question — "what comes next?" — can be built on top.

Planned work:

- Integrate SADC seasonal forecasts (3–6 month lead time)
- Add Indian Ocean Dipole (IOD) index alongside ENSO
- Rolling-origin cross-validation for forecast evaluation
- Extend to NDVI and soil moisture

None is included in the current deployment.

## 📚 References

- Eriksen, S., et al. (2021). Adaptation interventions and their effect on
  vulnerability in the Global South. World Development, 141, 105383.
- Niang, I., et al. (2014). Africa. In Climate Change 2014: Impacts,
  Adaptation, and Vulnerability. Cambridge University Press.
- Tschakert, P., et al. (2019). One thousand ways to experience loss.
  Global Environmental Change, 55, 58-72.

## 👤 Author

Legakwa Selemogo · github.com/mrselemogo777-gif

## License

MIT
