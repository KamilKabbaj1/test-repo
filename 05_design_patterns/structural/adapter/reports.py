"""Business functions, now free of any format conversion.

They depend on the ReportGeneratorInterface abstraction, not on the legacy
class (Dependency Inversion): a future native JSON generator could replace the
adapter without changing these functions.
"""

from .analytics_dashboard import AnalyticsDashboard
from .report_generator_interface import ReportGeneratorInterface


def show_sales_report(generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard) -> None:
    report_data = {"total_sales": 150000, "orders": 1234, "avg_order": 121.55}
    dashboard.display(generator.generate(report_data))


def show_inventory_report(generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard) -> None:
    report_data = {"total_items": 5000, "low_stock": 45, "out_of_stock": 12}
    dashboard.display(generator.generate(report_data))
