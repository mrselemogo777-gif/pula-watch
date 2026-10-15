"""Prediction view: district/year/dekad selector, run button, flag, feature table."""
import datetime as dt

import pandas as pd
import streamlit as st

from services.feature_builder import FeatureBuilder
from services.predictor import DroughtPredictor
from services.risk import RiskClassifier


class PredictionView:
    """Renders the main prediction panel."""

    def __init__(self, data_loader, predictor, feature_builder, risk_classifier):
        self.dl        = data_loader
        self.predictor = predictor
        self.fb        = feature_builder
        self.risk      = risk_classifier
        self.district  = None
        self.year      = None
        self.dekad     = None

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------
    def render(self, threshold: float, confirm_rule: bool, lag_max: float) -> None:
        """Draw the selector, run the prediction on click."""
        self._render_selector()

        if st.button("🚨 Run prediction", type="primary"):
            self._run_and_render(threshold, confirm_rule, lag_max)

    # ------------------------------------------------------------------
    # Selector
    # ------------------------------------------------------------------
    def _render_selector(self) -> None:
        st.subheader("Select district, year, and dekad")
        col1, col2, col3 = st.columns(3)

        with col1:
            self.district = st.selectbox(
                "District", self.dl.districts_list()
            )

        with col2:
            years = self.dl.years_for(self.district)
            self.year = st.selectbox("Year", years, index=0)

        with col3:
            dekads = self.dl.dekads_for(self.district, self.year)
            if not dekads:
                st.warning(
                    f"No dekads with complete lag features for "
                    f"{self.district} in {self.year}."
                )
                st.stop()
            self.dekad = st.selectbox("Dekad", dekads)

    # ------------------------------------------------------------------
    # Run + render
    # ------------------------------------------------------------------
    def _run_and_render(self, threshold, confirm_rule, lag_max) -> None:
        row = self.fb.build(self.district, self.dekad)
        probs = self.predictor.predict_proba(row)

        risk = self.risk.classify(
            probability=probs["probability"],
            lag_ratio=row["lagged_3mo_ratio"],
            threshold=threshold,
        )

        # Header
        st.markdown(f"### {self.district} — {self.dekad}")

        # Flag
        emoji, label = RiskClassifier.label(risk.tier)
        msg = f"{emoji} **{label}** — probability {risk.probability:.0%}"
        if risk.tier == "HIGH":
            st.error(msg)
        elif risk.tier == "ELEVATED":
            st.warning(msg)
        else:
            st.success(msg)

        # Rule status
        st.markdown(
            f"- **Threshold:** {risk.threshold:.2f} → "
            f"{'⚠️ exceeded' if risk.threshold_exceeded else 'not exceeded'}\n"
            f"- **Confirmation rule:** {'ON' if confirm_rule else 'OFF'}  "
            f"(lagged_3mo_ratio < {lag_max})\n"
            f"- **Lagged 3-month ratio:** {risk.lag_ratio:.3f} → "
            f"{'✓ rule fires' if risk.rule_fires else '✗ rule blocked'}"
        )

        # Feature table
        self._render_feature_table(row, probs)

        # Sparkline of last 6 dekads
        self._render_sparkline()

    # ------------------------------------------------------------------
    # Sub-renderers
    # ------------------------------------------------------------------
    def _render_feature_table(self, row: dict, probs: dict) -> None:
        with st.expander("📊 Full feature values for this dekad"):
            display_keys = [
                "rfh", "rfh_avg", "r1h", "r1h_avg", "rfq", "r1q",
                "month", "is_wet",
                "r3h_lag1", "r3h_lag2", "r3h_lag3",
                "r3h_lag4", "r3h_lag5", "r3h_lag6",
                "lagged_3mo_ratio",
                "recent_deficit_count",
                "neighbour_lag1_ratio", "neighbour_lag2_ratio",
            ]
            for k in display_keys:
                if k in row:
                    st.write(f"**{k}** = {row[k]:.3f}" if isinstance(row[k], float)
                             else f"**{k}** = {row[k]}")

            st.markdown(
                f"**Model internals:**\n"
                f"- Random Forest prob: {probs['rf_prob']:.3f}\n"
                f"- XGBoost prob: {probs['xgb_prob']:.3f}\n"
                f"- Ensemble (avg): {probs['probability']:.3f}"
            )

    def _render_sparkline(self) -> None:
        st.markdown("**Recent rainfall (last 6 dekads, mm)**")
        recent = (
            self.dl.rainfall[
                (self.dl.rainfall["district"] == self.district)
                & (self.dl.rainfall["date"].dt.date <= self.dekad)
            ]
            .sort_values("date")
            .tail(6)[["date", "rfh"]]
        )
        st.line_chart(recent.set_index("date")["rfh"])
