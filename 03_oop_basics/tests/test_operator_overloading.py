"""Tests for operator_overloading.py (run with `pytest -v`)."""

import pytest

from operator_overloading import Complex, Person


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
