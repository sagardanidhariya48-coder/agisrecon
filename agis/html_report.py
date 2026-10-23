#!/usr/bin/env python3

"""
AgisRecon2 - HTML Report Generator
===================================

Builds a standalone HTML report from the reconnaissance scans
and recon results that were already performed by AgisRecon2.

The generator reads the saved scan artifacts from the output
folder and supports every selection mode:

    - a single tool    : --module subfinder
    - multiple tools   : --module subfinder,httpx,nmap
    - all tools        : --module all (default)

Saved scans are read from the JSON reports first because they
keep the structured metadata, and the plain text reports are
used as a fallback for tools that were saved as text only.

Usage
-----
    python3 html_report.py
    python3 html_report.py --target gtu.ac.in
    python3 html_report.py --module nuclei
    python3 html_report.py --module subfinder,httpx,nmap
    python3 html_report.py --target gtu.ac.in --module all --open
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

try:
    from output.html import HTMLOutput
except ImportError:  # pragma: no cover - direct execution fallback
    sys.path.insert(
        0,
        str(Path(__file__).resolve().parent),
    )
    from output.html import HTMLOutput


APP_NAME = "AgisRecon2"
VERSION = "1.0.0"

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_DIR = PROJECT_ROOT / "output"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output" / "html"

# ANSI escape sequences emitted by colourful CLI tools.
ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

# Header fields of a plain text report.
TXT_FIELD_PATTERN = re.compile(
    r"^(Tool|Module|Target|Command|Timestamp|Results)\s+:\s+(.*)$"
)

# Order used when several tools are part of the same report.
TOOL_ORDER = (
    "subfinder",
    "assetfinder",
    "dnsx",
    "httpx",
    "nmap",
    "waybackurls",
    "katana",
    "nuclei",
)


# --------------------------------------------------------------------
# Scan loading
# --------------------------------------------------------------------

class ScanLoader:
    """
    Load previously performed scans from the output folder.

    JSON reports are preferred because they keep the structured
    metadata. Plain text reports are parsed as a fallback.
    """

    def __init__(
        self,
        input_dir: Optional[Path] = None,
    ):
        """
        Initialize the loader.

        Args:
            input_dir: Folder holding the saved scan artifacts.
        """

        if input_dir is None:
            input_dir = DEFAULT_INPUT_DIR

        self.input_dir = Path(input_dir)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def load(
        self,
        target: Optional[str] = None,
        tools: Optional[Sequence[str]] = None,
        latest_only: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Load saved scans.

        Args:
            target: Only keep scans performed against this target.
            tools: Only keep scans produced by these tools.
            latest_only: Keep only the most recent run of every
                         tool and target combination.

        Returns:
            List of scan records.
        """

        records: List[Dict[str, Any]] = []

        for record in self._load_json_scans():
            records.append(record)

        for record in self._load_txt_scans():
            records.append(record)

        records = self._deduplicate(records)

        records = self._filter(
            records=records,
            target=target,
            tools=tools,
        )

        records = self._sort(records)

        if latest_only:
            records = self._latest_only(records)

        return records

    # ---------------------------------------------------------
    # JSON scans
    # ---------------------------------------------------------

    def _load_json_scans(self) -> List[Dict[str, Any]]:
        """Load every scan saved as JSON."""

        records: List[Dict[str, Any]] = []

        json_dir = self.input_dir / "json"

        if not json_dir.is_dir():
            return records

        for file_path in sorted(json_dir.glob("*.json")):

            try:

                with file_path.open(
                    "r",
                    encoding="utf-8",
                ) as file:
                    data = json.load(file)

            except (OSError, ValueError):
                continue

            if not isinstance(data, dict):
                continue

            module = data.get("module")

            tool = module or data.get("tool") or "unknown"

            records.append(
                {
                    "tool": str(tool),
                    "module": str(module or tool),
                    "target": data.get("target"),
                    "command": data.get("command"),
                    "timestamp": self._format_timestamp(
                        data.get("timestamp")
                    ),
                    "results": data.get("results"),
                    "source": file_path,
                }
            )

        return records

    # ---------------------------------------------------------
    # Plain text scans
    # ---------------------------------------------------------

    def _load_txt_scans(self) -> List[Dict[str, Any]]:
        """Load every scan saved as plain text."""

        records: List[Dict[str, Any]] = []

        txt_dir = self.input_dir / "txt"

        if not txt_dir.is_dir():
            return records

        for file_path in sorted(txt_dir.glob("*.txt")):

            try:
                content = file_path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            except OSError:
                continue

            record = self._parse_txt_scan(content)

            if record is None:
                continue

            record["source"] = file_path

            records.append(record)

        return records

    @staticmethod
    def _parse_txt_scan(
        content: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Parse a plain text report into a scan record.
        """

        fields: Dict[str, str] = {}

        results: List[str] = []

        in_results = False

        for line in content.splitlines():

            stripped = line.strip()

            # Section separators carry no information. The footer
            # separator closes the results section.
            if stripped and set(stripped) <= {"=", "-"}:
                if "-" in stripped:
                    in_results = False
                continue

            match = TXT_FIELD_PATTERN.match(stripped)

            if match:
                fields[match.group(1).lower()] = match.group(2).strip()
                in_results = False
                continue

            if stripped == "Results":
                in_results = True
                continue

            if in_results:

                if stripped.startswith("- "):
                    results.append(stripped[2:].strip())

                elif stripped and stripped != "(no results)":
                    results.append(stripped)

        if not fields and not results:
            return None

        module = fields.get("module") or fields.get("tool")

        if not module:
            return None

        return {
            "tool": fields.get("tool") or module,
            "module": module,
            "target": fields.get("target"),
            "command": fields.get("command"),
            "timestamp": fields.get("timestamp"),
            "results": results,
        }

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    @staticmethod
    def _filter(
        records: List[Dict[str, Any]],
        target: Optional[str],
        tools: Optional[Sequence[str]],
    ) -> List[Dict[str, Any]]:
        """Filter records by target and tool."""

        filtered = records

        if target:

            target = str(target).strip().lower()

            filtered = [
                record
                for record in filtered
                if str(record.get("target") or "").strip().lower()
                == target
            ]

        if tools:

            wanted = {
                str(tool).strip().lower()
                for tool in tools
                if str(tool).strip()
            }

            filtered = [
                record
                for record in filtered
                if str(record.get("tool") or "").strip().lower()
                in wanted
                or str(record.get("module") or "").strip().lower()
                in wanted
            ]

        return filtered

    @staticmethod
    def _deduplicate(
        records: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicated scans.

        A JSON scan and a plain text scan of the same run share
        the same tool, target, and timestamp, so the JSON record
        is kept and the text record is dropped.
        """

        seen = set()

        unique: List[Dict[str, Any]] = []

        for record in records:

            key = (
                str(record.get("tool") or "").lower(),
                str(record.get("module") or "").lower(),
                str(record.get("target") or "").lower(),
                str(record.get("timestamp") or ""),
            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(record)

        return unique

    @staticmethod
    def _latest_only(
        records: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Keep only the most recent run of every tool and target.
        """

        latest: Dict[tuple[str, str], Dict[str, Any]] = {}

        for record in records:

            key = (
                str(record.get("tool") or "").lower(),
                str(record.get("target") or "").lower(),
            )

            current = latest.get(key)

            if current is None:
                latest[key] = record
                continue

            if ScanLoader._to_sortable(
                record.get("timestamp")
            ) >= ScanLoader._to_sortable(
                current.get("timestamp")
            ):
                latest[key] = record

        return list(latest.values())

    @staticmethod
    def _sort(
        records: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Sort records by tool order, target, and timestamp."""

        def sort_key(record: Dict[str, Any]) -> tuple:

            tool = str(record.get("tool") or "").lower()

            if tool in TOOL_ORDER:
                tool_rank = TOOL_ORDER.index(tool)
            else:
                tool_rank = len(TOOL_ORDER)

            return (
                tool_rank,
                tool,
                str(record.get("target") or "").lower(),
                ScanLoader._to_sortable(
                    record.get("timestamp")
                ),
            )

        return sorted(records, key=sort_key)

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def _to_sortable(value: Any) -> str:
        """Convert a timestamp into a sortable string."""

        if not value:
            return ""

        text = str(value).strip()

        text = ANSI_ESCAPE_PATTERN.sub("", text)

        text = text.replace("T", " ")
        text = text.replace("Z", "")

        return text

    @staticmethod
    def _format_timestamp(value: Any) -> str:
        """Normalize a timestamp for display."""

        if not value:
            return ""

        text = str(value).strip()

        text = ANSI_ESCAPE_PATTERN.sub("", text)

        if "T" in text:
            text = text.split(".")[0].replace("T", " ")

        return text


# --------------------------------------------------------------------
# Argument parser
# --------------------------------------------------------------------

def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        prog="html_report.py",
        description=(
            "Generate an HTML report from the reconnaissance "
            "scans performed by AgisRecon2."
        ),
    )

    parser.add_argument(
        "-t",
        "--target",
        help=(
            "Only report scans performed against this target. "
            "Example: gtu.ac.in"
        ),
    )

    parser.add_argument(
        "-m",
        "--module",
        default="all",
        help=(
            "Tool selection. Use 'all' for every tool, a single "
            "tool name such as 'nuclei', or a comma separated list "
            "such as 'subfinder,httpx,nmap'. "
            "Default: all."
        ),
    )

    parser.add_argument(
        "-o",
        "--output",
        help=(
            "Path of the generated HTML report. "
            "Default: output/html/agis_recon_report_<timestamp>.html"
        ),
    )

    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_INPUT_DIR),
        help=(
            "Folder holding the saved scan artifacts. "
            f"Default: {DEFAULT_INPUT_DIR}"
        ),
    )

    parser.add_argument(
        "--title",
        default=None,
        help=(
            "Report title. "
            "Default: AgisRecon2 Reconnaissance Report, with the "
            "target appended when a target is selected."
        ),
    )

    parser.add_argument(
        "--all-runs",
        action="store_true",
        help=(
            "Include every saved run instead of only the most "
            "recent run of every tool."
        ),
    )

    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_only",
        help=(
            "List the saved scans that were found and exit "
            "without generating a report."
        ),
    )

    parser.add_argument(
        "--open",
        action="store_true",
        dest="open_report",
        help="Open the generated report in the default browser.",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Display the AgisRecon2 version.",
    )

    return parser


# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------

def parse_tools(value: str) -> Optional[List[str]]:
    """
    Convert the module argument into a list of tool names.

    Returns:
        None when every tool should be reported, otherwise the
        list of requested tool names.
    """

    if value is None:
        return None

    cleaned = str(value).strip()

    if not cleaned or cleaned.lower() == "all":
        return None

    tools = [
        part.strip().lower()
        for part in cleaned.split(",")
        if part.strip()
    ]

    if not tools:
        return None

    if "all" in tools:
        return None

    return tools


def print_scans(
    records: List[Dict[str, Any]],
) -> None:
    """Display the scans that were found."""

    print()
    print(f"{'Tool':<14}{'Target':<24}{'Findings':>10}  Timestamp")
    print("-" * 72)

    for record in records:

        findings = len(record.get("results") or [])

        print(
            f"{str(record.get('tool')):<14}"
            f"{str(record.get('target') or 'N/A'):<24}"
            f"{findings:>10}  "
            f"{record.get('timestamp') or 'N/A'}"
        )

    print("-" * 72)
    print(f"Total scans: {len(records)}")


def build_title(
    target: Optional[str],
    tools: Optional[Sequence[str]],
) -> str:
    """Build the default report title."""

    title = "AgisRecon2 Reconnaissance Report"

    if target:
        title = f"{title} - {target}"

    elif tools:
        title = f"{title} - {', '.join(tools)}"

    return title


