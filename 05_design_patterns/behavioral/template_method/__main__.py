"""Demo: `python -m behavioral.template_method` (run from 05_design_patterns/)."""

from . import APIPipeline, CSVPipeline, DatabasePipeline, XMLPipeline

pipelines = [
    CSVPipeline("data/users.csv"),
    APIPipeline("https://api.example.com/users"),
    DatabasePipeline("postgresql://localhost/mydb"),
    XMLPipeline("data/orders.xml"),  # NEW!
]

for pipeline in pipelines:
    print(f"RUNNING {pipeline.name.upper()} PIPELINE")
    print("=" * 70)
    result = pipeline.run()
    print(f"\n{result}\n")
