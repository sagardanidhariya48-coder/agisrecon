"""
AgisRecon2 - Validator Utility

Provides validation functions used throughout the project.

Supported validation:
- Domain
- IP Address
- URL
- Port
- File existence

Example
-------
from utils.validator import validate_domain

if validate_domain("example.com"):
    print("Valid domain")
"""

from __future__ import annotations

import ipaddress
import re
from pathlib import Path
from urllib.parse import urlparse


# --------------------------------------------------------------------
# Regular Expressions
# --------------------------------------------------------------------

DOMAIN_REGEX = re.compile(
    r"^(?!-)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$"
)


# --------------------------------------------------------------------
# Domain Validation
# --------------------------------------------------------------------

def validate_domain(domain: str) -> bool:
    """
    Validate a domain name.

    Example:
        example.com
        sub.example.org
    """

    if not domain:
        return False

    return bool(DOMAIN_REGEX.fullmatch(domain.strip()))


# --------------------------------------------------------------------
# IP Address Validation
# --------------------------------------------------------------------

def validate_ip(ip: str) -> bool:
    """
    Validate IPv4 or IPv6 address.
    """

    try:
        ipaddress.ip_address(ip.strip())
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------
# URL Validation
# --------------------------------------------------------------------

def validate_url(url: str) -> bool:
    """
    Validate HTTP/HTTPS URL.
    """

    try:
        parsed = urlparse(url.strip())

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False


# --------------------------------------------------------------------
# Port Validation
# --------------------------------------------------------------------

def validate_port(port: int) -> bool:
    """
    Validate TCP/UDP port number.
    """

    return 1 <= port <= 65535


# --------------------------------------------------------------------
# File Validation
# --------------------------------------------------------------------

def validate_file(path: str) -> bool:
    """
    Check whether a file exists.
    """

    return Path(path).is_file()


# --------------------------------------------------------------------
# Directory Validation
# --------------------------------------------------------------------

def validate_directory(path: str) -> bool:
    """
    Check whether a directory exists.
    """

    return Path(path).is_dir()


# --------------------------------------------------------------------
# Self Test
# --------------------------------------------------------------------

if __name__ == "__main__":

    print("Domain Validation")
    print("-----------------")
    print(validate_domain("google.com"))
    print(validate_domain("sub.example.com"))
    print(validate_domain("bad_domain"))

    print("\nIP Validation")
    print("-------------")
    print(validate_ip("8.8.8.8"))
    print(validate_ip("2001:4860:4860::8888"))
    print(validate_ip("999.999.999.999"))

    print("\nURL Validation")
    print("--------------")
    print(validate_url("https://google.com"))
    print(validate_url("http://example.org"))
    print(validate_url("invalid-url"))

    print("\nPort Validation")
    print("---------------")
    print(validate_port(80))
    print(validate_port(65535))
    print(validate_port(70000))

    print("\nFile Validation")
    print("---------------")
    print(validate_file("README.md"))

    print("\nDirectory Validation")
    print("--------------------")
    print(validate_directory("."))