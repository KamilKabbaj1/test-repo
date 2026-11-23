"""Singleton pattern exercise: configuration manager."""

from .config_manager import ConfigManager
from .services import connect_database, process_payment, send_email, start_application

__all__ = ["ConfigManager", "connect_database", "process_payment", "send_email", "start_application"]
