"""Legacy reporting system: an external library that we CANNOT modify.

Copied unchanged from the statement. The adapter wraps it instead of editing it.
"""


class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        """Returns XML format - old system"""
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml
