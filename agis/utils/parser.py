"""
AgisRecon2 - Output Parser

This module provides helper functions to parse raw output from
external reconnaissance tools into structured Python objects.

Supported parsing:
- Lines
- JSON
- Key-Value pairs
- CSV
"""

from __future__ import annotations

import csv
import json
from io import StringIO
from typing import Any, Dict, List


def parse_lines(output: str, remove_empty: bool = True) -> List[str]:
    """
    Parse output into a list of lines.

    Args:
        output: Raw command output.
        remove_empty: Remove blank lines if True.

    Returns:
        List of cleaned lines.
    """

    lines = [line.strip() for line in output.splitlines()]

    if remove_empty:
        lines = [line for line in lines if line]

    return lines


def parse_json(output: str) -> Dict[str, Any]:
    """
    Parse JSON output.

    Args:
        output: JSON string.

    Returns:
        Parsed dictionary.

    Raises:
        ValueError: If JSON is invalid.
    """

    return json.loads(output)


def parse_csv(output: str) -> List[Dict[str, str]]:
    """
    Parse CSV formatted output.

    Args:
        output: CSV string.

    Returns:
        List of dictionaries.
    """

    reader = csv.DictReader(StringIO(output))
    return list(reader)


def parse_key_value(
    output: str,
    separator: str = ":"
) -> Dict[str, str]:
    """
    Parse key-value formatted text.

    Example:
        Name: John
        Age: 20

    Returns:
        Dictionary.
    """

    result: Dict[str, str] = {}

    for line in output.splitlines():
        if separator in line:
            key, value = line.split(separator, 1)
            result[key.strip()] = value.strip()

    return result


def unique_lines(lines: List[str]) -> List[str]:
    """
    Remove duplicate lines while preserving order.
    """

    seen = set()
    result = []

    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)

    return result


if __name__ == "__main__":

    sample = """
google.com
github.com

google.com
openai.com
"""

    print("Original:")
    print(sample)

    parsed = parse_lines(sample)

    print("\nParsed Lines:")
    print(parsed)

    print("\nUnique Lines:")
    print(unique_lines(parsed))

    json_sample = '{"tool":"AgisRecon2","version":1}'

    print("\nJSON:")
    print(parse_json(json_sample))

    kv_sample = """
Name: AgisRecon2
Version: 1.0
Author: Sagar
"""

    print("\nKey-Value:")
    print(parse_key_value(kv_sample))