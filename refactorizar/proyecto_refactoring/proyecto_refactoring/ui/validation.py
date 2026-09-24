"""Validacion de entradas de usuario de la capa UI, reutilizable por el menu."""

import re

_TEXTO_MAX = 100
_NOMBRE_ARCHIVO_RE = re.compile(r"^[\w\-. ]+$")


def pedir_texto(mensaje: str, max_len: int = _TEXTO_MAX) -> str:
    """Solicita un texto no vacio y acotado en longitud, re-pidiendo si es invalido.

    Args:
        mensaje: Prompt mostrado al usuario.
        max_len: Longitud maxima aceptada.

    Returns:
        Texto validado y sin espacios sobrantes.
    """
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("La entrada no puede estar vacia. Intenta de nuevo.")
        elif len(texto) > max_len:
            print(f"La entrada no puede superar {max_len} caracteres. Intenta de nuevo.")
        else:
            return texto


def pedir_entero_en_rango(mensaje: str, minimo: int, maximo: int) -> int | None:
    """Solicita un numero entero dentro del rango indicado.

    Returns:
        El numero validado, o None si el usuario presiona Enter para cancelar.
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            return None
        if not entrada.isdigit():
            print(f"Opcion invalida: ingresa un numero entre {minimo} y {maximo}.")
            continue
        numero = int(entrada)
        if minimo <= numero <= maximo:
            return numero
        print(f"Opcion invalida: ingresa un numero entre {minimo} y {maximo}.")


def sanitizar_nombre_archivo(nombre: str) -> str | None:
    """Sanitiza un nombre base de archivo, rechazando rutas y caracteres peligrosos.

    Args:
        nombre: Nombre ingresado por el usuario (sin extension).

    Returns:
        Nombre base seguro, o None si es invalido.
    """
    nombre = nombre.strip()
    if not nombre or "/" in nombre or "\\" in nombre or ".." in nombre:
        return None
    if not _NOMBRE_ARCHIVO_RE.fullmatch(nombre):
        return None
    return nombre
