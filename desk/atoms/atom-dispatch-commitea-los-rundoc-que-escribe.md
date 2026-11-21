---
sldb:
  by: agent
  at: '2026-11-21T08:29:03Z'
  authority: generated
  via: create_document
id: atom-dispatch-commitea-los-rundoc-que-escribe
title: dispatch commitea los RunDoc que escribe
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# dispatch commitea los RunDoc que escribe

## Answer

dispatch start commitea en la rama principal, con pathspec, los archivos del store que escribe record_scion_run (mensaje 'run: <agente>' y [skip ci]), y reap commitea igual los RunDoc pendientes de sus agentes antes del cherry-pick. Así el reap ya no choca con un store sin commitear cuando el commit del ejecutor también toca el store.
