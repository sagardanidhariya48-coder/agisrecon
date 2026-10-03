
"""
AgisRecon - Assetfinder Module

Wrapper for Assetfinder.

Assetfinder is used to discover domains and subdomains associated
with a target domain.
"""

import shutil
import subprocess
from typing import Any, List, Optional

from .base import BaseModule


class AssetfinderModule(BaseModule):
    """
    AgisRecon wrapper for the Assetfinder tool.
    """

    name: str = "assetfinder"
    description: str = "Domain and subdomain discovery using Assetfinder"
    command: str = "assetfinder"

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the Assetfinder module.

        Args:
            config: Optional module configuration.
        """
        super().__init__(config)

    def is_available(self) -> bool:
        """
        Check whether Assetfinder is installed and available in PATH.

        Returns:
            True if Assetfinder is available, otherwise False.
        """
        return shutil.which(self.command) is not None

    def run(self, target: str, **kwargs: Any) -> List[str]:
        """
        Run Assetfinder against the supplied target.

        Args:
            target: Domain to investigate.
            **kwargs: Optional module-specific arguments.

        Returns:
            A list of discovered domains and subdomains.

        Raises:
            ValueError: If the target is invalid.
            RuntimeError: If Assetfinder is unavailable or execution fails.
        """
        if not self.validate_target(target):
            raise ValueError("Invalid target provided.")

        if not self.is_available():
            raise RuntimeError(
                "Assetfinder is not installed or not available in PATH."
            )

        self.clear_results()

        command = [
            self.command,
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
                    f"Assetfinder execution failed: {error}"
                )

            raise RuntimeError(
                f"Assetfinder exited with code {process.returncode}."
            )

        for line in process.stdout.splitlines():
            result = line.strip()

            if result:
                self.add_result(result)

        return self.get_results()

