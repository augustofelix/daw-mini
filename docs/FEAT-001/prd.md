# PRD · FEAT-001 · Prioridad automática de tickets
## Contexto
Hoy, cuando entra un ticket, alguien de soporte lo lee y decide a mano si es urgente. Eso tarda y muchas veces los tickets importantes quedan abajo de la pila.

## Objetivo
Que al crear un ticket el sistema le asigne solo una prioridad (alta, media o baja) con reglas simples y predecibles, sin IA, y que deje registrado el motivo.

## Requerimientos funcionales
- **RF-01** El sistema debe asignar una prioridad (`alta`, `media` o `baja`) a todo ticket en el momento en que se crea.
- **RF-02** El sistema debe asignar prioridad `alta` cuando el título o la descripción contienen alguna expresión de la familia alta: caído, caída, caídos, caídas, se cayó, se cayeron, no funciona, no funcionan, no anda, no andan, no puedo entrar, urgente, urgentes, crítico, crítica, críticos, críticas, bloqueado, bloqueada, bloqueados, bloqueadas.
- **RF-03** El sistema debe asignar prioridad `media` cuando el título o la descripción contienen alguna expresión de la familia media (lento, lenta, lentos, lentas, tarda, tardan, demora, demoran, error, errores, falla, fallas, fallan) y no corresponde `alta`.
- **RF-04** El sistema debe asignar prioridad `baja` cuando no aplica ninguna regla de `alta` ni de `media`.
- **RF-05** El sistema debe subir un nivel la prioridad de los tickets de clientes VIP (baja→media, media→alta; alta queda alta). Un cliente es VIP si su nombre, sin espacios en los bordes y en minúsculas, está en la lista fija del código {`acme`, `globex`}. La firma de `crear_ticket` no cambia.
- **RF-06** El sistema debe guardar en el ticket un `motivo` corto, sin texto libre del ticket, con el formato `"<nivel final>: matcheó '<expresión>'"` o `"<nivel final>: sin coincidencias"`; si el cliente es VIP y subió se agrega `"; +1 por cliente VIP"`, y si ya era alta `"; cliente VIP, ya era alta"`. La expresión es la de la lista (con tildes); si hay varias, la primera según el orden de la lista.
- **RF-07** El matching debe ignorar mayúsculas y tildes, ser por palabra/expresión completa ("terror" no matchea "error") y, si matchean alta y media, debe ganar alta.

## Criterios de aceptación
- **AC-01** (RF-01) Dado un ticket nuevo con título "Consulta" y descripción "Hola", cuando se crea con `crear_ticket`, entonces el ticket tiene un atributo `prioridad` con valor en {`alta`, `media`, `baja`}.
- **AC-02** (RF-02) Dado un ticket con título "Login caído" y cliente no VIP, cuando se crea, entonces su prioridad es `alta`.
- **AC-03** (RF-02) Dado un ticket con descripción "Es urgente, necesito ayuda" y cliente no VIP, cuando se crea, entonces su prioridad es `alta`.
- **AC-04** (RF-07) Dado un ticket con descripción "El sistema anda lento y no funciona el login" y cliente no VIP, cuando se crea, entonces su prioridad es `alta`.
- **AC-05** (RF-03) Dado un ticket con descripción "La página anda lenta" y cliente no VIP, cuando se crea, entonces su prioridad es `media` y su `motivo` es `"media: matcheó 'lenta'"`.
- **AC-06** (RF-03) Dado un ticket con descripción "Me tira error al guardar" y cliente no VIP, cuando se crea, entonces su prioridad es `media`.
- **AC-07** (RF-04) Dado un ticket con título "Cambiar mi email" y descripción "Quiero actualizar mis datos" y cliente no VIP, cuando se crea, entonces su prioridad es `baja` y su `motivo` es `"baja: sin coincidencias"`.
- **AC-08** (RF-05) Dado un ticket con descripción "Quiero actualizar mis datos" del cliente "acme", cuando se crea, entonces su prioridad es `media` y su `motivo` es `"media: sin coincidencias; +1 por cliente VIP"`.
- **AC-09** (RF-05) Dado un ticket con título "Login caído" del cliente "globex", cuando se crea, entonces su prioridad es `alta` y su `motivo` es `"alta: matcheó 'caído'; cliente VIP, ya era alta"`.
- **AC-10** (RF-06) Dado un ticket con título "Login caído" y cliente no VIP, cuando se crea, entonces su `motivo` es `"alta: matcheó 'caído'"`.
- **AC-11** (RF-07) Dado un ticket con título "SISTEMA CAIDO" y cliente no VIP, cuando se crea, entonces su prioridad es `alta`.
- **AC-12** (RF-07) Dado un ticket con descripción "Fue un terror de día" y cliente no VIP, cuando se crea, entonces su prioridad es `baja`.
- **AC-13** (RF-05) Dado un ticket con descripción "Me tira error al guardar" del cliente "  ACME ", cuando se crea, entonces su prioridad es `alta` y su `motivo` es `"alta: matcheó 'error'; +1 por cliente VIP"`.
- **AC-14** (RF-02) Dado un ticket con descripción "No puedo entrar a mi cuenta" y cliente no VIP, cuando se crea, entonces su prioridad es `alta` y su `motivo` es `"alta: matcheó 'no puedo entrar'"`.
- **AC-15** (RF-03) Dado un ticket con descripción "La carga tarda mucho" y cliente no VIP, cuando se crea, entonces su prioridad es `media`.

## Fuera de alcance
- Que la prioridad cambie con el tiempo si nadie atiende el ticket.
- Usar IA o modelos de lenguaje para clasificar.
- Cambiar la prioridad a mano o reclasificar tickets ya creados.
