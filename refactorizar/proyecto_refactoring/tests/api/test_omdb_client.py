"""Tests de OmdbClient con HTTP mockeado (sin red real)."""

import pybreaker
import pytest
import requests
from api.omdb_client import OmdbClient, _crear_retrier
from config import AppConfig
from exceptions import ApiClientError, NetworkError

MODULO = "api.omdb_client"


@pytest.fixture
def client(config) -> OmdbClient:
    """Cliente OMDB con api_key de prueba."""
    return OmdbClient(config, api_key="test-key")


def _mock_response(mocker, data):
    response = mocker.Mock()
    response.json.return_value = data
    response.status_code = 200
    return response


def test_buscar_por_titulo_encontrada(client, mocker, omdb_response):
    mocker.patch(f"{MODULO}.requests.get", return_value=_mock_response(mocker, omdb_response))
    datos = client.buscar_por_titulo("Inception")
    assert datos == omdb_response
    assert datos is not None and datos["Title"] == "Inception"


def test_buscar_por_titulo_no_encontrada(client, mocker):
    mocker.patch(
        f"{MODULO}.requests.get",
        return_value=_mock_response(mocker, {"Response": "False"}),
    )
    assert client.buscar_por_titulo("NoExiste") is None


def test_buscar_por_actor_con_resultados(client, mocker, omdb_response):
    mocker.patch(
        f"{MODULO}.requests.get",
        return_value=_mock_response(mocker, {"Response": "True", "Search": [omdb_response]}),
    )
    resultados = client.buscar_por_actor("DiCaprio")
    assert resultados == [omdb_response]


def test_buscar_por_actor_sin_resultados(client, mocker):
    mocker.patch(
        f"{MODULO}.requests.get",
        return_value=_mock_response(mocker, {"Response": "False"}),
    )
    assert client.buscar_por_actor("Nadie") == []


def test_timeout_se_traduce_a_network_error(config, mocker):
    client = OmdbClient(config, api_key="test-key")
    mocker.patch(
        f"{MODULO}.requests.get",
        side_effect=requests.exceptions.Timeout("timeout"),
    )
    with pytest.raises(NetworkError, match="Timeout al contactar OMDB"):
        client._request({"t": "x", "apikey": "test-key"})


def test_connection_error_se_traduce_a_network_error(config, mocker):
    client = OmdbClient(config, api_key="test-key")
    mocker.patch(
        f"{MODULO}.requests.get",
        side_effect=requests.exceptions.ConnectionError("down"),
    )
    with pytest.raises(NetworkError, match="Fallo de conexion con OMDB"):
        client._request({"t": "x", "apikey": "test-key"})


def test_request_exception_se_traduce_a_api_client_error(config, mocker):
    client = OmdbClient(config, api_key="test-key")
    mocker.patch(
        f"{MODULO}.requests.get",
        side_effect=requests.exceptions.RequestException("http"),
    )
    with pytest.raises(ApiClientError, match="Error HTTP de OMDB"):
        client._request({"t": "x", "apikey": "test-key"})


def test_breaker_abierto_lanza_network_error(client, mocker):
    mocker.patch.object(
        client,
        "_breaker",
        **{"call.side_effect": pybreaker.CircuitBreakerError("open")},
    )
    with pytest.raises(NetworkError, match="circuito abierto"):
        client.buscar_por_titulo("Inception")


def test_retrier_reraise_tras_intentos(config, mocker):
    config_rapido = AppConfig(max_retries=1)
    client = OmdbClient(config_rapido, api_key="test-key")
    mock_get = mocker.patch(
        f"{MODULO}.requests.get",
        side_effect=requests.exceptions.ConnectionError("down"),
    )
    with pytest.raises(NetworkError):
        client.buscar_por_titulo("Inception")
    assert mock_get.call_count == 1


def test_crear_retrier_devuelve_retrier(config):
    retrier = _crear_retrier(config)
    assert hasattr(retrier, "stop")


def test_verbose_false_no_logs_debug(config, mocker, omdb_response):
    config_silencioso = AppConfig(verbose=False)
    client = OmdbClient(config_silencioso, api_key="test-key")
    mocker.patch(f"{MODULO}.requests.get", return_value=_mock_response(mocker, omdb_response))
    assert client.buscar_por_titulo("Inception") is not None
