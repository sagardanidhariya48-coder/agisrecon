
"""
AgisRecon - HTTPX Module

Wrapper for ProjectDiscovery HTTPX.

HTTPX is used to probe HTTP/HTTPS services and collect
basic information about reachable web services.
"""

import shutil
import subprocess
from typing import Any, List, Optional

from .base import BaseModule


class HTTPXModule(BaseModule):
    """
    AgisRecon wrapper for the HTTPX tool.
    """

    name: str = "httpx"
    description: str = "HTTP and HTTPS service probing using HTTPX"
    command: str = "httpx"

    def __init__(self, config: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the HTTPX module.

        Args:
            config: Optional module configuration.
        """
        super().__init__(config)

    def is_available(self) -> bool:
        """
        Check whether HTTPX is installed and available in PATH.

        Returns:
            True if HTTPX is available, otherwise False.
        """
        return shutil.which(self.command) is not None

    def run(self, target: str, **kwargs: Any) -> List[str]:
        """
        Run HTTPX against the supplied target.

        Args:
            target: Domain, hostname, IP address, or URL to probe.
            **kwargs: Optional HTTPX arguments.

        Returns:
            A list of discovered HTTP/HTTPS services.

        Raises:
            ValueError: If the target is invalid.
            RuntimeError: If HTTPX is unavailable or execution fails.
        """
        if not self.validate_target(target):
            raise ValueError("Invalid target provided.")

        if not self.is_available():
            raise RuntimeError(
                "HTTPX is not installed or not available in PATH."
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
                    f"HTTPX execution failed: {error}"
                )

            raise RuntimeError(
                f"HTTPX exited with code {process.returncode}."
            )

        for line in process.stdout.splitlines():
            result = line.strip()

            if result:
                self.add_result(result)

        return self.get_results()

