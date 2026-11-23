"""Strategy interface: what every report format must provide."""

from abc import ABC, abstractmethod


class FormatStrategy(ABC):
    @property
    @abstractmethod
    def extension(self) -> str:
        """File extension, e.g. ".csv".

        Each format knows its own extension, which removes the second if/elif
        chain of the old save_report().
        """

    @abstractmethod
    def format(self, data: list[dict]) -> str:
        """Turn the records into the report text."""
