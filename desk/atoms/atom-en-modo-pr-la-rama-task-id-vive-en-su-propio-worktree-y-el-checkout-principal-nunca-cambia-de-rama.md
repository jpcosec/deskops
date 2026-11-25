---
sldb:
  by: agent
  at: '2026-11-25T01:56:32Z'
  authority: generated
  via: create_document
id: atom-en-modo-pr-la-rama-task-id-vive-en-su-propio-worktree-y-el-checkout-principal-nunca-cambia-de-rama
title: En modo pr la rama task/<id> vive en su propio worktree y el checkout principal
  nunca cambia de rama
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
provenance: deskops/dispatch.py
---

# En modo pr la rama task/<id> vive en su propio worktree y el checkout principal nunca cambia de rama

## Answer

En modo pr, deskops/dispatch.py crea task/<id> desde la base y la saca solo en <root>/.worktrees/<task-id>; reap trae ahi los commits del ejecutor y un segundo intento parte de task/<id>. deskops/cli/commands/closeout.py (verify y commit) y deskops/integrate.py usan ese worktree cuando existe la rama, asi el closeout se commitea en task/<id> y viaja en el PR. El checkout principal, que comparten otras sesiones, sigue en la base. Lo prueban tests/test_dispatch.py y tests/test_integrate.py; lo documenta docs/operator-manual.md (Integrate modes).
