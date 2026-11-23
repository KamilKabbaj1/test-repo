from .payment_processor import PaymentProcessor


class BankTransferProcessor(PaymentProcessor):
    FLAT_FEE = 1.50
    MIN_IBAN_LENGTH = 15

    def validate(self, details: dict) -> bool:
        iban = details.get("iban") or ""
        return len(iban) >= self.MIN_IBAN_LENGTH

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid IBAN"}
        fee = self.FLAT_FEE
        return {"success": True, "method": "bank_transfer", "amount": round(amount + fee, 2), "fee": fee}
