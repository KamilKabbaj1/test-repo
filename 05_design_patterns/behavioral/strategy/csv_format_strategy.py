import csv
import io

from .format_strategy import FormatStrategy


class CSVFormatStrategy(FormatStrategy):
    @property
    def extension(self) -> str:
        return ".csv"

    def format(self, data: list[dict]) -> str:
        # The csv module instead of f"{name},{value}": a name that contains a
        # comma ("Sales, Q1") is quoted correctly instead of breaking the columns.
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["name", "value"])
        for item in data:
            writer.writerow([item["name"], item["value"]])
        return buffer.getvalue()
