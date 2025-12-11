# agents/alert_action_agent.py

from .base_agent import BaseAgent
from config import (
    ANOMALY_Z_THRESHOLD,
    MIN_RUL_WARNING,
    MCP_SERVER_LABEL,
    MCP_TOOL_NAME,
)

# Optional: try to import a real MCP maintenance function if it exists
try:
    from tools.mcp_maintenance import create_maintenance_ticket
except ImportError:
    def create_maintenance_ticket(machine_id: str, anomaly_score: float, rul: float) -> str:
        """
        Fallback stub for MCP maintenance integration.
        Returns a fake ticket ID.
        """
        # In a real deployment, this would call an MCP server or CMMS API.
        return f"STUB-TICKET-{machine_id}"


class AlertActionAgent(BaseAgent):
    """
    Decides when to generate maintenance alerts and tickets based on:
    - anomaly score (z-score threshold)
    - predicted RUL (below warning threshold)

    Integrates with an MCP-style maintenance interface.
    """

    def __init__(self, machine_id: str, logger):
        super().__init__(name="AlertActionAgent", machine_id=machine_id, logger=logger)

    def handle(self, health: float, anomaly_score: float, rul: float) -> None:
        """
        Evaluate conditions and trigger maintenance action if needed.

        Parameters
        ----------
        health : float
            Current health index.
        anomaly_score : float
            Anomaly score from AnomalyDetectionAgent.
        rul : float
            Predicted Remaining Useful Life.
        """
        trigger_anomaly = anomaly_score >= ANOMALY_Z_THRESHOLD
        trigger_rul = rul <= MIN_RUL_WARNING

        if not (trigger_anomaly or trigger_rul):
            self.log(
                f"No alert: health={health:.4f}, anomaly={anomaly_score:.2f}, RUL={rul:.2f}",
                level="debug",
            )
            return

        reason_parts = []
        if trigger_anomaly:
            reason_parts.append(f"anomaly_score={anomaly_score:.2f} ≥ {ANOMALY_Z_THRESHOLD}")
        if trigger_rul:
            reason_parts.append(f"RUL={rul:.2f} ≤ {MIN_RUL_WARNING}")

        reason = "; ".join(reason_parts)

        self.log(
            f"Triggering maintenance ticket due to: {reason}",
            level="warning",
        )

        # MCP-style call
        payload = {
            "type": "mcp",
            "server_label": MCP_SERVER_LABEL,
            "tool": MCP_TOOL_NAME,
            "machine_id": self.machine_id,
            "anomaly_score": float(anomaly_score),
            "rul": float(rul),
            "health": float(health),
        }

        self.log(f"MCP payload: {payload}", level="debug")

        ticket_id = create_maintenance_ticket(
            machine_id=self.machine_id,
            anomaly_score=anomaly_score,
            rul=rul,
        )

        self.log(
            f"Maintenance ticket created: {ticket_id} "
            f"(server_label={MCP_SERVER_LABEL}, tool={MCP_TOOL_NAME})",
            level="warning",
        )
