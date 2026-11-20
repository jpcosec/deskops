---
sldb:
  by: agent
  at: '2026-11-20T05:47:28Z'
  authority: generated
  via: create_document
id: atom-integrate-saltea-el-push-del-sha-de-codigo-cuando-ya-es-ancestro-de-origin
title: integrate saltea el push del sha de código cuando ya es ancestro de origin
five_wh_one_plus: how
tags:
- system:deskops
- topic:integrate
---

# integrate saltea el push del sha de código cuando ya es ancestro de origin

## Answer

En deskops/integrate.py, después del fetch de la copia, si el sha de código ya es ancestro de origin/<branch> (git merge-base --is-ancestor), integrate no lo empuja: imprime 'código ya en origin: <sha>' y empuja solo la punta. Pasa cuando el integrate de otra tarea ya empujó una punta local que contenía ese commit; antes, el push del código retrocedía main y git lo rechazaba como non-fast-forward.
