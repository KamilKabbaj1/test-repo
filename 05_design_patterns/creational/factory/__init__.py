"""Factory pattern exercise: refactor the payment system.

One class per file (slide 87: "Factory with 5 products = 5+ files"): adding
or changing a payment method touches only its own file.
"""

from .bank_transfer_processor import BankTransferProcessor
from .credit_card_processor import CreditCardProcessor
from .payment_factory import PaymentFactory
from .payment_processor import PaymentProcessor
from .paypal_processor import PayPalProcessor

__all__ = [
    "BankTransferProcessor",
    "CreditCardProcessor",
    "PayPalProcessor",
    "PaymentFactory",
    "PaymentProcessor",
]
