"""The interface every payment processor must follow."""

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Abstract Base Class = the "blueprint".

    Every processor "promises" to provide these two methods, so the code that
    uses a processor never needs to know which concrete class it got
    (polymorphism). Python refuses to instantiate a subclass that forgets one
    of them (TypeError), so an incomplete processor can never reach production.
    """

    @abstractmethod
    def validate(self, details: dict) -> bool:
        """Return True if the payment details are valid for this method."""

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        """Process the payment and return the result (same format for every method)."""
