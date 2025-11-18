"""
main.py

Entry point for the AI-Agent Industrial Equipment Health Monitoring System.

This script:
- Initializes the global MemoryBank
- Spawns a monitoring pipeline per machine
- Orchestrates the following agents in sequence:
    1) DataAcquisitionAgent
    2) SignalProcessingAgent
    3) AnomalyDetectionAgent
    4) PredictionAgent
    5) AlertActionAgent

Each machine is handled in its own thread using ThreadPoolExecutor.

Assumed agent interfaces (you should implement these in agents/):

    DataAcquisitionAgent(machine_id, logger, sample_rate, window_size)
        -> acquire_window() -> {
               "vibration": np.ndarray,
               "temperature": float,
               "acoustic": np.ndarray,
               "timestamp": float
           }

    SignalProcessingAgent(machine_id, logger)
        -> process(window_dict) -> {
               "health_index": float,
               "features": dict   # FFT bands, RMS, kurtosis, etc.
           }

    AnomalyDetectionAgent(machine_id, logger)
        -> detect(health_index: float, history: dict) -> {
               "anomaly_score": float
           }

    PredictionAgent(machine_id, logger)
        -> predict_rul(history: dict) -> float

    AlertActionAgent(machine_id, logger)
        -> handle(health: float, anomaly_score: float, rul: float) -> None
           (internally may call tools.mcp_maintenance.create_maintenance_ticket)

You can adapt these names / signatures as needed, as long as the main pipeline logic
remains consistent.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger

from config import (
    MACHINES,
    SAMPLE_RATE,
    WINDOW_SIZE,
    LOG_FILE,
    LOG_LEVEL,
)
from memory.memory_bank import MemoryBank

from agents.data_acquisition_agent import DataAcquisitionAgent
from agents.signal_processing_agent import SignalProcessingAgent
from agents.anomaly_detection_agent import AnomalyDetectionAgent
from agents.prediction_agent import PredictionAgent
from agents.alert_action_agent import AlertActionAgent


# ----------------------------------------------------------------------
# Monitoring Pipeline for a Single Machine
# ----------------------------------------------------------------------
def monitor_machine(
    machine_id: str,
    memory_bank: MemoryBank,
    cycles: int = 200,
    sleep_between_cycles: float = 0.1,
):
    """
    Runs the full monitoring pipeline for a single machine.

    Parameters
    ----------
    machine_id : str
        ID of the machine (e.g., "EQP-001").
    memory_bank : MemoryBank
        Shared MemoryBank instance for all machines.
    cycles : int
        Number of sensor windows to process for this demo run.
    sleep_between_cycles : float
        Sleep (seconds) between cycles to simulate real time.
    """
    logger.info(f"[{machine_id}] Starting monitoring pipeline for {cycles} cycles.")

    # Initialize agents for this machine
    da_agent = DataAcquisitionAgent(
        machine_id=machine_id,
        logger=logger,
        sample_rate=SAMPLE_RATE,
        window_size=WINDOW_SIZE,
    )
    sp_agent = SignalProcessingAgent(machine_id=machine_id, logger=logger)
    ad_agent = AnomalyDetectionAgent(machine_id=machine_id, logger=logger)
    pr_agent = PredictionAgent(machine_id=machine_id, logger=logger)
    aa_agent = AlertActionAgent(machine_id=machine_id, logger=logger)

    for cycle in range(cycles):
        try:
            # 1) Acquire sensor window
            window = da_agent.acquire_window()

            # 2) Signal processing -> health index + features
            sp_result = sp_agent.process(window)
            health_index = sp_result.get("health_index", 0.0)
            features = sp_result.get("features", {})

            # 3) Get history so far from memory
            history = memory_bank.get_history(machine_id)

            # 4) Anomaly detection
            anomaly_result = ad_agent.detect(health_index, history)
            anomaly_score = anomaly_result.get("anomaly_score", 0.0)

            # 5) RUL prediction
            rul = pr_agent.predict_rul(history)

            # 6) Store everything in memory
            memory_bank.store(
                machine_id=machine_id,
                health=health_index,
                anomaly=anomaly_score,
                rul=rul,
                timestamp=window.get("timestamp", time.time()),
                features=features,
            )

            # 7) Alert / Maintenance action
            aa_agent.handle(
                health=health_index,
                anomaly_score=anomaly_score,
                rul=rul,
            )

            logger.debug(
                f"[{machine_id}] Cycle={cycle} | "
                f"Health={health_index:.4f} | "
                f"Anomaly={anomaly_score:.4f} | "
                f"RUL={rul:.2f}"
            )

            time.sleep(sleep_between_cycles)

        except Exception as e:
            logger.exception(f"[{machine_id}] Error in monitoring loop: {e}")
            # Depending on your needs, you may break or continue.
            # Here we continue to keep the demo running.
            continue

    logger.info(f"[{machine_id}] Monitoring pipeline completed.")


# ----------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------
def main():
    """
    Sets up logging, initializes MemoryBank, and starts monitoring
    for all configured machines in parallel.
    """
    # Configure loguru
    logger.remove()  # remove default handler
    logger.add(
        LOG_FILE,
        level=LOG_LEVEL,
        rotation="5 MB",
        retention="10 days",
        backtrace=True,
        diagnose=True,
    )
    logger.add(
        lambda msg: print(msg, end=""),  # mirror to stdout
        level=LOG_LEVEL,
    )

    logger.info("Starting Industrial Equipment Health Monitor Agent System.")
    logger.info(f"Machines configured: {MACHINES}")

    # Shared memory bank across all agents/machines
    memory_bank = MemoryBank(max_history=500)

    # Run one pipeline per machine in parallel
    with ThreadPoolExecutor(max_workers=len(MACHINES)) as executor:
        futures = {
            executor.submit(monitor_machine, machine_id, memory_bank): machine_id
            for machine_id in MACHINES
        }

        for future in as_completed(futures):
            machine_id = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.exception(
                    f"[{machine_id}] Unhandled exception from monitoring task: {e}"
                )

    logger.info("All machine monitoring pipelines have finished. Shutting down.")


if __name__ == "__main__":
    main()
