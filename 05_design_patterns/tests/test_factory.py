"""Tests for the Factory pattern exercise."""

import pytest

from creational.factory import (
    BankTransferProcessor,
    CreditCardProcessor,
    PaymentFactory,
    PaymentProcessor,
    PayPalProcessor,
)


@pytest.fixture
def factory():
    return PaymentFactory()


@pytest.mark.parametrize(
    ("payment_type", "expected_class"),
    [
        ("credit_card", CreditCardProcessor),
        ("bank_transfer", BankTransferProcessor),
        ("paypal", PayPalProcessor),
    ],
)
def test_factory_returns_the_right_processor(factory, payment_type, expected_class):
    processor = factory.get_processor(payment_type)
    assert isinstance(processor, expected_class)
    assert isinstance(processor, PaymentProcessor)


def test_unknown_type_raises(factory):
    with pytest.raises(ValueError, match="Unknown payment type"):
        factory.get_processor("bitcoin")


def test_credit_card_fee(factory):
    result = factory.get_processor("credit_card").process(
        100.0, {"card_number": "1234567890123456", "cvv": "123"}
    )
    assert result == {"success": True, "method": "credit_card", "amount": 102.9, "fee": 2.9}


def test_bank_transfer_flat_fee(factory):
    result = factory.get_processor("bank_transfer").process(
        100.0, {"iban": "FR7630006000011234567890189"}
    )
    assert (result["amount"], result["fee"]) == (101.5, 1.5)


def test_paypal_fee(factory):
    result = factory.get_processor("paypal").process(100.0, {"email": "me@mail.com"})
    assert (result["amount"], result["fee"]) == (103.7, 3.7)


@pytest.mark.parametrize(
    ("payment_type", "details"),
    [
        ("credit_card", {"card_number": "123", "cvv": "123"}),
        ("credit_card", {"card_number": "1234567890123456", "cvv": "1"}),
        ("bank_transfer", {"iban": "FR76"}),
        ("paypal", {"email": "not-an-email"}),
        ("paypal", {}),
    ],
)
def test_invalid_details_are_rejected(factory, payment_type, details):
    processor = factory.get_processor(payment_type)
    assert processor.validate(details) is False
    assert processor.process(100.0, details)["success"] is False


def test_new_method_can_be_added_without_modifying_existing_code(factory):
    class ApplePayProcessor(PaymentProcessor):
        def validate(self, details):
            return "token" in details

        def process(self, amount, details):
            return {"success": True, "method": "apple_pay", "amount": amount, "fee": 0.0}

    factory.register("apple_pay", ApplePayProcessor)
    assert factory.get_processor("apple_pay").process(10.0, {"token": "x"})["method"] == "apple_pay"
    # Another factory is not affected.
    assert "apple_pay" not in PaymentFactory().available_types


def test_register_rejects_non_processor(factory):
    with pytest.raises(TypeError):
        factory.register("bad", dict)


def test_incomplete_processor_cannot_be_instantiated():
    class Incomplete(PaymentProcessor):
        def validate(self, details):
            return True

    with pytest.raises(TypeError):
        Incomplete()
