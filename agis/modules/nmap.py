
"""
AgisRecon - Nmap Module

Wrapper for Nmap.

Nmap is used for authorized network discovery and service
enumeration.
"""

import shutil
import subprocess
from typing import Any, List, Optional

from .base import BaseModule


class NmapModule(BaseModule):
    """
    AgisRecon wrapper for Nmap.
    """

    name: str = "nmap"
    description: str = "Network and service enumeration using Nmap"
    command: str = "nmap"

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the Nmap module.

        Args:
            config: Optional module configuration.
        """
        super().__init__(config)

    def is_available(self) -> bool:
        """
        Check whether Nmap is installed and available in PATH.

        Returns:
            True if Nmap is available, otherwise False.
        """
        return shutil.which(self.command) is not None

    def run(self, target: str, **kwargs: Any) -> List[str]:
        """
        Run a basic Nmap scan against the supplied target.

        Args:
            target: Authorized hostname or IP address to scan.
            **kwargs: Optional Nmap arguments.

        Returns:
            A list containing the output lines produced by Nmap.

        Raises:
            ValueError: If the target is invalid.
            RuntimeError: If Nmap is unavailable or execution fails.
        """
        if not self.validate_target(target):
            raise ValueError("Invalid target provided.")

        if not self.is_available():
            raise RuntimeError(
                "Nmap is not installed or not available in PATH."
            )

        self.clear_results()

        command = [
            self.command,
            "-sV",
            target.strip(),
        ]

        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as exc:
            raise RuntimeError(
                f"Failed to execute {self.command}: {exc}"
            ) from exc

        if process.returncode != 0:
            error = process.stderr.strip()

            if error:
                raise RuntimeError(
                    f"Nmap execution failed: {error}"
                )

            raise RuntimeError(
                f"Nmap exited with code {process.returncode}."
            )

        for line in process.stdout.splitlines():
            result = line.strip()

            if result:
                self.add_result(result)

        return self.get_results()

