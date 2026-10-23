##!/usr/bin/env python3

"""
AgisRecon2 - Main Entry Point
=============================

Main CLI for the AgisRecon2 reconnaissance framework.

Responsibilities
----------------
- Initialize the application
- Display the project banner
- Validate targets
- List reconnaissance modules
- Execute reconnaissance modules
- Log scan activity
- Generate terminal, JSON, and Markdown output

Architecture
------------
main.py
    |
    +-- config/
    +-- modules/
    +-- utils/
    +-- output/
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from modules import ModuleManager

from output import ReportManager

from utils import (
    get_logger,
    print_banner,
    validate_domain,
    validate_ip,
    validate_url,
)

from utils.helpers import clean_string


# --------------------------------------------------------------------
# Application Information
# --------------------------------------------------------------------

APP_NAME = "AgisRecon2"
VERSION = "1.0.0"


# --------------------------------------------------------------------
# Logger
# --------------------------------------------------------------------

logger = get_logger(APP_NAME)


# --------------------------------------------------------------------
# Argument Parser
# --------------------------------------------------------------------

def create_parser() -> argparse.ArgumentParser:
    """
    Create the command-line argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="main.py",
        description=(
            "AgisRecon2 - Modular reconnaissance framework"
        ),
    )

    parser.add_argument(
        "-t",
        "--target",
        help=(
            "Target domain, IP address, or HTTP/HTTPS URL."
        ),
    )

    parser.add_argument(
        "-m",
        "--module",
        help="Reconnaissance module to execute.",
    )

    parser.add_argument(
        "-o",
        "--output",
        choices=[
            "terminal",
            "json",
            "markdown",
            "txt",
            "html",
            "all",
        ],
        default="terminal",
        help=(
            "Output format. "
            "Default: terminal. "
            "Use 'all' for all supported formats."
        ),
    )

    parser.add_argument(
        "--list-modules",
        action="store_true",
        help="List all available reconnaissance modules.",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Display AgisRecon2 version.",
    )

    return parser


# --------------------------------------------------------------------
# Target Validation
# --------------------------------------------------------------------

def validate_target(target: str) -> bool:
    """
    Validate a reconnaissance target.

    Supported targets:
        - Domain
        - IPv4
        - IPv6
        - HTTP URL
        - HTTPS URL
    """

    target = clean_string(target)

    if not target:
        return False

    if validate_domain(target):
        return True

    if validate_ip(target):
        return True

    if validate_url(target):
        return True

    return False


# --------------------------------------------------------------------
# Module Manager
# --------------------------------------------------------------------

def create_module_manager() -> ModuleManager:
    """
    Create the AgisRecon2 module manager.
    """

    try:
        manager = ModuleManager()
        logger.debug("ModuleManager initialized.")
        return manager

    except Exception as exc:
        logger.exception(
            "Failed to initialize ModuleManager."
        )
        raise RuntimeError(
            f"Failed to initialize ModuleManager: {exc}"
        ) from exc


# --------------------------------------------------------------------
# List Modules
# --------------------------------------------------------------------

def list_modules(manager: ModuleManager) -> int:
    """
    Display all registered reconnaissance modules.
    """

    try:
        modules = manager.get_all_module_info()

    except Exception as exc:
        logger.exception(
            "Failed to retrieve module information."
        )
        print(f"[ERROR] Failed to retrieve modules: {exc}")
        return 1

    print()
    print("Available Modules")
    print("-" * 64)

    if not modules:
        print("No modules found.")
        print("-" * 64)
        return 0

    for module_name, info in modules.items():

        if isinstance(info, dict):
            name = info.get(
                "name",
                module_name,
            )

            description = info.get(
                "description",
                "No description available",
            )

            available = info.get(
                "available",
                False,
            )

        else:
            name = module_name
            description = str(info)
            available = False

        status = (
            "AVAILABLE"
            if available
            else "NOT AVAILABLE"
        )

        print(
            f"{name:<18} : {status}"
        )

        print(
            f"{'Description':<18} : {description}"
        )

        print()

    print("-" * 64)

    return 0


# --------------------------------------------------------------------
# Module Availability
# --------------------------------------------------------------------

def module_exists(
    manager: ModuleManager,
    module_name: str,
) -> bool:
    """
    Check whether a module exists.
    """

    try:
        modules = manager.get_all_module_info()
    except Exception:
        return False

    return module_name in modules


