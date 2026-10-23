"""
AgisRecon2 Output Package

Handles formatting and generation of reconnaissance results.

Available modules:
    terminal.py  - Terminal output
    json.py      - JSON output
    markdown.py  - Markdown output
    txt.py       - Plain text output
    html.py      - HTML output
    report.py    - Report generation
"""

from .terminal import *
from .json import *
from .markdown import *
from .txt import *
from .html import *
from .report import *

__all__ = [
    "terminal",
    "json",
    "markdown",
    "txt",
    "html",
    "report",
]