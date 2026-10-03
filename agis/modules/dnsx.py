
"""
AgisRecon - DNSX Module

Wrapper for ProjectDiscovery DNSX.

DNSX is used for DNS probing, resolution, and DNS record
information gathering.
"""

import shutil
import subprocess
from typing import Any, List, Optional

from .base import BaseModule


class DNSXModule(BaseModule):
    """
    AgisRecon wrapper for the DNSX tool.
    """

    name: str = "dnsx"
    description: str = "DNS resolution and DNS probing using DNSX"
    command: str = "dnsx"

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the DNSX module.

        Args:
            config: Optional module configuration.
        """
        super().__init__(config)

    def is_available(self) -> bool:
        """
        Check whether DNSX is installed and available in PATH.

        Returns:
            True if DNSX is available, otherwise False.
        """
        return shutil.which(self.command) is not None

    def run(self, target: str, **kwargs: Any) -> List[str]:
        """
        Run DNSX against the supplied target.

        Args:
            target: Domain or hostname to resolve.
            **kwargs: Optional DNSX arguments.

        Returns:
            A list of DNSX results.

        Raises:
            ValueError: If the target is invalid.
            RuntimeError: If DNSX is unavailable or execution fails.
        """
        if not self.validate_target(target):
            raise ValueError("Invalid target provided.")

        if not self.is_available():
            raise RuntimeError(
                "DNSX is not installed or not available in PATH."
            )

        self.clear_results()

        command = [
            self.command,
            "-silent",
        ]

        try:
            process = subprocess.run(
                command,
                input=f"{target.strip()}\n",
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
                    f"DNSX execution failed: {error}"
                )

            raise RuntimeError(
                f"DNSX exited with code {process.returncode}."
            )

        for line in process.stdout.splitlines():
            result = line.strip()

            if result:
                self.add_result(result)

        return self.get_results()

