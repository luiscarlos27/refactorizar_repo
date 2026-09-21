"""Industrial sensor telemetry and alert system."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol
import logging

logger = logging.getLogger(__name__)


class AlertLevel(str, Enum):
    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"


class SensorType(str, Enum):
    TEMPERATURE = "temp"
    PRESSURE = "press"


@dataclass(frozen=True)
class SensorConfig:
    temp_limit: float = 80.0
    press_limit: float = 100.0
    log_path: Path = Path("alerts.log")


@dataclass(frozen=True)
class SensorReading:
    sensor_type: SensorType
    value: float
    location: str = "unknown"


@dataclass
class Alert:
    message: str
    level: AlertLevel
    sensor_type: SensorType
    location: str


class AlertStorage(Protocol):
    def add(self, alert: Alert) -> None:
        ...

    def get_all(self) -> list[Alert]:
        ...


class InMemoryAlertStorage:
    def __init__(self) -> None:
        self._alerts: list[Alert] = []

    def add(self, alert: Alert) -> None:
        self._alerts.append(alert)

    def get_all(self) -> list[Alert]:
        return self._alerts.copy()


class AlertLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path

    def log(self, alert: Alert) -> None:
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"{alert.level.value.upper()}: {alert.message}\n")
        logger.info("Alert logged", extra={"level": alert.level.value})


class SensorProcessor(Protocol):
    def process(self, reading: SensorReading, config: SensorConfig) -> Alert:
        ...


class TemperatureProcessor:
    def process(self, reading: SensorReading, config: SensorConfig) -> Alert:
        value = reading.value
        if value > config.temp_limit:
            return Alert(
                message=f"High Temp {value} in {reading.location}",
                level=AlertLevel.CRITICAL,
                sensor_type=SensorType.TEMPERATURE,
                location=reading.location,
            )
        elif value > config.temp_limit - 10:
            return Alert(
                message=f"Temp high {value} in {reading.location}",
                level=AlertLevel.WARNING,
                sensor_type=SensorType.TEMPERATURE,
                location=reading.location,
            )
        else:
            return Alert(
                message=f"Temp OK {value}",
                level=AlertLevel.OK,
                sensor_type=SensorType.TEMPERATURE,
                location=reading.location,
            )


class PressureProcessor:
    def process(self, reading: SensorReading, config: SensorConfig) -> Alert:
        value = reading.value
        if value > config.press_limit:
            return Alert(
                message=f"High Pressure {value} in {reading.location}",
                level=AlertLevel.CRITICAL,
                sensor_type=SensorType.PRESSURE,
                location=reading.location,
            )
        else:
            return Alert(
                message=f"Pressure OK {value}",
                level=AlertLevel.OK,
                sensor_type=SensorType.PRESSURE,
                location=reading.location,
            )


class SensorManager:
    def __init__(
        self,
        config: SensorConfig | None = None,
        alert_storage: AlertStorage | None = None,
        alert_logger: AlertLogger | None = None,
    ):
        self.config = config or SensorConfig()
        self.alert_storage = alert_storage or InMemoryAlertStorage()
        self.alert_logger = alert_logger or AlertLogger(self.config.log_path)
        self._processors: dict[SensorType, SensorProcessor] = {
            SensorType.TEMPERATURE: TemperatureProcessor(),
            SensorType.PRESSURE: PressureProcessor(),
        }

    def process_readings(
        self,
        readings: list[SensorReading],
        notify: bool = True,
    ) -> int:
        critical_count = 0

        for reading in readings:
            processor = self._processors.get(reading.sensor_type)
            if processor is None:
                logger.warning("Unknown sensor type", extra={"type": reading.sensor_type})
                continue

            alert = processor.process(reading, self.config)

            if alert.level == AlertLevel.CRITICAL:
                self.alert_storage.add(alert)
                self.alert_logger.log(alert)
                critical_count += 1

                if notify:
                    self._send_notification(alert)

            logger.info(
                "Reading processed",
                extra={
                    "level": alert.level.value,
                    "sensor_type": reading.sensor_type.value,
                    "location": reading.location,
                },
            )

        return critical_count

    def _send_notification(self, alert: Alert) -> None:
        match alert.sensor_type:
            case SensorType.TEMPERATURE:
                logger.info(f"SENDING EMAIL: {alert.message}")
            case SensorType.PRESSURE:
                logger.info(f"SENDING SMS: {alert.message}")

    def get_alerts(self) -> list[Alert]:
        return self.alert_storage.get_all()
