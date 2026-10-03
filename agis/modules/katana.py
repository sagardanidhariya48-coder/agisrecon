
"""
AgisRecon - Katana Module

Wrapper for ProjectDiscovery Katana.

Katana is used for web crawling and endpoint discovery.
"""

import shutil
import subprocess
from typing import Any, List, Optional

from .base import BaseModule


class KatanaModule(BaseModule):
    """
    AgisRecon wrapper for the Katana tool.
    """

    name: str = "katana"
    description: str = "Web crawling and endpoint discovery using Katana"
    command: str = "katana"

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the Katana module.

        Args:
            config: Optional module configuration.
        """
        super().__init__(config)

    def is_available(self) -> bool:
        """
        Check whether Katana is installed and available in PATH.

        Returns:
            True if Katana is available, otherwise False.
        """
        return shutil.which(self.command) is not None

    def run(self, target: str, **kwargs: Any) -> List[str]:
        """
        Crawl the supplied target using Katana.

        Args:
            target: Authorized URL or web target to crawl.
            **kwargs: Optional Katana arguments.

        Returns:
            A list of discovered URLs and endpoints.

        Raises:
            ValueError: If the target is invalid.
            RuntimeError: If Katana is unavailable or execution fails.
        """
        if not self.validate_target(target):
            raise ValueError("Invalid target provided.")

        if not self.is_available():
            raise RuntimeError(
                "Katana is not installed or not available in PATH."
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
                    f"Katana execution failed: {error}"
                )

            raise RuntimeError(
                f"Katana exited with code {process.returncode}."
            )

        for line in process.stdout.splitlines():
            result = line.strip()

            if result:
                self.add_result(result)

        return self.get_results()

