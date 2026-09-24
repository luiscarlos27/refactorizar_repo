"""Tests de SeriesService: delegacion, cache y degradacion."""

import pytest
from exceptions import ApiClientError, SeriesNotFoundError
from models.series import Series
from services.series_service import SeriesService


@pytest.fixture
def service(mocker, tvmaze_client, cache) -> SeriesService:
    """Servicio de series con dependencias inyectadas reales."""
    return SeriesService(tvmaze_client=tvmaze_client, cache=cache)


@pytest.fixture
def tvmaze_client(config):
    """Cliente TVMaze real (no se llama a la red)."""
    from api.tvmaze_client import TvmazeClient

    return TvmazeClient(config)


def test_buscar_exito_guarda_en_cache(service, cache, mocker, tvmaze_response):
    mocker.patch.object(service._client, "buscar_series", return_value=[tvmaze_response])
    series = service.buscar("Breaking Bad")
    assert len(series) == 1
    assert isinstance(series[0], Series)
    assert cache.get("series_Breaking Bad") is not None


def test_buscar_usa_cache_sin_llamar_api(service, cache, mocker, tvmaze_response):
    cache.set("series_Breaking Bad", [tvmaze_response])
    mock_buscar = mocker.patch.object(
        service._client,
        "buscar_series",
        side_effect=AssertionError("no debe llamar a la API"),
    )
    series = service.buscar("Breaking Bad")
    assert series[0].name == "Breaking Bad"
    assert mock_buscar.call_count == 0


def test_buscar_api_error_degrada_a_lista_vacia(service, mocker):
    mocker.patch.object(service._client, "buscar_series", side_effect=ApiClientError("fallo"))
    assert service.buscar("Breaking Bad") == []


def test_buscar_network_error_degrada_a_lista_vacia(service, mocker):
    from exceptions import NetworkError

    mocker.patch.object(service._client, "buscar_series", side_effect=NetworkError("sin red"))
    assert service.buscar("Breaking Bad") == []


def test_buscar_sin_resultados_lanza_series_not_found(service, mocker):
    mocker.patch.object(service._client, "buscar_series", return_value=[])
    with pytest.raises(SeriesNotFoundError, match="Breaking Bad"):
        service.buscar("Breaking Bad")


def test_obtener_detalles_exito(service, mocker, tvmaze_response):
    mocker.patch.object(service._client, "obtener_detalles", return_value=tvmaze_response)
    serie = service.obtener_detalles(169)
    assert serie is not None
    assert serie.name == "Breaking Bad"


def test_obtener_detalles_api_error_degrada_a_none(service, mocker):
    mocker.patch.object(service._client, "obtener_detalles", side_effect=ApiClientError("fallo"))
    assert service.obtener_detalles(169) is None