def module_is_available(
    manager: ModuleManager,
    module_name: str,
) -> bool:
    """
    Check whether a module exists and its external tool
    is available on the system.
    """

    try:
        modules = manager.get_all_module_info()

        info = modules.get(module_name)

        if info is None:
            return False

        if isinstance(info, dict):
            return bool(
                info.get("available", False)
            )

        return False

    except Exception:
        return False


# --------------------------------------------------------------------
# Module Execution
# --------------------------------------------------------------------

def execute_module(
    manager: ModuleManager,
    module_name: str,
    target: str,
) -> Any:
    """
    Execute a reconnaissance module through ModuleManager.

    The ModuleManager remains responsible for module execution.
    main.py only orchestrates the workflow.
    """

    logger.info(
        "Executing module '%s' against '%s'.",
        module_name,
        target,
    )

    # Preferred ModuleManager API.
    if hasattr(manager, "run_module"):

        return manager.run_module(
            module_name,
            target,
        )

    # Alternative API.
    if hasattr(manager, "execute_module"):

        return manager.execute_module(
            module_name,
            target,
        )

    # Generic run API.
    if hasattr(manager, "run"):

        return manager.run(
            module_name,
            target,
        )

    # Generic execute API.
    if hasattr(manager, "execute"):

        return manager.execute(
            module_name,
            target,
        )

    raise RuntimeError(
        "ModuleManager does not provide a supported "
        "module execution method."
    )


# --------------------------------------------------------------------
# Tool Information
# --------------------------------------------------------------------

def get_tool_details(
    manager: ModuleManager,
    module_name: str,
) -> Dict[str, Optional[str]]:
    """
    Resolve the external tool used by a reconnaissance module.

    Args:
        manager: ModuleManager instance.
        module_name: Name of the executed module.

    Returns:
        Dictionary containing the tool executable and the
        command executed during the scan.
    """

    try:

        module = manager.get(module_name)

    except Exception:
        return {
            "tool": None,
            "command": None,
        }

    command = getattr(module, "command", None)

    return {
        "tool": command or module_name,
        "command": getattr(module, "last_command", None),
    }


# --------------------------------------------------------------------
# Generate Output
# --------------------------------------------------------------------

