# agents/data_acquisition_agent.py

import time
import numpy as np

from .base_agent import BaseAgent


class DataAcquisitionAgent(BaseAgent):
    """
    Simulates real-time sensor acquisition for a machine.

    Produces a window of:
    - vibration signal (numpy array)
    - acoustic signal (numpy array)
    - temperature (float)
    - timestamp (float, epoch seconds)

    For demonstration:
    - Normal machines: steady vibration with noise.
    - One machine (e.g., EQP-002) can be set to degrade over time.
    """

    def __init__(self, machine_id: str, logger, sample_rate: int, window_size: int):
        super().__init__(name="DataAcquisitionAgent", machine_id=machine_id, logger=logger)
        self.sample_rate = sample_rate
        self.window_size = window_size
        self._cycle = 0

        # Time vector for one window
        self.t = np.arange(window_size) / float(sample_rate)

    def acquire_window(self) -> dict:
        """
        Simulate sensor window for this cycle.

        Returns
        -------
        dict with keys:
        - "vibration": np.ndarray
        - "acoustic": np.ndarray
        - "temperature": float
        - "timestamp": float
        """
        self._cycle += 1

        # Base harmonic vibration (e.g., rotating machine)
        base_freq = 50.0  # Hz
        base_signal = 0.8 * np.sin(2 * np.pi * base_freq * self.t)

        # Add higher-frequency component
        hf_freq = 250.0
        hf_component = 0.2 * np.sin(2 * np.pi * hf_freq * self.t)

        # Degradation simulation for a specific machine (e.g., EQP-002)
        degradation_factor = 1.0
        if self.machine_id == "EQP-002":
            # Slowly increase noise and high-frequency vibration
            degradation_factor = 1.0 + 0.002 * self._cycle

        noise = 0.1 * degradation_factor * np.random.randn(self.window_size)

        vibration = base_signal + hf_component * degradation_factor + noise

        # Acoustic can be another noisy copy for demo
        acoustic = vibration + 0.05 * np.random.randn(self.window_size)

        # Temperature slowly drifts
        base_temp = 55.0
        temp_drift = 0.01 * self._cycle if self.machine_id == "EQP-002" else 0.0
        temperature = base_temp + temp_drift + np.random.randn() * 0.5

        timestamp = time.time()

        self.log(
            f"Acquired window #{self._cycle} | "
            f"Temp={temperature:.2f}°C",
            level="debug",
        )

        return {
            "vibration": vibration,
            "acoustic": acoustic,
            "temperature": float(temperature),
            "timestamp": float(timestamp),
        }
