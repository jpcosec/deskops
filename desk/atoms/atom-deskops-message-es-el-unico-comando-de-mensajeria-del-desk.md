---
sldb:
  by: agent
  at: '2026-11-17T01:11:30Z'
  authority: generated
  via: create_document
id: atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
title: deskops message es el unico comando de mensajeria del desk
five_wh_one_plus: what
tags:
- system:deskops
- topic:inbox
provenance: tests/test_message_cli.py
---

# deskops message es el unico comando de mensajeria del desk

## Answer

Las notas del inbox de un desk se envian, listan, leen y confirman con deskops message send|list|read|ack (send con --to <repo> para otro desk del ecosistema). El alias deskops inbox se retiro el 2026-11-16: deskops inbox ya no es un comando (invalid choice). Docs, la skill deskops-workflow y los tests usan solo deskops message.
