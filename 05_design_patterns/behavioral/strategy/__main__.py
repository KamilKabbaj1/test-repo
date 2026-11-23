"""Demo: `python -m behavioral.strategy` (run from 05_design_patterns/)."""

import tempfile
from pathlib import Path

from . import (
    CSVFormatStrategy,
    HTMLFormatStrategy,
    JSONFormatStrategy,
    PDFFormatStrategy,
    ReportGenerator,
)

data = [
    {"name": "Sales Q1", "value": 15000},
    {"name": "Sales Q2", "value": 18000},
    {"name": "Sales Q3", "value": 22000},
    {"name": "Sales Q4", "value": 25000},
]

generator = ReportGenerator(data)

print("=== PDF FORMAT ===")
generator.set_strategy(PDFFormatStrategy())
print(generator.generate_report())
print("\n" + "=" * 60 + "\n")

# Switch to CSV format dynamically
print("=== CSV FORMAT ===")
generator.set_strategy(CSVFormatStrategy())
print(generator.generate_report())
print("\n" + "=" * 60 + "\n")

print("=== JSON FORMAT ===")
generator.set_strategy(JSONFormatStrategy())
print(generator.generate_report())
print("\n" + "=" * 60 + "\n")

# NEW: HTML format added without modifying existing code
print("=== HTML FORMAT (NEW!) ===")
generator.set_strategy(HTMLFormatStrategy())
print(generator.generate_report())
print("\n" + "=" * 60 + "\n")

# Save a report (in a temporary folder, so the demo leaves no file in the repo)
generator.set_strategy(CSVFormatStrategy())
with tempfile.TemporaryDirectory() as folder:
    path = generator.save_report(Path(folder) / "sales_report")
    print(f"Saved {path.name}: {path.read_text(encoding='utf-8').splitlines()[0]} ...")
