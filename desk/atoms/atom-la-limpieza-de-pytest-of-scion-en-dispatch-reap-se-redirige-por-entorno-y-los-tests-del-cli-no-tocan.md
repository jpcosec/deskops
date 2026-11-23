---
sldb:
  by: agent
  at: '2026-11-23T15:11:14Z'
  authority: generated
  via: create_document
id: atom-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-redirige-por-entorno-y-los-tests-del-cli-no-tocan
title: La limpieza de pytest-of-scion en dispatch reap se redirige por entorno y los
  tests del CLI no tocan el /dev/shm real
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# La limpieza de pytest-of-scion en dispatch reap se redirige por entorno y los tests del CLI no tocan el /dev/shm real

## Answer

dispatch reap toma la ruta de limpieza de DESKOPS_SCION_PYTEST_TMP (por defecto /dev/shm/pytest-of-scion); el fixture Env de tests/test_dispatch.py la apunta a tmp_path, asi la salida del reap no depende del host ni se borra el directorio real.
