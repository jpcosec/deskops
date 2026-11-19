---
sldb:
  by: agent
  at: '2026-11-19T13:27:15Z'
  authority: generated
  via: create_document
id: atom-queue-run-deja-en-pending-un-trabajo-cuyo-codigo-de-salida-esta-en-retry-exit-codes
title: queue run deja en pending un trabajo cuyo código de salida está en retry_exit_codes
five_wh_one_plus: how
tags:
- system:deskops
- topic:queue
---

# queue run deja en pending un trabajo cuyo código de salida está en retry_exit_codes

## Answer

Cada tipo de trabajo de queue_jobs acepta retry_exit_codes (lista de enteros, vacía por defecto). Si el comando de un trabajo sale con uno de esos códigos, queue run lo devuelve de running a pending con el mismo id, suma attempts en su JSON, imprime 'en espera: <id> ocupado (exit <n>)' y retorna 0 sin correr los siguientes ni dejar nota unclear; la próxima corrida del timer lo reintenta. Cualquier otro código distinto de 0 sigue yendo a failed. Los desks ponen [3] en dispatch-executor y dispatch-tester, porque dispatch start sale con 3 cuando el cupo de scion está ocupado.
