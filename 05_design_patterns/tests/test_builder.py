"""Tests for the Builder pattern exercise."""

import dataclasses
from datetime import date

import pytest

from creational.builder import DeveloperBuilder, Employee, EmployeeBuilder, InternBuilder


def minimal_builder():
    return (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Developer", 50000)
    )


def test_fluent_builder_from_statement():
    employee = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .build()
    )
    assert isinstance(employee, Employee)
    assert (employee.first_name, employee.position, employee.salary) == ("John", "Senior Developer", 75000)
    assert employee.has_laptop and employee.has_vpn_access and employee.has_admin_rights
    assert not employee.has_parking


def test_each_step_returns_the_builder():
    builder = EmployeeBuilder()
    assert builder.with_name("A", "B") is builder
    assert builder.with_office("Lyon") is builder


def test_defaults_are_applied():
    employee = minimal_builder().build()
    assert employee.contract_type == "permanent"
    assert employee.start_date == date.today().isoformat()
    assert employee.manager_id is None
    assert not employee.has_admin_rights


@pytest.mark.parametrize(
    ("builder", "message"),
    [
        (EmployeeBuilder().with_email("a@b.c").with_job("X", "Y", 1), "Name is required"),
        (EmployeeBuilder().with_name("A", "B").with_email("nope").with_job("X", "Y", 1), "Valid email"),
        (EmployeeBuilder().with_name("A", "B").with_email("a@b.c"), "Job"),
        (EmployeeBuilder().with_name("A", "B").with_email("a@b.c").with_job("X", "Y", -1), "negative"),
    ],
)
def test_build_validates(builder, message):
    with pytest.raises(ValueError, match=message):
        builder.build()


def test_employee_is_immutable():
    employee = minimal_builder().build()
    with pytest.raises(dataclasses.FrozenInstanceError):
        employee.salary = 1_000_000


def test_senior_developer_preset_gets_admin_rights():
    dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
    assert (dev.department, dev.position, dev.salary) == ("Engineering", "Senior Developer", 75000)
    assert dev.has_laptop and dev.has_vpn_access and dev.has_admin_rights


def test_junior_developer_preset_has_no_admin_rights():
    dev = DeveloperBuilder("Ann", "Lee", "ann@company.com", position="Developer", salary=45000).build()
    assert dev.has_vpn_access and not dev.has_admin_rights


def test_intern_preset_can_still_be_customised():
    intern = InternBuilder("Jane", "Smith", "jane.smith@company.com").with_manager(42).build()
    assert (intern.position, intern.contract_type, intern.manager_id) == ("Intern", "internship", 42)
    assert intern.has_laptop and not intern.has_vpn_access
