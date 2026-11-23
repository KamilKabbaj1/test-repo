"""Abstract ETL pipeline: the workflow is written ONCE, in the template method run()."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final


class DataPipeline(ABC):
    def __init__(self, source: str, verbose: bool = True) -> None:
        self.source = source
        self.verbose = verbose
        self.data: list[dict] | None = None
        self.logs: list[str] = []
        # Simulated destination (the old code only printed "Loaded ..."):
        # it keeps the loaded records, so they can be checked.
        self.destination: list[dict] = []

    # ------------------------------------------------------------ template method
    # @final tells type checkers (mypy) that subclasses must NOT override run():
    # the order of the steps is guaranteed for every pipeline. Python itself does not
    # enforce it at runtime, so it is a documented contract.
    @final
    def run(self) -> str:
        try:
            self.connect()
            self.log(f"Extracting data from {self.name}...")
            self.data = self.extract()
            self.log(f"Extracted {len(self.data)} records")
            self.data = self.transform(self.data)
            self.validate(self.data)
            self.load(self.data)
        except Exception as error:
            self.on_error(error)
            raise  # the error is reported, never hidden
        finally:
            # finally: the cleanup ALWAYS runs, even if a step failed. In the old
            # code, a validation error skipped the cleanup.
            self.cleanup()
        return f"{self.name} Pipeline finished"

    # ------------------------------------------------------------ steps each pipeline MUST define
    @property
    @abstractmethod
    def name(self) -> str:
        """Short name used in messages: "CSV", "API"..."""

    @property
    @abstractmethod
    def required_fields(self) -> tuple[str, ...]:
        """Fields every record must contain to pass validation."""

    @abstractmethod
    def extract(self) -> list[dict]:
        """Read the raw records from the source."""

    @abstractmethod
    def transform_record(self, record: dict) -> dict:
        """Clean / enrich ONE record (the only part that really differs)."""

    # ------------------------------------------------------------ common steps, written once
    def transform(self, records: list[dict]) -> list[dict]:
        self.log(f"Transforming {self.name} data...")
        # The loop was copied in the 3 old classes: only the body of the loop
        # differs, so subclasses provide just transform_record.
        transformed = [self.transform_record(record) for record in records]
        self.log("Transformation complete")
        return transformed

    def validate(self, records: list[dict]) -> None:
        self.log("Validating data...")
        for record in records:
            missing = [field for field in self.required_fields if field not in record]
            if missing:
                raise ValueError(f"Invalid record structure, missing {missing}: {record}")
        self.log("Validation passed")

    def load(self, records: list[dict]) -> None:
        self.log("Loading data to destination...")
        self.destination.extend(records)
        self.log(f"Loaded {len(records)} records successfully")

    def cleanup(self) -> None:
        self.log("Cleaning up resources...")
        self.data = None
        self.log("Cleanup complete")

    def log(self, message: str) -> None:
        # One single place for logging (problem 3): to add timestamps or write
        # to a file for ALL pipelines, only this method changes.
        self.logs.append(message)
        if self.verbose:
            print(message)

    # ------------------------------------------------------------ hooks (optional overrides)
    def connect(self) -> None:
        """Hook: a default behaviour that a subclass MAY override."""
        self.log(f"Connecting to {self.name} source: {self.source}")
        self.log(f"{self.name} connection established")

    def on_error(self, error: Exception) -> None:
        """Hook called when a step fails, before the cleanup. Default: just log it."""
        self.log(f"ERROR: {error}")
