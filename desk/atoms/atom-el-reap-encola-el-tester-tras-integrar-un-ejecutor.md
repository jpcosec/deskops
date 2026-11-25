---
sldb:
  by: agent
  at: '2026-11-25T03:14:26Z'
  authority: generated
  via: create_document
id: atom-el-reap-encola-el-tester-tras-integrar-un-ejecutor
title: El reap encola el tester tras integrar un ejecutor
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch-reap
---

# El reap encola el tester tras integrar un ejecutor

## Answer

dispatch reap encola dispatch-tester cuando integra el commit de un ejecutor y no hay tester vivo ni un dispatch-tester pendiente o corriendo de la misma tarea, sea el intento que sea; cubre los reintentos, donde la tarea ya esta en ritual-testing y el hook de la transicion no corre.
