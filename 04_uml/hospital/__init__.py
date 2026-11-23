"""Hospital Management System (UML exercise 1), implementation of the task 3 design.

One module per responsibility: users, health problems, prescriptions, payments.
The package re-exports the public classes so callers can write
`from hospital import Patient, Organizer, ...`.
"""

from .health_problem import HealthProblem, ProblemStatus
from .payment import Cash, Check, CreditCard, Payment, PaymentMethod, PaymentStatus
from .prescription import Prescription
from .users import Doctor, Organizer, Patient, User

__all__ = [
    "Cash",
    "Check",
    "CreditCard",
    "Doctor",
    "HealthProblem",
    "Organizer",
    "Patient",
    "Payment",
    "PaymentMethod",
    "PaymentStatus",
    "Prescription",
    "ProblemStatus",
    "User",
]
