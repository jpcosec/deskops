---
sldb:
  by: agent
  at: '2026-11-22T08:15:00Z'
  authority: generated
  via: create_document
id: atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4
title: Los contenedores de scion traen pytest-xdist y la suite completa corre con
  -n 4
five_wh_one_plus: how
tags:
- system:deskops
- topic:runtime
---

# Los contenedores de scion traen pytest-xdist y la suite completa corre con -n 4

## Answer

pyproject.toml lleva pytest-xdist>=3.5 en el extra [dev], que el venv del contenedor instala con uv pip install -e '<desk>[dev]', y el bloque de entorno Python de deskops/runtime/scion.py que reciben executor y tester comprueba import xdist y muestra la suite completa con -n 4 (5270f990). Los ejecutores dejan de correr la suite en serie.
