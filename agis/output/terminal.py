"""
AgisRecon2 - Terminal Output

Handles displaying reconnaissance results in the terminal.
"""

from typing import Any, Dict, Iterable, Optional

try:
    from utils.colors import Colors
except ImportError:
    class Colors:
        RESET = "\033[0m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
        BOLD = "\033[1m"


class TerminalOutput:
    """Display AgisRecon2 results in the terminal."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    # ---------------------------------------------------------
    # Basic output
    # ---------------------------------------------------------

    def print_info(self, message: str) -> None:
        """Print an informational message."""
        print(f"{Colors.CYAN}[INFO]{Colors.RESET} {message}")

    def print_success(self, message: str) -> None:
        """Print a success message."""
        print(f"{Colors.GREEN}[+]{Colors.RESET} {message}")

    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        print(f"{Colors.YELLOW}[!]{Colors.RESET} {message}")

    def print_error(self, message: str) -> None:
        """Print an error message."""
        print(f"{Colors.RED}[-]{Colors.RESET} {message}")

    def print_debug(self, message: str) -> None:
        """Print a debug message when verbose mode is enabled."""
        if self.verbose:
            print(f"{Colors.BLUE}[DEBUG]{Colors.RESET} {message}")

    # ---------------------------------------------------------
    # Headers
    # ---------------------------------------------------------

    def print_header(self, title: str) -> None:
        """Print a section header."""
        line = "=" * 60

        print()
        print(f"{Colors.BOLD}{Colors.CYAN}{line}{Colors.RESET}")
        print(
            f"{Colors.BOLD}{Colors.WHITE}"
            f"{title.center(60)}"
            f"{Colors.RESET}"
        )
        print(f"{Colors.BOLD}{Colors.CYAN}{line}{Colors.RESET}")
        print()

    def print_section(self, title: str) -> None:
        """Print a smaller section title."""
        print()
        print(
            f"{Colors.BOLD}{Colors.CYAN}"
            f"--- {title} ---"
            f"{Colors.RESET}"
        )

    # ---------------------------------------------------------
    # Result output
    # ---------------------------------------------------------

    def print_result(
        self,
        name: str,
        value: Any,
        status: Optional[str] = None,
    ) -> None:
        """Print a single reconnaissance result."""

        if status:
            status_text = self._format_status(status)
            print(
                f"{Colors.WHITE}{name:<25}{Colors.RESET}"
                f" : {status_text}"
            )
        else:
            print(
                f"{Colors.WHITE}{name:<25}{Colors.RESET}"
                f" : {value}"
            )

    def print_results(
        self,
        results: Dict[str, Any],
        title: str = "Scan Results",
    ) -> None:
        """Print dictionary-based scan results."""

        self.print_header(title)

        if not results:
            self.print_warning("No results found.")
            return

        for name, value in results.items():
            if isinstance(value, (list, tuple, set)):
                self.print_list(name, value)
            elif isinstance(value, dict):
                self.print_dict(name, value)
            else:
                self.print_result(name, value)

    def print_list(
        self,
        title: str,
        items: Iterable[Any],
    ) -> None:
        """Print a list of reconnaissance results."""

        print(
            f"{Colors.BOLD}{Colors.WHITE}"
            f"{title}:{Colors.RESET}"
        )

        items = list(items)

        if not items:
            print(f"  {Colors.YELLOW}No results{Colors.RESET}")
            return

        for item in items:
            print(
                f"  {Colors.GREEN}•{Colors.RESET} "
                f"{item}"
            )

    def print_dict(
        self,
        title: str,
        data: Dict[str, Any],
    ) -> None:
        """Print nested dictionary results."""

        print(
            f"{Colors.BOLD}{Colors.WHITE}"
            f"{title}:{Colors.RESET}"
        )

        if not data:
            print(f"  {Colors.YELLOW}No data{Colors.RESET}")
            return

        for key, value in data.items():
            print(
                f"  {Colors.CYAN}{key}{Colors.RESET}"
                f" : {value}"
            )

    # ---------------------------------------------------------
    # Module output
    # ---------------------------------------------------------

    def module_started(self, module_name: str) -> None:
        """Display module execution start."""
        print(
            f"{Colors.CYAN}[*]{Colors.RESET} "
            f"Running module: "
            f"{Colors.BOLD}{module_name}{Colors.RESET}"
        )

    def module_completed(self, module_name: str) -> None:
        """Display successful module completion."""
        print(
            f"{Colors.GREEN}[+]{Colors.RESET} "
            f"Module completed: "
            f"{Colors.BOLD}{module_name}{Colors.RESET}"
        )

    def module_failed(
        self,
        module_name: str,
        error: Any,
    ) -> None:
        """Display module failure."""
        print(
            f"{Colors.RED}[-]{Colors.RESET} "
            f"Module failed: "
            f"{Colors.BOLD}{module_name}{Colors.RESET}"
        )

        if error:
            print(
                f"    {Colors.RED}{error}{Colors.RESET}"
            )

    # ---------------------------------------------------------
    # Scan output
    # ---------------------------------------------------------

    def scan_started(self, target: str) -> None:
        """Display scan start."""
        self.print_header("AgisRecon2 Reconnaissance")
        self.print_info(f"Target: {target}")

    def scan_completed(self, target: str) -> None:
        """Display scan completion."""
        print()
        self.print_success(
            f"Scan completed for: {target}"
        )

    def scan_failed(
        self,
        target: str,
        error: Any,
    ) -> None:
        """Display scan failure."""
        print()
        self.print_error(
            f"Scan failed for: {target}"
        )

        if error:
            self.print_error(str(error))

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def _format_status(status: str) -> str:
        """Format common status values."""

        status_lower = str(status).lower()

        if status_lower in {
            "success",
            "successful",
            "ok",
            "completed",
            "complete",
        }:
            return f"{Colors.GREEN}{status}{Colors.RESET}"

        if status_lower in {
            "warning",
            "warn",
        }:
            return f"{Colors.YELLOW}{status}{Colors.RESET}"

        if status_lower in {
            "error",
            "failed",
            "failure",
        }:
            return f"{Colors.RED}{status}{Colors.RESET}"

        return f"{Colors.WHITE}{status}{Colors.RESET}"


# -------------------------------------------------------------
# Default terminal output instance
# -------------------------------------------------------------

terminal = TerminalOutput()


# -------------------------------------------------------------
# Convenience functions
# -------------------------------------------------------------

def print_info(message: str) -> None:
    """Print an informational message."""
    terminal.print_info(message)


def print_success(message: str) -> None:
    """Print a success message."""
    terminal.print_success(message)


def print_warning(message: str) -> None:
    """Print a warning message."""
    terminal.print_warning(message)


def print_error(message: str) -> None:
    """Print an error message."""
    terminal.print_error(message)


def print_results(
    results: Dict[str, Any],
    title: str = "Scan Results",
) -> None:
    """Print scan results."""
    terminal.print_results(results, title)