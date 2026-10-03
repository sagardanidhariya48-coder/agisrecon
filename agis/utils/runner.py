"""
AgisRecon2 - Command Runner

This module provides a centralized way to execute external commands
used by reconnaissance tools such as:

- Subfinder
- Assetfinder
- HTTPX
- Naabu
- Nmap
- DNSX
- Katana

Every external tool should be executed through this module instead
of calling subprocess directly.
"""

from __future__ import annotations

import subprocess
import time
from typing import Dict, List, Optional


def run_command(
    command: List[str],
    timeout: int = 300,
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
) -> Dict[str, object]:
    """
    Execute an external command safely.

    Args:
        command: Command and arguments as a list.
        timeout: Maximum execution time in seconds.
        cwd: Working directory.
        env: Environment variables.

    Returns:
        Dictionary containing execution results.
    """

    start_time = time.perf_counter()

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env=env,
            check=False,
        )

        execution_time = round(time.perf_counter() - start_time, 3)

        return {
            "success": process.returncode == 0,
            "command": " ".join(command),
            "returncode": process.returncode,
            "stdout": process.stdout.strip(),
            "stderr": process.stderr.strip(),
            "execution_time": execution_time,
        }

    except subprocess.TimeoutExpired as exc:
        execution_time = round(time.perf_counter() - start_time, 3)

        return {
            "success": False,
            "command": " ".join(command),
            "returncode": None,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds.",
            "execution_time": execution_time,
        }

    except FileNotFoundError:
        execution_time = round(time.perf_counter() - start_time, 3)

        return {
            "success": False,
            "command": " ".join(command),
            "returncode": None,
            "stdout": "",
            "stderr": f"Command not found: {command[0]}",
            "execution_time": execution_time,
        }

    except Exception as exc:
        execution_time = round(time.perf_counter() - start_time, 3)

        return {
            "success": False,
            "command": " ".join(command),
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
            "execution_time": execution_time,
        }


if __name__ == "__main__":
    result = run_command(["echo", "AgisRecon2 Runner Test"])

    print("Success :", result["success"])
    print("Command :", result["command"])
    print("Code    :", result["returncode"])
    print("Output  :", result["stdout"])
    print("Error   :", result["stderr"])
    print("Time    :", result["execution_time"], "seconds")