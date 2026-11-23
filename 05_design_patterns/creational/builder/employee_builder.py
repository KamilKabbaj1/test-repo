"""Fluent builder: build an Employee step by step, by name instead of by position."""

from __future__ import annotations

from datetime import date

from .employee import Employee


class EmployeeBuilder:
    def __init__(self) -> None:
        # Every optional setting starts with its default value: the caller only
        # writes what differs, so there is no list of 17 positional arguments.
        self._fields: dict = {
            "start_date": date.today().isoformat(),
            "contract_type": "permanent",
        }

    # Each step stores its values and returns `self`: this is what allows the
    # chaining .with_name(...).with_job(...).build(). Each method groups
    # related values (name, job, equipment...), so the code reads like a sentence.
    def with_name(self, first_name: str, last_name: str) -> EmployeeBuilder:
        self._fields.update(first_name=first_name, last_name=last_name)
        return self

    def with_email(self, email: str) -> EmployeeBuilder:
        self._fields["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float) -> EmployeeBuilder:
        self._fields.update(department=department, position=position, salary=salary)
        return self

    def with_start_date(self, start_date: str) -> EmployeeBuilder:
        self._fields["start_date"] = start_date
        return self

    def with_manager(self, manager_id: int) -> EmployeeBuilder:
        self._fields["manager_id"] = manager_id
        return self

    def with_contact(
        self,
        phone: str | None = None,
        address: str | None = None,
        emergency_contact: str | None = None,
    ) -> EmployeeBuilder:
        self._fields.update(phone=phone, address=address, emergency_contact=emergency_contact)
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False) -> EmployeeBuilder:
        # Keyword arguments: `laptop=True` is readable, a bare `True` is not.
        self._fields.update(has_laptop=laptop, has_parking=parking)
        return self

    def with_access(self, vpn: bool = False, admin: bool = False) -> EmployeeBuilder:
        self._fields.update(has_vpn_access=vpn, has_admin_rights=admin)
        return self

    def with_office(self, office_location: str) -> EmployeeBuilder:
        self._fields["office_location"] = office_location
        return self

    def with_contract(self, contract_type: str) -> EmployeeBuilder:
        self._fields["contract_type"] = contract_type
        return self

    def build(self) -> Employee:
        # All the validation is in ONE place, run once, just before creating
        # the product. In the old code it was scattered after the dict creation.
        fields = self._fields
        if not fields.get("first_name") or not fields.get("last_name"):
            raise ValueError("Name is required")
        if "@" not in (fields.get("email") or ""):
            raise ValueError("Valid email is required")
        if "position" not in fields:
            raise ValueError("Job (department, position, salary) is required")
        if fields["salary"] < 0:
            raise ValueError("Salary cannot be negative")
        return Employee(**fields)
