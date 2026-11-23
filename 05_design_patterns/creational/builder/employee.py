"""The product: the final employee record."""

from dataclasses import dataclass


# @dataclass (slide 39) generates __init__, __repr__ and __eq__: the Employee
# is a simple data container, as the statement asks. frozen=True makes it
# immutable once built: every change has to go through the builder, which
# validates it.
@dataclass(frozen=True)
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str
    manager_id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: str | None = None
    contract_type: str = "permanent"
