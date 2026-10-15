"""Ensemble drought predictor.

Loads the trained Random Forest + XGBoost models and computes an
averaged probability for a given feature row.
"""
import joblib
import pandas as pd

from utils.config import (
    ENSEMBLE_PKL, FEATURES_PKL, ENSEMBLE_WEIGHTS, DEFAULT_THRESHOLD,
)


class DroughtPredictor:
    """Wraps the trained ensemble.

    Usage:
        predictor = DroughtPredictor().load()
        probs = predictor.predict_proba(feature_df)
    """

    def __init__(self):
        self.rf = None
        self.xgb = None
        self.features = None

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------
    def load(self) -> "DroughtPredictor":
        bundle = joblib.load(ENSEMBLE_PKL)
        self.rf  = bundle["rf"]
        self.xgb = bundle["xgb"]
        self.features = joblib.load(FEATURES_PKL)
        return self

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------
    def predict_proba(self, feature_row: dict) -> dict:
        """Return drought probabilities for one feature row.

        Returns
        -------
        dict with keys:
            probability  — ensemble average (0-1)
            rf_prob      — Random Forest only
            xgb_prob     — XGBoost only
        """
        X = pd.DataFrame([feature_row])[self.features].fillna(0)

        rf_p  = float(self.rf.predict_proba(X)[0, 1])
        xgb_p = float(self.xgb.predict_proba(X)[0, 1])
        p     = (ENSEMBLE_WEIGHTS["random_forest"] * rf_p
                 + ENSEMBLE_WEIGHTS["xgboost"]     * xgb_p)

        return {
            "probability": p,
            "rf_prob":     rf_p,
            "xgb_prob":    xgb_p,
        }
