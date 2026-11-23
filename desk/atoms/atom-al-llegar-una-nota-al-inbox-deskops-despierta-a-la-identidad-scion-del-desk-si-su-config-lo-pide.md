---
sldb:
  by: agent
  at: '2026-11-23T11:16:14Z'
  authority: generated
  via: create_document
id: atom-al-llegar-una-nota-al-inbox-deskops-despierta-a-la-identidad-scion-del-desk-si-su-config-lo-pide
title: Al llegar una nota al inbox, deskops despierta a la identidad scion del desk
  si su config lo pide
five_wh_one_plus: how
tags:
- system:deskops
- topic:identity
---

# Al llegar una nota al inbox, deskops despierta a la identidad scion del desk si su config lo pide

## Answer

DeskConfig gana identity (scion_project, agent, wake=false, command); message send llama a wake_identity tras escribir la nota, sin cambiar su rc; con la compuerta de memoria cerrada devuelve bloqueado y encola wake-identity; deskops message wake --root [--note] despierta a mano y sale con 3 si la compuerta bloquea.
