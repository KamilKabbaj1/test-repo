"""Catalogue items: CDs and tapes."""

from abc import ABC, abstractmethod


class Item(ABC):
    """Common data and stock management of every item.

    Abstract: the company only sells CDs and tapes, never a "generic item".
    """

    def __init__(self, code: str, title: str, price: float, stock: int = 0) -> None:
        if price < 0 or stock < 0:
            raise ValueError("price and stock must be non-negative")
        self.code = code
        self.title = title
        self.price = price
        self._stock = stock

    @property
    def stock(self) -> int:
        # Read-only from outside: the stock only changes through the methods
        # below, which forbid a negative stock.
        return self._stock

    def is_available(self, quantity: int = 1) -> bool:
        return self._stock >= quantity

    def remove_from_stock(self, quantity: int) -> None:
        if not self.is_available(quantity):
            raise ValueError(f"not enough {self.title!r} in stock")
        self._stock -= quantity

    def restock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self._stock += quantity

    @property
    @abstractmethod
    def kind(self) -> str:
        """Human-readable type, used on invoices ("CD", "Tape")."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.code!r}, {self.title!r})"


class CD(Item):
    def __init__(self, code: str, title: str, price: float, artist: str, stock: int = 0) -> None:
        super().__init__(code, title, price, stock)
        self.artist = artist

    @property
    def kind(self) -> str:
        return "CD"


class Tape(Item):
    def __init__(self, code: str, title: str, price: float, duration_minutes: int, stock: int = 0) -> None:
        super().__init__(code, title, price, stock)
        self.duration_minutes = duration_minutes

    @property
    def kind(self) -> str:
        return "Tape"
