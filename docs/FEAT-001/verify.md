# Verify · FEAT-001 · Prioridad automática de tickets

Suite: `python3 -m unittest discover -s tests -t .` → 17 tests, OK (15 de `tests/test_prioridad.py` + 2 de `tests/test_tickets.py`, sin regresiones).

| AC | Test | OK |
|---|---|---|
| AC-01 | `test_ac01_todo_ticket_tiene_prioridad` | Sí |
| AC-02 | `test_ac02_titulo_caido_es_alta` | Sí |
| AC-03 | `test_ac03_descripcion_urgente_es_alta` | Sí |
| AC-04 | `test_ac04_alta_gana_sobre_media` | Sí |
| AC-05 | `test_ac05_lenta_es_media_con_motivo` | Sí |
| AC-06 | `test_ac06_error_es_media` | Sí |
| AC-07 | `test_ac07_sin_coincidencias_es_baja` | Sí |
| AC-08 | `test_ac08_vip_sube_baja_a_media` | Sí |
| AC-09 | `test_ac09_vip_ya_alta_queda_alta` | Sí |
| AC-10 | `test_ac10_motivo_alta_no_vip` | Sí |
| AC-11 | `test_ac11_ignora_mayusculas_y_tildes` | Sí |
| AC-12 | `test_ac12_palabra_completa_terror_no_es_error` | Sí |
| AC-13 | `test_ac13_vip_con_espacios_y_mayusculas_sube_media_a_alta` | Sí |
| AC-14 | `test_ac14_no_puedo_entrar_es_alta` | Sí |
| AC-15 | `test_ac15_tarda_es_media` | Sí |

## Hallazgos
- Todos los tests pasan por `crear_ticket` (end-to-end), con asserts de igualdad exacta sobre `prioridad` y `motivo` cuando el AC los fija; ninguno es trivial. AC-01 solo verifica pertenencia al conjunto, que es exactamente lo que pide el AC.
- `prioridad.py` respeta la spec: `FAMILIA_ALTA`/`FAMILIA_MEDIA` en el orden y con las tildes del PRD; `normalizar` usa NFD descartando `Mn`; patrones `\b` + palabras unidas por `\s+` + `\b`, precompilados al importar; se recorre alta antes que media (RF-07: gana alta); el motivo usa la expresión original con tildes y el nivel final.
- `tickets.py`: firma de `crear_ticket` sin cambios; `Ticket` suma `prioridad="baja"` y `motivo=""` con defaults, compatibles con construcciones existentes (`test_tickets.py` sigue pasando).
- El motivo no incluye texto libre del ticket: solo nivel, expresión de la lista fija y sufijo VIP (RF-06).
- Observación menor (no bloqueante): `crear_ticket` ya trimea `cliente` antes de llamar a `es_vip`, por lo que AC-13 ejercita el trim de forma redundante; `es_vip` también hace `strip()`, así que el comportamiento es correcto por ambos caminos.

## Threat model
- Spoofing: el estado VIP sale de `CLIENTES_VIP` (frozenset fijo en código), match exacto tras `strip().lower()`. Presente.
- Tampering: riesgo aceptado; el `motivo` expone la expresión disparadora. Presente.
- Repudiation: el `motivo` se guarda en el `Ticket` al crearse. Presente.
- Denial of service: expresiones literales con `re.escape`, sin cuantificadores anidados; costo lineal. Presente.
- Information disclosure: el motivo solo agrega "cliente VIP", sin otros datos del cliente. Presente.

VEREDICTO: APROBADO
