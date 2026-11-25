---
sldb:
  by: agent
  at: '2026-11-25T01:56:44Z'
  authority: generated
  via: create_document
id: atom-un-dispatch-start-que-falla-antes-de-que-el-agente-arranque-no-gasta-intento
title: Un dispatch start que falla antes de que el agente arranque no gasta intento
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
provenance: deskops/dispatch.py
---

# Un dispatch start que falla antes de que el agente arranque no gasta intento

## Answer

Si scion templates sync o scion start fallan, o el agente queda en fase error o failed tras start, deskops/dispatch.py deshace el lanzamiento: borra el run_dir (lo que cuenta como intento), destrackea el RunDoc, quita su commit con reset --soft si sigue siendo HEAD (si no, commitea el borrado), quita worktree y rama del agente y borra el agente roto. Imprime fallo tecnico y no se gasto el intento N; el siguiente start usa el mismo intento. Lo prueba tests/test_dispatch.py.
