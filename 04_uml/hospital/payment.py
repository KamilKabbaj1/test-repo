"""Payment and payment methods (Strategy pattern, task 3 / question 3).

`PaymentMethod` is the strategy interface: one abstract method `pay`.
`Payment` *has a* PaymentMethod (composition) instead of having
`CheckPayment`, `CashPayment`... subclasses. WHY: the common logic (amount,
status, date) is written once, and adding a new method (PayPal...) means
adding one class here, without modifying `Payment` (Open/Closed principle).
"""

from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Imported only for type hints: avoids a circular import at runtime.
    from .prescription import Prescription


class PaymentMethod(ABC):
    """Interface kept minimal (slide 87): one method, nothing else."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process the payment and return a receipt text."""


class Cash(PaymentMethod):
    def pay(self, amount: float) -> str:
        return f"{amount:.2f} EUR paid in cash"


class Check(PaymentMethod):
    def __init__(self, check_number: str) -> None:
        self.check_number = check_number

    def pay(self, amount: float) -> str:
        return f"{amount:.2f} EUR paid by check n°{self.check_number}"


class CreditCard(PaymentMethod):
    def __init__(self, card_number: str) -> None:
        if not card_number.isdigit() or len(card_number) < 4:
            raise ValueError("invalid card number")
        # Data integrity / security (question 4): never keep the full number,
        # only the last 4 digits needed for the receipt.
        self._last_digits = card_number[-4:]

    def pay(self, amount: float) -> str:
        return f"{amount:.2f} EUR paid by credit card ****{self._last_digits}"


class PaymentStatus(Enum):
    RECEIVED = "received"    # the patient paid the platform
    FORWARDED = "forwarded"  # the organizer sent the money to the doctor


class Payment:
    _ids = itertools.count(1)  # shared by all payments: unique, increasing IDs

    def __init__(self, prescription: Prescription, method: PaymentMethod) -> None:
        self.id = f"PAY-{next(self._ids):03d}"
        self.prescription = prescription
        self.method = method
        # The amount is taken from the prescription, never given by the
        # caller: a patient cannot pay a different amount (question 4).
        self._amount = prescription.fee
        self._status = PaymentStatus.RECEIVED
        self.paid_at = datetime.now()
        # Polymorphism: we don't know (and don't care) which method it is.
        self.receipt = method.pay(self._amount)

    # Read-only properties: nobody can write `payment.amount = 0` from outside.
    @property
    def amount(self) -> float:
        return self._amount

    @property
    def status(self) -> PaymentStatus:
        return self._status

    def mark_forwarded(self) -> None:
        # The status can only move forward: forwarding twice would pay the
        # doctor twice.
        if self._status is PaymentStatus.FORWARDED:
            raise ValueError(f"payment {self.id} was already forwarded")
        self._status = PaymentStatus.FORWARDED
