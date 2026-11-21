---
sldb:
  by: agent
  at: '2026-11-21T05:35:05Z'
  authority: generated
  via: create_document
id: atom-integrate-no-empuja-por-separado-un-commit-de-codigo-que-no-avanza-rapido-sobre-el-remoto
title: integrate no empuja por separado un commit de código que no avanza rápido sobre
  el remoto
five_wh_one_plus: how
tags:
- system:deskops
- topic:integrate
---

# integrate no empuja por separado un commit de código que no avanza rápido sobre el remoto

## Answer

En _steps, el push del commit de código va solo si no está en el remoto y el remoto es su ancestro. Si el desk mergeó el remoto después del closeout, el código no avanza rápido: se omite su push, se imprime 'código va con el tip: <sha>' y el push del tip, que sí avanza rápido, lo lleva.
