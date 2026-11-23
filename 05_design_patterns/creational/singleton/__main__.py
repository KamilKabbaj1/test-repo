"""Demo: `python -m creational.singleton` (run from 05_design_patterns/)."""

from . import ConfigManager, connect_database, process_payment, send_email, start_application

# Config loaded ONCE for the whole request (it was loaded 4 times before).
print(start_application())
print(connect_database())
print(send_email("user@test.com", "Welcome"))
print(process_payment(99.99))

config = ConfigManager.get_instance()
print("Same instance:", config is ConfigManager.get_instance())
