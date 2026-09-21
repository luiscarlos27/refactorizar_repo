"""Tests for sensor telemetry system."""

import pytest
from pathlib import Path
from src.sensor_telemetry import (
    SensorConfig,
    SensorReading,
    SensorType,
    AlertLevel,
    SensorManager,
    InMemoryAlertStorage,
    AlertLogger,
)


@pytest.fixture
def config():
    return SensorConfig(temp_limit=80.0, press_limit=100.0)


@pytest.fixture
def manager(config):
    return SensorManager(config=config)


def test_temperature_critical_alert(manager):
    readings = [
        SensorReading(sensor_type=SensorType.TEMPERATURE, value=95.0, location="Zone-A"),
    ]

    critical_count = manager.process_readings(readings, notify=False)

    assert critical_count == 1
    alerts = manager.get_alerts()
    assert len(alerts) == 1
    assert alerts[0].level == AlertLevel.CRITICAL
    assert "High Temp" in alerts[0].message


def test_pressure_critical_alert(manager):
    readings = [
        SensorReading(sensor_type=SensorType.PRESSURE, value=110.0, location="Zone-B"),
    ]

    critical_count = manager.process_readings(readings, notify=False)

    assert critical_count == 1
    alerts = manager.get_alerts()
    assert alerts[0].level == AlertLevel.CRITICAL


def test_normal_readings(manager):
    readings = [
        SensorReading(sensor_type=SensorType.TEMPERATURE, value=75.0, location="Zone-A"),
        SensorReading(sensor_type=SensorType.PRESSURE, value=90.0, location="Zone-B"),
    ]

    critical_count = manager.process_readings(readings, notify=False)

    assert critical_count == 0
    assert len(manager.get_alerts()) == 0


def test_temperature_warning(manager):
    readings = [
        SensorReading(sensor_type=SensorType.TEMPERATURE, value=75.0, location="Zone-A"),
    ]

    critical_count = manager.process_readings(readings, notify=False)

    assert critical_count == 0


def test_unknown_sensor_type(manager):
    readings = [
        SensorReading(sensor_type="unknown", value=50.0, location="Zone-C"),
    ]

    critical_count = manager.process_readings(readings, notify=False)
    assert critical_count == 0


def test_log_file_creation(tmp_path):
    log_file = tmp_path / "alerts.log"
    config = SensorConfig(log_path=log_file)
    manager = SensorManager(config=config)

    readings = [
        SensorReading(sensor_type=SensorType.TEMPERATURE, value=95.0, location="Zone-A"),
    ]

    manager.process_readings(readings, notify=False)

    assert log_file.exists()
    content = log_file.read_text()
    assert "CRITICAL" in content


def test_multiple_readings_mixed_alerts(manager):
    readings = [
        SensorReading(sensor_type=SensorType.TEMPERATURE, value=95.0, location="Zone-A"),
        SensorReading(sensor_type=SensorType.PRESSURE, value=90.0, location="Zone-B"),
        SensorReading(sensor_type=SensorType.TEMPERATURE, value=75.0, location="Zone-C"),
    ]

    critical_count = manager.process_readings(readings, notify=False)

    assert critical_count == 1
    alerts = manager.get_alerts()
    assert len(alerts) == 1
    assert alerts[0].sensor_type == SensorType.TEMPERATURE


def test_custom_alert_storage():
    storage = InMemoryAlertStorage()
    config = SensorConfig()
    manager = SensorManager(config=config, alert_storage=storage)

    readings = [
        SensorReading(sensor_type=SensorType.TEMPERATURE, value=95.0, location="Zone-A"),
    ]

    manager.process_readings(readings, notify=False)

    assert len(storage.get_all()) == 1
