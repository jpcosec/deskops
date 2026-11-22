---
sldb:
  by: agent
  at: '2026-11-22T15:02:19Z'
  authority: generated
  via: create_document
id: atom-reap-no-pierde-los-commits-del-ejecutor
title: reap no pierde los commits del ejecutor
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# reap no pierde los commits del ejecutor

## Answer

dispatch reap cuenta los commits con base..rama al momento del reap, nunca borra una rama cuya punta no está en la base, y espera (sale 3, la cola reintenta) si el worktree del agente tiene cambios sin commitear o si el agente sigue vivo; git worktree remove ya no usa --force. El 2026-11-22 una carrera de 6 s entre el reap y el commit del ejecutor dejó colgante el intento 2 del guard de sldb. Commits 67f55538ddc6ce8bb025ab49f928e3aa9eaeb91c y 43b17685326610719574807f78044110330af4b9.
