"""Load rainfall and district boundary data for Pula Watch.

Single class, single job: get the app's data ready and cached.
Streamlit's @st.cache_data cannot hash `self`, so the cached readers
live as module-level functions and the class simply calls them.
"""
import pandas as pd
import geopandas as gpd
import streamlit as st

from utils.config import RAIN_CSV, SHAPE_FILE, DROUGHT_THRESHOLDS


# ---------------------------------------------------------------------
# Cached readers (module-level so Streamlit can hash the path arg)
# ---------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _read_rainfall(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df = df[df["adm_level"] == 1].copy()
    df["year"]  = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df


@st.cache_data(show_spinner=False)
def _read_districts(path: str) -> gpd.GeoDataFrame:
    return gpd.read_file(path)


# ---------------------------------------------------------------------
# DataLoader
# ---------------------------------------------------------------------
class DataLoader:
    """Loads and prepares the rainfall + district dataset.

    Everything downstream (features, model, views) reads from
    `self.rainfall` and `self.districts`.
    """

    def __init__(self):
        self.rainfall  = None
        self.districts = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def load(self) -> "DataLoader":
        """Load both sources, attach district names, add drought class."""
        self.rainfall  = _read_rainfall(str(RAIN_CSV))
        self.districts = _read_districts(str(SHAPE_FILE))
        self._attach_names()
        self._add_drought_class()
        return self

    # ------------------------------------------------------------------
    # Internal helpers (no caching needed here)
    # ------------------------------------------------------------------
    def _attach_names(self) -> None:
        """Map PCODE -> district name if not already present in CSV."""
        if "district" in self.rainfall.columns:
            return
        lookup = dict(zip(self.districts["ADM1_PCODE"], self.districts["ADM1_EN"]))
        self.rainfall["district"] = self.rainfall["PCODE"].map(lookup)

    def _add_drought_class(self) -> None:
        """Attach SADC/FEWS NET drought class + is_drought flag."""
        def classify(q):
            if pd.isna(q):
                return "Unknown"
            for limit, name in DROUGHT_THRESHOLDS:
                if q < limit:
                    return name
            return "Very Wet"

        self.rainfall["class"] = self.rainfall["r3q"].apply(classify)
        self.rainfall["is_drought"] = (
            self.rainfall["class"].isin(["Severe", "Extreme"]).astype(int)
        )

    # ------------------------------------------------------------------
    # Convenience accessors for the UI
    # ------------------------------------------------------------------
    def districts_list(self) -> list[str]:
        """Sorted list of district names for the dropdown."""
        return sorted(self.rainfall["district"].dropna().unique().tolist())

    def years_for(self, district: str) -> list[int]:
        """All years available for a district, newest first."""
        yrs = self.rainfall.loc[
            self.rainfall["district"] == district, "year"
        ].unique()
        return sorted((int(y) for y in yrs), reverse=True)

    def dekads_for(self, district: str, year: int) -> list:
        """Dekads in `year` that have complete lag features."""
        sub = self.rainfall[
            (self.rainfall["district"] == district)
            & (self.rainfall["year"] == year)
        ].sort_values("date")
        sub = sub[sub["r3h_lag6"].notna()]
        return sub["date"].dt.date.tolist()
