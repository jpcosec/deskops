---
sldb:
  by: agent
  at: '2026-11-26T02:59:50Z'
  authority: generated
  via: create_document
id: atom-pron-queda-archivado-y-la-puerta-al-store-es-la-api-de-sldb
atom_type: atom.adr
status: accepted
five_wh_one_plus: why
decided_on: '2026-11-25'
decided_by: JP
supersedes: []
partial_supersedes:
- atom-sldb-absorbe-kgdb-un-sustrato-con-dos-capas-internas
superseded_section: pron is a semantic shell
references:
- /mnt/ssd/proyectos/SLDB_1/sldb/docs/architecture/pron-is-archived.md
pointers: []
tags:
- system:deskops
---

# pron queda archivado y la puerta al store es la API de SLDB

## Context

El ADR del 2026-09-20 redujo pron a una cáscara semántica. Dos meses después graph_ui seguía abriendo el store por pron.world.store.Store, todo lo que usa tiene equivalente en sldb.api, la suite de pron estaba en rojo contra SLDB con una tarea bloqueada desde el 2026-11-16, specIR decidió no depender de pron, y ningún proyecto del workspace usa su capa de lenguaje. El dueño creía que pron ya estaba retirado: ningún registro lo decía.

## Decision

pron se archiva: sin trabajo nuevo, el código queda como referencia. La puerta a un store es la API de SLDB, para interfaces y agentes. A SLDB pasan el rechazo de una relación antes de escribirla, la prevalidación de un movimiento completo y un registro persistente de movimientos con deshacer entre sesiones.

## Consequences

El adaptador de graph_ui deja de importar pron y la edición por gestos escribe por SLDB; el diseño de septiembre con GestureDoc queda sin efecto. La compuerta G_SLDB_PRON_MCP del plan de specIR se reemplaza por las tres capacidades. legos pierde sesiones de solo lectura por proyección y se migrará a Kimun al retomarse. El registro y el repositorio de GitHub de pron aún no están marcados.

## Alternatives
