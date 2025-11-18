# agents/base_agent.py

from loguru import logger as default_logger


class BaseAgent:
    """
    Base class for all agents.

    Provides:
    - name
    - machine_id
    - logger
    - simple logging helper with standardized prefix
    """

    def __init__(self, name: str, machine_id: str, logger=None):
        self.name = name
        self.machine_id = machine_id
        self.logger = logger or default_logger

    def log(self, message: str, level: str = "info"):
        prefix = f"[{self.machine_id}][{self.name}] "
        if level.lower() == "debug":
            self.logger.debug(prefix + message)
        elif level.lower() == "warning":
            self.logger.warning(prefix + message)
        elif level.lower() == "error":
            self.logger.error(prefix + message)
        else:
            self.logger.info(prefix + message)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, machine_id={self.machine_id})"
