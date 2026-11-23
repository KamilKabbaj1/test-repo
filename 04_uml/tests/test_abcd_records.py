"""Tests for the abcd_records package (run with `pytest -v`)."""

import pytest

from abcd_records import (
    CD,
    BankDraft,
    Cash,
    Check,
    CollectionDepartmentClerk,
    Customer,
    DailyRecords,
    Member,
    MembershipApplication,
    Order,
    OrderProcessingClerk,
    OrderStatus,
    RegularMember,
    RoyalMember,
    Tape,
    UnavailableItemError,
)


@pytest.fixture
def royal():
    return RoyalMember("M-001", "Rita", "1 Abbey Road, London")


@pytest.fixture
def regular():
    return RegularMember("M-002", "Rob", "2 Penny Lane, Liverpool")


@pytest.fixture
def kind_of_blue():
    return CD("CD-01", "Kind of Blue", 15.0, artist="Miles Davis", stock=3)


@pytest.fixture
def abbey_road():
    return CD("CD-02", "Abbey Road", 20.0, artist="The Beatles", stock=0)


@pytest.fixture
def clerk(royal, regular, tmp_path):
    # tmp_path: a temporary folder created by pytest, removed afterwards.
    # The real file system is never touched.
    return OrderProcessingClerk("Olivia", [royal, regular], DailyRecords(tmp_path / "orders.txt"))


# ---------------------------------------------------------------- members
def test_member_is_abstract():
    with pytest.raises(TypeError):
        Member("M-9", "nobody", "nowhere")


@pytest.mark.parametrize(
    ("member", "discount", "unavailable", "priority"),
    [
        (RoyalMember("M-1", "R", "a"), 0.10, True, True),
        (RegularMember("M-2", "G", "b"), 0.0, False, False),
    ],
)
def test_member_types(member, discount, unavailable, priority):
    assert (member.discount_rate, member.can_order_unavailable, member.has_priority) == (
        discount,
        unavailable,
        priority,
    )


# ---------------------------------------------------------------- membership
def test_non_member_receives_application_form(clerk, kind_of_blue):
    visitor = Customer("Nina", "3 Main Street")
    result = clerk.receive_order(visitor, {kind_of_blue: 1})
    assert isinstance(result, MembershipApplication)
    assert result.applicant is visitor
    assert kind_of_blue.stock == 3  # nothing was reserved


def test_unregistered_member_is_rejected(clerk, kind_of_blue):
    impostor = RoyalMember("M-001", "Fake Rita", "?")  # same ID, other person
    assert not clerk.verify_membership(impostor)
    assert isinstance(clerk.receive_order(impostor, {kind_of_blue: 1}), MembershipApplication)


# ---------------------------------------------------------------- scenario (level 2)
def test_royal_orders_two_cds_one_unavailable_and_pays_by_check(
    clerk, royal, kind_of_blue, abbey_road
):
    order = clerk.receive_order(royal, {kind_of_blue: 1, abbey_road: 1})
    assert isinstance(order, Order)
    assert [line.backordered for line in order.lines] == [False, True]

    invoice = clerk.process_order(order)
    assert order.status is OrderStatus.PROCESSED
    assert kind_of_blue.stock == 2       # the available CD is reserved
    assert order.subtotal == 35.0
    assert order.discount == 3.5         # 10 % Royal discount
    assert invoice.total == 31.5
    assert [line.item for line in order.shipping_list.lines_to_ship] == [kind_of_blue]
    assert clerk.backorders == [order.lines[1]]

    payment = CollectionDepartmentClerk("Colin").collect_payment(order, Check("0042"))
    assert order.status is OrderStatus.PAID
    assert payment.receipt == "31.50 EUR received by check n°0042"


def test_invoice_text(clerk, royal, kind_of_blue, abbey_road):
    invoice = clerk.process_order(clerk.receive_order(royal, {kind_of_blue: 1, abbey_road: 1}))
    text = invoice.render()
    assert "Abbey Road x1: 20.00 (backordered)" in text
    assert "Discount: -3.50" in text
    assert text.endswith("TOTAL: 31.50")


# ---------------------------------------------------------------- availability
def test_regular_cannot_order_unavailable_item(clerk, regular, abbey_road):
    with pytest.raises(UnavailableItemError):
        clerk.receive_order(regular, {abbey_road: 1})


def test_regular_pays_full_price(clerk, regular, kind_of_blue):
    order = clerk.receive_order(regular, {kind_of_blue: 2})
    assert clerk.process_order(order).total == 30.0


def test_backorders_are_shipped_after_restock(clerk, royal, abbey_road):
    order = clerk.receive_order(royal, {abbey_road: 2})
    clerk.process_order(order)
    assert clerk.ship_backorders() == []  # still out of stock

    abbey_road.restock(5)
    shipped = clerk.ship_backorders()
    assert shipped == order.lines
    assert abbey_road.stock == 3
    assert clerk.backorders == []
    assert order.shipping_list.lines_to_ship == order.lines


# ---------------------------------------------------------------- priority
def test_royal_orders_are_processed_first(clerk, royal, regular, kind_of_blue):
    regular_order = clerk.receive_order(regular, {kind_of_blue: 1})
    royal_order = clerk.receive_order(royal, {kind_of_blue: 1})
    invoices = clerk.process_orders([regular_order, royal_order])
    assert [invoice.order for invoice in invoices] == [royal_order, regular_order]


# ---------------------------------------------------------------- payments
@pytest.mark.parametrize(
    ("method", "expected"),
    [
        (Cash(), "15.00 EUR received in cash"),
        (Check("7"), "15.00 EUR received by check n°7"),
        (BankDraft("BD-9"), "15.00 EUR received by bank draft n°BD-9"),
    ],
)
def test_all_payment_types(clerk, regular, kind_of_blue, method, expected):
    order = clerk.receive_order(regular, {kind_of_blue: 1})
    clerk.process_order(order)
    assert CollectionDepartmentClerk("Colin").collect_payment(order, method).receipt == expected


def test_order_cannot_be_paid_before_processing_or_twice(clerk, regular, kind_of_blue):
    collector = CollectionDepartmentClerk("Colin")
    order = clerk.receive_order(regular, {kind_of_blue: 1})
    with pytest.raises(ValueError):
        collector.collect_payment(order, Cash())
    clerk.process_order(order)
    collector.collect_payment(order, Cash())
    with pytest.raises(ValueError):
        collector.collect_payment(order, Cash())
    assert len(collector.payments) == 1


# ---------------------------------------------------------------- daily records
def test_processed_orders_are_saved_in_daily_records(clerk, royal, regular, kind_of_blue):
    first = clerk.receive_order(royal, {kind_of_blue: 1})
    second = clerk.receive_order(regular, {kind_of_blue: 1})
    clerk.process_orders([first, second])
    entries = clerk.records.entries()
    assert [entry[1] for entry in entries] == [first.order_id, second.order_id]
    assert entries[0][2:] == ["M-001", "13.50", "processed"]


def test_order_cannot_be_processed_twice(clerk, regular, kind_of_blue):
    order = clerk.receive_order(regular, {kind_of_blue: 1})
    clerk.process_order(order)
    with pytest.raises(ValueError):
        clerk.process_order(order)
    assert kind_of_blue.stock == 2  # the stock was reserved only once


def test_tape_is_an_item():
    tape = Tape("T-01", "Thriller", 8.0, duration_minutes=42, stock=1)
    assert tape.kind == "Tape"
    with pytest.raises(ValueError):
        tape.remove_from_stock(2)
