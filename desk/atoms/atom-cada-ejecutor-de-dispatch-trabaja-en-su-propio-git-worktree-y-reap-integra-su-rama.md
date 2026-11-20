---
sldb:
  by: agent
  at: '2026-11-20T18:17:10Z'
  authority: generated
  via: create_document
id: atom-cada-ejecutor-de-dispatch-trabaja-en-su-propio-git-worktree-y-reap-integra-su-rama
title: Cada ejecutor de dispatch trabaja en su propio git worktree y reap integra
  su rama
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# Cada ejecutor de dispatch trabaja en su propio git worktree y reap integra su rama

## Answer

deskops dispatch start executor crea la rama deskops/<name> (name = agente scion de la tarea, rol e intento) desde la rama local de integrate.branch (o main) y el worktree <desk>/.worktrees/<name>, ignorado por .git/info/exclude; el prompt.md le dice al ejecutor que trabaje y commitee ahí. Al terminar, dispatch reap hace cherry-pick de los commits de esa rama sobre la rama local principal, en orden, y borra el worktree y la rama; si hay conflicto aborta, deja todo y sale con error. El tester sigue probando la rama principal e integrate no cambia. Así varios ejecutores del mismo repo no se pisan el árbol de trabajo.
