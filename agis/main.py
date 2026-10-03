#!/usr/bin/env python3

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
from typing import Any, Dict

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
# Generate Output
# --------------------------------------------------------------------

def generate_output(
    report_manager: ReportManager,
    results: Any,
    target: str,
    module: str,
    output_format: str,
) -> Dict[str, Any]:
    """
    Generate reconnaissance output.

    ReportManager is the single integration point for
    terminal, JSON, and Markdown output.
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
            ],
        )

    return report_manager.generate(
        results=results,
        target=target,
        module=module,
        formats=[output_format],
    )


# --------------------------------------------------------------------
# Run Scan
# --------------------------------------------------------------------

def run_scan(
    target: str,
    module_name: str,
    output_format: str,
) -> int:
    """
    Execute a complete reconnaissance scan.
    """

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
    # Generate results
    # ---------------------------------------------------------------

    try:

        generated = generate_output(
            report_manager=report_manager,
            results=results,
            target=target,
            module=module_name,
            output_format=output_format,
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
    # Run Scan
    # ---------------------------------------------------------------

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