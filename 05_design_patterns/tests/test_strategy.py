"""Tests for the Strategy pattern exercise."""

import json

import pytest

from behavioral.strategy import (
    CSVFormatStrategy,
    ExcelFormatStrategy,
    FormatStrategy,
    HTMLFormatStrategy,
    JSONFormatStrategy,
    PDFFormatStrategy,
    ReportGenerator,
)

DATA = [{"name": "Sales Q1", "value": 15000}, {"name": "Sales Q2", "value": 18000}]


# Each format is tested on its own: this is "easy to test each format independently".
def test_pdf_format():
    report = PDFFormatStrategy().format(DATA)
    assert report.splitlines() == [
        "PDF REPORT",
        "=" * 50,
        "| Sales Q1             |      15000 |",
        "| Sales Q2             |      18000 |",
        "=" * 50,
        "End of PDF Report",
    ]


def test_excel_format():
    assert ExcelFormatStrategy().format(DATA) == (
        "EXCEL REPORT\n" + "-" * 50 + "\nName\tValue\nSales Q1\t15000\nSales Q2\t18000\n" + "-" * 50 + "\n"
    )


def test_csv_format():
    assert CSVFormatStrategy().format(DATA) == "name,value\nSales Q1,15000\nSales Q2,18000\n"


def test_csv_quotes_values_with_commas():
    assert CSVFormatStrategy().format([{"name": "Sales, Q1", "value": 1}]) == 'name,value\n"Sales, Q1",1\n'


def test_json_format():
    assert json.loads(JSONFormatStrategy().format(DATA)) == DATA


def test_html_format_escapes_values():
    report = HTMLFormatStrategy().format([{"name": "<b>R&D</b>", "value": 1}])
    assert "<td>&lt;b&gt;R&amp;D&lt;/b&gt;</td>" in report
    assert report.startswith("<table>") and report.endswith("</table>")


def test_switching_strategy_at_runtime():
    generator = ReportGenerator(DATA, PDFFormatStrategy())
    assert generator.generate_report().startswith("PDF REPORT")
    generator.set_strategy(CSVFormatStrategy())
    assert generator.generate_report().startswith("name,value")


def test_no_strategy_raises():
    with pytest.raises(RuntimeError):
        ReportGenerator(DATA).generate_report()


@pytest.mark.parametrize(
    ("strategy", "extension"),
    [
        (PDFFormatStrategy(), ".pdf"),
        (ExcelFormatStrategy(), ".xlsx"),
        (CSVFormatStrategy(), ".csv"),
        (JSONFormatStrategy(), ".json"),
        (HTMLFormatStrategy(), ".html"),
    ],
)
def test_save_report_uses_strategy_extension(tmp_path, strategy, extension):
    path = ReportGenerator(DATA, strategy).save_report(tmp_path / "sales_report")
    assert path.name == f"sales_report{extension}"
    assert path.read_text(encoding="utf-8") == strategy.format(DATA)


def test_new_format_works_with_unchanged_generator():
    class MarkdownFormatStrategy(FormatStrategy):
        extension = ".md"

        def format(self, data):
            return "\n".join(f"- {item['name']}: {item['value']}" for item in data)

    generator = ReportGenerator(DATA, MarkdownFormatStrategy())
    assert generator.generate_report() == "- Sales Q1: 15000\n- Sales Q2: 18000"
