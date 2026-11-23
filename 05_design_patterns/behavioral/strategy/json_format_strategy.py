import json

from .format_strategy import FormatStrategy


class JSONFormatStrategy(FormatStrategy):
    @property
    def extension(self) -> str:
        return ".json"

    def format(self, data: list[dict]) -> str:
        return json.dumps(data, indent=2)
