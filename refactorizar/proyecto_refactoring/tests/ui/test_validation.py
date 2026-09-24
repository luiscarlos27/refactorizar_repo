"""Tests de la validacion de entradas de la capa UI (input mockeado)."""

import builtins

import pytest
from ui.validation import pedir_entero_en_rango, pedir_texto, sanitizar_nombre_archivo


def _simular_input(monkeypatch, respuestas):
    iterador = iter(respuestas)
    monkeypatch.setattr(builtins, "input", lambda _mensaje="": next(iterador))
    impresos = []
    def _imprimir(*args, **kwargs):
        impresos.append(" ".join(map(str, args)))

    monkeypatch.setattr(builtins, "print", _imprimir)
    return impresos


def test_pedir_texto_valido(monkeypatch):
    _simular_input(monkeypatch, ["  Inception  "])
    assert pedir_texto("Titulo: ") == "Inception"


def test_pedir_texto_vacio_vuelve_a_pedir(monkeypatch):
    impresos = _simular_input(monkeypatch, ["   ", "Inception"])
    assert pedir_texto("Titulo: ") == "Inception"
    assert any("no puede estar vacia" in linea for linea in impresos)


def test_pedir_texto_excede_longitud_vuelve_a_pedir(monkeypatch):
    _simular_input(monkeypatch, ["x" * 101, "Inception"])
    assert pedir_texto("Titulo: ", max_len=100) == "Inception"


def test_pedir_texto_vacio_no_llama_a_la_api(monkeypatch):
    _simular_input(monkeypatch, ["", "Matrix"])
    assert pedir_texto("Titulo: ") == "Matrix"


def test_pedir_entero_en_rango_valido(monkeypatch):
    _simular_input(monkeypatch, ["3"])
    assert pedir_entero_en_rango("Opcion: ", 1, 10) == 3


def test_pedir_entero_en_rango_limites(monkeypatch):
    _simular_input(monkeypatch, ["1"])
    assert pedir_entero_en_rango("Opcion: ", 1, 10) == 1
    _simular_input(monkeypatch, ["10"])
    assert pedir_entero_en_rango("Opcion: ", 1, 10) == 10


def test_pedir_entero_fuera_de_rango_vuelve_a_pedir(monkeypatch):
    impresos = _simular_input(monkeypatch, ["99", "3"])
    assert pedir_entero_en_rango("Opcion: ", 1, 10) == 3
    assert any("Opcion invalida" in linea for linea in impresos)


def test_pedir_entero_no_numerico_vuelve_a_pedir(monkeypatch):
    impresos = _simular_input(monkeypatch, ["abc", "3"])
    assert pedir_entero_en_rango("Opcion: ", 1, 10) == 3
    assert any("Opcion invalida" in linea for linea in impresos)


def test_pedir_entero_enter_cancela(monkeypatch):
    _simular_input(monkeypatch, [""])
    assert pedir_entero_en_rango("Opcion: ", 1, 10) is None


@pytest.mark.parametrize(
    "nombre, esperado",
    [
        ("favoritos", "favoritos"),
        ("mis-datos_2024", "mis-datos_2024"),
        ("  datos  ", "datos"),
    ],
)
def test_sanitizar_nombre_archivo_valido(nombre, esperado):
    assert sanitizar_nombre_archivo(nombre) == esperado


@pytest.mark.parametrize(
    "nombre",
    [
        "",
        "   ",
        "../etc/passwd",
        "carpeta/archivo",
        "carpeta\\archivo",
        "C:/datos",
        "archivo;del",
    ],
)
def test_sanitizar_nombre_archivo_peligroso_rechazado(nombre):
    assert sanitizar_nombre_archivo(nombre) is None
