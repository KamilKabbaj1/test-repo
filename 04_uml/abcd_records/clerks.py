"""The two clerks (rules 6 and 7): one class per job (Single Responsibility).

- OrderProcessingClerk: membership check, orders, stock, invoice, shipping.
- CollectionDepartmentClerk: payments only.
"""

from __future__ import annotations

import itertools
from collections.abc import Iterable

from .documents import Invoice, MembershipApplication, ShippingList
from .items import Item
from .members import Customer, Member
from .order import Order, OrderLine, OrderStatus
from .payment import Payment, PaymentMethod
from .records import DailyRecords


class OrderProcessingClerk:
    _order_ids = itertools.count(1)  # shared by all clerks: unique order IDs

    def __init__(self, name: str, members: Iterable[Member], records: DailyRecords) -> None:
        self.name = name
        # Registry of the club members, indexed by ID for a quick lookup.
        self._members = {member.member_id: member for member in members}
        # The records object is injected: the clerk does not know or care
        # where the file is (Dependency Inversion principle).
        self.records = records
        self.backorders: list[OrderLine] = []

    def verify_membership(self, customer: Customer) -> bool:
        # Being a Member instance is not enough: the ID must be registered.
        return (
            isinstance(customer, Member)
            and self._members.get(customer.member_id) is customer
        )

    def receive_order(
        self, customer: Customer, requests: dict[Item, int]
    ) -> Order | MembershipApplication:
        """Rules 1-2: members get an Order, others get an application form."""
        if not self.verify_membership(customer):
            return MembershipApplication(customer)
        # After verify_membership, we know the customer is a registered Member.
        order = Order(f"ORD-{next(self._order_ids):04d}", customer)
        for item, quantity in requests.items():
            # Raises UnavailableItemError for a Regular member (rule 4).
            order.add_line(item, quantity)
        return order

    def process_order(self, order: Order) -> Invoice:
        """Reserve the stock, print the documents and save the order (rule 8)."""
        order.mark_processed()  # first: refuses an order processed twice
        for line in order.lines:
            if line.backordered:
                self.backorders.append(line)
            else:
                line.item.remove_from_stock(line.quantity)
        order.shipping_list = ShippingList(order)
        self.records.save(order)
        return Invoice(order)

    def process_orders(self, orders: Iterable[Order]) -> list[Invoice]:
        """Process several orders, priority members first (rule 3)."""
        # sorted() is stable: inside each group the arrival order is kept.
        # `not has_priority` is False for Royal, and False sorts before True.
        queue = sorted(orders, key=lambda order: not order.member.has_priority)
        return [self.process_order(order) for order in queue]

    def ship_backorders(self) -> list[OrderLine]:
        """Ship the backordered lines whose item is back in stock."""
        shipped = []
        for line in list(self.backorders):  # copy: we remove while iterating
            if line.item.is_available(line.quantity):
                line.item.remove_from_stock(line.quantity)
                line.backordered = False
                self.backorders.remove(line)
                shipped.append(line)
        return shipped


class CollectionDepartmentClerk:
    def __init__(self, name: str) -> None:
        self.name = name
        self.payments: list[Payment] = []

    def collect_payment(self, order: Order, method: PaymentMethod) -> Payment:
        # Check first: an unprocessed or already paid order must be refused
        # BEFORE the method charges anything (no double payment).
        if order.status is not OrderStatus.PROCESSED:
            raise ValueError(f"order {order.order_id} cannot be paid in state {order.status.value}")
        payment = Payment(order, method)
        order.mark_paid(payment)
        self.payments.append(payment)
        return payment
