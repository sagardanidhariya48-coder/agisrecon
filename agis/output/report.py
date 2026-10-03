"""
AgisRecon2 - Report Manager

Central output manager for reconnaissance results.

Supported formats:
    - terminal
    - json
    - markdown
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .terminal import TerminalOutput
from .json import JSONOutput
from .markdown import MarkdownOutput


class ReportManager:
    """Manage AgisRecon2 reconnaissance reports."""

    SUPPORTED_FORMATS = {
        "terminal",
        "json",
        "markdown",
    }

    def __init__(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        verbose: bool = True,
    ):
        """
        Initialize the report manager.

        Args:
            output_dir: Base directory for generated reports.
            verbose: Enable verbose terminal output.
        """

        if output_dir is None:
            output_dir = Path("output")

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.terminal = TerminalOutput(
            verbose=verbose
        )

        self.json = JSONOutput(
            output_dir=self.output_dir / "json"
        )

        self.markdown = MarkdownOutput(
            output_dir=self.output_dir / "markdown"
        )

    # ---------------------------------------------------------
    # Generate report
    # ---------------------------------------------------------

    def generate(
        self,
        results: Any,
        target: Optional[str] = None,
        module: Optional[str] = None,
        formats: Optional[
            Union[str, List[str]]
        ] = None,
        filename: Optional[str] = None,
        title: str = "AgisRecon2 Reconnaissance Report",
    ) -> Dict[str, Optional[Path]]:
        """
        Generate reconnaissance output.

        Args:
            results:
                Results returned by a reconnaissance module.

            target:
                Target being scanned.

            module:
                Name of the module that produced the results.

            formats:
                Output format or list of formats.
                Supported:
                    terminal
                    json
                    markdown

            filename:
                Optional base filename.

            title:
                Markdown report title.

        Returns:
            Dictionary containing generated file paths.
        """

        selected_formats = self._normalize_formats(
            formats
        )

        generated: Dict[str, Optional[Path]] = {}

        for output_format in selected_formats:

            if output_format == "terminal":

                self._generate_terminal(
                    results=results,
                    target=target,
                    module=module,
                    title=title,
                )

                generated["terminal"] = None

            elif output_format == "json":

                json_filename = self._build_filename(
                    filename=filename,
                    extension=".json",
                    target=target,
                    module=module,
                )

                generated["json"] = self.json.save(
                    results=results,
                    filename=json_filename,
                    target=target,
                    module=module,
                )

            elif output_format == "markdown":

                markdown_filename = self._build_filename(
                    filename=filename,
                    extension=".md",
                    target=target,
                    module=module,
                )

                generated["markdown"] = (
                    self.markdown.save(
                        results=results,
                        filename=markdown_filename,
                        target=target,
                        module=module,
                        title=title,
                    )
                )

        return generated

    # ---------------------------------------------------------
    # Terminal generation
    # ---------------------------------------------------------

    def _generate_terminal(
        self,
        results: Any,
        target: Optional[str],
        module: Optional[str],
        title: str,
    ) -> None:
        """Display results in the terminal."""

        self.terminal.print_header(title)

        if target:
            self.terminal.print_info(
                f"Target: {target}"
            )

        if module:
            self.terminal.print_info(
                f"Module: {module}"
            )

        self.terminal.print_section(
            "Results"
        )

        if isinstance(results, dict):
            self.terminal.print_results(
                results,
                title="",
            )

        elif isinstance(
            results,
            (list, tuple, set),
        ):
            self.terminal.print_list(
                "Results",
                results,
            )

        else:
            self.terminal.print_result(
                "Result",
                results,
            )

    # ---------------------------------------------------------
    # Normalize formats
    # ---------------------------------------------------------

    def _normalize_formats(
        self,
        formats: Optional[
            Union[str, List[str]]
        ],
    ) -> List[str]:
        """
        Normalize and validate requested formats.

        If no format is provided, terminal output is used.
        """

        if formats is None:
            return ["terminal"]

        if isinstance(formats, str):

            if formats.lower() == "all":
                return [
                    "terminal",
                    "json",
                    "markdown",
                ]

            formats = [formats]

        normalized = []

        for output_format in formats:

            output_format = (
                str(output_format)
                .strip()
                .lower()
            )

            if output_format == "md":
                output_format = "markdown"

            if output_format == "txt":
                output_format = "terminal"

            if output_format not in self.SUPPORTED_FORMATS:
                raise ValueError(
                    f"Unsupported output format: "
                    f"{output_format}. "
                    f"Supported formats: "
                    f"{', '.join(sorted(self.SUPPORTED_FORMATS))}"
                )

            if output_format not in normalized:
                normalized.append(
                    output_format
                )

        return normalized

    # ---------------------------------------------------------
    # Filename handling
    # ---------------------------------------------------------

    @staticmethod
    def _build_filename(
        filename: Optional[str],
        extension: str,
        target: Optional[str],
        module: Optional[str],
    ) -> Optional[str]:
        """
        Build a filename while preserving the supplied
        filename when possible.
        """

        if filename:

            filename = Path(
                filename
            ).name

            if filename.endswith(
                extension
            ):
                return filename

            return (
                f"{filename}{extension}"
            )

        return None

    # ---------------------------------------------------------
    # Individual output helpers
    # ---------------------------------------------------------

    def terminal_output(
        self,
        results: Any,
        target: Optional[str] = None,
        module: Optional[str] = None,
        title: str = "AgisRecon2 Reconnaissance Report",
    ) -> None:
        """Display results in the terminal."""

        self.generate(
            results=results,
            target=target,
            module=module,
            formats=["terminal"],
            title=title,
        )

    def json_output(
        self,
        results: Any,
        target: Optional[str] = None,
        module: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Path:
        """Save results as JSON."""

        generated = self.generate(
            results=results,
            target=target,
            module=module,
            formats=["json"],
            filename=filename,
        )

        return generated["json"]

    def markdown_output(
        self,
        results: Any,
        target: Optional[str] = None,
        module: Optional[str] = None,
        filename: Optional[str] = None,
        title: str = "AgisRecon2 Reconnaissance Report",
    ) -> Path:
        """Save results as Markdown."""

        generated = self.generate(
            results=results,
            target=target,
            module=module,
            formats=["markdown"],
            filename=filename,
            title=title,
        )

        return generated["markdown"]

    # ---------------------------------------------------------
    # Generate everything
    # ---------------------------------------------------------

    def generate_all(
        self,
        results: Any,
        target: Optional[str] = None,
        module: Optional[str] = None,
        filename: Optional[str] = None,
        title: str = "AgisRecon2 Reconnaissance Report",
    ) -> Dict[str, Optional[Path]]:
        """
        Generate terminal, JSON, and Markdown output.
        """

        return self.generate(
            results=results,
            target=target,
            module=module,
            formats="all",
            filename=filename,
            title=title,
        )


# -------------------------------------------------------------
# Default report manager
# -------------------------------------------------------------

report_manager = ReportManager()


# -------------------------------------------------------------
# Convenience functions
# -------------------------------------------------------------

def generate_report(
    results: Any,
    target: Optional[str] = None,
    module: Optional[str] = None,
    formats: Optional[
        Union[str, List[str]]
    ] = None,
    filename: Optional[str] = None,
    title: str = "AgisRecon2 Reconnaissance Report",
) -> Dict[str, Optional[Path]]:
    """
    Generate AgisRecon2 output using the default
    ReportManager instance.
    """

    return report_manager.generate(
        results=results,
        target=target,
        module=module,
        formats=formats,
        filename=filename,
        title=title,
    )


def generate_all_reports(
    results: Any,
    target: Optional[str] = None,
    module: Optional[str] = None,
    filename: Optional[str] = None,
    title: str = "AgisRecon2 Reconnaissance Report",
) -> Dict[str, Optional[Path]]:
    """Generate all supported report formats."""

    return report_manager.generate_all(
        results=results,
        target=target,
        module=module,
        filename=filename,
        title=title,
    )