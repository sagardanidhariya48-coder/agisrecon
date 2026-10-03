"""
config/constants.py

Project-wide constants used throughout the Recon Framework.

Purpose:
    - Store values that should never change during runtime.
    - Prevent hardcoded strings throughout the project.
    - Keep modules consistent and easy to maintain.
"""

# ==============================================================================
# Project Information
# ==============================================================================

PROJECT_NAME = "Recon Framework"
PROJECT_VERSION = "1.0.0"
AUTHOR = "Sagar Danidhariya"

# ==============================================================================
# Exit Codes
# ==============================================================================

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_INVALID_INPUT = 2
EXIT_TOOL_NOT_FOUND = 3

# ==============================================================================
# Scan Status
# ==============================================================================

STATUS_PENDING = "PENDING"
STATUS_RUNNING = "RUNNING"
STATUS_COMPLETED = "COMPLETED"
STATUS_FAILED = "FAILED"
STATUS_SKIPPED = "SKIPPED"

# ==============================================================================
# Supported Protocols
# ==============================================================================

HTTP = "http"
HTTPS = "https"

SUPPORTED_PROTOCOLS = (
    HTTP,
    HTTPS,
)

# ==============================================================================
# Output Formats
# ==============================================================================

FORMAT_TXT = "txt"
FORMAT_JSON = "json"
FORMAT_CSV = "csv"

SUPPORTED_OUTPUT_FORMATS = (
    FORMAT_TXT,
    FORMAT_JSON,
    FORMAT_CSV,
)

# ==============================================================================
# File Extensions
# ==============================================================================

TXT_EXTENSION = ".txt"
JSON_EXTENSION = ".json"
CSV_EXTENSION = ".csv"
LOG_EXTENSION = ".log"

# ==============================================================================
# Directory Names
# ==============================================================================

OUTPUT_FOLDER = "output"
LOG_FOLDER = "logs"
TEMP_FOLDER = "temp"

# ==============================================================================
# Log Levels
# ==============================================================================

LOG_DEBUG = "DEBUG"
LOG_INFO = "INFO"
LOG_WARNING = "WARNING"
LOG_ERROR = "ERROR"
LOG_CRITICAL = "CRITICAL"

# ==============================================================================
# Default Encoding
# ==============================================================================

DEFAULT_ENCODING = "utf-8"

# ==============================================================================
# ANSI Terminal Colors
# ==============================================================================

RESET = "\033[0m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BOLD = "\033[1m"

# ==============================================================================
# Banner
# ==============================================================================

BANNER = rf"""
{CYAN}
========================================================
              Recon Framework v{PROJECT_VERSION}
========================================================
{RESET}
"""

# ==============================================================================
# Module Names
# ==============================================================================

MODULE_SUBDOMAIN = "Subdomain Enumeration"
MODULE_DNS = "DNS Enumeration"
MODULE_HTTP = "HTTP Probing"
MODULE_PORT = "Port Scanning"
MODULE_CRAWLER = "Web Crawling"
MODULE_SCREENSHOT = "Screenshot Capture"
MODULE_TECH = "Technology Detection"

# ==============================================================================
# Exported Objects
# ==============================================================================

__all__ = [
    "PROJECT_NAME",
    "PROJECT_VERSION",
    "AUTHOR",
    "EXIT_SUCCESS",
    "EXIT_FAILURE",
    "EXIT_INVALID_INPUT",
    "EXIT_TOOL_NOT_FOUND",
    "STATUS_PENDING",
    "STATUS_RUNNING",
    "STATUS_COMPLETED",
    "STATUS_FAILED",
    "STATUS_SKIPPED",
    "HTTP",
    "HTTPS",
    "SUPPORTED_PROTOCOLS",
    "FORMAT_TXT",
    "FORMAT_JSON",
    "FORMAT_CSV",
    "SUPPORTED_OUTPUT_FORMATS",
    "TXT_EXTENSION",
    "JSON_EXTENSION",
    "CSV_EXTENSION",
    "LOG_EXTENSION",
    "OUTPUT_FOLDER",
    "LOG_FOLDER",
    "TEMP_FOLDER",
    "LOG_DEBUG",
    "LOG_INFO",
    "LOG_WARNING",
    "LOG_ERROR",
    "LOG_CRITICAL",
    "DEFAULT_ENCODING",
    "RESET",
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "WHITE",
    "BOLD",
    "BANNER",
    "MODULE_SUBDOMAIN",
    "MODULE_DNS",
    "MODULE_HTTP",
    "MODULE_PORT",
    "MODULE_CRAWLER",
    "MODULE_SCREENSHOT",
    "MODULE_TECH",
]