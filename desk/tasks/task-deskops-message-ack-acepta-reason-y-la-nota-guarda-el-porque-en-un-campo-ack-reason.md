---
sldb:
  by: agent
  at: '2026-11-17T01:29:59Z'
  authority: generated
  via: create_document
id: task-deskops-message-ack-acepta-reason-y-la-nota-guarda-el-porque-en-un-campo-ack-reason
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-222401-suggestion-deskops-message-ack-no-admite-una-raz-n-y-inboxnote-no-tiene-un-campo-para-guardarla.md
depends_on: []
pills: []
files:
- deskops/models/inbox.py
- deskops/cli/registry.py
- deskops/cli/commands/message.py
- tests/test_message_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
---

# deskops message ack acepta --reason y la nota guarda el porque en un campo ack_reason

## Rationale

_Explain why this task exists or the business driver behind it._

IR (nota 20261116-222401): al cerrar notas con deskops message ack no hay forma de dejar el porque. ack no acepta --reason y el modelo de la nota (deskops/models/inbox.py) solo tiene kind, sender_project, target_project, created_at, status, acknowledged_by y acknowledged_at, asi que deskops edit inbox-note tampoco puede escribirlo. Con la regla de JP de procesar cada nota al llegar (ack si es aviso o ya resuelta, tarea o drawer y ack si es trabajo), el porque de cada ack tiene que quedar en el desk.

## Goal

_Describe the concrete result this task must produce._

deskops message ack <selector> --reason <texto> marca la nota como acknowledged y guarda el texto en un campo opcional ack_reason del modelo de la nota; sin --reason el ack funciona como hoy y ack_reason queda vacio; deskops message read muestra ack_reason cuando existe.

## Scope

_State what is in scope and what is out of scope._

Entra: el campo opcional ack_reason en deskops/models/inbox.py (y lo que el store necesite para declararlo), la opcion --reason de message ack en deskops/cli/registry.py y deskops/cli/commands/message.py, la salida de message read, y tests. Sale: notas ya existentes (no se migran; ack_reason vacio es valido) y otros desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Agregar ack_reason (texto, opcional, por defecto vacio) al modelo de la nota. 2) --reason en message ack; escribirlo junto con acknowledged_by y acknowledged_at. 3) message read lo muestra. 4) Tests en desk sandbox (tmp_path): ack con --reason lo guarda y read lo muestra; ack sin --reason sigue igual; una nota vieja sin el campo sigue leyendose. 5) Correr test_command_registry.py y los goldens de ayuda (cambia la ayuda de message ack).

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py

## Done When

_Name the observable condition that makes the task complete._

ack --reason guarda y read muestra ack_reason, el ack sin --reason no cambia, las notas viejas siguen leyendose y los tres archivos de la Validation pasan.
