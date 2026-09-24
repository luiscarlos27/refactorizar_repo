"""Tests de TvmazeClient con HTTP mockeado (sin red real)."""

import pybreaker
import pytest
import requests
from api.tvmaze_client import TvmazeClient
from constants import TVMAZE_BASE_URL
from exceptions import ApiClientError, NetworkError

MODULO = "api.tvmaze_client"


@pytest.fixture
def client(config) -> TvmazeClient:
    """Cliente TVMaze con configuracion por defecto."""
    return TvmazeClient(config)


def _mock_response(mocker, data):
    response = mocker.Mock()
    response.json.return_value = data
    response.status_code = 200
    return response


def test_buscar_series_con_resultados(client, mocker, tvmaze_response):
    mock_get = mocker.patch(
        f"{MODULO}.requests.get",
        return_value=_mock_response(mocker, [tvmaze_response]),
    )
    resultados = client.buscar_series("Breaking Bad")
    assert resultados == [tvmaze_response]
    _, kwargs = mock_get.call_args
    assert kwargs["params"] == {"q": "Breaking Bad"}
    assert kwargs["timeout"] == client._config.timeout


def test_buscar_series_sin_resultados(client, mocker):
    mocker.patch(f"{MODULO}.requests.get", return_value=_mock_response(mocker, []))
    assert client.buscar_series("NoExiste") == []


def test_obtener_detalles(client, mocker, tvmaze_response):
    mock_get = mocker.patch(
        f"{MODULO}.requests.get",
        return_value=_mock_response(mocker, tvmaze_response),
    )
    datos = client.obtener_detalles(169)
    assert datos == tvmaze_response
    args, kwargs = mock_get.call_args
    assert args[0] == f"{TVMAZE_BASE_URL}/shows/169"
    assert kwargs["params"] is None


def test_timeout_se_traduce_a_network_error(client, mocker):
    mocker.patch(
        f"{MODULO}.requests.get",
        side_effect=requests.exceptions.Timeout("timeout"),
    )
    with pytest.raises(NetworkError, match="Timeout al contactar TVMaze"):
        client._request(f"{TVMAZE_BASE_URL}/shows/1", None)


def test_connection_error_se_traduce_a_network_error(client, mocker):
    mocker.patch(
        f"{MODULO}.requests.get",
        side_effect=requests.exceptions.ConnectionError("down"),
    )
    with pytest.raises(NetworkError, match="Fallo de conexion con TVMaze"):
        client._request(f"{TVMAZE_BASE_URL}/shows/1", None)


def test_request_exception_se_traduce_a_api_client_error(client, mocker):
    mocker.patch(
        f"{MODULO}.requests.get",
        side_effect=requests.exceptions.RequestException("http"),
    )
    with pytest.raises(ApiClientError, match="Error HTTP de TVMaze"):
        client._request(f"{TVMAZE_BASE_URL}/shows/1", None)


def test_breaker_abierto_lanza_network_error(client, mocker):
    mocker.patch.object(
        client,
        "_breaker",
        **{"call.side_effect": pybreaker.CircuitBreakerError("open")},
    )
    with pytest.raises(NetworkError, match="circuito abierto"):
        client.buscar_series("Breaking Bad")
