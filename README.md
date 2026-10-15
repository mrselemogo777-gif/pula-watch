# Pula Watch — Botswana Drought Early-Warning System



## Notebook

The full methodology is in `pula_watch.ipynb`:

- Data loading & district mapping (HDX / WFP CHIRPS v2)
- Drought definition (SADC / FEWS NET thresholds)
- Historical analysis (2023 = worst year on record)
- Feature engineering with **leakage audit** (v1–v3 rejected)
- Random Forest + XGBoost training
- 5-fold cross-validation
- Temporal holdout (train pre-2015, test 2015+)
- Threshold analysis & ensemble comparison

## Model

Ensemble of Random Forest + XGBoost, trained on 30 lagged rainfall features.

| Metric | Value |
|---|---|
| Accuracy (random split) | 96.2% |
| Accuracy (temporal holdout) | 96.0% |
| ROC-AUC | 0.985 |
| F1 (balanced, threshold 0.65) | 0.812 |
| Precision (drought) | 0.834 |
| Recall (drought) | 0.792 |

## Data

Rainfall: HDX / WFP CHIRPS v2 — 16,360 dekads × 10 rural districts × 1981–2026.

## Author

Legakwa Selemogo · [@mrselemogo777-gif](https://github.com/mrselemogo777-gif)
