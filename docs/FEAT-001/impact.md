# Impacto · FEAT-001 · Prioridad automática de tickets

## Archivos afectados
- `src/tickettriage/tickets.py` · `Ticket` suma los campos `prioridad` y `motivo`; `crear_ticket` calcula la prioridad al crear (recibe info de VIP según lo que se defina en CLARIFY).
- `src/tickettriage/prioridad.py` (nuevo) · reglas puras y deterministas: palabras clave → nivel, ajuste VIP, armado del motivo.
- `tests/test_prioridad.py` (nuevo) · tests de las reglas y de los AC del PRD.
- `tests/test_tickets.py` · sin cambios esperados; tiene que seguir en verde (compatibilidad de `crear_ticket`).

## Riesgos
- Romper la firma de `crear_ticket`: si se agrega un parámetro de VIP tiene que ser opcional, con default no VIP.
- Falsos positivos o negativos por matching de texto ("no funciona" vs "funciona", mayúsculas, tildes, palabras dentro de otras como "terror" → "error").
- Orden de reglas: si un texto matchea alta y media, tiene que ganar alta siempre.
- Origen de la lista de VIP sin definir (hardcode vs config): afecta el diseño y los tests.

## Dependencias
- Ninguna externa: solo stdlib (`re`, `unicodedata` si hay que normalizar tildes).
- Bloqueado por CLARIFY: palabras clave exactas, cómo se identifica a un VIP, cuánto se sube la prioridad y el formato del motivo.
