# AI-Agent-for-Industrial-Equipment-Health-Monitoring

End-to-end intelligent maintenance with multi-agent monitoring, FFT-based signal analysis, anomaly detection, and Remaining Useful Life (RUL) estimation.

---

## Overview

This project presents an **AI-driven predictive maintenance system** for industrial equipment health monitoring. It uses simulated vibration, temperature, and acoustic sensor data to:

1. Acquire and process sensor signals in near real time
2. Extract spectral and statistical features
3. Detect abnormal operating behavior
4. Estimate Remaining Useful Life (RUL)
5. Trigger maintenance actions through an MCP-style interface

This repository is designed as a **capstone-style demonstration** of agent engineering concepts, including multi-agent orchestration, tool use, memory/state tracking, observability, and practical industrial monitoring workflows.

---

## Key Features

### Multi-Agent Architecture
Five specialized agents operate sequentially for each machine and in parallel across multiple machines:

- **Data Acquisition Agent** – Simulates real-time sensor streams such as vibration, temperature, and acoustic data
- **Signal Processing Agent** – Performs FFT, bandpass filtering, envelope detection, and feature extraction
- **Anomaly Detection Agent** – Computes anomaly scores using z-scores and trend-based health indicators
- **Prediction Agent** – Estimates RUL using a degradation-based model
- **Alert & Action Agent** – Generates maintenance tickets through an MCP-style maintenance interface

### Custom Signal Processing Tools
The project includes a signal-processing toolkit built with NumPy and SciPy, supporting:

- Bandpass filtering
- Hilbert envelope detection
- FFT spectral analysis
- RMS, kurtosis, and skewness extraction
- Temperature and acoustic indicators

### Memory Bank for Degradation Tracking
Each machine maintains a historical memory of:

- Health index values
- Anomaly scores
- RUL predictions
- Timestamped sensor windows

This enables trend-based diagnostics and forecasting over time.

### Parallel Monitoring
The system uses `ThreadPoolExecutor` to simulate **parallel monitoring of multiple machines**, reflecting a realistic industrial IoT deployment pattern.

---

## MCP-Style Maintenance Actions

The **Alert & Action Agent** communicates with a CMMS-like interface using a structured MCP-style tool call:

```json
{
  "type": "mcp",
  "server_label": "maintenance_cmms",
  "tool": "create_maintenance_ticket"
}
```

This represents how an autonomous agent could create a maintenance ticket in a CMMS or EAM system.

---

## Observability

Logging is implemented using `loguru`, enabling:

- Detailed agent execution logs
- Health index and RUL trend tracking
- Maintenance actions and trigger records

The logging layer can be extended to support OpenTelemetry traces and spans for more advanced observability.

---

## Repository Structure

```text
industrial-equipment-health-agent/
├── main.py
├── agents/
│   ├── base_agent.py
│   ├── data_acquisition_agent.py
│   ├── signal_processing_agent.py
│   ├── anomaly_detection_agent.py
│   ├── prediction_agent.py
│   └── alert_action_agent.py
├── tools/
│   ├── signal_tools.py
│   └── mcp_maintenance.py
├── memory/
│   └── memory_bank.py
├── config.py
├── README.md
└── requirements.txt
```

> The structure may vary slightly depending on how the codebase is organized.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/industrial-equipment-health-agent.git
cd industrial-equipment-health-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the System

Run the monitoring pipeline with:

```bash
python main.py
```

This will:

- Simulate sensor data for multiple machines
- Process signals
- Detect anomalies
- Predict RUL
- Trigger maintenance tickets
- Log system activity to `health_monitor.log`

---

## Dataset Used in This Project

This project uses a **fully synthetic dataset generated at runtime**.

The simulation includes:

- Vibration signals with sinusoidal, noisy, and harmonic components
- Acoustic signals derived from vibration patterns
- Temperature readings with drift and noise

Although the current implementation uses synthetic data, the architecture is designed to be adaptable to real-time industrial sensor streams.

---

## Example Output

```text
[DataAcquisitionAgent] Fetching sensor window for EQP-002
[SignalProcessingAgent] Running bandpass + envelope + FFT
[AnomalyDetectionAgent] Health index=0.1523, anomaly score=2.45
[PredictionAgent] Estimated RUL=78.4 time units
[AlertActionAgent] No alert triggered.
```

If an anomaly becomes severe:

```text
[AlertActionAgent] Triggering maintenance ticket via MCP.
[MCP] Creating maintenance ticket: EQP-002, anomaly=4.23, RUL=45.0
Ticket created: TCK-EQP-002-1731718472
```

---

## Project Goals

This project demonstrates several core concepts from an Agent Engineering workflow or capstone:

- **Multi-Agent System** – Sequential and parallel agent orchestration
- **Tools** – Custom signal-processing tools and an MCP-style maintenance tool
- **Memory & State** – Long-term memory for health and RUL tracking

Additional concepts that can be highlighted include:

- Context engineering through compact feature passing
- Observability through structured logs
- Evaluation through fault simulation and anomaly progression
- Runnable deployment as a pipeline script

---

## Evaluation Approach

A simple way to evaluate the system is to:

1. Simulate a degrading machine, such as `EQP-002`
2. Track how the anomaly score increases over time
3. Observe the RUL estimate decrease as degradation progresses
4. Compare behavior against a normally operating machine

Possible extensions include:

- Plotting anomaly score versus cycles
- Measuring detection accuracy
- Evaluating false positives and false negatives
- Replacing the synthetic RUL model with a learned model

---

## Future Improvements

Potential next steps for the repository include:

- Integrating real sensor streams or recorded industrial datasets
- Replacing heuristic anomaly detection with ML-based methods
- Using a learned RUL prediction model
- Adding dashboards for visualization and monitoring
- Expanding the MCP layer to connect with real maintenance systems

