"""Repositorio de historial de busquedas, unico dueno de su estado."""

from typing import Any


class HistoryRepository:
    """Almacena titulo y fecha de cada busqueda."""

    def __init__(self) -> None:
        self._historial: list[dict[str, str]] = []

    def registrar(self, titulo: str) -> None:
        """Registra una busqueda en el historial."""
        self._historial.append({"titulo": titulo, "fecha": "hoy"})

    def listar(self) -> list[dict[str, str]]:
        """Devuelve una copia del historial."""
        return list(self._historial)

    def limpiar(self) -> None:
        """Vacía el historial."""
        self._historial.clear()

    @property
    def cantidad(self) -> int:
        """Numero de entradas del historial."""
        return len(self._historial)

    def to_json_list(self) -> list[dict[str, str]]:
        """Serializa el historial para exportacion JSON."""
        return list(self._historial)

    def cargar(self, datos: list[dict[str, Any]]) -> None:
        """Reemplaza el estado con datos importados de JSON."""
        self._historial = [
            {"titulo": str(d.get("titulo", "")), "fecha": str(d.get("fecha", "hoy"))}
            for d in datos
        ]
