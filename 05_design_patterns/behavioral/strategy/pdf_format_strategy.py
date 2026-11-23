from .format_strategy import FormatStrategy


class PDFFormatStrategy(FormatStrategy):
    # Simulated PDF, as in the statement: a text table (a real PDF would use a library).
    @property
    def extension(self) -> str:
        return ".pdf"

    def format(self, data: list[dict]) -> str:
        report = "PDF REPORT\n"
        report += "=" * 50 + "\n"
        for item in data:
            report += f"| {item['name']:20} | {item['value']:10} |\n"
        report += "=" * 50 + "\n"
        report += "End of PDF Report"
        return report
