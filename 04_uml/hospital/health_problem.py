"""Health problem posted by a patient, with status tracking (task 3)."""

from __future__ import annotations

import itertools
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .prescription import Prescription
    from .users import Doctor, Patient


class ProblemStatus(Enum):
    # An Enum (not plain strings): a typo such as "pendng" is impossible,
    # and the list of possible values is written in one place.
    PENDING = "pending"
    IN_REVIEW = "in-review"
    RESOLVED = "resolved"


class HealthProblem:
    _ids = itertools.count(1)

    def __init__(self, patient: Patient, description: str) -> None:
        if not description.strip():
            raise ValueError("description must not be empty")
        self.id = f"HP-{next(self._ids):03d}"
        self.patient = patient
        self.description = description
        self.created_at = datetime.now()
        self._status = ProblemStatus.PENDING
        self.doctor: Doctor | None = None              # 0..1 reviewing doctor
        self.prescription: Prescription | None = None  # 0..1 answer

    @property
    def status(self) -> ProblemStatus:
        # Read-only: the status only changes through the two methods below,
        # which check that the transition is allowed.
        return self._status

    def start_review(self, doctor: Doctor) -> None:
        """PENDING -> IN_REVIEW: the organizer gave the problem to a doctor."""
        if self._status is not ProblemStatus.PENDING:
            raise ValueError(f"problem {self.id} is not pending")
        self.doctor = doctor
        self._status = ProblemStatus.IN_REVIEW

    def resolve(self, prescription: Prescription) -> None:
        """IN_REVIEW -> RESOLVED: the prescription was delivered to the patient."""
        if self._status is not ProblemStatus.IN_REVIEW:
            raise ValueError(f"problem {self.id} is not in review")
        self.prescription = prescription
        self._status = ProblemStatus.RESOLVED

    def __repr__(self) -> str:
        return f"HealthProblem({self.id}, {self._status.value})"
