
"""
AgisRecon - Waybackurls Module

Wrapper for Waybackurls.

Waybackurls is used to retrieve URLs previously observed by
the Wayback Machine for a target domain.
"""

import shutil
import subprocess
from typing import Any, List, Optional

from .base import BaseModule


class WaybackURLsModule(BaseModule):
    """
    AgisRecon wrapper for the Waybackurls tool.
    """

    name: str = "waybackurls"
    description: str = "Archived URL discovery using Waybackurls"
    command: str = "waybackurls"

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the Waybackurls module.

        Args:
            config: Optional module configuration.
        """
        super().__init__(config)

    def is_available(self) -> bool:
        """
        Check whether Waybackurls is installed and available in PATH.

        Returns:
            True if Waybackurls is available, otherwise False.
        """
        return shutil.which(self.command) is not None

    def run(self, target: str, **kwargs: Any) -> List[str]:
        """
        Retrieve archived URLs for the supplied target.

        Args:
            target: Authorized domain to query.
            **kwargs: Optional module-specific arguments.

        Returns:
            A list of archived URLs.

        Raises:
            ValueError: If the target is invalid.
            RuntimeError: If Waybackurls is unavailable or execution fails.
        """
        if not self.validate_target(target):
            raise ValueError("Invalid target provided.")

        if not self.is_available():
            raise RuntimeError(
                "Waybackurls is not installed or not available in PATH."
            )

        self.clear_results()

        command = [
            self.command,
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
                    f"Waybackurls execution failed: {error}"
                )

            raise RuntimeError(
                f"Waybackurls exited with code {process.returncode}."
            )

        for line in process.stdout.splitlines():
            result = line.strip()

            if result:
                self.add_result(result)

        return self.get_results()
