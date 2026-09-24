"""Tests del HistoryRepository: registro, listado y persistencia JSON."""

from storage.history_repository import HistoryRepository


def test_registrar_y_listar():
    repo = HistoryRepository()
    repo.registrar("Inception")
    entradas = repo.listar()
    assert len(entradas) == 1
    assert entradas[0]["titulo"] == "Inception"
    assert "fecha" in entradas[0]


def test_listar_devuelve_copia():
    repo = HistoryRepository()
    repo.registrar("Inception")
    copia = repo.listar()
    copia.clear()
    assert repo.cantidad == 1


def test_limpiar_vacia_el_historial():
    repo = HistoryRepository()
    repo.registrar("Inception")
    repo.limpiar()
    assert repo.cantidad == 0
    assert repo.listar() == []


def test_to_json_list():
    repo = HistoryRepository()
    repo.registrar("Inception")
    assert repo.to_json_list() == [{"titulo": "Inception", "fecha": "hoy"}]


def test_cargar_reemplaza_el_estado():
    repo = HistoryRepository()
    repo.registrar("Vieja")
    repo.cargar([{"titulo": "Inception", "fecha": "ayer"}])
    assert repo.cantidad == 1
    assert repo.listar()[0] == {"titulo": "Inception", "fecha": "ayer"}


def test_cargar_con_claves_faltantes_usa_valores_por_defecto():
    repo = HistoryRepository()
    repo.cargar([{}])
    assert repo.listar()[0] == {"titulo": "", "fecha": "hoy"}


def test_cargar_lista_vacia():
    repo = HistoryRepository()
    repo.registrar("Vieja")
    repo.cargar([])
    assert repo.cantidad == 0
