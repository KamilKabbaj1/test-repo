from .payment_processor import PaymentProcessor


class PayPalProcessor(PaymentProcessor):
    FEE_RATE = 0.034   # 3.4 %
    FIXED_FEE = 0.30   # + 0.30 EUR

    def validate(self, details: dict) -> bool:
        email = details.get("email") or ""
        return "@" in email

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid PayPal email"}
        fee = round(amount * self.FEE_RATE + self.FIXED_FEE, 2)
        return {"success": True, "method": "paypal", "amount": round(amount + fee, 2), "fee": fee}
