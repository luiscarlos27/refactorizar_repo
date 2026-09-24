"""Jerarquia de excepciones del dominio con base comun ``AppError``."""


class AppError(Exception):
    """Error base de la aplicacion de peliculas y series."""


class ApiClientError(AppError):
    """Error al comunicarse con una API externa."""


class NetworkError(ApiClientError):
    """Fallo de red o timeout en una llamada HTTP."""


class MovieNotFoundError(AppError):
    """Pelicula no encontrada en OMDB."""


class SeriesNotFoundError(AppError):
    """Serie no encontrada en TVMaze."""


class ConfigError(AppError):
    """Configuracion invalida o faltante."""
