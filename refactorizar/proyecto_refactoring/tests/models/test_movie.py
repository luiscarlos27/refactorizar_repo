"""Tests del modelo Movie: creacion, validacion y conversion."""

import pytest
from models.movie import Movie, _flotante, _texto


def test_creacion_con_valores_minimos():
    movie = Movie(title="Inception")
    assert movie.title == "Inception"
    assert movie.year is None
    assert movie.rating is None


def test_anio_invalido_lanza_value_error():
    with pytest.raises(ValueError, match="Anio invalido"):
        Movie(title="Old", year="1800")


def test_anio_futuro_valido():
    from datetime import datetime

    anio = str(datetime.now().year + 1)
    movie = Movie(title="Futura", year=anio)
    assert movie.year == anio


@pytest.mark.parametrize("rating", [-0.1, 10.1, 11.0])
def test_rating_fuera_de_rango_lanza_value_error(rating):
    with pytest.raises(ValueError, match="Rating invalido"):
        Movie(title="X", rating=rating)


@pytest.mark.parametrize("rating", [0.0, 5.5, 10.0])
def test_rating_valido(rating):
    assert Movie(title="X", rating=rating).rating == rating


def test_anio_no_numerico_no_valida_rango():
    movie = Movie(title="X", year="N/A")
    assert movie.year == "N/A"


def test_from_omdb_con_claves_originales(omdb_response):
    movie = Movie.from_omdb(omdb_response)
    assert movie.title == "Inception"
    assert movie.year == "2010"
    assert movie.rating == 8.8
    assert movie.genre == "Sci-Fi"
    assert movie.director == "Christopher Nolan"
    assert movie.actors == "Leonardo DiCaprio"
    assert movie.plot.startswith("Un ladron")
    assert movie.country == "USA"
    assert movie.awards == "4 Oscars"


def test_from_omdb_con_claves_normalizadas():
    movie = Movie.from_omdb({"title": "Memento", "year": "2000", "rating": "8.4"})
    assert movie.title == "Memento"
    assert movie.year == "2000"
    assert movie.rating == 8.4


def test_from_omdb_sin_datos_relevante_titulo_desconocida():
    movie = Movie.from_omdb({})
    assert movie.title == "Desconocida"
    assert movie.year is None
    assert movie.rating is None


def test_from_omdb_con_campos_na():
    movie = Movie.from_omdb({"Title": "X", "Year": "N/A", "imdbRating": "N/A"})
    assert movie.year is None
    assert movie.rating is None


def test_to_dict_serializa_todos_los_campos(omdb_response):
    movie = Movie.from_omdb(omdb_response)
    datos = movie.to_dict()
    assert datos["title"] == "Inception"
    assert datos["year"] == "2010"
    assert datos["rating"] == 8.8
    assert set(datos) == {
        "title",
        "year",
        "rating",
        "genre",
        "director",
        "actors",
        "plot",
        "country",
        "awards",
    }


@pytest.mark.parametrize(
    "valor, esperado",
    [(None, None), ("", None), ("N/A", None), ("2010", "2010"), (1994, "1994")],
)
def test_texto_conversion(valor, esperado):
    assert _texto(valor) == esperado


@pytest.mark.parametrize(
    "valor, esperado",
    [(None, None), ("", None), ("N/A", None), ("8.8", 8.8), ("abc", None), (8, 8.0)],
)
def test_flotante_conversion(valor, esperado):
    assert _flotante(valor) == esperado
