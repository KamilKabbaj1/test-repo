"""Abstract decorator: holds the wrapped component and delegates to it."""

from abc import abstractmethod

from ..order_component import OrderComponent


class OrderDecorator(OrderComponent):
    def __init__(self, order: OrderComponent) -> None:
        # Protected `_order` (slide 87: "use _order (protected) for decorator
        # inheritance"): the subclasses need it, outside code does not.
        # Composition: the decorator HAS A component and is one too.
        self._order = order

    # Template for every decorator: cost and description = those of the wrapped
    # component + this decorator's own line. The subclasses only say what they
    # add (`_extra_cost` and `_label`), so the delegation is written once.
    def get_cost(self) -> float:
        return self._order.get_cost() + self._extra_cost()

    def get_description(self) -> str:
        return f"{self._order.get_description()}\n{self._label()}"

    @abstractmethod
    def _extra_cost(self) -> float:
        """Amount added (positive) or removed (negative) by this option."""

    @abstractmethod
    def _label(self) -> str:
        """Breakdown line for this option."""
