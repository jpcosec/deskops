---
sldb:
  by: agent
  at: '2026-11-22T10:48:44Z'
  authority: generated
  via: create_document
id: atom-dispatch-start-tester-espera-a-que-la-rama-del-ejecutor-este-integrada
title: dispatch start tester espera a que la rama del ejecutor esté integrada
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# dispatch start tester espera a que la rama del ejecutor esté integrada

## Answer

dispatch start tester sale con EXIT_BUSY (3, la cola reintenta) e imprime que espera si existe una rama deskops/<ejecutor> de la tarea con commits fuera de la rama principal. Cuando el reap la integra y la borra, el tester lanza; así no prueba main sin el cambio.
