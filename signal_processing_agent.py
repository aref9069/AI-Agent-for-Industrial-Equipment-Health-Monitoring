# agents/signal_processing_agent.py

import numpy as np
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import kurtosis, skew

from .base_agent import BaseAgent
from config import BANDPASS_LOW, BANDPASS_HIGH, SAMPLE_RATE, NFFT


class SignalProcessingAgent(BaseAgent):
    """
    Performs classical vibration signal processing:
    - Bandpass filter
    - Envelope detection
    - FFT-based feature extraction
    - Health index computation
    """

    def __init__(self, machine_id: str, logger):
        super().__init__(name="SignalProcessingAgent", machine_id=machine_id, logger=logger)
        self._b, self._a = self._design_bandpass()

    def _design_bandpass(self, order: int = 4):
        nyq = 0.5 * SAMPLE_RATE
        low = BANDPASS_LOW / nyq
        high = BANDPASS_HIGH / nyq
        b, a = butter(order, [low, high], btype="band")
        return b, a

    def _bandpass(self, signal: np.ndarray) -> np.ndarray:
        return filtfilt(self._b, self._a, signal)

    def _envelope(self, signal: np.ndarray) -> np.ndarray:
        analytic = hilbert(signal)
        return np.abs(analytic)

    def _compute_fft_magnitude(self, signal: np.ndarray) -> np.ndarray:
        fft_vals = np.fft.rfft(signal, n=NFFT)
        return np.abs(fft_vals)

    def process(self, window: dict) -> dict:
        """
        Process raw sensor window into health metrics.

        Parameters
        ----------
        window : dict
            Expected keys: "vibration", optionally "acoustic", "temperature".

        Returns
        -------
        dict with:
        - "health_index": float
        - "features": dict
        """
        vib = window["vibration"]
        temp = window.get("temperature", 0.0)

        # 1) Bandpass filter
        vib_bp = self._bandpass(vib)

        # 2) Envelope
        env = self._envelope(vib_bp)

        # 3) FFT magnitude
        fft_mag = self._compute_fft_magnitude(vib_bp)

        # 4) Basic statistical features
        rms = float(np.sqrt(np.mean(vib_bp**2)))
        env_mean = float(np.mean(env))
        env_std = float(np.std(env) + 1e-6)
        k = float(kurtosis(vib_bp))
        s = float(skew(vib_bp))

        # 5) Simple health index:
        #    lower envelope mean + lower RMS → healthier
        #    we compress into [0, 1]-ish via 1 / (1 + value)
        raw_metric = env_mean + rms
        health_index = 1.0 / (1.0 + raw_metric)

        features = {
            "rms": rms,
            "env_mean": env_mean,
            "env_std": env_std,
            "kurtosis": k,
            "skewness": s,
            "temperature": float(temp),
            "fft_mag_sample": fft_mag[:16].tolist(),  # small sample of spectrum
        }

        self.log(
            f"Computed health_index={health_index:.4f} | "
            f"RMS={rms:.4f} | env_mean={env_mean:.4f}",
            level="debug",
        )

        return {
            "health_index": float(health_index),
            "features": features,
        }