def generate_output(
    report_manager: ReportManager,
    results: Any,
    target: str,
    module: str,
    output_format: str,
    tool: Optional[str] = None,
    command: Optional[str] = None,
    scans: Optional[list[dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Generate reconnaissance output.

    ReportManager is the single integration point for
    terminal, JSON, Markdown, plain text, and HTML output.
    """

    logger.debug(
        "Generating '%s' output.",
        output_format,
    )

    if output_format == "all":

        return report_manager.generate(
            results=results,
            target=target,
            module=module,
            formats=[
                "terminal",
                "json",
                "markdown",
                "txt",
                "html",
            ],
            tool=tool,
            command=command,
            scans=scans,
        )

    return report_manager.generate(
        results=results,
        target=target,
        module=module,
        formats=[output_format],
        tool=tool,
        command=command,
        scans=scans,
    )


def run_all_modules(
    target: str,
    output_format: str,
) -> int:
    """
    Execute all reconnaissance modules as a pipeline.
    Run each module in order, display output after each module,
    and continue to the next tool.
    """

    target = clean_string(target)

    logger.info("Starting AgisRecon2 pipeline scan (all modules).")
    logger.info("Target: %s", target)
    logger.info("Output: %s", output_format)

    if not validate_target(target):

        logger.error("Invalid target: %s", target)

        print(f"[ERROR] Invalid target: {target}")
        print("[INFO] Supported targets: domain, IP address, HTTP/HTTPS URL.")

        return 1

    try:
        manager = create_module_manager()
    except RuntimeError as exc:
        print(f"[ERROR] {exc}")
        return 1

    try:
        report_manager = ReportManager(
            output_dir="output",
            verbose=True,
        )
    except Exception as exc:
        logger.exception("Failed to initialize ReportManager.")
        print(f"[ERROR] Failed to initialize ReportManager: {exc}")
        return 1

    print()
    print(f"[INFO] Target : {target}")
    print(f"[INFO] Module : all (pipeline)")
    print(f"[INFO] Output : {output_format}")
    print()

    modules = manager.list_modules()
    total = len(modules)
    exit_code = 0

    scan_records: list[dict[str, Any]] = []

    for idx, module_name in enumerate(modules, start=1):
        print("=" * 64)
        print(f"[PIPELINE] [{idx}/{total}] Running module: {module_name}")
        print("=" * 64)
        print()

        if not module_is_available(manager, module_name):
            print(f"[WARNING] Module '{module_name}' is not available. Skipping.")
            print()
            logger.warning("Module '%s' is not available. Skipping.", module_name)
            continue

        try:
            results = execute_module(
                manager=manager,
                module_name=module_name,
                target=target,
            )
        except KeyboardInterrupt:
            logger.warning("Scan interrupted by user.")
            print()
            print("[WARNING] Scan interrupted by user.")
            return 130
        except Exception as exc:
            logger.exception("Module execution failed for '%s'.", module_name)
            print(f"[ERROR] Module '{module_name}' execution failed: {exc}")
            print()
            exit_code = 1
            continue

        tool_details = get_tool_details(manager=manager, module_name=module_name)

        scan_records.append(
            {
                "tool": tool_details["tool"] or module_name,
                "module": module_name,
                "target": target,
                "command": tool_details["command"],
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "results": results,
            }
        )

        try:
            generated = generate_output(
                report_manager=report_manager,
                results=results,
                target=target,
                module=module_name,
                output_format=output_format,
                tool=tool_details["tool"],
                command=tool_details["command"],
            )
        except Exception as exc:
            logger.exception("Output generation failed for '%s'.", module_name)
            print(f"[ERROR] Output generation failed for '{module_name}': {exc}")
            print()
            exit_code = 1
            continue

        if generated:
            print()
            for format_name, file_path in generated.items():
                if file_path:
                    print(
                        f"[SUCCESS] "
                        f"{format_name.capitalize()} output saved: "
                        f"{file_path}"
                    )
                    logger.info(
                        "%s output saved: %s",
                        format_name,
                        file_path,
                    )
            print()

        print(f"[PIPELINE] [{idx}/{total}] Completed module: {module_name}")
        print()

    # ---------------------------------------------------------------
    # Consolidated HTML report
    # ---------------------------------------------------------------

    if scan_records:

        try:

            consolidated = report_manager.html.save(
                target=target,
                module="all",
                title=(
                    f"AgisRecon2 Reconnaissance Report - {target}"
                ),
                scans=scan_records,
            )

            print(f"[SUCCESS] Consolidated HTML report saved: {consolidated}")
            logger.info(
                "Consolidated HTML report saved: %s",
                consolidated,
            )

        except Exception as exc:

            logger.exception("Consolidated HTML report generation failed.")
            print(f"[ERROR] Consolidated HTML report failed: {exc}")
            exit_code = 1

    logger.info("Pipeline scan completed.")
    print("=" * 64)
    print(f"[SUCCESS] Pipeline completed for '{target}'.")
    print("=" * 64)

    return exit_code


def run_scan(
    target: str,
    module_name: str,
    output_format: str,
) -> int:
    """Execute a complete reconnaissance scan."""

    # ---------------------------------------------------------------
    # Clean target
    # ---------------------------------------------------------------

    target = clean_string(target)

    logger.info(
        "Starting AgisRecon2 scan."
    )

    logger.info(
        "Target: %s",
        target,
    )

    logger.info(
        "Module: %s",
        module_name,
    )

    logger.info(
        "Output: %s",
        output_format,
    )

    # ---------------------------------------------------------------
    # Validate target
    # ---------------------------------------------------------------

    if not validate_target(target):

        logger.error(
            "Invalid target: %s",
            target,
        )

        print(
            f"[ERROR] Invalid target: {target}"
        )

        print(
            "[INFO] Supported targets: "
            "domain, IP address, HTTP/HTTPS URL."
        )

        return 1

    # ---------------------------------------------------------------
    # Initialize ModuleManager
    # ---------------------------------------------------------------

    try:

        manager = create_module_manager()

    except RuntimeError as exc:

        print(
            f"[ERROR] {exc}"
        )

        return 1

    # ---------------------------------------------------------------
    # Check module
    # ---------------------------------------------------------------

    if not module_exists(
        manager,
        module_name,
    ):

        logger.error(
            "Unknown module: %s",
            module_name,
        )

        print(
            f"[ERROR] Unknown module: {module_name}"
        )

        print(
            "[INFO] Use --list-modules "
            "to see available modules."
        )

        return 1

    # ---------------------------------------------------------------
    # Check module availability
    # ---------------------------------------------------------------

    if not module_is_available(
        manager,
        module_name,
    ):

        logger.error(
            "Module '%s' is not available.",
            module_name,
        )

        print(
            f"[ERROR] Module '{module_name}' "
            "is not available."
        )

        return 1

    # ---------------------------------------------------------------
    # Initialize ReportManager
    # ---------------------------------------------------------------

    try:

        report_manager = ReportManager(
            output_dir="output",
            verbose=True,
        )

    except Exception as exc:

        logger.exception(
            "Failed to initialize ReportManager."
        )

        print(
            f"[ERROR] Failed to initialize "
            f"ReportManager: {exc}"
        )

        return 1

    # ---------------------------------------------------------------
    # Start scan
    # ---------------------------------------------------------------

    print()
    print(
        f"[INFO] Target : {target}"
    )
    print(
        f"[INFO] Module : {module_name}"
    )
    print(
        f"[INFO] Output : {output_format}"
    )
    print()

    logger.info(
        "Scan started."
    )

    try:

        results = execute_module(
            manager=manager,
            module_name=module_name,
            target=target,
        )

    except KeyboardInterrupt:

        logger.warning(
            "Scan interrupted by user."
        )

        print()
        print(
            "[WARNING] Scan interrupted by user."
        )

        return 130

    except Exception as exc:

        logger.exception(
            "Module execution failed."
        )

        print(
            f"[ERROR] Module execution failed: {exc}"
        )

        return 1

    # ---------------------------------------------------------------
    # Resolve tool information
    # ---------------------------------------------------------------

    tool_details = get_tool_details(
        manager=manager,
        module_name=module_name,
    )

    # ---------------------------------------------------------------
    # Generate results
    # ---------------------------------------------------------------

    try:

        generated = generate_output(
            report_manager=report_manager,
            results=results,
            target=target,
            module=module_name,
            output_format=output_format,
            tool=tool_details["tool"],
            command=tool_details["command"],
        )

    except Exception as exc:

        logger.exception(
            "Output generation failed."
        )

        print(
            f"[ERROR] Output generation failed: {exc}"
        )

        return 1

    # ---------------------------------------------------------------
    # Display generated files
    # ---------------------------------------------------------------

    if generated:

        print()

        for format_name, file_path in generated.items():

            if file_path:

                print(
                    f"[SUCCESS] "
                    f"{format_name.capitalize()} output saved: "
                    f"{file_path}"
                )

                logger.info(
                    "%s output saved: %s",
                    format_name,
                    file_path,
                )

    # ---------------------------------------------------------------
    # Complete
    # ---------------------------------------------------------------

    logger.info(
        "Scan completed successfully."
    )

    print()
    print(
        f"[SUCCESS] Scan completed for '{target}'."
    )

    return 0


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main() -> int:
    """
    Main application entry point.
    """

    parser = create_parser()
    args = parser.parse_args()

    # ---------------------------------------------------------------
    # Version
    # ---------------------------------------------------------------

    if args.version:

        print(
            f"{APP_NAME} v{VERSION}"
        )

        return 0

    # ---------------------------------------------------------------
    # Banner
    # ---------------------------------------------------------------

    print_banner()

    # ---------------------------------------------------------------
    # List Modules
    # ---------------------------------------------------------------

    if args.list_modules:

        try:

            manager = create_module_manager()

        except RuntimeError as exc:

            print(
                f"[ERROR] {exc}"
            )

            return 1

        return list_modules(manager)

    # ---------------------------------------------------------------
    # Target Required
    # ---------------------------------------------------------------

    if not args.target:

        parser.error(
            "--target is required unless using "
            "--list-modules or --version."
        )

    # ---------------------------------------------------------------
    # Module Required
    # ---------------------------------------------------------------

    if not args.module:

        parser.error(
            "--module is required unless using "
            "--list-modules or --version."
        )

    # ---------------------------------------------------------------
    # Run Scan (including pipeline)
    # ---------------------------------------------------------------

    if args.module and args.module.strip().lower() == "all":
        return run_all_modules(
            target=args.target,
            output_format=args.output,
        )

    return run_scan(
        target=args.target,
        module_name=args.module,
        output_format=args.output,
    )


# --------------------------------------------------------------------
# Program Entry Point
# --------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())