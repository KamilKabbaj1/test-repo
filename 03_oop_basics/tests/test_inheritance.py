"""Tests for inheritance.py (run with `pytest -v`)."""

import pytest

from inheritance import (
    BankAccount,
    Bicycle,
    Car,
    Employee,
    Person,
    SavingsAccount,
    Student,
    Vehicle,
)


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


# ---------------------------------------------------------------- Bank accounts
def test_deposit_and_withdraw():
    account = BankAccount("FR-001", 100)
    account.deposit(50)
    assert account.withdraw(30) is True
    assert account.balance == 120


def test_withdraw_more_than_balance_changes_nothing():
    account = BankAccount("FR-001", 100)
    assert account.withdraw(500) is False
    assert account.balance == 100


@pytest.mark.parametrize("amount", [0, -10])
def test_non_positive_amounts_are_rejected(amount):
    account = BankAccount("FR-001", 100)
    with pytest.raises(ValueError):
        account.deposit(amount)
    with pytest.raises(ValueError):
        account.withdraw(amount)


def test_balance_is_read_only():
    account = BankAccount("FR-001", 100)
    with pytest.raises(AttributeError):
        account.balance = 1_000_000


def test_transfer_success():
    source, destination = BankAccount("A", 100), BankAccount("B", 10)
    assert source.transfer(destination, 60) is True
    assert (source.balance, destination.balance) == (40, 70)


def test_transfer_insufficient_balance():
    source, destination = BankAccount("A", 100), BankAccount("B", 10)
    assert source.transfer(destination, 150) is False
    assert (source.balance, destination.balance) == (100, 10)


def test_savings_account_interest():
    savings = SavingsAccount("S-1", 1000, interest_rate=0.03)
    assert savings.add_interest() == pytest.approx(30)
    assert savings.check_balance() == pytest.approx(1030)


def test_savings_account_is_a_bank_account():
    # Liskov substitution: a SavingsAccount works wherever a BankAccount is expected.
    savings = SavingsAccount("S-1", 200, interest_rate=0.01)
    checking = BankAccount("C-1", 0)
    assert savings.transfer(checking, 50) is True
    assert checking.balance == 50
    assert isinstance(savings, BankAccount)


def test_negative_interest_rate_is_rejected():
    with pytest.raises(ValueError):
        SavingsAccount("S-1", 100, interest_rate=-0.1)
