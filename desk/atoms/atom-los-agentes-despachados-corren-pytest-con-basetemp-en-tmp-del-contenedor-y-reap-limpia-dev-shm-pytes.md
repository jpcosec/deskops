---
sldb:
  by: agent
  at: '2026-11-23T08:07:20Z'
  authority: generated
  via: create_document
id: atom-los-agentes-despachados-corren-pytest-con-basetemp-en-tmp-del-contenedor-y-reap-limpia-dev-shm-pytes
title: Los agentes despachados corren pytest con basetemp en /tmp del contenedor y
  reap limpia /dev/shm/pytest-of-scion
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# Los agentes despachados corren pytest con basetemp en /tmp del contenedor y reap limpia /dev/shm/pytest-of-scion

## Answer

dispatch start agrega al prompt de ejecutor y tester export PYTEST_ADDOPTS=--basetemp=/tmp/pytest-<agente>; dispatch reap borra /dev/shm/pytest-of-scion solo si no queda ningun agente running del proyecto.
