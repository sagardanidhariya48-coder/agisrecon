"""
config/tools.py

Central configuration for all external tools used by the Recon Framework.

Purpose:
    - Store the executable name or absolute path of every external tool.
    - Keep tool configuration in one place.
    - Avoid hardcoding tool names throughout the project.
    - Make updating tool paths easy.

Example:
    from config.tools import SUBFINDER

    subprocess.run([SUBFINDER, "-d", domain])

If a tool is installed in a custom location, simply replace the executable
name with its full path.

Example:
    SUBFINDER = "/usr/local/bin/subfinder"
"""

from pathlib import Path

# ==============================================================================
# Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ==============================================================================
# External Tool Executables
# ==============================================================================

# -----------------------------
# Subdomain Enumeration
# -----------------------------

SUBFINDER = "subfinder"
ASSETFINDER = "assetfinder"

# -----------------------------
# DNS Enumeration
# -----------------------------

DNSX = "dnsx"

# -----------------------------
# HTTP Probing
# -----------------------------

HTTPX = "httpx"

# -----------------------------
# Port Scanning
# -----------------------------

NMAP = "nmap"

# -----------------------------
# Directory & Content Discovery
# -----------------------------

FEROXBUSTER = "feroxbuster"

# -----------------------------
# Crawling
# -----------------------------

KATANA = "katana"

# -----------------------------
# Screenshot Capture
# -----------------------------

AQUATONE = "aquatone"

# -----------------------------
# Technology Detection
# -----------------------------

WHATWEB = "whatweb"

# -----------------------------
# Network Utilities
# -----------------------------

PING = "ping"
TRACEROUTE = "traceroute"

# ==============================================================================
# Tool Registry
# ==============================================================================

TOOLS = {
    "subfinder": SUBFINDER,
    "assetfinder": ASSETFINDER,
    "dnsx": DNSX,
    "httpx": HTTPX,
    "nmap": NMAP,
    "feroxbuster": FEROXBUSTER,
    "katana": KATANA,
    "aquatone": AQUATONE,
    "whatweb": WHATWEB,
    "ping": PING,
    "traceroute": TRACEROUTE,
}

# ==============================================================================
# Helper Functions
# ==============================================================================

def get_tool(tool_name: str) -> str:
    """
    Return the executable name or path for a tool.

    Args:
        tool_name (str): Tool identifier.

    Returns:
        str: Executable name or absolute path.

    Raises:
        KeyError: If the tool is not registered.
    """
    try:
        return TOOLS[tool_name.lower()]
    except KeyError as exc:
        raise KeyError(f"Unknown tool: {tool_name}") from exc


def list_tools() -> list[str]:
    """
    Return a sorted list of registered tool names.
    """
    return sorted(TOOLS.keys())


# ==============================================================================
# Module Exports
# ==============================================================================

__all__ = [
    "PROJECT_ROOT",
    "SUBFINDER",
    "ASSETFINDER",
    "DNSX",
    "HTTPX",
    "NMAP",
    "FEROXBUSTER",
    "KATANA",
    "AQUATONE",
    "WHATWEB",
    "PING",
    "TRACEROUTE",
    "TOOLS",
    "get_tool",
    "list_tools",
]