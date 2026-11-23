from .order_decorator import OrderDecorator


class ExpressShippingDecorator(OrderDecorator):
    COST = 15.00

    def _extra_cost(self) -> float:
        return self.COST

    def _label(self) -> str:
        return f"Express shipping: +{self.COST:.2f}€"
