---
sldb:
  by: agent
  at: '2026-11-20T23:08:26Z'
  authority: generated
  via: create_document
id: atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso
title: 'Se borró el camino legacy de deskops message: sin subcomando es un error de
  uso'
five_wh_one_plus: how
tags:
- system:deskops
- topic:messages
---

# Se borró el camino legacy de deskops message: sin subcomando es un error de uso

## Answer

En deskops/cli/commands/message.py se borró _run_legacy: deskops message sin subcomando sale con rc 2 y un error de uso que nombra send, list, read y ack. El escenario e2e inbox-to-task usa deskops message list --root ., y los tests de message e inbox se actualizaron. El código partió del trabajo sin commitear de otra sesión (patch en runs/subagents/20261120-message-legacy-wip/).
