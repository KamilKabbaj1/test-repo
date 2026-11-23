from .data_pipeline import DataPipeline


class DatabasePipeline(DataPipeline):
    name = "Database"
    required_fields = ("product_id", "price")
    TAX_RATE = 0.2

    def extract(self) -> list[dict]:
        return [
            {"product_id": 501, "product_name": "laptop", "price": 1200},
            {"product_id": 502, "product_name": "mouse", "price": 25},
        ]

    def transform_record(self, record: dict) -> dict:
        price = float(record["price"])
        return {
            **record,
            "price": price,
            "product_name": record["product_name"].title(),
            "tax": price * self.TAX_RATE,
        }
