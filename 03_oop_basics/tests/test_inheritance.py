"""Tests for inheritance.py (run with `pytest -v`)."""

import pytest

from inheritance import Bicycle, Car, Employee, Person, Student, Vehicle


# ---------------------------------------------------------------- Vehicles
@pytest.mark.parametrize(
    ("vehicle", "expected"),
    [
        (Vehicle(), "Driving a vehicle"),
        (Car(), "Driving a car"),
        (Bicycle(), "Riding a bicycle"),
    ],
)
def test_drive_is_polymorphic(vehicle, expected):
    # Same call, different behaviour depending on the real class.
    assert vehicle.drive() == expected


def test_car_and_bicycle_are_vehicles():
    assert isinstance(Car(), Vehicle)
    assert isinstance(Bicycle(), Vehicle)


# ---------------------------------------------------------------- Persons
def test_person_introduce():
    assert Person("Ana", 30, "Paris").introduce() == (
        "Hi, I'm Ana, 30 years old, living at Paris."
    )


def test_student_extends_person():
    student = Student("Kamil", 20, "Gif-sur-Yvette", "computer science")
    assert isinstance(student, Person)
    assert student.name == "Kamil"  # attribute set by Person.__init__
    assert student.introduce() == (
        "Hi, I'm Kamil, 20 years old, living at Gif-sur-Yvette. "
        "I study computer science."
    )


def test_employee_extends_person():
    employee = Employee("Bob", 45, "Lyon", "ACME")
    assert employee.company == "ACME"
    assert employee.introduce().endswith("I work at ACME.")
