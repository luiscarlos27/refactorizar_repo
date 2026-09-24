"""Punto de entrada de la aplicacion: compone y arranca las dependencias."""

import sys

from api.omdb_client import OmdbClient
from api.tvmaze_client import TvmazeClient
from config import AppConfig
from constants import APP_NAME
from logging_config import setup_logging
from services.movie_service import MovieService
from services.series_service import SeriesService
from storage.cache import Cache
from storage.favorites_repository import FavoritesRepository
from storage.history_repository import HistoryRepository
from ui.menu import Menu


def main() -> None:
    """Composicion raiz de la aplicacion (composition root)."""
    config = AppConfig()
    setup_logging(config)

    cache_peliculas = Cache()
    cache_series = Cache()

    omdb_client = OmdbClient(config)
    tvmaze_client = TvmazeClient(config)

    favoritas = FavoritesRepository()
    historial = HistoryRepository()

    movie_service = MovieService(
        omdb_client=omdb_client,
        favorites=favoritas,
        history=historial,
        cache=cache_peliculas,
    )
    series_service = SeriesService(
        tvmaze_client=tvmaze_client,
        cache=cache_series,
    )

    menu = Menu(
        movie_service=movie_service,
        series_service=series_service,
        config=config,
        app_name=APP_NAME,
    )
    menu.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido")
        sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)
