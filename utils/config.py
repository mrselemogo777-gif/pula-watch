"""Central configuration for Pula Watch.

All paths, thresholds, and constants live here. Nothing else should
hardcode them.
"""
from pathlib import Path

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
BASE_DIR      = Path(__file__).resolve().parent.parent
MODELS_DIR    = BASE_DIR / "models"
UTILS_DIR     = BASE_DIR / "utils"

RAIN_CSV      = UTILS_DIR / "bwa-rainfall-engineered.csv"
SHAPE_FILE    = UTILS_DIR / "bwa_admbnda_adm1_2011.shp"

ENSEMBLE_PKL  = MODELS_DIR / "drought_ensemble.pkl"
FEATURES_PKL  = MODELS_DIR / "features.pkl"
METADATA_JSON = MODELS_DIR / "metadata.json"

# ---------------------------------------------------------------------
# Drought classification (SADC / FEWS NET thresholds on r3q)
# ---------------------------------------------------------------------
DROUGHT_THRESHOLDS = [
    (50,  "Extreme"),
    (60,  "Severe"),
    (80,  "Moderate"),
    (120, "Normal"),
    (160, "Wet"),
    (float("inf"), "Very Wet"),
]
DROUGHT_CLASSES = {"Severe", "Extreme"}

# ---------------------------------------------------------------------
# Operating points (probability thresholds)
# ---------------------------------------------------------------------
PERSONAS = {
    "Farmer / community alert": {"threshold": 0.50, "confirm_rule": False},
    "Balanced (default)":       {"threshold": 0.65, "confirm_rule": False},
    "Budget-constrained":       {"threshold": 0.80, "confirm_rule": True},
}

DEFAULT_THRESHOLD = 0.65
DEFAULT_LAG_MAX   = 0.72
THRESHOLD_RANGE   = (0.20, 0.90, 0.05)  # min, max, step

# ---------------------------------------------------------------------
# Risk tiers
# ---------------------------------------------------------------------
RISK_HIGH     = 0.80   # prob >= 0.80 AND rule fires
RISK_ELEVATED = 0.65   # prob >= 0.65

# ---------------------------------------------------------------------
# Ensemble weights
# ---------------------------------------------------------------------
ENSEMBLE_WEIGHTS = {"random_forest": 0.5, "xgboost": 0.5}
