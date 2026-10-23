"""
AgisRecon - Helper Utilities

Contains reusable helper functions shared across the project.

These functions are intentionally generic and do not belong
to any other utility module.
"""

from __future__ import annotations

import hashlib
import platform
import secrets
import shutil
import socket
from datetime import datetime
from typing import Iterable, List


# --------------------------------------------------------------------
# Time
# --------------------------------------------------------------------

def current_timestamp() -> str:
    """
    Return current local timestamp.

    Example:
        2026-09-09 11:30:45
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------------------------
# List Helpers
# --------------------------------------------------------------------

def remove_duplicates(items: Iterable[str]) -> List[str]:
    """
    Remove duplicates while preserving order.
    """

    return list(dict.fromkeys(items))


# --------------------------------------------------------------------
# String Helpers
# --------------------------------------------------------------------

def clean_string(text: str) -> str:
    """
    Remove leading/trailing whitespace.
    """

    return text.strip()


# --------------------------------------------------------------------
# Hashing
# --------------------------------------------------------------------

def sha256_hash(text: str) -> str:
    """
    Return SHA256 hash.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# --------------------------------------------------------------------
# Random
# --------------------------------------------------------------------

def random_token(length: int = 16) -> str:
    """
    Generate secure random hexadecimal token.
    """

    return secrets.token_hex(length)


# --------------------------------------------------------------------
# Networking
# --------------------------------------------------------------------

def hostname() -> str:
    """
    Return local hostname.
    """

    return socket.gethostname()


# --------------------------------------------------------------------
# System
# --------------------------------------------------------------------

def operating_system() -> str:
    """
    Return operating system name.
    """

    return platform.system()


def command_exists(command: str) -> bool:
    """
    Check if a command exists on the system.
    """

    return shutil.which(command) is not None


# --------------------------------------------------------------------
# Self Test
# --------------------------------------------------------------------

if __name__ == "__main__":

    print("Current Time:")
    print(current_timestamp())

    print("\nRemove Duplicates:")
    print(remove_duplicates([
        "google.com",
        "github.com",
        "google.com",
        "openai.com"
    ]))

    print("\nClean String:")
    print(clean_string("   AgisRecon   "))

    print("\nSHA256:")
    print(sha256_hash("AgisRecon"))

    print("\nRandom Token:")
    print(random_token())

    print("\nHostname:")
    print(hostname())

    print("\nOperating System:")
    print(operating_system())

    print("\nPython Exists:")
    print(command_exists("python"))

    print("\nGit Exists:")
    print(command_exists("git"))