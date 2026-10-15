"""Turn a drought probability into an operational risk tier.

Decision rules (matching the trained ensemble's operating points):

    HIGH      — probability >= 0.80 AND lagged_3mo_ratio < lag_max
    ELEVATED  — probability >= 0.65
    LOW       — anything below

The confirmation rule (lagged ratio) is what pushes an 80% flag from
"elevated" into "high confidence" — it stops isolated dry dekads from
being treated as full droughts.
"""
from dataclasses import dataclass

from utils.config import RISK_HIGH, RISK_ELEVATED, DEFAULT_LAG_MAX


@dataclass
class RiskResult:
    """The full decision for one prediction."""
    probability: float
    lag_ratio: float
    threshold: float
    tier: str             # "HIGH" | "ELEVATED" | "LOW"
    rule_fires: bool      # lag_ratio < lag_max
    threshold_exceeded: bool
    is_drought: bool      # final decision after rule


class RiskClassifier:
    """Applies threshold + confirmation rule to a probability."""

    def __init__(self, lag_max: float = DEFAULT_LAG_MAX):
        self.lag_max = lag_max

    def classify(self, probability: float, lag_ratio: float,
                 threshold: float) -> RiskResult:
        """Return the tier + decision for one prediction."""
        threshold_exceeded = probability >= threshold
        rule_fires         = lag_ratio < self.lag_max

        if probability >= RISK_HIGH and rule_fires:
            tier = "HIGH"
        elif probability >= RISK_ELEVATED:
            tier = "ELEVATED"
        else:
            tier = "LOW"

        # Final decision: exceeded threshold AND (rule off OR rule fires)
        # — but the app treats the rule as optional. When the rule is ON,
        #   the user has already chosen to require it; when OFF, only the
        #   probability matters.
        is_drought = threshold_exceeded and rule_fires

        return RiskResult(
            probability=probability,
            lag_ratio=lag_ratio,
            threshold=threshold,
            tier=tier,
            rule_fires=rule_fires,
            threshold_exceeded=threshold_exceeded,
            is_drought=is_drought,
        )

    # Convenience: the tier → emoji/label the UI uses
    @staticmethod
    def label(tier: str) -> tuple[str, str]:
        """Returns (emoji, plain label)."""
        return {
            "HIGH":     ("🔴", "HIGH CONFIDENCE DROUGHT RISK"),
            "ELEVATED": ("🟡", "ELEVATED RISK"),
            "LOW":      ("🟢", "LOW RISK"),
        }[tier]
