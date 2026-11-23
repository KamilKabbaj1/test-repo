"""Tests for the Singleton pattern exercise."""

import json

import pytest

from creational.singleton import (
    ConfigManager,
    connect_database,
    process_payment,
    send_email,
    start_application,
)


# autouse: runs around EVERY test of this file. Each test starts without an
# instance, so one test cannot leak its config into another.
@pytest.fixture(autouse=True)
def fresh_singleton():
    ConfigManager.reset()
    yield
    ConfigManager.reset()


@pytest.fixture
def config_file(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"app": {"name": "TestApp", "debug": False}, "database": {"host": "db", "port": 1}}))
    return path


def test_get_instance_returns_the_same_object():
    assert ConfigManager.get_instance() is ConfigManager.get_instance()


def test_direct_instantiation_is_refused():
    ConfigManager.get_instance()
    with pytest.raises(RuntimeError):
        ConfigManager(ConfigManager.DEFAULT_PATH)


def test_file_is_read_only_once(config_file):
    config = ConfigManager.get_instance(config_file)
    config_file.write_text(json.dumps({"app": {"name": "Changed"}}))  # modified on disk
    assert ConfigManager.get_instance().get("app.name") == "TestApp"  # not re-read


def test_get_nested_values_with_dotted_keys():
    config = ConfigManager.get_instance()  # default config.json of the statement
    assert config.get("database.host") == "localhost"
    assert config.get("database.port") == 5432
    assert config.get("app.debug") is True


def test_get_missing_key_returns_default():
    config = ConfigManager.get_instance()
    assert config.get("database.user") is None
    assert config.get("nope.deeper", default="x") == "x"
    assert config.get("app.name.too.deep") is None


def test_changes_are_seen_by_every_module(config_file):
    ConfigManager.get_instance(config_file).set("database.host", "prod-db")
    assert connect_database() == "Connecting to database at prod-db:1"


def test_services_use_the_shared_config():
    assert start_application() == "Starting PaymentPlatform (debug=True)"
    assert process_payment(99.99) == "Processing 99.99€ in sandbox mode"
    assert "no-reply@company.com via smtp.company.com" in send_email("user@test.com", "Welcome")
