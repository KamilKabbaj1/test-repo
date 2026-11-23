"""The four services of the statement, refactored.

`load_config()` is replaced by `ConfigManager.get_instance()`: the first call
reads the file, the next ones reuse the same object (no I/O). The functions return
their message instead of printing it, so they are easy to test. The demo prints them.
"""

from .config_manager import ConfigManager


def start_application() -> str:
    config = ConfigManager.get_instance()
    return f"Starting {config.get('app.name')} (debug={config.get('app.debug')})"


def connect_database() -> str:
    config = ConfigManager.get_instance()
    return f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}"


def send_email(to: str, subject: str) -> str:
    config = ConfigManager.get_instance()
    return (
        f"Sending email '{subject}' to {to} from {config.get('email.sender')} "
        f"via {config.get('email.smtp_host')}"
    )


def process_payment(amount: float) -> str:
    config = ConfigManager.get_instance()
    return f"Processing {amount}€ in {config.get('payment.environment')} mode"
