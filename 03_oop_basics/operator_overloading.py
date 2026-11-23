"""Operator overloading exercises (slide 67).

Statement: https://gist.github.com/bdallard/b2f2c910e3a9b564a30c86991c97b4fc

Key idea (slides 32-33): special "dunder" methods let our own classes work with
Python operators. `a + b` is translated by Python into `a.__add__(b)`.

Convention used everywhere in this file: when the other operand has the wrong
type, the method returns `NotImplemented` (it does NOT raise). WHY: Python then
tries the reflected operation on the other object (e.g. `b.__radd__(a)`), and
if nobody knows how to handle it, Python itself raises a clean `TypeError`.
"""


# --------------------------------------------------------------------------
# Problem 1 - Complex numbers: + and -
# --------------------------------------------------------------------------
class Complex:
    """A complex number `real + imag * i`."""

    def __init__(self, real: float, imag: float = 0.0) -> None:
        self.real = real
        self.imag = imag

    def __add__(self, other: "Complex") -> "Complex":
        # (a + bi) + (c + di) = (a + c) + (b + d)i
        if not isinstance(other, Complex):
            return NotImplemented
        # Return a NEW object instead of modifying self: `a + b` must not change `a`,
        # exactly like with built-in numbers.
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: "Complex") -> "Complex":
        # (a + bi) - (c + di) = (a - c) + (b - d)i
        if not isinstance(other, Complex):
            return NotImplemented
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other: object) -> bool:
        # Not required by the statement, but without it `Complex(1, 2) == Complex(1, 2)`
        # compares identities (two different objects -> False), which makes testing impossible.
        if not isinstance(other, Complex):
            return NotImplemented
        return self.real == other.real and self.imag == other.imag

    # Defining __eq__ sets __hash__ to None automatically: Complex objects are
    # mutable, so they must not be used as dict keys anyway.

    def __repr__(self) -> str:
        # __repr__ gives a readable output in print(), the debugger and pytest errors.
        sign = "+" if self.imag >= 0 else "-"
        return f"Complex({self.real} {sign} {abs(self.imag)}i)"


# --------------------------------------------------------------------------
# Problem 2 - Person compared by age with >
# --------------------------------------------------------------------------
class Person:
    """A person who can be compared to another one by age."""

    def __init__(self, name: str, age: int, gender: str) -> None:
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other: "Person") -> bool:
        # p1 > p2  <=>  p1.age > p2.age
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age

    # Only `>` is asked. Python still accepts `p1 < p2`: it is translated into the
    # reflected call `p2 > p1`, so it works without writing __lt__.

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, age={self.age}, gender={self.gender!r})"
