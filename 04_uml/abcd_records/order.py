"""Orders and order lines."""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import TYPE_CHECKING

from .items import Item
from .members import Member

if TYPE_CHECKING:
    from .documents import ShippingList
    from .payment import Payment


class UnavailableItemError(Exception):
    """A Regular member asked for an item that is out of stock (rule 4)."""


class OrderStatus(Enum):
    RECEIVED = "received"    # created, lines can still be added
    PROCESSED = "processed"  # stock reserved, invoice + shipping list printed
    PAID = "paid"            # payment collected


class OrderLine:
    """One item with a quantity, possibly waiting for stock.

    WHY a class: an Order -> Item link alone cannot store "how many copies" or
    "this line is backordered".
    """

    def __init__(self, item: Item, quantity: int, backordered: bool = False) -> None:
        self.item = item
        self.quantity = quantity
        self.backordered = backordered

    @property
    def subtotal(self) -> float:
        return self.item.price * self.quantity

    def __repr__(self) -> str:
        flag = ", backordered" if self.backordered else ""
        return f"OrderLine({self.item.title!r} x{self.quantity}{flag})"


class Order:
    def __init__(self, order_id: str, member: Member) -> None:
        self.order_id = order_id
        self.member = member
        self.date = date.today()
        self.lines: list[OrderLine] = []  # composition: the lines die with the order
        self._status = OrderStatus.RECEIVED
        self.shipping_list: ShippingList | None = None
        self.payment: Payment | None = None

    @property
    def status(self) -> OrderStatus:
        return self._status

    def add_line(self, item: Item, quantity: int) -> OrderLine:
        if self._status is not OrderStatus.RECEIVED:
            raise ValueError("cannot modify an order that is already processed")
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if item.is_available(quantity):
            line = OrderLine(item, quantity)
        elif self.member.can_order_unavailable:
            # Polymorphism: Royal says True, Regular says False. No type test here.
            line = OrderLine(item, quantity, backordered=True)
        else:
            raise UnavailableItemError(f"{item.title!r} is not available")
        self.lines.append(line)
        return line

    # Prices are computed on demand (properties) instead of being stored:
    # adding a line can never leave a stale total behind.
    @property
    def subtotal(self) -> float:
        return sum(line.subtotal for line in self.lines)

    @property
    def discount(self) -> float:
        return round(self.subtotal * self.member.discount_rate, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal - self.discount, 2)

    # The status only moves forward, and each method checks where it comes from.
    def mark_processed(self) -> None:
        if self._status is not OrderStatus.RECEIVED:
            raise ValueError(f"order {self.order_id} was already processed")
        if not self.lines:
            raise ValueError("cannot process an empty order")
        self._status = OrderStatus.PROCESSED

    def mark_paid(self, payment: Payment) -> None:
        if self._status is not OrderStatus.PROCESSED:
            raise ValueError(f"order {self.order_id} cannot be paid in state {self._status.value}")
        self.payment = payment
        self._status = OrderStatus.PAID

    def __repr__(self) -> str:
        return f"Order({self.order_id}, {self.member.name!r}, {self._status.value})"
