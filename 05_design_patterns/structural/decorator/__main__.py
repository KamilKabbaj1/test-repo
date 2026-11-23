"""Demo: `python -m structural.decorator` (run from 05_design_patterns/)."""

from . import (
    BaseOrder,
    DiscountDecorator,
    ExpressShippingDecorator,
    GiftWrapDecorator,
    InsuranceDecorator,
    PremiumMemberDecorator,
)

# Simple order
order = BaseOrder(100.00)
print(order.get_description())
print(f"Total: {order.get_cost():.2f}€")

print("\n---\n")

# Build an order with decorators: readable and flexible
order = BaseOrder(100.00)
order = ExpressShippingDecorator(order)
order = InsuranceDecorator(order)
order = GiftWrapDecorator(order)
order = DiscountDecorator(order, percent=15)
order = PremiumMemberDecorator(order)

print(order.get_description())
print(f"Total: {order.get_cost():.2f}€")
