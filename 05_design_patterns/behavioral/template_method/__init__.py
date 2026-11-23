"""Template Method pattern exercise: data ETL pipelines (one class per file)."""

from .api_pipeline import APIPipeline
from .csv_pipeline import CSVPipeline
from .data_pipeline import DataPipeline
from .database_pipeline import DatabasePipeline
from .xml_pipeline import XMLPipeline

__all__ = ["APIPipeline", "CSVPipeline", "DataPipeline", "DatabasePipeline", "XMLPipeline"]
