"""Demo: `python -m creational.builder` (run from 05_design_patterns/)."""

from . import DeveloperBuilder, EmployeeBuilder, InternBuilder

# Fluent, readable creation
employee = (
    EmployeeBuilder()
    .with_name("John", "Doe")
    .with_email("john.doe@company.com")
    .with_job("Engineering", "Senior Developer", 75000)
    .with_equipment(laptop=True, parking=False)
    .with_access(vpn=True, admin=True)
    .build()
)
print(employee)

# Or use a preset
dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
intern = InternBuilder("Jane", "Smith", "jane.smith@company.com").with_manager(42).build()
print(dev)
print(intern)
