"""Singleton configuration manager: the file is read once, the instance is shared."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigManager:
    # Default file: next to this module, so it is found whatever the current
    # directory is (the old code depended on where the program was launched).
    DEFAULT_PATH = Path(__file__).with_name("config.json")

    # The single instance, stored on the CLASS: shared by every module.
    _instance: ConfigManager | None = None

    def __init__(self, path: Path) -> None:
        # Guard: a second `ConfigManager(...)` would silently create a second
        # copy of the config, which is exactly what the pattern forbids.
        if ConfigManager._instance is not None:
            raise RuntimeError("ConfigManager is a singleton: use ConfigManager.get_instance()")
        self.path = Path(path)
        with self.path.open(encoding="utf-8") as file:
            self._data: dict = json.load(file)

    # @classmethod (slide 87): the method works on the class itself, so it can
    # be called before any instance exists.
    @classmethod
    def get_instance(cls, path: Path | str | None = None) -> ConfigManager:
        """Return THE instance, reading the file only on the first call.

        `path` is only used on that first call (e.g. a test config file).
        """
        if cls._instance is None:
            cls._instance = cls(Path(path) if path else cls.DEFAULT_PATH)
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Forget the instance: the next get_instance() reloads the file.

        Useful for tests (problem 4, "hard to mock"): there is now one single
        point to override.
        """
        cls._instance = None

    def get(self, key: str, default: Any = None) -> Any:
        """Read a nested value with a dotted key: get("database.host")."""
        value: Any = self._data
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, key: str, value: Any) -> None:
        """Change a value in memory: every module sees it, since they share the instance.

        This fixes problem 3 (changes not synchronized).
        """
        *parents, last = key.split(".")
        node = self._data
        for part in parents:
            node = node.setdefault(part, {})
        node[last] = value
