"""Tests for the Template Method pattern exercise."""

import pytest

from behavioral.template_method import (
    APIPipeline,
    CSVPipeline,
    DatabasePipeline,
    DataPipeline,
    XMLPipeline,
)


@pytest.mark.parametrize(
    ("pipeline_class", "expected_result"),
    [
        (CSVPipeline, "CSV Pipeline finished"),
        (APIPipeline, "API Pipeline finished"),
        (DatabasePipeline, "Database Pipeline finished"),
        (XMLPipeline, "XML Pipeline finished"),
    ],
)
def test_every_pipeline_follows_the_same_workflow(pipeline_class, expected_result):
    pipeline = pipeline_class("source", verbose=False)
    assert pipeline.run() == expected_result
    # The steps always happen in the same order.
    steps = ["Connecting", "Extracting", "Transforming", "Validating", "Loading", "Cleaning up"]
    positions = [next(i for i, line in enumerate(pipeline.logs) if line.startswith(step)) for step in steps]
    assert positions == sorted(positions)
    assert pipeline.data is None  # cleaned up


def test_csv_transformation():
    pipeline = CSVPipeline("data/users.csv", verbose=False)
    pipeline.run()
    assert pipeline.destination == [
        {"id": 1, "name": "ALICE", "age": 30},
        {"id": 2, "name": "BOB", "age": 25},
    ]


def test_api_transformation_adds_grade():
    pipeline = APIPipeline("url", verbose=False)
    pipeline.run()
    assert [(r["username"], r["score"], r["grade"]) for r in pipeline.destination] == [
        ("charlie", 85, "B"),
        ("diana", 92, "A"),
    ]


def test_database_transformation_adds_tax():
    pipeline = DatabasePipeline("db", verbose=False)
    pipeline.run()
    laptop = pipeline.destination[0]
    assert (laptop["product_name"], laptop["price"], laptop["tax"]) == ("Laptop", 1200.0, pytest.approx(240.0))


def test_xml_pipeline_parses_and_converts():
    pipeline = XMLPipeline("data/orders.xml", verbose=False)
    pipeline.run()
    assert pipeline.destination == [
        {"order_id": 1, "customer": "Eve", "amount": 99.5},
        {"order_id": 2, "customer": "Frank", "amount": 15.0},
    ]


class BrokenPipeline(DataPipeline):
    """Produces a record without the required field, and overrides both hooks."""

    name = "Broken"
    required_fields = ("id",)

    def extract(self):
        return [{"no_id": 1}]

    def transform_record(self, record):
        return record

    def connect(self):
        self.log("Connecting with a custom hook")

    def on_error(self, error):
        self.log(f"custom error handler: {type(error).__name__}")


def test_validation_error_still_runs_cleanup_and_hooks():
    pipeline = BrokenPipeline("x", verbose=False)
    with pytest.raises(ValueError, match="missing"):
        pipeline.run()
    assert pipeline.logs[0] == "Connecting with a custom hook"
    assert "custom error handler: ValueError" in pipeline.logs
    assert pipeline.logs[-1] == "Cleanup complete"
    assert pipeline.destination == []  # nothing loaded


def test_incomplete_pipeline_cannot_be_created():
    class Incomplete(DataPipeline):
        name = "Incomplete"
        required_fields = ()

        def extract(self):
            return []

    with pytest.raises(TypeError):
        Incomplete("x")


def test_verbose_prints_logs(capsys):
    CSVPipeline("data/users.csv").run()
    assert "Validation passed" in capsys.readouterr().out
