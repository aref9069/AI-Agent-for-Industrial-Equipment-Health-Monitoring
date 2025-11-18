"""
Global Configuration File for Industrial Equipment Health Monitoring Agent System
-------------------------------------------------------------------------------

This file defines system-wide constants for:
- Sensor simulation parameters
- FFT and filtering settings
- Machine registry
- Anomaly detection thresholds
- RUL estimation model parameters
- Logging options

All agents import values from this file for consistent behavior.
"""

from typing import List


# --------------------------------------------------------------
# MACHINE CONFIGURATION
# --------------------------------------------------------------

# List of machines to simulate/monitor
MACHINES: List[str] = [
    "EQP-001",
    "EQP-002",
    "EQP-003",
]


# --------------------------------------------------------------
# SAMPLING / SENSOR SETTINGS
# --------------------------------------------------------------

# Sampling frequency for vibration sensors (Hz)
SAMPLE_RATE = 2000  

# Number of samples per acquisition window
WINDOW_SIZE = 512    

# Temperature drift simulation (optional)
TEMP_BASELINE = 55.0  
TEMP_VARIATION = 4.0  


# --------------------------------------------------------------
# SIGNAL PROCESSING SETTINGS
# --------------------------------------------------------------

# Bandpass filter range (Hz)
BANDPASS_LOW = 10
BANDPASS_HIGH = 800

# FFT settings
NFFT = 512


# --------------------------------------------------------------
# ANOMALY DETECTION PARAMETERS
# --------------------------------------------------------------

# Z-score threshold for triggering anomaly condition
ANOMALY_Z_THRESHOLD = 3.0

# Health index normalization factor
HEALTH_SCALE = 1.0


# --------------------------------------------------------------
# RUL ESTIMATION PARAMETERS
# --------------------------------------------------------------

# Simple linear degradation model (example)
# Higher = healthier; lower = approaching failure
INITIAL_HEALTH = 1.0  
DEGRADATION_RATE = 0.0008  # per cycle or per window

# Minimum RUL before raising a warning
MIN_RUL_WARNING = 50.0  


# --------------------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------------------

LOG_FILE = "health_monitor.log"
LOG_LEVEL = "INFO"   # DEBUG, INFO, WARNING, ERROR


# --------------------------------------------------------------
# MCP CONFIGURATION (Stub)
# --------------------------------------------------------------

MCP_SERVER_LABEL = "maintenance_cmms"
MCP_TOOL_NAME = "create_maintenance_ticket"


# --------------------------------------------------------------
# RANDOM SEED (optional)
# --------------------------------------------------------------

RANDOM_SEED = 42
