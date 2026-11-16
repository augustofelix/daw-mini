"""Prioridad automática de tickets: reglas puras y deterministas, sin IA."""
import re
import unicodedata

FAMILIA_ALTA: tuple[str, ...] = (
    "caído", "caída", "caídos", "caídas",
    "se cayó", "se cayeron",
    "no funciona", "no funcionan",
    "no anda", "no andan",
    "no puedo entrar",
    "urgente", "urgentes",
    "crítico", "crítica", "críticos", "críticas",
    "bloqueado", "bloqueada", "bloqueados", "bloqueadas",
)

FAMILIA_MEDIA: tuple[str, ...] = (
    "lento", "lenta", "lentos", "lentas",
    "tarda", "tardan",
    "demora", "demoran",
    "error", "errores",
    "falla", "fallas", "fallan",
)

CLIENTES_VIP: frozenset[str] = frozenset({"acme", "globex"})

_NIVELES = ("baja", "media", "alta")


def normalizar(texto: str) -> str:
    """Minúsculas y sin tildes."""
    descompuesto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def _compilar(expresion: str) -> re.Pattern:
    palabras = normalizar(expresion).split()
    return re.compile(r"\b" + r"\s+".join(re.escape(p) for p in palabras) + r"\b")


_REGLAS = tuple(
    (nivel, expresion, _compilar(expresion))
    for nivel, familia in (("alta", FAMILIA_ALTA), ("media", FAMILIA_MEDIA))
    for expresion in familia
)


def es_vip(cliente: str) -> bool:
    return cliente.strip().lower() in CLIENTES_VIP


def calcular_prioridad(titulo: str, descripcion: str, cliente: str) -> tuple[str, str]:
    """Devuelve (prioridad, motivo); prioridad ∈ {"alta", "media", "baja"}."""
    texto = normalizar(titulo + "\n" + descripcion)
    base, expresion = "baja", None
    for nivel, expr, patron in _REGLAS:
        if patron.search(texto):
            base, expresion = nivel, expr
            break

    final = base
    sufijo = ""
    if es_vip(cliente):
        if base == "alta":
            sufijo = "; cliente VIP, ya era alta"
        else:
            final = _NIVELES[_NIVELES.index(base) + 1]
            sufijo = "; +1 por cliente VIP"

    if expresion is None:
        motivo = f"{final}: sin coincidencias"
    else:
        motivo = f"{final}: matcheó '{expresion}'"
    return final, motivo + sufijo
