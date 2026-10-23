"""
AgisRecon2 - Utility Package
============================

This package contains reusable utility modules shared across the
entire AgisRecon2 project.

Modules
-------
runner         : Execute external commands safely.
parser         : Parse raw tool output.
logger         : Centralized logging.
validator      : Input validation utilities.
file_manager   : File and directory operations.
banner         : CLI banner display.
colors         : ANSI terminal colors.
helpers        : General helper functions.

Example
-------
from utils import get_logger, validate_domain

logger = get_logger()
"""

from .logger import get_logger
from .validator import (
    validate_domain,
    validate_ip,
    validate_url,
)
from .runner import run_command
from .file_manager import (
    ensure_directory,
    read_json,
    write_json,
)
from .banner import print_banner

__all__ = [
    "get_logger",
    "validate_domain",
    "validate_ip",
    "validate_url",
    "run_command",
    "ensure_directory",
    "read_json",
    "write_json",
    "print_banner",
]

__version__ = "1.0.0"