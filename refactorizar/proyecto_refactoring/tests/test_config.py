"""Tests de AppConfig: valores por defecto, tipos e invariantes."""

import pytest
from config import AppConfig
from constants import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from exceptions import AppError, ConfigError


def test_valores_por_defecto_validos():
    config = AppConfig()
    assert config.timeout == DEFAULT_TIMEOUT
    assert config.max_retries == DEFAULT_MAX_RETRIES
    assert config.circuit_fail_max == 5
    assert config.circuit_reset_timeout == 30.0
    assert config.debug is True
    assert config.verbose is True


def test_config_error_es_subclase_de_app_error():
    assert issubclass(ConfigError, AppError)


@pytest.mark.parametrize(
    "campo, valor",
    [
        ("debug", "si"),
        ("verbose", 1),
        ("timeout", "30"),
        ("timeout", True),
        ("timeout", 0),
        ("timeout", -5),
        ("max_retries", "3"),
        ("max_retries", True),
        ("max_retries", -1),
        ("circuit_fail_max", "5"),
        ("circuit_fail_max", 0),
        ("circuit_reset_timeout", "30"),
        ("circuit_reset_timeout", 0),
        ("circuit_reset_timeout", -1.0),
    ],
)
def test_configuracion_invalida_lanza_config_error(campo, valor):
    with pytest.raises(ConfigError):
        AppConfig(**{campo: valor})
