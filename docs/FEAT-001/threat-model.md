# Threat model · FEAT-001 · Prioridad automática de tickets

| Categoría | Amenaza | Mitigación |
|---|---|---|
| Spoofing | Un cliente se hace pasar por VIP (manda otro nombre en `cliente`) para que su prioridad suba. | El estado VIP sale de una lista controlada por el sistema, no de un flag del input; el matching de cliente es exacto y normalizado (trim y minúsculas). |
| Tampering | Un usuario mete "urgente caído no funciona" en cualquier ticket para forzar la prioridad `alta`. | Se acepta como riesgo conocido de un sistema por reglas; el `motivo` deja a la vista qué palabra disparó la regla, así soporte detecta el abuso. |
| Repudiation | No se puede explicar después por qué un ticket quedó con cierta prioridad. | Cada ticket guarda el `motivo` (regla y palabra clave que matcheó, y si hubo ajuste VIP) en el momento de crearse. |
| Denial of service | Una descripción enorme o una regex patológica hace lenta la creación de tickets. | Matching con palabras clave literales o regex simples sin backtracking anidado; el costo es lineal en el largo del texto. |
| Information disclosure | El `motivo` expone que un cliente es VIP a quien no debería saberlo. | El motivo es para el equipo de soporte (uso interno); no se agregan datos del cliente más allá de "cliente VIP". |
