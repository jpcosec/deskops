---
sldb:
  by: agent
  at: '2026-11-23T06:14:51Z'
  authority: generated
  via: create_document
id: atom-integrate-corre-la-suite-con-basetemp-propio-y-limpia-temporales-de-corridas-muertas
title: integrate corre la suite con basetemp propio y limpia temporales de corridas
  muertas
five_wh_one_plus: how
tags:
- system:deskops
- topic:integrate
---

# integrate corre la suite con basetemp propio y limpia temporales de corridas muertas

## Answer

integrate pasa a la suite PYTEST_ADDOPTS con --basetemp dentro de su carpeta deskops-integrate-*, que el finally borra, y al empezar, bajo el lock de suite, borra las carpetas deskops-integrate-* de corridas muertas (pid de owner.pid que ya no vive, o sin owner.pid y más viejas que suite_timeout). Así /dev/shm no acumula pytest-of-<usuario> ni restos de un integrate matado por OOM.
