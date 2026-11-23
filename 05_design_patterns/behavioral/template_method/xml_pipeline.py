"""The validation test of the statement: a NEW pipeline, with XML-specific
extraction and transformation, written without touching the base class."""

import xml.etree.ElementTree as ET

from .data_pipeline import DataPipeline


class XMLPipeline(DataPipeline):
    name = "XML"
    required_fields = ("order_id", "customer")

    # Simulated file content (like the other pipelines, no real file is read).
    SAMPLE_XML = """
    <orders>
        <order id="1" customer="eve" amount="99.50"/>
        <order id="2" customer="frank" amount="15"/>
    </orders>
    """

    def extract(self) -> list[dict]:
        root = ET.fromstring(self.SAMPLE_XML)
        # XML attributes are always strings: the transform step converts them.
        return [
            {"order_id": order.get("id"), "customer": order.get("customer"), "amount": order.get("amount")}
            for order in root.iter("order")
        ]

    def transform_record(self, record: dict) -> dict:
        return {
            **record,
            "order_id": int(record["order_id"]),
            "customer": record["customer"].title(),
            "amount": float(record["amount"]),
        }
