"""Tests de MovieService: delegacion, cache y degradacion."""

import json

import pytest
from exceptions import ApiClientError, MovieNotFoundError
from models.movie import Movie
from services.movie_service import MovieService


@pytest.fixture
def service(mocker, omdb_client, favorites, history, cache) -> MovieService:
    """Servicio de peliculas con dependencias inyectadas reales."""
    return MovieService(
        omdb_client=omdb_client,
        favorites=favorites,
        history=history,
        cache=cache,
    )


@pytest.fixture
def omdb_client(config):
    """Cliente OMDB real con api_key de prueba (no se llama a la red)."""
    from api.omdb_client import OmdbClient

    return OmdbClient(config, api_key="test-key")


def test_buscar_por_titulo_exito_guarda_en_cache(service, cache, mocker, omdb_response):
    mocker.patch("api.omdb_client.requests.get", return_value=_respuesta(mocker, omdb_response))
    movie = service.buscar_por_titulo("Inception")
    assert movie.title == "Inception"
    assert cache.get("Inception") is not None


def test_buscar_por_titulo_usa_cache_sin_llamar_api(service, cache, mocker, sample_movie):
    cache.set("Inception", {"Title": "Inception", "Year": "2010", "imdbRating": "8.8"})
    mock_get = mocker.patch(
        "api.omdb_client.requests.get",
        side_effect=AssertionError("no debe llamar a la API"),
    )
    movie = service.buscar_por_titulo("Inception")
    assert movie.title == "Inception"
    assert mock_get.call_count == 0


def test_buscar_por_titulo_api_error_degrada_a_none(service, mocker):
    mocker.patch.object(
        service._omdb_client,
        "buscar_por_titulo",
        side_effect=ApiClientError("fallo"),
    )
    assert service.buscar_por_titulo("Inception") is None


def test_buscar_por_titulo_network_error_degrada_a_none(service, mocker):
    from exceptions import NetworkError

    mocker.patch.object(
        service._omdb_client,
        "buscar_por_titulo",
        side_effect=NetworkError("sin red"),
    )
    assert service.buscar_por_titulo("Inception") is None


def test_buscar_por_titulo_no_encontrada_lanza_movie_not_found(service, mocker):
    mocker.patch.object(service._omdb_client, "buscar_por_titulo", return_value=None)
    with pytest.raises(MovieNotFoundError, match="Inception"):
        service.buscar_por_titulo("Inception")


def test_buscar_por_actor_exito(service, mocker, omdb_response):
    mocker.patch.object(
        service._omdb_client,
        "buscar_por_actor",
        return_value=[omdb_response],
    )
    peliculas = service.buscar_por_actor("DiCaprio")
    assert len(peliculas) == 1
    assert isinstance(peliculas[0], Movie)


def test_buscar_por_actor_degrada_a_lista_vacia(service, mocker):
    mocker.patch.object(
        service._omdb_client,
        "buscar_por_actor",
        side_effect=ApiClientError("fallo"),
    )
    assert service.buscar_por_actor("DiCaprio") == []


def test_populares_devuelve_catalogo_local(service):
    populares = service.populares()
    assert len(populares) == 5
    assert all(isinstance(p, Movie) for p in populares)
    assert populares[0].title == "The Shawshank Redemption"


def test_buscar_por_genero_accion(service):
    peliculas = service.buscar_por_genero("accion")
    assert len(peliculas) == 2
    assert peliculas[0].title == "Die Hard"


def test_buscar_por_genero_comedia(service):
    peliculas = service.buscar_por_genero("Comedia")
    assert len(peliculas) == 2
    assert peliculas[0].title == "Superbad"


def test_buscar_por_genero_otro_combina_catalogos(service):
    peliculas = service.buscar_por_genero("thriller")
    assert len(peliculas) == 4


def test_delegacion_favoritas(service, favorites, sample_movie):
    assert service.agregar_favorita(sample_movie) is True
    assert service.agregar_favorita(sample_movie) is False
    assert favorites.cantidad == 1
    assert service.listar_favoritas()[0].title == "Inception"
    assert service.eliminar_favorita("Inception") is True
    assert service.listar_favoritas() == []


def test_delegacion_historial(service, history, sample_movie):
    service.registrar_busqueda(sample_movie)
    assert history.cantidad == 1
    assert service.listar_historial()[0]["titulo"] == "Inception"
    service.limpiar_historial()
    assert service.listar_historial() == []


def test_estadisticas_combina_repositorios(service, sample_movie):
    service.agregar_favorita(sample_movie)
    service.registrar_busqueda(sample_movie)
    stats = service.estadisticas()
    assert stats == {"total_favoritas": 1, "total_historial": 1}


def test_exportar_a_json(service, favorites, history, sample_movie, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    service.agregar_favorita(sample_movie)
    service.registrar_busqueda(sample_movie)
    service.exportar_a_json("datos.json")
    with open(tmp_path / "datos.json", encoding="utf-8") as f:
        data = json.load(f)
    assert data["favoritas"][0]["title"] == "Inception"
    assert data["historial"][0]["titulo"] == "Inception"
    assert data["estadisticas"]["total_favoritas"] == 1


def test_importar_a_json(service, favorites, history, tmp_path, monkeypatch, sample_movie):
    monkeypatch.chdir(tmp_path)
    archivo = tmp_path / "datos.json"
    archivo.write_text(
        json.dumps(
            {
                "favoritas": [{"Title": "Inception", "Year": "2010", "imdbRating": "8.8"}],
                "historial": [{"titulo": "Inception", "fecha": "hoy"}],
            }
        ),
        encoding="utf-8",
    )
    service.importar_a_json("datos.json")
    assert favorites.listar()[0].title == "Inception"
    assert history.listar()[0]["titulo"] == "Inception"


def test_importar_a_json_sin_claves(service, favorites, history, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "vacio.json").write_text("{}", encoding="utf-8")
    service.importar_a_json("vacio.json")
    assert favorites.listar() == []
    assert history.listar() == []


def _respuesta(mocker, data):
    response = mocker.Mock()
    response.json.return_value = data
    response.status_code = 200
    return response
