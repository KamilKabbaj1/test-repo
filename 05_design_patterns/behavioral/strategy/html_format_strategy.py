"""The "final test" of the statement: a new format added WITHOUT modifying
any existing strategy or the ReportGenerator. Just this new file."""

import html

from .format_strategy import FormatStrategy


class HTMLFormatStrategy(FormatStrategy):
    @property
    def extension(self) -> str:
        return ".html"

    def format(self, data: list[dict]) -> str:
        # html.escape: a value containing "<" or "&" must not break the page
        # (or inject markup).
        rows = "\n".join(
            f"    <tr><td>{html.escape(str(item['name']))}</td>"
            f"<td>{html.escape(str(item['value']))}</td></tr>"
            for item in data
        )
        return (
            "<table>\n"
            "    <tr><th>Name</th><th>Value</th></tr>\n"
            f"{rows}\n"
            "</table>"
        )
