---
sldb:
  by: agent
  at: '2026-11-20T00:52:21Z'
  authority: generated
  via: create_document
id: atom-dispatch-start-solo-se-frena-por-la-memoria-de-la-maquina-o-porque-la-tarea-ya-tiene-agente
title: dispatch start solo se frena por la memoria de la máquina o porque la tarea
  ya tiene agente
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# dispatch start solo se frena por la memoria de la máquina o porque la tarea ya tiene agente

## Answer

deskops dispatch start (deskops/dispatch.py) lanza un agente scion si la memoria pasa el gate de la cola (wait_reason de deskops/queue.py: disponible >= queue_min_available_gb y PSI avg60 < queue_max_psi_avg60) y si la tarea no tiene ya un agente running (label deskops.task_id). No hay tope de agentes: el límite es físico, así que varios ejecutores y testers de distintas tareas y desks corren en paralelo. Si no puede, sale con 3 ('ocupado: memoria: ...' u 'ocupado: la tarea ya tiene agente <name>') y la cola lo reintenta por retry_exit_codes.
