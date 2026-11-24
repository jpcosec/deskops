---
sldb:
  by: agent
  at: '2026-11-24T20:09:24Z'
  authority: generated
  via: create_document
id: atom-un-solo-vocabulario-de-tags-semanticos-en-deskops-resuelto-por-el-store-semantico-de-sldb
title: Un solo vocabulario de tags semanticos en deskops resuelto por el store semantico
  de sldb
five_wh_one_plus: how
tags:
- system:deskops
- topic:tags
---

# Un solo vocabulario de tags semanticos en deskops resuelto por el store semantico de sldb

## Answer

deskops deja de escribir tags que el modelo ya dice (workspace:desk, artifact:task), repetidos y nombres de clase; TaskDoc.__semantics__ suma board.tareas y la semantica hija board.tareas.ui marca las tareas de UI; deskops tags migrate --apply reescribe los documentos y reindexa los que tienen indice semantico viejo. Criterio de JP sobre el desk real: sldb find board.tareas --in semantic --type doc da las 50 tareas y board.tareas.ui solo la de UI, sin listas ni filtros propios de deskops.
