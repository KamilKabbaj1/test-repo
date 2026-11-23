"""Inheritance exercises (slide 67).

Statement: https://gist.github.com/bdallard/b2f2c910e3a9b564a30c86991c97b4fc

Key ideas (slides 34-35):
- inheritance = a child class reuses the attributes and methods of its parent
  ("is-a" relationship: a Car IS A Vehicle);
- polymorphism = the same method name gives a different behaviour depending
  on the real class of the object, so code can treat all children uniformly.
"""


# --------------------------------------------------------------------------
# Problem 1 - Vehicle / Car / Bicycle: overriding a method
# --------------------------------------------------------------------------
class Vehicle:
    # Not an ABC: the statement wants `Vehicle().drive()` to work and return
    # "Driving a vehicle", so the parent must be instantiable.
    def drive(self) -> str:
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self) -> str:
        # Overriding: same signature as the parent, new behaviour.
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self) -> str:
        return "Riding a bicycle"


# --------------------------------------------------------------------------
# Problem 2 - Person / Student / Employee: extending __init__ with super()
# --------------------------------------------------------------------------
class Person:
    def __init__(self, name: str, age: int, address: str) -> None:
        self.name = name
        self.age = age
        self.address = address

    def introduce(self) -> str:
        return f"Hi, I'm {self.name}, {self.age} years old, living at {self.address}."


class Student(Person):
    def __init__(self, name: str, age: int, address: str, field_of_study: str) -> None:
        # super().__init__ lets the parent set its own attributes: the code is
        # not duplicated, and a change in Person is automatically inherited.
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self) -> str:
        # Reuse the parent sentence and add the specific part (extension,
        # rather than rewriting everything).
        return f"{super().introduce()} I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name: str, age: int, address: str, company: str) -> None:
        super().__init__(name, age, address)
        self.company = company

    def introduce(self) -> str:
        return f"{super().introduce()} I work at {self.company}."


# --------------------------------------------------------------------------
# Problem 3 - BankAccount / SavingsAccount
# --------------------------------------------------------------------------
class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0) -> None:
        if balance < 0:
            raise ValueError("initial balance must be non-negative")
        self.account_number = account_number
        # Leading underscore = "internal, don't touch from outside" (Python
        # convention, slide 58). The only way to change the balance is through
        # deposit / withdraw, which check the amounts: the balance can never
        # become negative or be set to an arbitrary value.
        self._balance = balance

    @property
    def balance(self) -> float:
        # Read-only property: `account.balance` works, `account.balance = 1e6`
        # raises AttributeError because there is no setter.
        return self._balance

    @staticmethod
    def _check_amount(amount: float) -> None:
        # Shared by deposit and withdraw: the rule is written only once.
        # A negative deposit would actually be a hidden withdrawal.
        if amount <= 0:
            raise ValueError("amount must be positive")

    def deposit(self, amount: float) -> None:
        self._check_amount(amount)
        self._balance += amount

    def withdraw(self, amount: float) -> bool:
        """Withdraw `amount`. Return False (and change nothing) if the balance is too low."""
        self._check_amount(amount)
        # Not enough money is a normal business case, not a programming
        # error, so it is reported with a boolean instead of an exception.
        # It is the same convention as the one asked for transfer().
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def transfer(self, destination: "BankAccount", amount: float) -> bool:
        """Move `amount` to `destination`. Return False if the balance is insufficient."""
        # Reuse withdraw/deposit instead of touching _balance directly: the
        # checks stay in one place, and a subclass that overrides withdraw
        # (fees, overdraft...) is automatically respected.
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.account_number!r}, balance={self._balance})"


class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, balance: float = 0.0, interest_rate: float = 0.0) -> None:
        super().__init__(account_number, balance)
        if interest_rate < 0:
            raise ValueError("interest rate must be non-negative")
        self.interest_rate = interest_rate  # e.g. 0.03 for 3 %

    def add_interest(self) -> float:
        """Add the interests to the balance and return the amount added."""
        interest = self._balance * self.interest_rate
        # Protected attribute: accessible to the subclass by convention, no
        # need to go through deposit (which refuses an amount of 0).
        self._balance += interest
        return interest

    def check_balance(self) -> float:
        # Asked by the statement. It simply returns the read-only property.
        return self.balance
