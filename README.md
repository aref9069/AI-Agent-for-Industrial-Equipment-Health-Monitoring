# AI-Agent-for-Industrial-Equipment-Health-Monitoring
End-to-End Intelligent Maintenance: Multi-Agent Monitoring with FFT Analysis, Anomaly Detection, and RUL Estimation.

---

## 🚀 Overview

This project implements an **AI-driven predictive maintenance multi-agent system** designed for industrial equipment health monitoring.  
Using vibration, temperature, and acoustic sensor data, the system:

1. Acquires and processes real-time sensor signals  
2. Extracts spectral and statistical features  
3. Detects anomalies  
4. Estimates Remaining Useful Life (RUL)  
5. Generates maintenance actions via an MCP-style interface  

The repository serves as a **capstone demonstration**, integrating multi-agent orchestration, custom toolchains, memory management, observability, and realistic industrial health-monitoring workflows.

---

## 🧠 Key Features

### ✔ Multi-Agent Architecture
Five coordinated agents operate sequentially per machine and in parallel across machines:

- **Data Acquisition Agent** – Simulates real-time sensor streams (vibration, temperature, acoustic).  
- **Signal Processing Agent** – Performs FFT, bandpass filtering, envelope detection, and feature extraction.  
- **Anomaly Detection Agent** – Computes anomaly scores using z-scores and trend-based health indices.  
- **Prediction Agent** – Estimates RUL using a simple degradation model.  
- **Alert & Action Agent** – Creates maintenance tickets via an MCP-style maintenance interface.

---

### ✔ Custom Signal Processing Tools
Signal-processing toolkit built using NumPy/SciPy, including:

- Bandpass filtering  
- Hilbert envelope detection  
- FFT spectral analysis  
- RMS, kurtosis, skewness  
- Temperature & acoustic indicators  

---

### ✔ Memory Bank for Degradation Tracking
Each machine stores historical:

- Health index values  
- Anomaly scores  
- RUL predictions  
- Timestamped sensor windows  

Enabling trend-based diagnostics and forecasting.

---

### ✔ Parallel Monitoring
The system uses `ThreadPoolExecutor` to simulate **real-time parallel monitoring of multiple machines**, similar to industrial IoT deployments.

---

### ✔ MCP-Style Maintenance Actions
The Alert & Action Agent communicates with a CMMS-like interface using a structured MCP-style call:

```json
{
  "type": "mcp",
  "server_label": "maintenance_cmms",
  "tool": "create_maintenance_ticket"
}


This represents how an agent would open tickets in a CMMS/EAM system.

✔ Observability

Logging is implemented through loguru, producing:

Detailed agent execution logs

Health index and RUL trends

Maintenance actions and triggers

These logs can be extended to support OpenTelemetry spans/traces.

📁 Repository Structure
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


(Structure may vary depending on how you split the provided code.)

🔧 Installation
1. Clone the repository
git clone https://github.com/<your-username>/industrial-equipment-health-agent.git
cd industrial-equipment-health-agent

2. Install dependencies
pip install -r requirements.txt

▶️ Running the System

Run the monitoring pipeline:

python main.py


This will:

Simulate sensor data for multiple machines

Process signals

Detect anomalies

Predict RUL

Trigger maintenance tickets

Log everything to health_monitor.log

## ✅ Dataset Used in This Project
⭐ The dataset is synthetic and fully generated at runtime

The project simulates:

Vibration signals (sinusoidal + noise + harmonic components)

Acoustic signals (slightly modified copy of vibration)

Temperature readings (random drift + noise)

However,it is designed to work with real-time sensor streams that industrial equipment typically generates.

## 🧪 Output Example (Console)

[DataAcquisitionAgent] Fetching sensor window for EQP-002
[SignalProcessingAgent] Running bandpass + envelope + FFT
[AnomalyDetectionAgent] Health index=0.1523, anomaly score=2.45
[PredictionAgent] Estimated RUL=78.4 time units
[AlertActionAgent] No alert triggered.


If an anomaly is severe:

[AlertActionAgent] Triggering maintenance ticket via MCP.
[MCP] Creating maintenance ticket: EQP-002, anomaly=4.23, RUL=45.0
Ticket created: TCK-EQP-002-1731718472

📝 Project Goals (Capstone Alignment)

This project demonstrates at least 3 required concepts from the Agent Engineering course:

✔ Multi-Agent System

Sequential & parallel agent orchestration.

✔ Tools

Custom signal processing tools + MCP maintenance tool.

✔ Memory & State

Long-term MemoryBank for health & RUL trends.

Additional optional features:

Context engineering (compact feature passing)

Observability (logs)

Evaluation (fault simulation & anomaly curves)

Agent “deployment” via a runnable pipeline script

📈 Evaluation Approach (Suggested)

To validate performance:

Simulate a degrading machine (EQP-002 in current code).

Track how anomaly score increases over time.

Observe RUL decreasing with trend model.

Compare with normal machine behavior.

You may extend this repository with:

plots of anomaly score vs cycles

detection accuracy metrics

false positive/false negative analysis
