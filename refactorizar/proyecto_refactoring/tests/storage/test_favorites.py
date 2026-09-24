"""Tests del FavoritesRepository: estado y persistencia JSON."""

from models.movie import Movie
from storage.favorites_repository import FavoritesRepository


def test_agregar_y_listar(sample_movie):
    repo = FavoritesRepository()
    assert repo.agregar(sample_movie) is True
    assert repo.cantidad == 1
    assert repo.listar()[0].title == "Inception"


def test_agregar_duplicado_por_titulo_devuelve_false(sample_movie):
    repo = FavoritesRepository()
    repo.agregar(sample_movie)
    assert repo.agregar(Movie(title="Inception")) is False
    assert repo.cantidad == 1


def test_listar_devuelve_copia(sample_movie):
    repo = FavoritesRepository()
    repo.agregar(sample_movie)
    copia = repo.listar()
    copia.clear()
    assert repo.cantidad == 1


def test_eliminar_existente_y_no_existente(sample_movie):
    repo = FavoritesRepository()
    repo.agregar(sample_movie)
    assert repo.eliminar("Inception") is True
    assert repo.eliminar("Inception") is False
    assert repo.cantidad == 0


def test_to_json_list_serializa(sample_movie):
    repo = FavoritesRepository()
    repo.agregar(sample_movie)
    datos = repo.to_json_list()
    assert datos == [sample_movie.to_dict()]


def test_cargar_reemplaza_el_estado():
    repo = FavoritesRepository()
    repo.agregar(Movie(title="Vieja"))
    repo.cargar([{"Title": "Inception", "Year": "2010", "imdbRating": "8.8"}])
    assert repo.cantidad == 1
    assert repo.listar()[0].title == "Inception"


def test_cargar_lista_vacia():
    repo = FavoritesRepository()
    repo.agregar(Movie(title="Vieja"))
    repo.cargar([])
    assert repo.cantidad == 0
