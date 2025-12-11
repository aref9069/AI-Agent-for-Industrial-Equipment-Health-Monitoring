# tools/mcp_maintenance.py

import time
from loguru import logger


def create_maintenance_ticket_via_mcp(
    equipment_id: str,
    anomaly_score: float,
    rul_estimate: float,
) -> dict:
    """
    Stub for an MCP-style maintenance tool.

    In a real deployment, this function would:
    - Call an MCP server
    - Or call a CMMS / EAM system's REST API via an MCP tool
    - Return the created ticket metadata

    For this capstone, we log the action and return a mock ticket object.

    Parameters
    ----------
    equipment_id : str
        ID of the equipment (e.g., 'EQP-001').
    anomaly_score : float
        Current anomaly score for the machine.
    rul_estimate : float
        Current Remaining Useful Life estimate.

    Returns
    -------
    dict
        Mock maintenance ticket metadata.
    """
    timestamp = int(time.time())
    ticket_id = f"TCK-{equipment_id}-{timestamp}"

    logger.info(
        f"[MCP] Creating maintenance ticket: equipment={equipment_id}, "
        f"anomaly={anomaly_score:.2f}, RUL={rul_estimate:.1f}, ticket={ticket_id}"
    )

    ticket = {
        "ticket_id": ticket_id,
        "equipment_id": equipment_id,
        "anomaly_score": anomaly_score,
        "rul_estimate": rul_estimate,
        "created_at": timestamp,
        "status": "CREATED",
        "source": "industrial-equipment-health-agent",
    }

    return ticket
