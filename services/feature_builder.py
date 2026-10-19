"""Build the 31-feature input row for a single district-dekad.

The trained ensemble expects a specific 31-column vector. This class
extracts that vector from the engineered rainfall DataFrame.
"""
import pandas as pd

from utils.config import FEATURES_PKL  # not strictly needed, but documents intent


class FeatureBuilder:
    """Turns (district, date) into a model-ready feature dict.

    The DataFrame is passed in once; every call returns a fresh row.
    """

    def __init__(self, rainfall: pd.DataFrame, features: list[str]):
        self.rainfall = rainfall
        self.features = features

    
    # Public API
    
    def build(self, district: str, dekad) -> dict:
        """Return a dict of all 31 features for one district-dekad.

        Parameters
        ----------
        district : str
            District name, e.g. "CENTRAL".
        dekad : datetime.date
            The dekad date, e.g. datetime.date(1982, 1, 1).

        Returns
        -------
        dict mapping feature name -> value
        """
        row = self._lookup(district, dekad)
        return self._to_dict(row)

    def build_frame(self, district: str, dekad) -> pd.DataFrame:
        """Same as build(), but wrapped in a single-row DataFrame.

        Useful for direct model calls that expect a DataFrame.
        """
        return pd.DataFrame([self.build(district, dekad)])[self.features]

    
    # Internal

    def _lookup(self, district: str, dekad) -> pd.Series:
        mask = (
            (self.rainfall["district"] == district)
            & (self.rainfall["date"].dt.date == dekad)
        )
        matches = self.rainfall.loc[mask]
        if matches.empty:
            raise ValueError(
                f"No rainfall row for district={district!r} dekad={dekad}"
            )
        return matches.iloc[0]

    def _to_dict(self, row: pd.Series) -> dict:
        """Pull each feature out of the row as a plain Python float/int."""
        out = {}
        for name in self.features:
            val = row[name]
            # Preserve is_wet and month as ints; everything else as float
            if name in {"month", "is_wet", "recent_deficit_count"}:
                out[name] = int(val)
            else:
                out[name] = float(val)
        return out
