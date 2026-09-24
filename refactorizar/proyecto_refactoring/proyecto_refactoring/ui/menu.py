"""Navegacion y flujos interactivos. Delegan en servicios inyectados."""

from config import AppConfig
from exceptions import AppError, MovieNotFoundError, SeriesNotFoundError
from services.movie_service import MovieService
from services.series_service import SeriesService

from ui import display


class Menu:
    """Menu de la aplicacion compuesto con dependencias inyectadas.

    Args:
        movie_service: Servicio de casos de uso de peliculas.
        series_service: Servicio de casos de uso de series.
        config: Configuracion mutable de la aplicacion.
        app_name: Nombre mostrado en el encabezado.
    """

    def __init__(
        self,
        movie_service: MovieService,
        series_service: SeriesService,
        config: AppConfig,
        app_name: str,
    ) -> None:
        self._movie_service = movie_service
        self._series_service = series_service
        self._config = config
        self._app_name = app_name

    def run(self) -> None:
        """Arranca el menu principal."""
        opciones = {
            "1": self._buscar_pelicula,
            "2": self._buscar_actor,
            "3": self._buscar_series,
            "4": self._peliculas_populares,
            "5": self._buscar_por_genero,
            "6": self._ver_favoritos,
            "7": self._ver_historial,
            "8": self._estadisticas,
            "9": self._exportar,
            "10": self._importar,
            "11": self._configuracion,
        }

        while True:
            display.clear_screen()
            display.print_header(self._app_name)
            print("1. Buscar pelicula por titulo")
            print("2. Buscar por actor")
            print("3. Buscar series")
            print("4. Ver peliculas populares")
            print("5. Buscar por genero")
            print("6. Ver favoritos")
            print("7. Ver historial")
            print("8. Ver estadisticas")
            print("9. Exportar datos")
            print("10. Importar datos")
            print("11. Configuracion")
            print("12. Salir")

            opcion = input("\nSeleccione una opcion: ")

            if opcion == "12":
                print("Hasta luego!")
                break
            if opcion in opciones:
                opciones[opcion]()
            else:
                print("Opcion invalida")
                display.delay(1)

    def _buscar_pelicula(self) -> None:
        """Flujo de busqueda de pelicula por titulo."""
        titulo = input("Ingrese el titulo de la pelicula: ")
        print("Buscando...")
        display.delay(1)

        try:
            pelicula = self._movie_service.buscar_por_titulo(titulo)
        except MovieNotFoundError:
            display.mostrar_pelicula(None)
            input("\nPresione Enter para continuar...")
            return
        except AppError as exc:
            print(f"No se pudo completar la búsqueda: {exc}")
            input("\nPresione Enter para continuar...")
            return

        if pelicula is None:
            print("No se pudo completar la búsqueda")
            input("\nPresione Enter para continuar...")
            return

        display.mostrar_pelicula(pelicula)
        self._movie_service.registrar_busqueda(pelicula)
        opcion = input("\nAgregar a favoritos? (s/n): ")
        if opcion.lower() == "s":
            if self._movie_service.agregar_favorita(pelicula):
                print("Agregada a favoritos!")
            else:
                print("Ya esta en favoritos")

        input("\nPresione Enter para continuar...")

    def _buscar_actor(self) -> None:
        """Flujo de busqueda de peliculas por actor."""
        actor = input("Ingrese el nombre del actor: ")
        print("Buscando peliculas del actor...")

        peliculas = self._movie_service.buscar_por_actor(actor)

        if len(peliculas) > 0:
            display.mostrar_lista_peliculas(peliculas)

            opcion = input("\nSeleccione una pelicula para ver detalles (0 para volver): ")
            if opcion.isdigit():
                indice = int(opcion) - 1
                if 0 <= indice < len(peliculas):
                    try:
                        detalles = self._movie_service.buscar_por_titulo(peliculas[indice].title)
                        display.mostrar_pelicula(detalles)
                    except AppError:
                        print("No se pudo completar la búsqueda")
        else:
            print("No se encontraron peliculas para ese actor")

        input("\nPresione Enter para continuar...")

    def _buscar_series(self) -> None:
        """Flujo de busqueda de series."""
        nombre = input("Ingrese el nombre de la serie: ")
        print("Buscando series...")

        try:
            series = self._series_service.buscar(nombre)
        except SeriesNotFoundError:
            print("No se encontraron series")
            input("\nPresione Enter para continuar...")
            return
        except AppError:
            print("No se pudo completar la búsqueda")
            input("\nPresione Enter para continuar...")
            return

        if len(series) > 0:
            for i, serie in enumerate(series, start=1):
                print(f"{i}. {serie.name} ({serie.status or ''})")

            opcion = input("\nSeleccione una serie para ver detalles (0 para volver): ")
            if opcion.isdigit():
                indice = int(opcion) - 1
                if 0 <= indice < len(series):
                    id_serie = series[indice].id_
                    if id_serie is not None:
                        detalles = self._series_service.obtener_detalles(id_serie)
                        if detalles is not None:
                            display.mostrar_serie(detalles)
                        else:
                            print("No se pudo completar la búsqueda")
        else:
            print("No se pudo completar la búsqueda")

        input("\nPresione Enter para continuar...")

    def _peliculas_populares(self) -> None:
        """Muestra las peliculas populares."""
        display.print_header("PELICULAS POPULARES")
        peliculas = self._movie_service.populares()
        display.mostrar_lista_peliculas(peliculas)
        input("\nPresione Enter para continuar...")

    def _buscar_por_genero(self) -> None:
        """Flujo de busqueda de peliculas por genero."""
        print("Generos disponibles: accion, comedia")
        genero = input("Ingrese el genero: ")
        print("Buscando...")

        peliculas = self._movie_service.buscar_por_genero(genero)
        display.mostrar_lista_peliculas(peliculas)

        input("\nPresione Enter para continuar...")

    def _ver_favoritos(self) -> None:
        """Muestra las peliculas favoritas."""
        display.print_header("MIS FAVORITOS")
        favoritas = self._movie_service.listar_favoritas()

        if len(favoritas) > 0:
            for i, pelicula in enumerate(favoritas, start=1):
                print(f"{i}. {pelicula.title}")

            opcion = input("\nDesea eliminar alguna? (numero o Enter para volver): ")
            if opcion.isdigit():
                indice = int(opcion) - 1
                if 0 <= indice < len(favoritas) and self._movie_service.eliminar_favorita(
                    favoritas[indice].title
                ):
                    print("Eliminada de favoritos")
        else:
            print("No tienes peliculas favoritas")

        input("\nPresione Enter para continuar...")

    def _ver_historial(self) -> None:
        """Muestra el historial de busquedas."""
        display.print_header("HISTORIAL DE BUSQUEDAS")
        historial = self._movie_service.listar_historial()

        if len(historial) > 0:
            for i, entrada in enumerate(historial, start=1):
                print(f"{i}. {entrada['titulo']}")

            opcion = input("\nLimpiar historial? (s/n): ")
            if opcion.lower() == "s":
                self._movie_service.limpiar_historial()
                print("Historial limpiado")
        else:
            print("No hay historial")

        input("\nPresione Enter para continuar...")

    def _estadisticas(self) -> None:
        """Muestra las estadisticas de la aplicacion."""
        display.print_header("ESTADISTICAS")
        stats = self._movie_service.estadisticas()
        print(f"Total favoritas: {stats['total_favoritas']}")
        print(f"Total historial: {stats['total_historial']}")
        input("\nPresione Enter para continuar...")

    def _exportar(self) -> None:
        """Exporta los datos a un archivo JSON."""
        nombre = input("Nombre del archivo (sin extension): ")
        self._movie_service.exportar_a_json(f"{nombre}.json")
        print(f"Exportado a {nombre}.json")
        input("\nPresione Enter para continuar...")

    def _importar(self) -> None:
        """Importa los datos desde un archivo JSON."""
        nombre = input("Nombre del archivo (sin extension): ")
        try:
            self._movie_service.importar_a_json(f"{nombre}.json")
            print(f"Importado desde {nombre}.json")
        except OSError:
            print("Error al importar archivo")
        input("\nPresione Enter para continuar...")

    def _configuracion(self) -> None:
        """Permite modificar la configuracion de la aplicacion."""
        display.print_header("CONFIGURACION")
        print(f"1. Debug: {self._config.debug}")
        print(f"2. Verbose: {self._config.verbose}")
        print(f"3. Timeout: {self._config.timeout}")

        opcion = input("\nSeleccione opcion a cambiar (0 para volver): ")
        if opcion == "1":
            self._config.debug = not self._config.debug
            print(f"Debug ahora es: {self._config.debug}")
        elif opcion == "2":
            self._config.verbose = not self._config.verbose
            print(f"Verbose ahora es: {self._config.verbose}")
        elif opcion == "3":
            try:
                self._config.timeout = int(input("Nuevo timeout: "))
            except ValueError:
                print("Timeout invalido")

        input("\nPresione Enter para continuar...")
