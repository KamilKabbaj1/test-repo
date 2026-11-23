"""Tests for the Adapter pattern exercise."""

import json

from structural.adapter import (
    AnalyticsDashboard,
    LegacyReportAdapter,
    LegacyReportGenerator,
    ReportGeneratorInterface,
    show_sales_report,
)


def test_adapter_implements_the_expected_interface():
    assert isinstance(LegacyReportAdapter(LegacyReportGenerator()), ReportGeneratorInterface)


def test_adapter_converts_legacy_xml_to_json():
    adapter = LegacyReportAdapter(LegacyReportGenerator())
    result = json.loads(adapter.generate({"total_sales": 150000, "avg_order": 121.55, "region": "EU"}))
    # Types are restored: int, float, str.
    assert result == {"total_sales": 150000, "avg_order": 121.55, "region": "EU"}


def test_adapter_really_uses_the_legacy_output():
    # A fake legacy generator proves the adapter parses the XML it receives
    # instead of re-dumping the original data.
    class FakeLegacy:
        def generate_report(self, data):
            return "<report>\n  <source>legacy</source>\n</report>"

    assert json.loads(LegacyReportAdapter(FakeLegacy()).generate({"ignored": 1})) == {"source": "legacy"}


def test_dashboard_displays_adapted_report(capsys):
    # capsys captures what is printed, so the output can be checked.
    show_sales_report(LegacyReportAdapter(LegacyReportGenerator()), AnalyticsDashboard())
    output = capsys.readouterr().out
    assert "=== Analytics Dashboard ===" in output
    assert "total_sales: 150000" in output
    assert "avg_order: 121.55" in output
