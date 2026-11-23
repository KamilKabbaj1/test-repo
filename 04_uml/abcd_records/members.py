"""Customers and members (rules 1 to 4)."""

from abc import ABC, abstractmethod


class Customer:
    """Anyone who contacts ABCD Records. A non-member is a plain Customer."""

    def __init__(self, name: str, address: str) -> None:
        self.name = name
        self.address = address

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"


class Member(Customer, ABC):
    """A record club member: the only kind of customer allowed to order (rule 1).

    Abstract: every member is either Regular or Royal (rule 3). The differences
    are BEHAVIOURS (discount, unavailable items, priority), so they are
    abstract properties overridden by each subclass. The clerk then never has to
    write `if member_type == "royal"` (polymorphism, slide 86).
    """

    def __init__(self, member_id: str, name: str, address: str) -> None:
        super().__init__(name, address)
        self.member_id = member_id

    @property
    @abstractmethod
    def discount_rate(self) -> float:
        """Fraction of the price removed, e.g. 0.10 for 10 %."""

    @property
    @abstractmethod
    def can_order_unavailable(self) -> bool:
        """Can this member order an item that is out of stock (rule 4)?"""

    @property
    @abstractmethod
    def has_priority(self) -> bool:
        """Are this member's orders processed first (rule 3)?"""


class RegularMember(Member):
    @property
    def discount_rate(self) -> float:
        return 0.0

    @property
    def can_order_unavailable(self) -> bool:
        return False

    @property
    def has_priority(self) -> bool:
        return False


class RoyalMember(Member):
    # Named constant instead of a "magic number" hidden in the code.
    DISCOUNT_RATE = 0.10

    @property
    def discount_rate(self) -> float:
        return self.DISCOUNT_RATE

    @property
    def can_order_unavailable(self) -> bool:
        return True

    @property
    def has_priority(self) -> bool:
        return True
