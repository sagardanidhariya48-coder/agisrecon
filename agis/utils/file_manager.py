"""
AgisRecon2 - File Manager Utility

Provides reusable file and directory management functions
for the entire project.

Features
--------
- Create directories
- Read text files
- Write text files
- Append text files
- Read JSON files
- Write JSON files
- Delete files
- Check file existence

Example
-------
from utils.file_manager import write_text

write_text("output.txt", "Hello World")
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


# --------------------------------------------------------------------
# Directory Operations
# --------------------------------------------------------------------

def ensure_directory(path: str | Path) -> Path:
    """
    Create a directory if it does not exist.

    Returns:
        Path object.
    """

    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


# --------------------------------------------------------------------
# File Operations
# --------------------------------------------------------------------

def write_text(path: str | Path, content: str) -> None:
    """
    Write text to a file.
    """

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        content,
        encoding="utf-8",
    )


def append_text(path: str | Path, content: str) -> None:
    """
    Append text to a file.
    """

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as file:
        file.write(content)


def read_text(path: str | Path) -> str:
    """
    Read text from a file.
    """

    return Path(path).read_text(
        encoding="utf-8"
    )


# --------------------------------------------------------------------
# JSON Operations
# --------------------------------------------------------------------

def write_json(
    path: str | Path,
    data: Dict[str, Any],
    indent: int = 4,
) -> None:
    """
    Write dictionary to JSON file.
    """

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=indent,
            ensure_ascii=False,
        )


def read_json(path: str | Path) -> Dict[str, Any]:
    """
    Read JSON file.
    """

    with Path(path).open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# --------------------------------------------------------------------
# Delete
# --------------------------------------------------------------------

def delete_file(path: str | Path) -> bool:
    """
    Delete a file.

    Returns:
        True if deleted.
    """

    path = Path(path)

    if path.exists():
        path.unlink()
        return True

    return False


# --------------------------------------------------------------------
# Exists
# --------------------------------------------------------------------

def file_exists(path: str | Path) -> bool:
    """
    Check whether file exists.
    """

    return Path(path).is_file()


def directory_exists(path: str | Path) -> bool:
    """
    Check whether directory exists.
    """

    return Path(path).is_dir()


# --------------------------------------------------------------------
# Self Test
# --------------------------------------------------------------------

if __name__ == "__main__":

    print("Creating directory...")
    ensure_directory("output")

    print("Writing text...")
    write_text(
        "output/test.txt",
        "Hello AgisRecon2\n"
    )

    print("Appending text...")
    append_text(
        "output/test.txt",
        "Second Line\n"
    )

    print("\nReading text:")
    print(read_text("output/test.txt"))

    sample = {
        "tool": "AgisRecon2",
        "version": "1.0"
    }

    write_json(
        "output/sample.json",
        sample
    )

    print("\nReading JSON:")
    print(read_json("output/sample.json"))

    print("\nFile Exists:")
    print(file_exists("output/test.txt"))

    print("\nDirectory Exists:")
    print(directory_exists("output"))

    print("\nDeleting file:")
    print(delete_file("output/test.txt"))