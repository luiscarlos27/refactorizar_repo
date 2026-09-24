"""Fixtures reutilizables de la suite de tests.

Ajusta ``sys.path`` para importar los modulos del paquete (imports planos)
y provee clientes mockeados, repositorios con directorio temporal y modelos
de ejemplo sin acceso a la red.
"""

import sys
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
PAQUETE_DIR = BASE_DIR / "proyecto_refactoring"

if str(PAQUETE_DIR) not in sys.path:
    sys.path.insert(0, str(PAQUETE_DIR))


from config import AppConfig  # noqa: E402
from models.movie import Movie  # noqa: E402
from models.series import Series  # noqa: E402
from storage.cache import Cache  # noqa: E402
from storage.favorites_repository import FavoritesRepository  # noqa: E402
from storage.history_repository import HistoryRepository  # noqa: E402


@pytest.fixture
def config() -> AppConfig:
    """Configuracion con valores por defecto validos."""
    return AppConfig()


@pytest.fixture
def sample_movie() -> Movie:
    """Pelicula de ejemplo para tests de servicios y repositorios."""
    return Movie(title="Inception", year="2010", rating=8.8, genre="Sci-Fi")


@pytest.fixture
def sample_series() -> Series:
    """Serie de ejemplo para tests de servicios."""
    return Series(id_=1, name="Breaking Bad", language="English", genres=["Drama"])


@pytest.fixture
def omdb_response() -> dict:
    """Respuesta cruda de OMDB para una pelicula encontrada."""
    return {
        "Response": "True",
        "Title": "Inception",
        "Year": "2010",
        "imdbRating": "8.8",
        "Genre": "Sci-Fi",
        "Director": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio",
        "Plot": "Un ladron que roba secretos.",
        "Country": "USA",
        "Awards": "4 Oscars",
    }


@pytest.fixture
def tvmaze_response() -> dict:
    """Respuesta cruda de TVMaze para los detalles de una serie."""
    return {
        "id": 169,
        "name": "Breaking Bad",
        "language": "English",
        "genres": ["Drama", "Crime"],
        "rating": {"average": 9.3},
        "status": "Ended",
        "premiered": "2008-01-20",
        "ended": "2013-09-29",
        "runtime": 60,
        "summary": "<p>Un profesor de quimica.</p>",
    }


@pytest.fixture
def cache() -> Cache:
    """Cache en memoria con TTL corto."""
    return Cache(ttl_segundos=300)


@pytest.fixture
def favorites() -> FavoritesRepository:
    """Repositorio de favoritas vacio."""
    return FavoritesRepository()


@pytest.fixture
def history() -> HistoryRepository:
    """Repositorio de historial vacio."""
    return HistoryRepository()
