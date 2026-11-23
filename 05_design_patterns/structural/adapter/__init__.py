"""Adapter pattern exercise: legacy XML reports for a JSON dashboard."""

from .analytics_dashboard import AnalyticsDashboard
from .legacy_report_adapter import LegacyReportAdapter
from .legacy_report_generator import LegacyReportGenerator
from .report_generator_interface import ReportGeneratorInterface
from .reports import show_inventory_report, show_sales_report

__all__ = [
    "AnalyticsDashboard",
    "LegacyReportAdapter",
    "LegacyReportGenerator",
    "ReportGeneratorInterface",
    "show_inventory_report",
    "show_sales_report",
]
