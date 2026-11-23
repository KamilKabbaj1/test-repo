"""Preset builder for interns."""

from .employee_builder import EmployeeBuilder


class InternBuilder(EmployeeBuilder):
    """Interns: laptop only, no VPN or admin rights, internship contract.

    The values come from the "intern with minimal access" example of the statement.
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        department: str = "Marketing",
        salary: float = 15000,
    ) -> None:
        super().__init__()
        (
            self.with_name(first_name, last_name)
            .with_email(email)
            .with_job(department, "Intern", salary)
            .with_equipment(laptop=True)
            .with_access(vpn=False, admin=False)
            .with_office("Paris HQ")
            .with_contract("internship")
        )
