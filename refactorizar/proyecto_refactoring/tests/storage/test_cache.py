"""Tests del Cache en memoria con TTL."""

from storage.cache import Cache


def test_set_y_get():
    cache = Cache()
    cache.set("clave", {"dato": 1})
    assert cache.get("clave") == {"dato": 1}


def test_get_clave_inexistente_devuelve_none():
    assert Cache().get("no-existe") is None


def test_ttl_expirado_devuelve_none_y_elimina_entrada():
    cache = Cache(ttl_segundos=300)
    cache.set("clave", "valor", ttl_segundos=0)
    assert cache.get("clave") is None
    assert cache.get("clave") is None


def test_ttl_por_defecto_se_usa_cuando_no_se_indica():
    cache = Cache(ttl_segundos=1)
    cache.set("clave", "valor")
    assert cache.get("clave") == "valor"


def test_clear_elimina_todos_los_valores():
    cache = Cache()
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    assert cache.get("a") is None
    assert cache.get("b") is None
