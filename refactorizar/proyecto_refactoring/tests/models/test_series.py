"""Tests del modelo Series: construccion desde TVMaze y conversion."""

from models.series import Series, _rating_promedio, _texto


def test_from_tvmaze_con_detalles_directos(tvmaze_response):
    serie = Series.from_tvmaze(tvmaze_response)
    assert serie.id_ == 169
    assert serie.name == "Breaking Bad"
    assert serie.language == "English"
    assert serie.genres == ["Drama", "Crime"]
    assert serie.rating == 9.3
    assert serie.status == "Ended"
    assert serie.premiered == "2008-01-20"
    assert serie.ended == "2013-09-29"
    assert serie.runtime == 60
    assert serie.summary == "<p>Un profesor de quimica.</p>"


def test_from_tvmaze_con_resultado_de_busqueda(tvmaze_response):
    serie = Series.from_tvmaze({"show": tvmaze_response})
    assert serie.id_ == 169
    assert serie.name == "Breaking Bad"


def test_from_tvmaze_sin_datos():
    serie = Series.from_tvmaze({})
    assert serie.id_ is None
    assert serie.name == ""
    assert serie.genres == []
    assert serie.rating is None


def test_from_tvmaze_generos_no_lista():
    serie = Series.from_tvmaze({"id": 1, "name": "X", "genres": "Drama"})
    assert serie.genres == []


def test_from_tvmaze_rating_sin_promedio():
    serie = Series.from_tvmaze({"id": 1, "name": "X", "rating": {"average": None}})
    assert serie.rating is None


def test_from_tvmaze_rating_formato_invalido():
    serie = Series.from_tvmaze({"id": 1, "name": "X", "rating": {"average": "abc"}})
    assert serie.rating is None


def test_from_tvmaze_rating_no_diccionario():
    serie = Series.from_tvmaze({"id": 1, "name": "X", "rating": 9.0})
    assert serie.rating is None


def test_rating_promedio_auxiliar():
    assert _rating_promedio({"average": "7.5"}) == 7.5
    assert _rating_promedio(None) is None
    assert _rating_promedio("no-dict") is None


def test_texto_auxiliar():
    assert _texto(None) is None
    assert _texto("") is None
    assert _texto("Ended") == "Ended"
