
"""
AgisRecon - Nuclei Module

Wrapper for ProjectDiscovery Nuclei.

Nuclei is used for authorized vulnerability and security
template scanning.
"""

import shutil
import subprocess
from typing import Any, List, Optional

from .base import BaseModule


class NucleiModule(BaseModule):
    """
    AgisRecon wrapper for the Nuclei tool.
    """

    name: str = "nuclei"
    description: str = "Template-based security scanning using Nuclei"
    command: str = "nuclei"

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the Nuclei module.

        Args:
            config: Optional module configuration.
        """
        super().__init__(config)

    def is_available(self) -> bool:
        """
        Check whether Nuclei is installed and available in PATH.

        Returns:
            True if Nuclei is available, otherwise False.
        """
        return shutil.which(self.command) is not None

    def run(self, target: str, **kwargs: Any) -> List[str]:
        """
        Run Nuclei against the supplied target.

        Args:
            target: Authorized URL or web target to scan.
            **kwargs: Optional Nuclei arguments.

        Returns:
            A list of Nuclei findings.

        Raises:
            ValueError: If the target is invalid.
            RuntimeError: If Nuclei is unavailable or execution fails.
        """
        if not self.validate_target(target):
            raise ValueError("Invalid target provided.")

        if not self.is_available():
            raise RuntimeError(
                "Nuclei is not installed or not available in PATH."
            )

        self.clear_results()

        command = [
            self.command,
            "-u",
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
                    f"Nuclei execution failed: {error}"
                )

            raise RuntimeError(
                f"Nuclei exited with code {process.returncode}."
            )

        for line in process.stdout.splitlines():
            result = line.strip()

            if result:
                self.add_result(result)

        return self.get_results()

