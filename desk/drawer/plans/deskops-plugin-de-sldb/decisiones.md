# Decisiones: deskops como plugin de sldb

El plan por fases F0-F5 (brief, alcance, dag) se retiró el 2026-11-25: lo reemplazan las macros M0-M6 del Board, que salen de diagnostico.md. Estas decisiones siguen vigentes.

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| D1 | deskops es un plugin sobre sldb, no una reimplementación. Lo modelado del workflow es dato en el store y lo evalúan reglas, aristas y vistas de sldb; deskops conserva como código solo dispatch/scion, git (worktrees, cierre, integrate), la cola, herdr, el lanzador de revisores y un CLI delgado. | JP | conversación 2026-11-25; átomo `atom-deskops-es-un-plugin-sobre-sldb-no-una-reimplementacion` | 2026-11-25 |
| D2 | Primero el refactor; las 53 tareas del Board quedan congeladas y se revisan al final (nodo L05). | JP | conversación 2026-11-25 | 2026-11-25 |
| D3 | El slop (docs, tests añejos, código desorganizado, falta de lint) se limpia dentro del refactor: F0 y F5. | JP | conversación 2026-11-25 | 2026-11-25 |
| D4 | deskops exige git en cada desk; deskops y sldb pueden apoyarse en git (cambios, blob ids, evidencia de cierre). Resuelve la tarea task-jp-decide-si-deskops-exige-git-en-cada-desk-o-acepta-otra-evidencia-de-cierre (se cierra en L05 citando el átomo). | JP | conversación 2026-11-25; átomo `atom-deskops-exige-git-en-cada-desk` | 2026-11-25 |
| D6 | La conciliación de deskops entre johanes y robocop2 la ejecuta el despacho de robocop2 con la receta v2 (`sala/2026-11-25-planificacion/deskops-conciliacion.md`: sha fijos, drenar cola, agentes y worktrees, respaldo, merge con el driver de sldb más inventario, validación por diferencia de fallidos). Las cuatro tareas nuevas sin trabajo van al drawer. | JP | conversación 2026-11-25 y 2026-11-26 | 2026-11-26 |
| D7 | Los tres bugs del despacho (no relanzar -a2 con result-summary.md, exit 255 de parada pedida, motivo de limits_exceeded) entran antes de E1, como excepción al orden de etapas. | JP | conversación 2026-11-25 | 2026-11-25 |

## Pendientes (no bloquean F0–F3)

| Id | Pregunta | Recomendación |
|---|---|---|
| P1 | Meta de líneas de Python al final (tarea "JP fija N") | ~16 000 (−40 %), medida en L04 |
