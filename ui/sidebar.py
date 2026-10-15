"""Sidebar: persona selector, threshold slider, rule toggle."""
import streamlit as st

from utils.config import (
    PERSONAS, DEFAULT_LAG_MAX, THRESHOLD_RANGE,
)


class Sidebar:
    """Renders the entire sidebar and returns the user's chosen config."""

    def __init__(self):
        self.persona = None
        self.threshold = None
        self.confirm_rule = None
        self.lag_max = None

    def render(self) -> dict:
        """Draw the sidebar and return the selected settings."""
        st.sidebar.header("Operating point")

        # Persona radio
        self.persona = st.sidebar.radio(
            "Deployment scenario:",
            list(PERSONAS.keys()),
            index=1,  # "Balanced (default)"
        )
        persona_cfg = PERSONAS[self.persona]

        # Threshold slider (default from persona)
        lo, hi, step = THRESHOLD_RANGE
        self.threshold = st.sidebar.slider(
            "Threshold",
            lo, hi,
            float(persona_cfg["threshold"]),
            step,
        )

        # Confirmation rule toggle
        self.confirm_rule = st.sidebar.checkbox(
            "Apply confirmation rule (lagged_3mo_ratio < 0.72)",
            value=persona_cfg["confirm_rule"],
        )

        # Lag max number input
        self.lag_max = st.sidebar.number_input(
            "Confirmation lag max",
            0.50, 1.00,
            float(DEFAULT_LAG_MAX),
            0.01,
        )

        # Operating points reference table
        st.sidebar.markdown("---")
        st.sidebar.markdown(
            """
**Operating points**

| Persona | Prec | Rec |
|---|---|---|
| Farmer (0.50) | 0.72 | 0.84 |
| Balanced (0.65) | 0.83 | 0.79 |
| Budget (0.80 + rule) | **0.91** | 0.65 |
"""
        )

        return {
            "persona": self.persona,
            "threshold": self.threshold,
            "confirm_rule": self.confirm_rule,
            "lag_max": self.lag_max,
        }
