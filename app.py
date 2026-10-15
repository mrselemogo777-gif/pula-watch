"""Pula Watch — Botswana Drought Classification Tool.

Streamlit entry point. Wires together data, model, and views.
"""
import streamlit as st

from utils.data_loader       import DataLoader
from services.feature_builder import FeatureBuilder
from services.predictor       import DroughtPredictor
from services.risk            import RiskClassifier
from ui.sidebar               import Sidebar
from ui.prediction_view       import PredictionView
from ui.history_view          import HistoryView
from ui.map_view              import MapView

import joblib
from utils.config import FEATURES_PKL, DEFAULT_LAG_MAX


# ────────────────────────────────────────────────────────────
# Page
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pula Watch — Botswana Drought Classification",
    page_icon="🌧️",
    layout="wide",
)

st.title("🌧️ Pula Watch")
st.caption("Botswana Drought Classification Tool · "
           "Ensemble (RF + XGBoost) · 1981–2026")
st.warning(
    "**Decision-support tool.** Outputs require human review. "
    "Not designed for autonomous aid triggering, livestock movement, or "
    "water rationing without confirmation from a qualified officer.",
    icon="⚠️",
)


# ────────────────────────────────────────────────────────────
# Bootstrapping (cached by Streamlit on rerun)
# ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_app():
    dl          = DataLoader().load()
    features    = joblib.load(FEATURES_PKL)
    predictor   = DroughtPredictor().load()
    fb          = FeatureBuilder(dl.rainfall, features)
    risk        = RiskClassifier(lag_max=DEFAULT_LAG_MAX)
    return dl, predictor, fb, risk


dl, predictor, fb, risk = load_app()


# ────────────────────────────────────────────────────────────
# UI
# ────────────────────────────────────────────────────────────
settings = Sidebar().render()

PredictionView(dl, predictor, fb, risk).render(
    threshold=settings["threshold"],
    confirm_rule=settings["confirm_rule"],
    lag_max=settings["lag_max"],
)

st.markdown("---")

HistoryView(dl).render()
MapView(dl).render()

st.caption(
    "Data: HDX / WFP CHIRPS v2 · Ensemble RF + XGBoost · "
    "30 lagged/spatial features · Human review required before action"
)
