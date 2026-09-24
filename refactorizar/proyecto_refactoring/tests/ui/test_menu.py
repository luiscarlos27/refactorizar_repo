"""Tests de Menu con servicios simulados e input monkeypacheado."""

import builtins

import pytest
from config import AppConfig
from exceptions import MovieNotFoundError, SeriesNotFoundError
from ui.menu import Menu, _pedir_nombre_archivo


@pytest.fixture
def menu(mocker, monkeypatch, tmp_path):
    """Menu con servicios simulados, delay anulado y cwd temporal."""
    movie_service = mocker.Mock()
    series_service = mocker.Mock()
    config = AppConfig()
    monkeypatch.chdir(tmp_path)
    _anular_delay(monkeypatch)
    return Menu(
        movie_service=movie_service,
        series_service=series_service,
        config=config,
        app_name="Test",
    )


def _anular_delay(monkeypatch):
    from ui import display

    monkeypatch.setattr(display, "delay", lambda seconds: None)


def _simular_input(monkeypatch, respuestas):
    iterador = iter(respuestas)
    monkeypatch.setattr(builtins, "input", lambda _mensaje="": next(iterador, "12"))


def test_pedir_nombre_archivo_valido(monkeypatch):
    _simular_input(monkeypatch, ["datos"])
    assert _pedir_nombre_archivo() == "datos"


def test_pedir_nombre_archivo_invalido(monkeypatch):
    _simular_input(monkeypatch, ["../etc/passwd"])
    assert _pedir_nombre_archivo() is None


def test_run_salir_imprimiendo_opcion_invalida(menu, monkeypatch):
    _simular_input(monkeypatch, ["99", "12"])
    menu.run()


def test_buscar_pelicula_exito_y_agrega_favoritos(menu, monkeypatch, sample_movie):
    menu._movie_service.buscar_por_titulo.return_value = sample_movie
    menu._movie_service.agregar_favorita.return_value = True
    _simular_input(monkeypatch, ["1", "Inception", "s", ""])
    menu.run()
    menu._movie_service.buscar_por_titulo.assert_called_once_with("Inception")
    menu._movie_service.agregar_favorita.assert_called_once_with(sample_movie)


def test_buscar_pelicula_exito_sin_favoritos(menu, monkeypatch, sample_movie):
    menu._movie_service.buscar_por_titulo.return_value = sample_movie
    _simular_input(monkeypatch, ["1", "Inception", "n", ""])
    menu.run()
    menu._movie_service.registrar_busqueda.assert_called_once_with(sample_movie)
    menu._movie_service.agregar_favorita.assert_not_called()


def test_buscar_pelicula_favorito_duplicado(menu, monkeypatch, sample_movie):
    menu._movie_service.buscar_por_titulo.return_value = sample_movie
    menu._movie_service.agregar_favorita.return_value = False
    _simular_input(monkeypatch, ["1", "Inception", "s", ""])
    menu.run()
    menu._movie_service.agregar_favorita.assert_called_once_with(sample_movie)


def test_buscar_pelicula_no_encontrada(menu, monkeypatch):
    menu._movie_service.buscar_por_titulo.side_effect = MovieNotFoundError("X")
    _simular_input(monkeypatch, ["1", "NoExiste", ""])
    menu.run()


def test_buscar_pelicula_app_error(menu, monkeypatch):
    from exceptions import NetworkError

    menu._movie_service.buscar_por_titulo.side_effect = NetworkError("boom")
    _simular_input(monkeypatch, ["1", "Inception", ""])
    menu.run()


def test_buscar_pelicula_degradada_a_none(menu, monkeypatch):
    menu._movie_service.buscar_por_titulo.return_value = None
    _simular_input(monkeypatch, ["1", "Inception", ""])
    menu.run()


def test_buscar_actor_sin_resultados(menu, monkeypatch):
    menu._movie_service.buscar_por_actor.return_value = []
    _simular_input(monkeypatch, ["2", "Nadie", ""])
    menu.run()


def test_buscar_actor_selecciona_volver(menu, monkeypatch, sample_movie):
    menu._movie_service.buscar_por_actor.return_value = [sample_movie]
    _simular_input(monkeypatch, ["2", "DiCaprio", "0", ""])
    menu.run()


def test_buscar_actor_ver_detalles(menu, monkeypatch, sample_movie):
    menu._movie_service.buscar_por_actor.return_value = [sample_movie]
    menu._movie_service.buscar_por_titulo.return_value = sample_movie
    _simular_input(monkeypatch, ["2", "DiCaprio", "1", ""])
    menu.run()


def test_buscar_actor_detalles_app_error(menu, monkeypatch, sample_movie):
    from exceptions import NetworkError

    menu._movie_service.buscar_por_actor.return_value = [sample_movie]
    menu._movie_service.buscar_por_titulo.side_effect = NetworkError("boom")
    _simular_input(monkeypatch, ["2", "DiCaprio", "1", ""])
    menu.run()


def test_buscar_series_sin_resultados_error(menu, monkeypatch):
    menu._series_service.buscar.side_effect = SeriesNotFoundError("X")
    _simular_input(monkeypatch, ["3", "NoExiste", ""])
    menu.run()


def test_buscar_series_app_error(menu, monkeypatch):
    from exceptions import NetworkError

    menu._series_service.buscar.side_effect = NetworkError("boom")
    _simular_input(monkeypatch, ["3", "Lost", ""])
    menu.run()


def test_buscar_series_lista_vacia(menu, monkeypatch):
    menu._series_service.buscar.return_value = []
    _simular_input(monkeypatch, ["3", "Lost", ""])
    menu.run()


