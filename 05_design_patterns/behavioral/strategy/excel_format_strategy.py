from .format_strategy import FormatStrategy


class ExcelFormatStrategy(FormatStrategy):
    # Simulated Excel (tab-separated text), as in the statement.
    @property
    def extension(self) -> str:
        return ".xlsx"

    def format(self, data: list[dict]) -> str:
        report = "EXCEL REPORT\n"
        report += "-" * 50 + "\n"
        report += "Name\tValue\n"
        for item in data:
            report += f"{item['name']}\t{item['value']}\n"
        report += "-" * 50 + "\n"
        return report
