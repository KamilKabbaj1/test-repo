"""Users of the platform: abstract User + Patient, Doctor, Organizer (task 3)."""

from __future__ import annotations

import itertools
from abc import ABC, abstractmethod

from .health_problem import HealthProblem
from .payment import Payment, PaymentMethod
from .prescription import Prescription


class User(ABC):
    """What every actor shares: id, name, password, login/logout.

    Abstract (ABC): a "generic user" does not exist on the platform, and
    putting the shared code here avoids writing it three times (DRY).
    """

    def __init__(self, user_id: str, name: str, password: str) -> None:
        self.id = user_id
        self.name = name
        # Private: never readable from outside. A real system would store a
        # hash (bcrypt...), never the clear password.
        self._password = password
        self._logged_in = False

    @property
    def logged_in(self) -> bool:
        return self._logged_in

    def login(self, password: str) -> bool:
        self._logged_in = password == self._password
        return self._logged_in

    def logout(self) -> None:
        self._logged_in = False

    @property
    @abstractmethod
    def role(self) -> str:
        """Each concrete user must say what it is: forces subclasses to exist."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.id!r}, {self.name!r})"


class Patient(User):
    def __init__(self, user_id: str, name: str, password: str, email: str) -> None:
        super().__init__(user_id, name, password)
        self.email = email
        self.problems: list[HealthProblem] = []
        self._prescriptions: list[Prescription] = []  # history (task 3)

    @property
    def role(self) -> str:
        return "patient"

    @property
    def prescription_history(self) -> list[Prescription]:
        # Return a copy: the caller can read the history but not modify it.
        return list(self._prescriptions)

    def submit_problem(self, description: str) -> HealthProblem:
        problem = HealthProblem(self, description)
        self.problems.append(problem)
        return problem

    def receive_prescription(self, prescription: Prescription) -> None:
        self._prescriptions.append(prescription)

    def pay(self, prescription: Prescription, method: PaymentMethod) -> Payment:
        # Integrity checks BEFORE creating anything (question 4): if a check
        # fails, nothing has been modified.
        if prescription not in self._prescriptions:
            raise ValueError("this prescription was not delivered to this patient")
        if prescription.is_paid:
            raise ValueError(f"prescription {prescription.id} is already paid")
        payment = Payment(prescription, method)
        prescription.payment = payment
        return payment


class Doctor(User):
    def __init__(self, user_id: str, name: str, password: str, speciality: str) -> None:
        super().__init__(user_id, name, password)
        self.speciality = speciality
        self.received_payments: list[Payment] = []

    @property
    def role(self) -> str:
        return "doctor"

    @property
    def earnings(self) -> float:
        # Computed from the payments: no separate counter to keep in sync.
        return sum(payment.amount for payment in self.received_payments)

    def prescribe(self, problem: HealthProblem, content: str, fee: float) -> Prescription:
        if problem.doctor is not self:
            raise ValueError(f"problem {problem.id} is not assigned to {self.name}")
        return Prescription(problem, self, content, fee)

    def receive_payment(self, payment: Payment) -> None:
        self.received_payments.append(payment)


class Organizer(User):
    """Intermediary of the workflow, and also administrator (issues member IDs)."""

    # Class attributes: shared by ALL organizers, so two organizers can never
    # issue the same ID.
    _patient_ids = itertools.count(1)
    _doctor_ids = itertools.count(1)

    @property
    def role(self) -> str:
        return "organizer"

    # --- administrator tasks ------------------------------------------------
    def register_patient(self, name: str, password: str, email: str) -> Patient:
        return Patient(f"P-{next(self._patient_ids):03d}", name, password, email)

    def register_doctor(self, name: str, password: str, speciality: str) -> Doctor:
        return Doctor(f"D-{next(self._doctor_ids):03d}", name, password, speciality)

    # --- business workflow (steps 2, 4 and 6) ------------------------------
    def assign(self, problem: HealthProblem, doctor: Doctor) -> None:
        """Step 2: read the problem and consult a doctor."""
        problem.start_review(doctor)

    def send_prescription(self, prescription: Prescription) -> None:
        """Step 4: deliver the prescription to the patient."""
        problem = prescription.problem
        problem.resolve(prescription)
        problem.patient.receive_prescription(prescription)

    def forward_payment(self, payment: Payment) -> None:
        """Step 6: send the money to the doctor who wrote the prescription."""
        payment.mark_forwarded()  # raises if already forwarded: no double pay
        payment.prescription.doctor.receive_payment(payment)
