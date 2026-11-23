---
sldb:
  by: agent
  at: '2026-11-23T00:10:06Z'
  authority: generated
  via: create_document
id: atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola
title: deskops queue job set edita los trabajos de la cola
five_wh_one_plus: how
tags:
- system:deskops
- topic:queue
---

# deskops queue job set edita los trabajos de la cola

## Answer

El comando 'deskops queue job set <trabajo> <campo> <valor> [--json]' cambia un campo de queue.jobs en desk/config.json, valida con QueueJobSpec y sale 2 sin escribir si no valida. dispatch-reap declara retry_exit_codes [3], así que la cola reintenta el reap que espera en vez de dejarlo en failed.
