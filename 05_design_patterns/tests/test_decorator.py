"""Tests for the Decorator pattern exercise."""

import pytest

from structural.decorator import (
    BaseOrder,
    DiscountDecorator,
    ExpressShippingDecorator,
    GiftWrapDecorator,
    InsuranceDecorator,
    OrderComponent,
    OrderDecorator,
    PremiumMemberDecorator,
)


def test_base_order():
    order = BaseOrder(100.0)
    assert order.get_cost() == 100.0
    assert order.get_description() == "Base price: 100.00€"


@pytest.mark.parametrize(
    ("decorator", "expected_cost"),
    [
        (ExpressShippingDecorator, 115.0),
        (InsuranceDecorator, 105.0),
        (GiftWrapDecorator, 105.0),
        (PremiumMemberDecorator, 90.0),
        (lambda order: DiscountDecorator(order, percent=15), 85.0),
    ],
)
def test_each_decorator_alone(decorator, expected_cost):
    decorated = decorator(BaseOrder(100.0))
    assert isinstance(decorated, OrderComponent)
    assert decorated.get_cost() == pytest.approx(expected_cost)


def test_full_chain_from_statement():
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)    # 115.00
    order = InsuranceDecorator(order)          # +5.75 -> 120.75
    order = GiftWrapDecorator(order)           # 125.75
    order = DiscountDecorator(order, percent=15)  # -18.86 -> 106.89
    order = PremiumMemberDecorator(order)      # -10.69 -> 96.20
    assert order.get_cost() == pytest.approx(96.19875)
    assert order.get_description().splitlines() == [
        "Base price: 100.00€",
        "Express shipping: +15.00€",
        "Insurance (5%): +5.75€",
        "Gift wrap: +5.00€",
        "Discount (15%): -18.86€",
        "Premium member (10%): -10.69€",
    ]


def test_order_of_decorators_matters():
    # Insurance on the goods only vs on goods + shipping.
    goods_only = ExpressShippingDecorator(InsuranceDecorator(BaseOrder(100.0)))
    with_shipping = InsuranceDecorator(ExpressShippingDecorator(BaseOrder(100.0)))
    assert goods_only.get_cost() == pytest.approx(120.0)
    assert with_shipping.get_cost() == pytest.approx(120.75)


def test_same_decorator_can_be_applied_twice():
    order = GiftWrapDecorator(GiftWrapDecorator(BaseOrder(10.0)))
    assert order.get_cost() == pytest.approx(20.0)


def test_new_option_needs_no_change_to_existing_classes():
    class LoyaltyPointsDecorator(OrderDecorator):
        def _extra_cost(self):
            return -2.0

        def _label(self):
            return "Loyalty points: -2.00€"

    order = LoyaltyPointsDecorator(ExpressShippingDecorator(BaseOrder(10.0)))
    assert order.get_cost() == pytest.approx(23.0)
    assert order.get_description().endswith("Loyalty points: -2.00€")


@pytest.mark.parametrize("percent", [0, -5, 150])
def test_invalid_discount(percent):
    with pytest.raises(ValueError):
        DiscountDecorator(BaseOrder(100.0), percent=percent)


def test_negative_base_price():
    with pytest.raises(ValueError):
        BaseOrder(-1)
