"""
AgisRecon2 - Logger Utility

Provides a centralized logging system for the entire project.

Features
--------
- Console logging
- File logging
- Automatic log directory creation
- Configurable log level
- Reusable logger instance

Example
-------
from utils.logger import get_logger

logger = get_logger()

logger.info("Recon started")
logger.warning("Tool not found")
logger.error("Scan failed")
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

# --------------------------------------------------------------------
# Default Configuration
# --------------------------------------------------------------------

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "agisrecon2.log"

LOG_LEVEL = logging.INFO

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_logger: Optional[logging.Logger] = None


# --------------------------------------------------------------------
# Logger Factory
# --------------------------------------------------------------------

def get_logger(name: str = "AgisRecon2") -> logging.Logger:
    """
    Return a configured logger instance.

    Parameters
    ----------
    name : str
        Logger name.

    Returns
    -------
    logging.Logger
    """

    global _logger

    if _logger is not None:
        return _logger

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    _logger = logger

    return logger


# --------------------------------------------------------------------
# Test
# --------------------------------------------------------------------

if __name__ == "__main__":

    logger = get_logger()

    logger.debug("Debug message")
    logger.info("Recon started")
    logger.warning("This is a warning")
    logger.error("Example error")
    logger.critical("Critical issue")