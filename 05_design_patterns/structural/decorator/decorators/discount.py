from ..order_component import OrderComponent
from .order_decorator import OrderDecorator


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float) -> None:
        if not 0 < percent <= 100:
            raise ValueError("percent must be in ]0, 100]")
        super().__init__(order)
        self.percent = percent

    def _extra_cost(self) -> float:
        # Negative: a discount removes money from the wrapped total.
        return -self._order.get_cost() * self.percent / 100

    def _label(self) -> str:
        return f"Discount ({self.percent:g}%): -{-self._extra_cost():.2f}€"
