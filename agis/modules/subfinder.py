
"""
AgisRecon - Subfinder Module

Wrapper for ProjectDiscovery Subfinder.

Subfinder is used for passive subdomain enumeration.
"""

import shutil
import subprocess
from typing import Any, List, Optional

from .base import BaseModule


class SubfinderModule(BaseModule):
    """
    AgisRecon wrapper for the Subfinder tool.
    """

    name: str = "subfinder"
    description: str = "Passive subdomain enumeration using Subfinder"
    command: str = "subfinder"

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the Subfinder module.

        Args:
            config: Optional module configuration.
        """
        super().__init__(config)

    def is_available(self) -> bool:
        """
        Check whether the Subfinder executable is available.

        Returns:
            True if Subfinder is installed and available in PATH.
        """
        return shutil.which(self.command) is not None

    def run(self, target: str, **kwargs: Any) -> List[str]:
        """
        Run Subfinder against the supplied target.

        Args:
            target: Domain to enumerate.
            **kwargs: Optional Subfinder arguments.

        Returns:
            A list of discovered subdomains.

        Raises:
            ValueError: If the target is invalid.
            RuntimeError: If Subfinder is not installed or execution fails.
        """
        if not self.validate_target(target):
            raise ValueError("Invalid target provided.")

        if not self.is_available():
            raise RuntimeError(
                "Subfinder is not installed or not available in PATH."
            )

        self.clear_results()

        command = [
            self.command,
            "-d",
            target.strip(),
            "-silent",
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
                    f"Subfinder execution failed: {error}"
                )

            raise RuntimeError(
                f"Subfinder exited with code {process.returncode}."
            )

        for line in process.stdout.splitlines():
            result = line.strip()

            if result:
                self.add_result(result)

        return self.get_results()

