from .payment_processor import PaymentProcessor


class CreditCardProcessor(PaymentProcessor):
    # Named constant: the business rule is visible at the top of the class,
    # instead of a 0.029 hidden in the middle of an if/elif block.
    FEE_RATE = 0.029  # 2.9 %

    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number") or ""
        cvv = details.get("cvv") or ""
        return len(card_number) == 16 and len(cvv) == 3

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid credit card details"}
        fee = round(amount * self.FEE_RATE, 2)
        return {"success": True, "method": "credit_card", "amount": round(amount + fee, 2), "fee": fee}
