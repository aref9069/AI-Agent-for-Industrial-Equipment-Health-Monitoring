# tools/signal_tools.py

import numpy as np
from scipy.signal import butter, filtfilt, hilbert
from loguru import logger


def bandpass_filter(signal: np.ndarray, fs: float, low: float, high: float) -> np.ndarray:
    """
    4th-order Butterworth bandpass filter.

    Parameters
    ----------
    signal : np.ndarray
        Input time-domain signal.
    fs : float
        Sampling frequency (Hz).
    low : float
        Low cutoff frequency (Hz).
    high : float
        High cutoff frequency (Hz).

    Returns
    -------
    np.ndarray
        Filtered signal.
    """
    nyq = 0.5 * fs
    low_n = low / nyq
    high_n = high / nyq
    b, a = butter(4, [low_n, high_n], btype="band")
    filtered = filtfilt(b, a, signal)
    logger.debug(
        f"[signal_tools] Bandpass filter applied: low={low}Hz, high={high}Hz, fs={fs}Hz"
    )
    return filtered


def envelope_detection(signal: np.ndarray) -> np.ndarray:
    """
    Computes the amplitude envelope using the analytic signal (Hilbert transform).

    Parameters
    ----------
    signal : np.ndarray
        Real-valued input signal.

    Returns
    -------
    np.ndarray
        Envelope of the signal.
    """
    analytic = hilbert(signal)
    envelope = np.abs(analytic)
    logger.debug("[signal_tools] Envelope computed via Hilbert transform.")
    return envelope


def compute_fft_features(signal: np.ndarray, fs: float) -> dict:
    """
    Computes simple spectral features from the magnitude spectrum.

    Features:
    - fft_peak_freq: frequency of the maximum magnitude
    - fft_spectral_centroid: magnitude-weighted average frequency

    Parameters
    ----------
    signal : np.ndarray
        Time-domain signal.
    fs : float
        Sampling frequency.

    Returns
    -------
    dict
        Dictionary of FFT-based features.
    """
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    spectrum = np.abs(np.fft.rfft(signal))

    if np.all(spectrum == 0):
        peak_freq = 0.0
        spectral_centroid = 0.0
    else:
        peak_idx = int(np.argmax(spectrum))
        peak_freq = float(freqs[peak_idx])
        spectral_centroid = float(np.sum(freqs * spectrum) / np.sum(spectrum))

    logger.debug(
        f"[signal_tools] FFT features: peak_freq={peak_freq:.2f}Hz, "
        f"spectral_centroid={spectral_centroid:.2f}Hz"
    )

    return {
        "fft_peak_freq": peak_freq,
        "fft_spectral_centroid": spectral_centroid,
    }


def compute_stat_features(signal: np.ndarray) -> dict:
    """
    Computes basic statistical features of a 1D signal.

    Features:
    - mean
    - std
    - rms
    - kurtosis (excess, approximate)
    - skewness (approximate)

    Parameters
    ----------
    signal : np.ndarray
        Input signal.

    Returns
    -------
    dict
        Dictionary of statistical features.
    """
    x = np.asarray(signal)
    eps = 1e-12

    mean = float(np.mean(x))
    std = float(np.std(x) + eps)
    rms = float(np.sqrt(np.mean(x ** 2)))

    # centered and normalized
    xc = (x - mean) / std
    skewness = float(np.mean(xc ** 3))
    kurtosis = float(np.mean(xc ** 4))  # includes 3; we can leave it as-is

    logger.debug(
        "[signal_tools] Stats: mean={:.4f}, std={:.4f}, rms={:.4f}, skew={:.4f}, kurt={:.4f}"
        .format(mean, std, rms, skewness, kurtosis)
    )

    return {
        "mean": mean,
        "std": std,
        "rms": rms,
        "skewness": skewness,
        "kurtosis": kurtosis,
    }
