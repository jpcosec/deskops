---
sldb:
  by: agent
  at: '2026-11-25T17:33:15Z'
  authority: generated
  via: create_document
id: atom-deskops-es-un-plugin-sobre-sldb-no-una-reimplementacion
title: deskops es un plugin sobre sldb, no una reimplementación
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:architecture
provenance: desk/drawer/plans/deskops-plugin-de-sldb/decisiones.md
---

# deskops es un plugin sobre sldb, no una reimplementación

## Answer

Decisión de JP del 25-11-2026: deskops es un plugin sobre sldb. Lo modelado del workflow (ciclo de vida, transiciones, compuertas de activación y de cierre, tipos de tarea y su evidencia, recibos de revisión, ritos, fases, board, inbox y drawer) es dato en el store de sldb y lo evalúan reglas, aristas y vistas de sldb. deskops conserva como código propio solo lo que sldb no puede ser: dispatch y scion, git (worktrees, commits de cierre, integrate), la cola, herdr, el lanzador de revisores y un CLI delgado. Lo que reimplementa sldb se borra y se usa la API de sldb; lo genérico que sldb no tiene se pide por su inbox y no se construye en deskops. El refactor va antes que las tareas sueltas del Board: plan desk/drawer/plans/deskops-plugin-de-sldb/.
