"""One decorator per file: a new option = a new file, nothing else changes."""

from .discount import DiscountDecorator
from .express_shipping import ExpressShippingDecorator
from .gift_wrap import GiftWrapDecorator
from .insurance import InsuranceDecorator
from .order_decorator import OrderDecorator
from .premium_member import PremiumMemberDecorator

__all__ = [
    "DiscountDecorator",
    "ExpressShippingDecorator",
    "GiftWrapDecorator",
    "InsuranceDecorator",
    "OrderDecorator",
    "PremiumMemberDecorator",
]
