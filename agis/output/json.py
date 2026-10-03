"""
AgisRecon2 - JSON Output

Handles formatting, saving, and loading reconnaissance
results in JSON format.
"""

import json as _json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union


class JSONOutput:
    """Handle AgisRecon2 JSON output."""

    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        """
        Initialize JSON output handler.

        Args:
            output_dir: Directory where JSON results will be stored.
        """

        if output_dir is None:
            output_dir = Path("output") / "json"

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Convert results
    # ---------------------------------------------------------

    @staticmethod
    def format_results(
        results: Any,
        target: Optional[str] = None,
        module: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a standardized JSON-compatible result structure.
        """

        data = {
            "tool": "AgisRecon2",
            "target": target,
            "module": module,
            "timestamp": datetime.now().isoformat(),
            "results": results,
        }

        return data

    # ---------------------------------------------------------
    # Serialize
    # ---------------------------------------------------------

    @staticmethod
    def dumps(
        data: Any,
        indent: int = 4,
    ) -> str:
        """
        Convert Python data to formatted JSON string.
        """

        return _json.dumps(
            data,
            indent=indent,
            ensure_ascii=False,
            default=str,
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save(
        self,
        results: Any,
        filename: Optional[str] = None,
        target: Optional[str] = None,
        module: Optional[str] = None,
    ) -> Path:
        """
        Save reconnaissance results as a JSON file.

        Returns:
            Path to the created JSON file.
        """

        data = self.format_results(
            results=results,
            target=target,
            module=module,
        )

        if filename is None:
            filename = self._generate_filename(
                target=target,
                module=module,
            )

        if not filename.endswith(".json"):
            filename += ".json"

        file_path = self.output_dir / filename

        with file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            _json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
                default=str,
            )

        return file_path

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    @staticmethod
    def load(
        file_path: Union[str, Path],
    ) -> Dict[str, Any]:
        """
        Load reconnaissance results from a JSON file.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"JSON file not found: {file_path}"
            )

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return _json.load(file)

    # ---------------------------------------------------------
    # Generate filename
    # ---------------------------------------------------------

    @staticmethod
    def _generate_filename(
        target: Optional[str] = None,
        module: Optional[str] = None,
    ) -> str:
        """
        Generate a timestamp-based JSON filename.
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        target_name = (
            str(target).replace("://", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            if target
            else "target"
        )

        module_name = (
            str(module).replace(" ", "_")
            if module
            else "scan"
        )

        return (
            f"{target_name}_"
            f"{module_name}_"
            f"{timestamp}.json"
        )

    # ---------------------------------------------------------
    # Check valid JSON
    # ---------------------------------------------------------

    @staticmethod
    def is_valid(
        data: Any,
    ) -> bool:
        """
        Check whether data can be serialized to JSON.
        """

        try:
            _json.dumps(
                data,
                default=str,
            )
            return True

        except (TypeError, ValueError):
            return False


# -------------------------------------------------------------
# Default JSON output instance
# -------------------------------------------------------------

json_output = JSONOutput()


# -------------------------------------------------------------
# Convenience functions
# -------------------------------------------------------------

def save_json(
    results: Any,
    filename: Optional[str] = None,
    target: Optional[str] = None,
    module: Optional[str] = None,
) -> Path:
    """
    Save results as JSON using the default handler.
    """

    return json_output.save(
        results=results,
        filename=filename,
        target=target,
        module=module,
    )


def load_json(
    file_path: Union[str, Path],
) -> Dict[str, Any]:
    """
    Load results from a JSON file.
    """

    return JSONOutput.load(file_path)


def format_json(
    results: Any,
    target: Optional[str] = None,
    module: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create the standardized AgisRecon2 JSON structure.
    """

    return JSONOutput.format_results(
        results=results,
        target=target,
        module=module,
    )