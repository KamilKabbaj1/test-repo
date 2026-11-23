"""Preset builder for developers."""

from .employee_builder import EmployeeBuilder


class DeveloperBuilder(EmployeeBuilder):
    """Pre-fills the usual developer setup, which can still be changed before build().

    The values come from the "developer with full access" example of the
    statement. This solves the "hidden logic" smell: the rule "a senior developer
    always gets admin rights" is written once here, instead of being remembered
    by whoever calls create_employee.
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        position: str = "Senior Developer",
        salary: float = 75000,
    ) -> None:
        super().__init__()
        is_senior = position.startswith("Senior")
        (
            self.with_name(first_name, last_name)
            .with_email(email)
            .with_job("Engineering", position, salary)
            .with_equipment(laptop=True)
            .with_access(vpn=True, admin=is_senior)
            .with_office("Paris HQ")
        )
