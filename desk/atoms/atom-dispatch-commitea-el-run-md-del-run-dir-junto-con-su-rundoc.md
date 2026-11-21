---
sldb:
  by: agent
  at: '2026-11-21T19:29:05Z'
  authority: generated
  via: create_document
id: atom-dispatch-commitea-el-run-md-del-run-dir-junto-con-su-rundoc
title: dispatch commitea el run.md del run dir junto con su RunDoc
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# dispatch commitea el run.md del run dir junto con su RunDoc

## Answer

_run_store_paths incluye el run.md del run dir del agente (exec-<nombre>, o exec-<nombre>-testing para testers) si existe, y _commit_run_store lo commitea junto con el store. El RunDoc commiteado siempre tiene su archivo en el mismo commit, y el gate de store de integrate pasa con agentes vivos.
