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
    Display the AgisRecon startup banner with vibrant terminal styling.
    """
    # ANSI Escape Codes for styling (Cyan/Blue aesthetic)
    CYAN = "\033[36m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    banner = rf"""
    {CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗{RESET}
    {CYAN}║                                                                                  ║{RESET}
    {CYAN}║{BLUE}   █████╗  ██████╗ ██╗███████╗    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗     {CYAN}║{RESET}
    {CYAN}║{BLUE}  ██╔══██╗██╔════╝ ██║██╔════╝    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║     {CYAN}║{RESET}
    {CYAN}║{BLUE}  ███████║██║  ███╗██║███████╗    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║     {CYAN}║{RESET}
    {CYAN}║{BLUE}  ██╔══██║██║   ██║██║╚════██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║     {CYAN}║{RESET}
    {CYAN}║{BLUE}  ██║  ██║╚██████╔╝██║███████║    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║     {CYAN}║{RESET}
    {CYAN}║{BLUE}  ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝     {CYAN}║{RESET}
    {CYAN}║                                                                                  ║{RESET}
    {CYAN}║{BOLD}                         Agis Recon - Framework v2.0                              {CYAN}║{RESET}
    {CYAN}║                                                                                  ║{RESET}
    {CYAN}╚══════════════════════════════════════════════════════════════════════════════════╝{RESET}
    """
    print(banner)


    print(f" Version : {VERSION}")
    print(f" Author  : {AUTHOR}")
    print(f" License : {LICENSE}")
    print(f" Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 62)


if __name__ == "__main__":
    print_banner()
