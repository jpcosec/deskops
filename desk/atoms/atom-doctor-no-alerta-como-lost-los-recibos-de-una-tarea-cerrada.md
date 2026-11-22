---
sldb:
  by: agent
  at: '2026-11-22T00:17:23Z'
  authority: generated
  via: create_document
id: atom-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
title: doctor no alerta como lost los recibos de una tarea cerrada
five_wh_one_plus: how
tags:
- system:deskops
- topic:doctor
---

# doctor no alerta como lost los recibos de una tarea cerrada

## Answer

closed_task_ids reconoce como cerrada una tarea con commit de asunto exacto 'closeout: <task-id>' (o con los trailers Closeout-Mode/Run-Id), y doctor deja de alertar como lost los recibos de tareas cerradas: en IR baja de 83 a 0. Commits c0df7045058dc5c4ddd6d5f143f9fae4038cd47f y 91f44d0d1710c2c428d5edebb8a9e8424c42f89f. Agotó los dos intentos de tester; el texto de la alerta lost restante y el test con closeout real siguen en una tarea aparte. La verificación del coordinador está en runs/subagents/20261122-verif-doctor-lost.
