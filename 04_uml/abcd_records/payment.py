"""Payment methods (rule 5): Cash, Check, Bank Draft.

Same design as the hospital exercise (Strategy): `Payment` *has a*
`PaymentMethod`. A new method is one new class, and `Payment` and the clerks
stay unchanged (Open/Closed principle).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process the payment and return a receipt text."""


class Cash(PaymentMethod):
    def pay(self, amount: float) -> str:
        return f"{amount:.2f} EUR received in cash"


class Check(PaymentMethod):
    def __init__(self, check_number: str) -> None:
        self.check_number = check_number

    def pay(self, amount: float) -> str:
        return f"{amount:.2f} EUR received by check n°{self.check_number}"


class BankDraft(PaymentMethod):
    def __init__(self, draft_number: str) -> None:
        self.draft_number = draft_number

    def pay(self, amount: float) -> str:
        return f"{amount:.2f} EUR received by bank draft n°{self.draft_number}"


class Payment:
    def __init__(self, order: Order, method: PaymentMethod) -> None:
        self.order = order
        self.method = method
        # The amount comes from the order (discount included), never from the
        # caller: nobody can pay less than the invoice.
        self.amount = order.total
        self.paid_at = datetime.now()
        self.receipt = method.pay(self.amount)
