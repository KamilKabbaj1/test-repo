from .order_component import OrderComponent


class BaseOrder(OrderComponent):
    """The concrete object at the centre: just the base price, no options."""

    def __init__(self, base_price: float) -> None:
        if base_price < 0:
            raise ValueError("base price must be non-negative")
        self.base_price = base_price

    def get_cost(self) -> float:
        return self.base_price

    def get_description(self) -> str:
        return f"Base price: {self.base_price:.2f}€"
