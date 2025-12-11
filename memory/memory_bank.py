"""
Memory Bank for Industrial Equipment Health Monitoring Agent System
-------------------------------------------------------------------

Stores long-term state for each machine including:
- Health index history
- Anomaly scores
- RUL predictions
- Sensor timestamps
- Optional raw or processed features

This module is intentionally lightweight and thread-safe,
acting as the persistent memory backbone for all agents.
"""

import threading
from collections import defaultdict, deque
from typing import Dict, Any, List


class MemoryBank:
    """
    Thread-safe memory manager for storing machine degradation history.
    
    Example usage:
        mem = MemoryBank()
        mem.store("EQP-001", health=0.82, anomaly=1.25, rul=140, features={...})
        hist = mem.get_history("EQP-001")
    """

    def __init__(self, max_history: int = 500):
        """
        Parameters
        ----------
        max_history : int
            Maximum number of stored entries per metric per machine.
            Uses deque to maintain a rolling history.
        """
        self.lock = threading.Lock()
        self.max_history = max_history

        # Internal structure:
        # machine_id -> {
        #     "health": deque,
        #     "anomaly": deque,
        #     "rul": deque,
        #     "timestamp": deque,
        #     "features": deque
        # }
        self.memory: Dict[str, Dict[str, deque]] = defaultdict(
            lambda: {
                "health": deque(maxlen=self.max_history),
                "anomaly": deque(maxlen=self.max_history),
                "rul": deque(maxlen=self.max_history),
                "timestamp": deque(maxlen=self.max_history),
                "features": deque(maxlen=self.max_history),
            }
        )

    # ------------------------------------------------------------------
    # Store new datapoint
    # ------------------------------------------------------------------
    def store(
        self,
        machine_id: str,
        health: float,
        anomaly: float,
        rul: float,
        timestamp: float,
        features: Dict[str, Any] = None,
    ):
        """
        Stores a new observation for the machine.

        Parameters
        ----------
        machine_id : str
            Machine identifier (e.g., 'EQP-001').
        health : float
            Health index from signal processing agent.
        anomaly : float
            Computed anomaly score.
        rul : float
            Estimated remaining useful life.
        timestamp : float
            Timestamp associated with the observation.
        features : dict, optional
            Any additional processed features (FFT bands, RMS, stats, etc.).
        """
        with self.lock:
            self.memory[machine_id]["health"].append(health)
            self.memory[machine_id]["anomaly"].append(anomaly)
            self.memory[machine_id]["rul"].append(rul)
            self.memory[machine_id]["timestamp"].append(timestamp)
            self.memory[machine_id]["features"].append(features or {})

    # ------------------------------------------------------------------
    # Retrieve history for a machine
    # ------------------------------------------------------------------
    def get_history(self, machine_id: str) -> Dict[str, List[Any]]:
        """
        Returns the full metric history for a machine as lists.
        """
        with self.lock:
            if machine_id not in self.memory:
                return {}

            return {
                key: list(values)
                for key, values in self.memory[machine_id].items()
            }

    # ------------------------------------------------------------------
    # Retrieve most recent entry
    # ------------------------------------------------------------------
    def latest(self, machine_id: str) -> Dict[str, Any]:
        """
        Returns the most recent datapoint for the machine.
        """
        with self.lock:
            mem = self.memory[machine_id]

            if len(mem["health"]) == 0:
                return {}

            return {
                "health": mem["health"][-1],
                "anomaly": mem["anomaly"][-1],
                "rul": mem["rul"][-1],
                "timestamp": mem["timestamp"][-1],
                "features": mem["features"][-1],
            }

    # ------------------------------------------------------------------
    # Return all machines being monitored
    # ------------------------------------------------------------------
    def list_machines(self) -> List[str]:
        """
        Returns a list of all machine IDs stored in the memory bank.
        """
        with self.lock:
            return list(self.memory.keys())
