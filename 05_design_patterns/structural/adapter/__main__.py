"""Demo: `python -m structural.adapter` (run from 05_design_patterns/)."""

from . import (
    AnalyticsDashboard,
    LegacyReportAdapter,
    LegacyReportGenerator,
    show_inventory_report,
    show_sales_report,
)

# The adapter wraps the legacy system. The dashboard doesn't know it is talking to it.
report_generator = LegacyReportAdapter(LegacyReportGenerator())
dashboard = AnalyticsDashboard()

json_report = report_generator.generate({"total_sales": 150000, "orders": 1234})
dashboard.display(json_report)

show_sales_report(report_generator, dashboard)
show_inventory_report(report_generator, dashboard)