def build_output_path(
    target: Optional[str],
    tools: Optional[Sequence[str]],
) -> Path:
    """Build the default output path for the generated report."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    target_name = (
        str(target)
        .replace("://", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        if target
        else "all_targets"
    )

    if tools:
        tool_name = "_".join(tools)
    else:
        tool_name = "all"

    return (
        DEFAULT_OUTPUT_DIR
        / f"agis_recon_report_{target_name}_{tool_name}_{timestamp}.html"
    )


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main() -> int:
    """Main application entry point."""

    parser = create_parser()

    args = parser.parse_args()

    if args.version:

        print(f"{APP_NAME} v{VERSION}")

        return 0

    tools = parse_tools(args.module)

    loader = ScanLoader(
        input_dir=Path(args.input_dir)
    )

    records = loader.load(
        target=args.target,
        tools=tools,
        latest_only=not args.all_runs,
    )

    if args.list_only:

        if not records:
            print("[ERROR] No saved scans were found.")
            return 1

        print_scans(records)

        return 0

    if not records:

        print("[ERROR] No saved scans matched the selection.")

        print(
            "[INFO] Run a scan first, for example:"
        )
        print(
            "[INFO] python3 main.py --target example.com "
            "--module subfinder --output all"
        )

        return 1

    output_path = Path(args.output) if args.output else build_output_path(
        target=args.target,
        tools=tools,
    )

    title = args.title or build_title(
        target=args.target,
        tools=tools,
    )

    if output_path.parent and not output_path.parent.exists():
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    report = HTMLOutput(
        output_dir=output_path.parent
    )

    html = report.format_results(
        title=title,
        scans=records,
    )

    output_path.write_text(
        html,
        encoding="utf-8",
    )

    print()
    print("[INFO] Scans included :", len(records))

    for record in records:
        print(
            f"[INFO]   - {record.get('tool')}: "
            f"{len(record.get('results') or [])} findings"
        )

    print(f"[SUCCESS] HTML report saved: {output_path}")

    if args.open_report:

        try:
            webbrowser.open(output_path.resolve().as_uri())
        except Exception:
            print("[WARNING] Could not open the report automatically.")

    return 0


# --------------------------------------------------------------------
# Program Entry Point
# --------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())
