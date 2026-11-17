---
sldb:
  by: agent
  at: '2026-11-17T13:34:04Z'
  authority: generated
  via: create_document
id: task-el-test-de-llaves-de-message-send-deja-de-ser-xfail-porque-sldb-ya-renderiza-los-valores-literales
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- runs/subagents/test-deskops-t-bfb4a8401ae2/verdict.md
depends_on: []
pills: []
files:
- tests/test_message_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
---

# el test de llaves de message send deja de ser xfail porque sldb ya renderiza los valores literales

## Rationale

_Explain why this task exists or the business driver behind it._

La tarea de llaves (63b519b2) dejo en tests/test_message_cli.py un test xfail(strict=True) con reason SLDB_JINJA_VALUE_NOTE (lineas 359-365), a la espera de que sldb dejara de compilar como Jinja los valores de los campos. sldb lo arreglo en d49f6ddc ('El valor de un campo se renderiza literal: render_model_markdown deja de compilar los valores del usuario como Jinja'), ya instalado en /mnt/ssd/herramientas/sldb. Con eso las 4 variantes dan XPASS estricto y tests/test_message_cli.py falla, lo que deja roja la suite de deskops (lo encontro el tester de ack --reason).

## Goal

_Describe the concrete result this task must produce._

tests/test_message_cli.py::test_message_send_keeps_braces_in_the_body_literal es un test normal (sin xfail) y sus 4 variantes pasan contra el sldb instalado; la constante SLDB_JINJA_VALUE_NOTE se borra si ya no se usa.

## Scope

_State what is in scope and what is out of scope._

Entra: el decorador xfail y la constante SLDB_JINJA_VALUE_NOTE en tests/test_message_cli.py. Sale: codigo de deskops y de sldb, y el resto de los tests.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Confirmar que el sldb que importa el venv incluye d49f6ddc (git -C /mnt/ssd/herramientas/sldb merge-base --is-ancestor d49f6ddc HEAD). 2) Quitar el xfail y la constante. 3) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_message_cli.py pasa entero sin xfail ni XPASS y git diff solo toca ese archivo.
