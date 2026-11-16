# Spec · FEAT-001 · Prioridad automática de tickets

## Diseño
- **Nuevo `src/tickettriage/prioridad.py`** · reglas puras y deterministas, solo stdlib (`re`, `unicodedata`).
  - `FAMILIA_ALTA` y `FAMILIA_MEDIA`: tuplas con las expresiones de RF-02 y RF-03, en ese orden y con tildes (forma que se muestra en el motivo).
  - `CLIENTES_VIP = frozenset({"acme", "globex"})`.
  - `normalizar(texto)`: minúsculas + sin tildes (NFD, descarta categoría `Mn`).
  - Matching: se normaliza `titulo + "\n" + descripcion`. Cada expresión se normaliza y se compila como `\b` + palabras unidas por `\s+` + `\b` (expresión completa, regex literal sin backtracking anidado → costo lineal). Se precompilan al importar el módulo.
  - Orden: se recorre `FAMILIA_ALTA` en orden; si alguna matchea, base = `alta` con esa expresión. Si no, `FAMILIA_MEDIA` en orden → `media`. Si no, `baja` sin expresión.
  - VIP: `es_vip(cliente)` = `cliente.strip().lower() in CLIENTES_VIP`. Si es VIP y base < alta, final = base + 1 nivel; si base es alta, final = alta.
  - Motivo (con nivel final):
    - con expresión: `f"{final}: matcheó '{expresion}'"`
    - sin expresión: `f"{final}: sin coincidencias"`
    - VIP que subió: `+ "; +1 por cliente VIP"`
    - VIP ya alta: `+ "; cliente VIP, ya era alta"`
- **Modificado `src/tickettriage/tickets.py`** · `Ticket` suma `prioridad: str = "baja"` y `motivo: str = ""` (con default, compatibles con construcciones existentes). `crear_ticket` conserva la firma y llama a `calcular_prioridad` con los valores ya trimeados.

## Interfaz
```python
# src/tickettriage/prioridad.py
FAMILIA_ALTA: tuple[str, ...]
FAMILIA_MEDIA: tuple[str, ...]
CLIENTES_VIP: frozenset[str]

def normalizar(texto: str) -> str: ...
def es_vip(cliente: str) -> bool: ...
def calcular_prioridad(titulo: str, descripcion: str, cliente: str) -> tuple[str, str]:
    """Devuelve (prioridad, motivo); prioridad ∈ {"alta", "media", "baja"}."""

# src/tickettriage/tickets.py
@dataclass
class Ticket:
    titulo: str
    descripcion: str
    cliente: str
    creado: datetime = ...
    prioridad: str = "baja"
    motivo: str = ""

def crear_ticket(titulo: str, descripcion: str, cliente: str) -> Ticket: ...  # firma sin cambios
```

## Plan de tests
En `tests/test_prioridad.py`, todo vía `crear_ticket`; cliente no VIP = `"juan"`; título "Problema" cuando el AC solo da descripción (y descripción "" cuando solo da título):
- AC-01: `crear_ticket("Consulta", "Hola", "juan").prioridad in {"alta", "media", "baja"}`.
- AC-02: título "Login caído" → `alta`.
- AC-03: descripción "Es urgente, necesito ayuda" → `alta`.
- AC-04: descripción "El sistema anda lento y no funciona el login" → `alta`.
- AC-05: descripción "La página anda lenta" → `media`, motivo `"media: matcheó 'lenta'"`.
- AC-06: descripción "Me tira error al guardar" → `media`.
- AC-07: título "Cambiar mi email", descripción "Quiero actualizar mis datos" → `baja`, motivo `"baja: sin coincidencias"`.
- AC-08: descripción "Quiero actualizar mis datos", cliente "acme" → `media`, motivo `"media: sin coincidencias; +1 por cliente VIP"`.
- AC-09: título "Login caído", cliente "globex" → `alta`, motivo `"alta: matcheó 'caído'; cliente VIP, ya era alta"`.
- AC-10: título "Login caído", no VIP → motivo `"alta: matcheó 'caído'"`.
- AC-11: título "SISTEMA CAIDO" → `alta`.
- AC-12: descripción "Fue un terror de día" → `baja`.
- AC-13: descripción "Me tira error al guardar", cliente "  ACME " → `alta`, motivo `"alta: matcheó 'error'; +1 por cliente VIP"`.
- AC-14: descripción "No puedo entrar a mi cuenta" → `alta`, motivo `"alta: matcheó 'no puedo entrar'"`.
- AC-15: descripción "La carga tarda mucho" → `media`.
