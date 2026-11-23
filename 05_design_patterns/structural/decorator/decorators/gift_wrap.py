from .order_decorator import OrderDecorator


class GiftWrapDecorator(OrderDecorator):
    COST = 5.00

    def _extra_cost(self) -> float:
        return self.COST

    def _label(self) -> str:
        return f"Gift wrap: +{self.COST:.2f}€"
