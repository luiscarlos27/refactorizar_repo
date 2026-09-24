"""Tests de la jerarquia de excepciones de dominio."""

from exceptions import (
    ApiClientError,
    AppError,
    ConfigError,
    MovieNotFoundError,
    NetworkError,
    SeriesNotFoundError,
)


def test_base_comun_cubre_todas_las_subclases():
    subclases = [
        ApiClientError,
        NetworkError,
        MovieNotFoundError,
        SeriesNotFoundError,
        ConfigError,
    ]
    for subclase in subclases:
        assert issubclass(subclase, AppError)


def test_network_error_es_subclase_de_api_client_error():
    assert issubclass(NetworkError, ApiClientError)


def test_mensajes_descriptivos():
    assert str(MovieNotFoundError("Inception")) == "Inception"
    assert str(SeriesNotFoundError("Lost")) == "Lost"
