---
sldb:
  by: agent
  at: '2026-11-18T22:07:05Z'
  authority: generated
  via: create_document
id: atom-contenedores-scion-venv-propio-con-uv-python-3-12-via-a
title: 'Contenedores scion: venv propio con uv python 3.12 (vía a)'
five_wh_one_plus: how
tags:
- system:deskops
- topic:scion
provenance: deskops/runtime/scion.py
---

# Contenedores scion: venv propio con uv python 3.12 (vía a)

## Answer

Decision 2026-11-18: via (a). El .venv del workspace apunta a /usr/bin/python3.12 del host, ausente en las imagenes scion (solo 3.13), asi que no arranca. El agents.md generado para ejecutor y tester abre con un paso que corre 'uv venv /tmp/ws-venv --python 3.12', 'uv pip install -e <desk_root>[dev] -e <sldb>' y pone /tmp/ws-venv/bin primero en PATH sin PYTHONPATH. Medido en scion-claude: uv venv 27.9 s (incluye descargar CPython 3.12.16), install 2.2 s, total ~30 s (< 3 min), tests/test_dispatch.py 18 passed en 188 s. Scion no tiene hook de inicio, por eso es una instruccion en agents.md. Via (b) (imagen con python3.12) no fue necesaria.
