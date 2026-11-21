---
sldb:
  by: agent
  at: '2026-11-21T23:07:36Z'
  authority: generated
  via: create_document
id: atom-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado
title: dispatch start no falla si el RunDoc de la identidad ya está trackeado
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# dispatch start no falla si el RunDoc de la identidad ya está trackeado

## Answer

Antes de record_scion_run, dispatch start des-trackea el RunDoc run-<slug> de la identidad si ya existe en el store, de modo que un relanzamiento con la misma identidad no falla. Si el record falla, borra el run_dir solo cuando quedó vacío.
