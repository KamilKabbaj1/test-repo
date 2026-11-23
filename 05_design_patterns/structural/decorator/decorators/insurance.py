from .order_decorator import OrderDecorator


class InsuranceDecorator(OrderDecorator):
    RATE = 0.05  # 5 %

    # Difference with the old code, chosen on purpose: the insurance covers 5 % of
    # WHAT IT WRAPS (the order with the options added before it), not always of the base price.
    # The order of the decorators makes it explicit: to insure the goods only,
    # wrap BaseOrder with InsuranceDecorator first.
    def _extra_cost(self) -> float:
        return self._order.get_cost() * self.RATE

    def _label(self) -> str:
        return f"Insurance (5%): +{self._extra_cost():.2f}€"
