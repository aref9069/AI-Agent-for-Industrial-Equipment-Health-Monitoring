# agents/prediction_agent.py

from .base_agent import BaseAgent
from config import INITIAL_HEALTH, DEGRADATION_RATE


class PredictionAgent(BaseAgent):
    """
    Simple Remaining Useful Life (RUL) estimator.

    Uses a crude linear degradation model:
        health ~ INITIAL_HEALTH - DEGRADATION_RATE * cycles

    and estimates RUL as:
        RUL ≈ max(health / DEGRADATION_RATE, 0)

    This is intentionally simple for demonstration and can be
    replaced with a learned RUL model.
    """

    def __init__(self, machine_id: str, logger):
        super().__init__(name="PredictionAgent", machine_id=machine_id, logger=logger)

    def predict_rul(self, history: dict) -> float:
        """
        Parameters
        ----------
        history : dict
            Output of MemoryBank.get_history(machine_id), expected keys:
            "health", "anomaly", "rul", "timestamp", "features".

        Returns
        -------
        float
            Estimated RUL (time / cycles until failure).
        """
        health_hist = history.get("health", [])

        if not health_hist:
            # No history: assume fresh machine
            est_rul = INITIAL_HEALTH / max(DEGRADATION_RATE, 1e-6)
            self.log(
                f"No history yet, using default RUL estimate={est_rul:.2f}",
                level="debug",
            )
            return float(est_rul)

        current_health = float(health_hist[-1])

        # Linear degradation model estimate
        est_rul = max(current_health / max(DEGRADATION_RATE, 1e-6), 0.0)

        self.log(
            f"Current health={current_health:.4f} → Estimated RUL={est_rul:.2f}",
            level="info",
        )

        return float(est_rul)
