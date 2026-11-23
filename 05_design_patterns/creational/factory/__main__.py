"""Demo: `python -m creational.factory` (run from 05_design_patterns/)."""

from . import PaymentFactory

factory = PaymentFactory()

processor = factory.get_processor("credit_card")
print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

processor = factory.get_processor("bank_transfer")
print(processor.process(100.0, {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}))
