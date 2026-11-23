"""Operator overloading exercises (slide 67).

Statement: https://gist.github.com/bdallard/b2f2c910e3a9b564a30c86991c97b4fc

Key idea (slides 32-33): special "dunder" methods let our own classes work with
Python operators. `a + b` is translated by Python into `a.__add__(b)`.

Convention used everywhere in this file: when the other operand has the wrong
type, the method returns `NotImplemented` (it does NOT raise). WHY: Python then
tries the reflected operation on the other object (e.g. `b.__radd__(a)`), and
if nobody knows how to handle it, Python itself raises a clean `TypeError`.
"""

import math


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


# --------------------------------------------------------------------------
# Problem 4 - Vector: * is the dot product
# (the statement has no problem 3: the numbering follows the original gist)
# --------------------------------------------------------------------------
class Vector:
    """A vector in 3D space."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other: "Vector") -> float:
        # Dot product: u . v = ux*vx + uy*vy + uz*vz -> a number, not a Vector.
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"


# --------------------------------------------------------------------------
# Problem 5 - Circle: ALL six comparison operators, based on the radius
# --------------------------------------------------------------------------
class Circle:
    """A circle, compared to other circles by radius."""

    def __init__(self, radius: float) -> None:
        # Goes through the property setter below, so the validation also
        # applies at creation time.
        self.radius = radius

    # @property (slide 87, "leverage @property for state encapsulation"):
    # `circle.radius` still looks like a plain attribute from the outside,
    # but every assignment is checked. A negative radius can never exist.
    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("radius must be non-negative")
        self._radius = value

    # The statement asks to overload every operator, so the six are written
    # explicitly. In real code, `@functools.total_ordering` generates the four
    # others from __eq__ and __lt__ alone (less code, same behaviour).
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __ne__(self, other: object) -> bool:
        # Python 3 derives != from == automatically; written here because the
        # statement lists it explicitly.
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius != other.radius

    def __lt__(self, other: "Circle") -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __le__(self, other: "Circle") -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius <= other.radius

    def __gt__(self, other: "Circle") -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius

    def __ge__(self, other: "Circle") -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius >= other.radius

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius})"


# --------------------------------------------------------------------------
# Problem 6 - 2D point compared by Euclidean distance from the origin
# --------------------------------------------------------------------------
class Point2D:
    """A 2D point, compared to other points by distance from the origin."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @property
    def distance(self) -> float:
        # Computed property: always up to date if x or y change, no duplicated
        # state to keep in sync. math.hypot(x, y) = sqrt(x**2 + y**2).
        return math.hypot(self.x, self.y)

    # Every comparison delegates to `distance`: the rule lives in one place.
    # Note: (3, 4) == (4, 3) == (0, 5) here, because they are all at distance 5.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance == other.distance

    def __lt__(self, other: "Point2D") -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance < other.distance

    def __le__(self, other: "Point2D") -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance <= other.distance

    def __gt__(self, other: "Point2D") -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance > other.distance

    def __ge__(self, other: "Point2D") -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance >= other.distance

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"
