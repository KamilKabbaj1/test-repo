"""Adapter: makes the legacy XML generator look like a JSON ReportGeneratorInterface."""

import json
import xml.etree.ElementTree as ET

from .legacy_report_generator import LegacyReportGenerator
from .report_generator_interface import ReportGeneratorInterface


class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy: LegacyReportGenerator) -> None:
        # Composition: the adapter HAS A legacy generator (it wraps it) rather
        # than inheriting from it. The legacy API (generate_report, XML) stays
        # hidden, and any object with a compatible generate_report() can be given
        # (a fake one in tests, for example).
        self._legacy = legacy

    def generate(self, data: dict) -> str:
        xml_report = self._legacy.generate_report(data)
        # The conversion is written ONCE here, instead of in every report function.
        # It really parses the XML output: the old code "cheated" by dumping
        # the original data again.
        root = ET.fromstring(xml_report)
        converted = {child.tag: self._parse_value(child.text or "") for child in root}
        return json.dumps(converted)

    @staticmethod
    def _parse_value(text: str) -> int | float | str:
        # XML only stores text: "150000" must become the number 150000 again,
        # otherwise the dashboard would receive strings.
        for convert in (int, float):
            try:
                return convert(text)
            except ValueError:
                pass
        return text
