from .data_pipeline import DataPipeline


class CSVPipeline(DataPipeline):
    name = "CSV"  # a class attribute is enough to implement an abstract property
    required_fields = ("id", "name")

    def extract(self) -> list[dict]:
        # Simulated data, as in the statement (no real file is read).
        return [
            {"id": 1, "name": "Alice", "age": "30"},
            {"id": 2, "name": "Bob", "age": "25"},
        ]

    def transform_record(self, record: dict) -> dict:
        # Build a new dict instead of modifying the input record in place.
        return {**record, "age": int(record["age"]), "name": record["name"].upper()}
