"""Prescription written by a doctor for one health problem."""

from __future__ import annotations

import itertools
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .health_problem import HealthProblem
    from .payment import Payment
    from .users import Doctor


class Prescription:
    _ids = itertools.count(1)

    def __init__(self, problem: HealthProblem, doctor: Doctor, content: str, fee: float) -> None:
        if fee < 0:
            raise ValueError("fee must be non-negative")
        self.id = f"RX-{next(self._ids):03d}"
        self.problem = problem
        self.doctor = doctor
        self.content = content
        self.fee = fee
        self.issued_at = datetime.now()  # timestamp asked in task 3
        # 0..1 payment: None until the patient pays.
        self.payment: Payment | None = None

    @property
    def is_paid(self) -> bool:
        return self.payment is not None

    def __repr__(self) -> str:
        return f"Prescription({self.id}, fee={self.fee})"
