## REFORMULACION
WS30 es una validación ejecutable —no un agregado— cuyo repo dueño es `graph_ui`. Propósito: que una persona recorra manualmente UF01–UF05, incluida autoría/edición, conocimiento, tarea, errores, conflicto en dos ventanas y teclado. Resultado: acta humana bajo protocolo en `runs/subagents/workspace-documental-acceptance/manual/` y resolución del gate `G_HUMAN_MANUAL`; no implementación. Límites: no corregir otros repos, no inventar causalidad, no declarar `ready` por tests, usar entradas WS17 materializadas por WS40 y no limitarse a búsqueda.

## AMBIGUEDADES
1. «WS16 ya cubre lectura completa». `depends_on` no incluye WS16. Obligaría a inventar si se reutiliza esa evidencia, repetir lectura completa o declarar cubierto un prerrequisito ausente.
2. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no figura en `depends_on` ni se indica ruta/productor de `validacion-humana.md`; obligaría a inventar escenarios o buscarlos fuera del input.
3. «un fallo de guion bloquea el gate ... una observación solo se registra». No hay criterio para distinguir fallo de observación; obligaría a inventar la clasificación y, con ella, el bloqueo del gate.
4. «que supervisor receptor autorice diagnóstico antes de atribuir nodo». El actor no está identificado; obligaría a inventar quién autoriza.

## DRY-RUN
Un ejecutor futuro leería WS30, el protocolo/guion, las actas y salidas de WS17, WS21–WS26, WS28 y WS42, y el manifiesto WS40. Prepararía el corpus temporal Taller, recorrería UF01–UF05 con la persona, registraría rutas/hashes y recorridos en el acta, y ante fallo abriría tarea en el nodo causante o incidente sin diagnóstico atribuido. No modificaría código ni otros repos; solo produciría el acta bajo `manual/`. Validaría después: registro humano, evidencia del gate y trazabilidad para WS43. Dependencias pendientes: guion WS08/validacion-humana y evidencia WS16.

## FUTURO
La persona participante ejecuta y firma el acta; WS31 y WS43 la consumen; el responsable del repo o supervisor decide atribución/diagnóstico. WS17 aporta plantillas y WS40 las materializa; los nodos dependientes implementan los flujos, no WS30.
