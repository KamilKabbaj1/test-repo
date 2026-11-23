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