def test_buscar_series_selecciona_volver(menu, monkeypatch, sample_series):
    menu._series_service.buscar.return_value = [sample_series]
    _simular_input(monkeypatch, ["3", "Breaking Bad", "0", ""])
    menu.run()


def test_buscar_series_ver_detalles(menu, monkeypatch, sample_series):
    menu._series_service.buscar.return_value = [sample_series]
    menu._series_service.obtener_detalles.return_value = sample_series
    _simular_input(monkeypatch, ["3", "Breaking Bad", "1", ""])
    menu.run()


def test_buscar_series_detalles_none(menu, monkeypatch, sample_series):
    menu._series_service.buscar.return_value = [sample_series]
    menu._series_service.obtener_detalles.return_value = None
    _simular_input(monkeypatch, ["3", "Breaking Bad", "1", ""])
    menu.run()


def test_buscar_series_id_none(menu, monkeypatch):
    from models.series import Series

    serie = Series(id_=None, name="Sin id")
    menu._series_service.buscar.return_value = [serie]
    _simular_input(monkeypatch, ["3", "Sin id", "1", ""])
    menu.run()


def test_peliculas_populares(menu, monkeypatch, sample_movie):
    menu._movie_service.populares.return_value = [sample_movie]
    _simular_input(monkeypatch, ["4", ""])
    menu.run()
    menu._movie_service.populares.assert_called_once()


def test_buscar_por_genero(menu, monkeypatch, sample_movie):
    menu._movie_service.buscar_por_genero.return_value = [sample_movie]
    _simular_input(monkeypatch, ["5", "accion", ""])
    menu.run()
    menu._movie_service.buscar_por_genero.assert_called_once_with("accion")


def test_ver_favoritos_vacio(menu, monkeypatch):
    menu._movie_service.listar_favoritas.return_value = []
    _simular_input(monkeypatch, ["6", ""])
    menu.run()


def test_ver_favoritos_elimina(menu, monkeypatch, sample_movie):
    menu._movie_service.listar_favoritas.return_value = [sample_movie]
    menu._movie_service.eliminar_favorita.return_value = True
    _simular_input(monkeypatch, ["6", "1", ""])
    menu.run()
    menu._movie_service.eliminar_favorita.assert_called_once_with("Inception")


def test_ver_historial_vacio(menu, monkeypatch):
    menu._movie_service.listar_historial.return_value = []
    _simular_input(monkeypatch, ["7", ""])
    menu.run()


def test_ver_historial_limpia(menu, monkeypatch):
    menu._movie_service.listar_historial.return_value = [{"titulo": "Inception", "fecha": "hoy"}]
    _simular_input(monkeypatch, ["7", "s", ""])
    menu.run()
    menu._movie_service.limpiar_historial.assert_called_once()


def test_ver_historial_no_limpia(menu, monkeypatch):
    menu._movie_service.listar_historial.return_value = [{"titulo": "Inception", "fecha": "hoy"}]
    _simular_input(monkeypatch, ["7", "n", ""])
    menu.run()
    menu._movie_service.limpiar_historial.assert_not_called()


def test_estadisticas(menu, monkeypatch):
    menu._movie_service.estadisticas.return_value = {
        "total_favoritas": 2,
        "total_historial": 3,
    }
    _simular_input(monkeypatch, ["8", ""])
    menu.run()


def test_exportar_nombre_invalido(menu, monkeypatch):
    _simular_input(monkeypatch, ["9", "archivo/malo", ""])
    menu.run()
    menu._movie_service.exportar_a_json.assert_not_called()


def test_exportar_exito(menu, monkeypatch):
    _simular_input(monkeypatch, ["9", "datos", ""])
    menu.run()
    menu._movie_service.exportar_a_json.assert_called_once_with("datos.json")


def test_importar_nombre_invalido(menu, monkeypatch):
    _simular_input(monkeypatch, ["10", "../etc/passwd", ""])
    menu.run()
    menu._movie_service.importar_a_json.assert_not_called()


def test_importar_exito(menu, monkeypatch):
    _simular_input(monkeypatch, ["10", "datos", ""])
    menu.run()
    menu._movie_service.importar_a_json.assert_called_once_with("datos.json")


def test_importar_oserror(menu, monkeypatch):
    menu._movie_service.importar_a_json.side_effect = OSError("no existe")
    _simular_input(monkeypatch, ["10", "datos", ""])
    menu.run()


def test_configuracion_toggle_debug(menu, monkeypatch):
    estado_inicial = menu._config.debug
    _simular_input(monkeypatch, ["11", "1", ""])
    menu.run()
    assert menu._config.debug is not estado_inicial


def test_configuracion_toggle_verbose(menu, monkeypatch):
    estado_inicial = menu._config.verbose
    _simular_input(monkeypatch, ["11", "2", ""])
    menu.run()
    assert menu._config.verbose is not estado_inicial


def test_configuracion_timeout_valido(menu, monkeypatch):
    _simular_input(monkeypatch, ["11", "3", "60", ""])
    menu.run()
    assert menu._config.timeout == 60


def test_configuracion_timeout_invalido(menu, monkeypatch):
    _simular_input(monkeypatch, ["11", "3", "abc", ""])
    menu.run()
    assert menu._config.timeout != 0 or menu._config.timeout > 0


def test_configuracion_volver(menu, monkeypatch):
    estado_debug = menu._config.debug
    _simular_input(monkeypatch, ["11", "0", ""])
    menu.run()
    assert menu._config.debug is estado_debug
