"""The factory: the "middleman" that turns a string into the right processor."""

from .bank_transfer_processor import BankTransferProcessor
from .credit_card_processor import CreditCardProcessor
from .payment_processor import PaymentProcessor
from .paypal_processor import PayPalProcessor


class PaymentFactory:
    # A dictionary maps each name to a CLASS (not an instance). It replaces the
    # long if/elif chain: finding the right processor is a single lookup.
    _DEFAULT_PROCESSORS: dict[str, type[PaymentProcessor]] = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    def __init__(self) -> None:
        # Each factory gets its own copy: registering a method on one factory
        # (e.g. in a test) does not affect the others.
        self._processors = dict(self._DEFAULT_PROCESSORS)

    def register(self, payment_type: str, processor_class: type[PaymentProcessor]) -> None:
        """Add a new payment method WITHOUT modifying this file (Open/Closed).

        The 20 future methods (Apple Pay, crypto...) are each a new class plus one
        `register` call. The existing processors are never touched.
        """
        if not issubclass(processor_class, PaymentProcessor):
            raise TypeError("processor_class must inherit from PaymentProcessor")
        self._processors[payment_type] = processor_class

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        try:
            processor_class = self._processors[payment_type]
        except KeyError:
            # An unknown type is a programming error: raise instead of
            # returning an error dict that someone could forget to check.
            raise ValueError(f"Unknown payment type: {payment_type}") from None
        return processor_class()  # instantiate the chosen class

    @property
    def available_types(self) -> list[str]:
        return sorted(self._processors)
