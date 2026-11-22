---
sldb:
  by: agent
  at: '2026-11-22T19:18:20Z'
  authority: generated
  via: create_document
id: atom-cada-intento-de-dispatch-tiene-su-propio-rundoc-con-intencion-y-confirmacion-separadas
title: Cada intento de dispatch tiene su propio RunDoc, con intención y confirmación
  separadas
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# Cada intento de dispatch tiene su propio RunDoc, con intención y confirmación separadas

## Answer

dispatch registra un RunDoc por intento con identidad propia (exec-<agente> y -a2), separa la intención de lanzar de la confirmación de que el agente arrancó, y el closeout actualiza el RunDoc del intento que cierra. Toca el modelo de RunDoc (run.py), dispatch.py, el runtime de scion y el closeout; el snapshot de contratos de modelo se actualizó con la tarea.
