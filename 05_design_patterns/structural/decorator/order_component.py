"""The common interface of the order and of every decorator."""

from abc import ABC, abstractmethod


class OrderComponent(ABC):
    """A decorated order IS STILL an OrderComponent.

    This is the key of the pattern: a decorator can wrap a BaseOrder or
    another decorator, indefinitely, and the caller always uses the same two methods.
    """

    @abstractmethod
    def get_cost(self) -> float:
        """Total cost, in euros."""

    @abstractmethod
    def get_description(self) -> str:
        """Price breakdown, one line per component."""
