---
sldb:
  by: agent
  at: '2026-11-21T10:43:03Z'
  authority: generated
  via: create_document
id: atom-init-y-sus-tests-asumen-la-resolucion-por-nombre-de-enlaces-de-sldb-3
title: init y sus tests asumen la resolución por nombre de enlaces de sldb (#3)
five_wh_one_plus: how
tags:
- system:deskops
- topic:init
---

# init y sus tests asumen la resolución por nombre de enlaces de sldb (#3)

## Answer

Con sldb #3 un enlace cuyo path no existe pero cuyo nombre resuelve al store dueño ya no está roto: init no lo repara ni imprime 'Replaced broken'. tests/test_doctor_model_registration.py cubre ese caso, el enlace a un store sano distinto (Warning) y el enlace realmente roto (reemplazo). La suite de deskops vuelve a verde contra el sldb de herramientas.
