"""The interface the NEW code expects (the "target" of the adapter)."""

from abc import ABC, abstractmethod


class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        """Return the report as a JSON string."""
