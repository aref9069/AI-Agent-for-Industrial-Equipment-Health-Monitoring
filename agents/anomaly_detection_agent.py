# agents/anomaly_detection_agent.py

from .base_agent import BaseAgent


class AnomalyDetectionAgent(BaseAgent):
    """
    Computes an anomaly score using z-score normalization of the
    current health index relative to a baseline mean and std.
    """

    def __init__(self, machine_id: str, logger, baseline_mean: float = 0.1, baseline_std: float = 0.05):
        super().__init__(name="AnomalyDetectionAgent", machine_id=machine_id, logger=logger)
        self.baseline_mean = baseline_mean
        self.baseline_std = baseline_std

    def detect(self, health_index: float, history: dict) -> dict:
        """
        Parameters
        ----------
        health_index : float
            Latest health index from SignalProcessingAgent.
        history : dict
            Full history from MemoryBank (not heavily used here, but available).

        Returns
        -------
        dict with:
        - "anomaly_score": float
        """
        z = (health_index - self.baseline_mean) / (self.baseline_std + 1e-6)
        anomaly_score = abs(z)

        self.log(
            f"Health Index={health_index:.4f} | "
            f"Baseline Mean={self.baseline_mean:.4f} | "
            f"Baseline Std={self.baseline_std:.4f} | "
            f"Anomaly Score={anomaly_score:.2f}",
            level="info",
        )

        return {"anomaly_score": float(anomaly_score)}
