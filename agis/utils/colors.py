"""
AgisRecon - Terminal Colors

Centralized color/theme manager for AgisRecon.

Features
--------
- Cross-platform (Linux, Windows, macOS)
- Automatic ANSI support using Colorama
- Ready-made themes for banner, info, success, error, etc.
- Helper methods for cleaner printing

Example
-------
from utils.colors import Color

print(Color.banner("AgisRecon"))
print(Color.success("[+] Scan completed"))
print(Color.error("[-] Tool not found"))
"""

from __future__ import annotations

from colorama import Fore, Style, init

# Enable ANSI colors (especially on Windows)
init(autoreset=True)


class Color:
    """ANSI Color Theme for AgisRecon"""

    # --------------------------------------------------
    # Base Colors
    # --------------------------------------------------

    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE

    LIGHT_BLACK = Fore.LIGHTBLACK_EX
    LIGHT_RED = Fore.LIGHTRED_EX
    LIGHT_GREEN = Fore.LIGHTGREEN_EX
    LIGHT_YELLOW = Fore.LIGHTYELLOW_EX
    LIGHT_BLUE = Fore.LIGHTBLUE_EX
    LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
    LIGHT_CYAN = Fore.LIGHTCYAN_EX
    LIGHT_WHITE = Fore.LIGHTWHITE_EX

    # --------------------------------------------------
    # Styles
    # --------------------------------------------------

    RESET = Style.RESET_ALL
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM
    NORMAL = Style.NORMAL

    # --------------------------------------------------
    # AgisRecon Theme
    # --------------------------------------------------

    BANNER = LIGHT_CYAN + BRIGHT
    TITLE = LIGHT_BLUE + BRIGHT
    INFO = CYAN
    SUCCESS = LIGHT_GREEN + BRIGHT
    WARNING = LIGHT_YELLOW + BRIGHT
    ERROR = LIGHT_RED + BRIGHT
    DEBUG = LIGHT_MAGENTA
    MODULE = LIGHT_BLUE
    VALUE = WHITE
    PROMPT = GREEN + BRIGHT

    # --------------------------------------------------
    # Helper Methods
    # --------------------------------------------------

    @staticmethod
    def banner(text: str) -> str:
        return f"{Color.BANNER}{text}{Color.RESET}"

    @staticmethod
    def title(text: str) -> str:
        return f"{Color.TITLE}{text}{Color.RESET}"

    @staticmethod
    def success(text: str) -> str:
        return f"{Color.SUCCESS}{text}{Color.RESET}"

    @staticmethod
    def error(text: str) -> str:
        return f"{Color.ERROR}{text}{Color.RESET}"

    @staticmethod
    def warning(text: str) -> str:
        return f"{Color.WARNING}{text}{Color.RESET}"

    @staticmethod
    def info(text: str) -> str:
        return f"{Color.INFO}{text}{Color.RESET}"

    @staticmethod
    def debug(text: str) -> str:
        return f"{Color.DEBUG}{text}{Color.RESET}"

    @staticmethod
    def module(text: str) -> str:
        return f"{Color.MODULE}{text}{Color.RESET}"

    @staticmethod
    def value(text: str) -> str:
        return f"{Color.VALUE}{text}{Color.RESET}"

    @staticmethod
    def prompt(text: str) -> str:
        return f"{Color.PROMPT}{text}{Color.RESET}"


# --------------------------------------------------
# Self Test
# --------------------------------------------------

if __name__ == "__main__":

    print()
    print(Color.banner("=" * 70))
    print(Color.title("                 AgisRecon Theme Preview"))
    print(Color.banner("=" * 70))
    print()

    print(Color.success("[+] SUCCESS"))
    print(Color.error("[-] ERROR"))
    print(Color.warning("[!] WARNING"))
    print(Color.info("[*] INFO"))
    print(Color.debug("[D] DEBUG"))
    print(Color.module("[MODULE] Subfinder"))
    print(Color.value("example.com"))
    print(Color.prompt("AgisRecon >"))

    print()
    print(Color.banner("=" * 70))