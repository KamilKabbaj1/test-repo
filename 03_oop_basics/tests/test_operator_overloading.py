"""Tests for operator_overloading.py (run with `pytest -v`)."""

import pytest

from operator_overloading import Circle, Complex, Person, Point2D, Vector


# ---------------------------------------------------------------- Complex
def test_complex_addition():
    assert Complex(1, 2) + Complex(3, -5) == Complex(4, -3)


def test_complex_subtraction():
    assert Complex(1, 2) - Complex(3, -5) == Complex(-2, 7)


def test_complex_addition_returns_new_object():
    # `a + b` must not modify `a`.
    a, b = Complex(1, 1), Complex(2, 2)
    result = a + b
    assert result is not a
    assert a == Complex(1, 1)


def test_complex_with_wrong_type_raises_type_error():
    # __add__ returns NotImplemented, so Python raises TypeError itself.
    with pytest.raises(TypeError):
        Complex(1, 2) + 3


def test_complex_repr():
    assert repr(Complex(1, -2)) == "Complex(1 - 2i)"


# ---------------------------------------------------------------- Person
def test_person_greater_than_by_age():
    old, young = Person("Alice", 40, "F"), Person("Bob", 20, "M")
    assert old > young
    assert not young > old


def test_person_same_age_is_not_greater():
    assert not Person("A", 30, "F") > Person("B", 30, "M")


def test_person_less_than_uses_reflected_greater_than():
    assert Person("Bob", 20, "M") < Person("Alice", 40, "F")


# ---------------------------------------------------------------- Vector
def test_vector_dot_product():
    assert Vector(1, 2, 3) * Vector(4, -5, 6) == 1 * 4 + 2 * -5 + 3 * 6


def test_orthogonal_vectors_have_zero_dot_product():
    assert Vector(1, 0, 0) * Vector(0, 1, 0) == 0


def test_vector_times_number_is_not_supported():
    with pytest.raises(TypeError):
        Vector(1, 2, 3) * 2


# ---------------------------------------------------------------- Circle
@pytest.mark.parametrize(
    ("r1", "r2", "expected"),
    [
        # (r1, r2, (==, !=, <, <=, >, >=))
        (1, 2, (False, True, True, True, False, False)),
        (2, 2, (True, False, False, True, False, True)),
        (3, 2, (False, True, False, False, True, True)),
    ],
)
def test_circle_comparisons(r1, r2, expected):
    a, b = Circle(r1), Circle(r2)
    assert (a == b, a != b, a < b, a <= b, a > b, a >= b) == expected


def test_circle_negative_radius_is_rejected():
    with pytest.raises(ValueError):
        Circle(-1)
    circle = Circle(1)
    with pytest.raises(ValueError):
        circle.radius = -5


def test_circles_can_be_sorted():
    # sorted() only needs __lt__.
    circles = [Circle(3), Circle(1), Circle(2)]
    assert [c.radius for c in sorted(circles)] == [1, 2, 3]


# ---------------------------------------------------------------- Point2D
def test_point_distance():
    assert Point2D(3, 4).distance == 5


@pytest.mark.parametrize(
    ("p1", "p2", "expected"),
    [
        # (p1, p2, (==, <, <=, >, >=))
        (Point2D(1, 1), Point2D(3, 4), (False, True, True, False, False)),
        (Point2D(3, 4), Point2D(0, 5), (True, False, True, False, True)),
        (Point2D(0, -6), Point2D(3, 4), (False, False, False, True, True)),
    ],
)
def test_point_comparisons(p1, p2, expected):
    assert (p1 == p2, p1 < p2, p1 <= p2, p1 > p2, p1 >= p2) == expected
