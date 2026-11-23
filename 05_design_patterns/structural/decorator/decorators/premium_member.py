from .order_decorator import OrderDecorator


class PremiumMemberDecorator(OrderDecorator):
    RATE = 0.10  # 10 %

    def _extra_cost(self) -> float:
        return -self._order.get_cost() * self.RATE

    def _label(self) -> str:
        return f"Premium member (10%): -{-self._extra_cost():.2f}€"
