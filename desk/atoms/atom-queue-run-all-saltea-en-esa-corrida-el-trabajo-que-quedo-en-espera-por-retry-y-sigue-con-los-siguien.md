---
sldb:
  by: agent
  at: '2026-11-20T01:46:59Z'
  authority: generated
  via: create_document
id: atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien
title: queue run --all saltea en esa corrida el trabajo que quedó en espera por retry
  y sigue con los siguientes
five_wh_one_plus: how
tags:
- system:deskops
- topic:queue
---

# queue run --all saltea en esa corrida el trabajo que quedó en espera por retry y sigue con los siguientes

## Answer

En deskops/queue.py (run_queue), si un trabajo sale con un código de retry_exit_codes vuelve a pending con attempts sumado, se imprime 'en espera: <id> ocupado (exit <n>)' y, con --all, la corrida sigue con los siguientes pendientes en orden sin reintentarlo hasta la próxima corrida. Así un dispatch-reap o un integrate que está detrás corre aunque un ejecutor espere. Sin --all se corre un solo trabajo. Un fallo de verdad sigue deteniendo la cola con 1.
