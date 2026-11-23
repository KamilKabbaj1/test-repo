"""Context class: generates and saves a report with the current strategy."""

from __future__ import annotations

from pathlib import Path

from .format_strategy import FormatStrategy


class ReportGenerator:
    def __init__(self, data: list[dict], strategy: FormatStrategy | None = None) -> None:
        self.data = data
        # Composition: the generator HAS A strategy and delegates the
        # formatting to it. It does not know any concrete format.
        self._strategy = strategy

    def set_strategy(self, strategy: FormatStrategy) -> None:
        """Change the format at runtime (problem 4 of the statement)."""
        self._strategy = strategy

    def generate_report(self) -> str:
        return self._require_strategy().format(self.data)

    def save_report(self, filename: str | Path) -> Path:
        """Write the report to `filename` + the extension of the current format."""
        strategy = self._require_strategy()
        path = Path(f"{filename}{strategy.extension}")
        path.write_text(strategy.format(self.data), encoding="utf-8")
        return path

    def _require_strategy(self) -> FormatStrategy:
        # Raise instead of returning "Unknown format" like the old code: an
        # error string could end up in a saved file without anyone noticing.
        if self._strategy is None:
            raise RuntimeError("no format strategy set: call set_strategy() first")
        return self._strategy
