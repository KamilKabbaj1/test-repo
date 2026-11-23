"""New analytics dashboard (client code): it only understands JSON."""

import json


class AnalyticsDashboard:
    def display(self, json_data: str) -> None:
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")
