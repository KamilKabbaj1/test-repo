"""Printed documents: invoice, shipping list, membership application.

They are separate from Order (Single Responsibility principle): Order knows
WHAT was ordered. Each document only knows HOW to present it, so a change in
the invoice layout never touches the order logic.
"""

from __future__ import annotations

from datetime import datetime

from .members import Customer
from .order import Order, OrderLine


class Invoice:
    def __init__(self, order: Order) -> None:
        self.order = order

    @property
    def total(self) -> float:
        return self.order.total

    def render(self) -> str:
        """Text of the printed invoice (all lines are charged, backordered ones included)."""
        lines = [f"INVOICE {self.order.order_id} - {self.order.member.name}"]
        for line in self.order.lines:
            note = " (backordered)" if line.backordered else ""
            lines.append(
                f"  {line.item.kind} {line.item.title} x{line.quantity}: {line.subtotal:.2f}{note}"
            )
        lines.append(f"  Subtotal: {self.order.subtotal:.2f}")
        if self.order.discount:
            lines.append(f"  Discount: -{self.order.discount:.2f}")
        lines.append(f"  TOTAL: {self.total:.2f}")
        return "\n".join(lines)


class ShippingList:
    def __init__(self, order: Order) -> None:
        self.order = order

    @property
    def lines_to_ship(self) -> list[OrderLine]:
        # Computed each time, so the list stays correct when a backordered
        # line is shipped later.
        return [line for line in self.order.lines if not line.backordered]

    def render(self) -> str:
        lines = [f"SHIP TO {self.order.member.name}, {self.order.member.address}"]
        lines += [f"  {line.item.title} x{line.quantity}" for line in self.lines_to_ship]
        return "\n".join(lines)


class MembershipApplication:
    """Form sent to a non-member who tried to order (rule 2)."""

    def __init__(self, applicant: Customer) -> None:
        self.applicant = applicant
        self.issued_at = datetime.now()

    def __repr__(self) -> str:
        return f"MembershipApplication({self.applicant.name!r})"
