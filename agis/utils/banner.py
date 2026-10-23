"""
AgisRecon2 - Banner Utility

Displays the application banner and project information.
"""

from __future__ import annotations

from datetime import datetime


VERSION = "1.0.0"
AUTHOR = "Sagar Danidhariya"
LICENSE = "MIT"


def print_banner() -> None:
    """
    Display the AgisRecon2 startup banner.
    """

    banner = rf"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     █████╗  ██████╗ ██╗███████╗                              ║
    ║    ██╔══██╗██╔════╝ ██║██╔════╝                              ║
    ║    ███████║██║  ███╗██║███████╗                              ║
    ║    ██╔══██║██║   ██║██║╚════██║                              ║
    ║    ██║  ██║╚██████╔╝██║███████║                              ║
    ║    ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝                              ║
    ║                                                              ║
    ║                AgisRecon2 - Recon Framework                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """

    print(banner)

    print(f" Version : {VERSION}")
    print(f" Author  : {AUTHOR}")
    print(f" License : {LICENSE}")
    print(f" Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 62)


if __name__ == "__main__":
    print_banner()