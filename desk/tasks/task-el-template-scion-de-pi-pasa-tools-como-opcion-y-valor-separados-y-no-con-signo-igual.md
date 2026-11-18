---
sldb:
  by: agent
  at: '2026-11-18T05:54:01Z'
  authority: generated
  via: create_document
id: task-el-template-scion-de-pi-pasa-tools-como-opcion-y-valor-separados-y-no-con-signo-igual
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/runtime/scion.py
- tests/test_scion_runtime.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
---

# El template scion de pi pasa tools como opcion y valor separados y no con signo igual

## Rationale

_Explain why this task exists or the business driver behind it._

El 2026-11-18 dos testers despachados por scion con harness pi murieron a los 10 segundos con codigo 1. `deskops runtime template` escribe en scion-agent.yaml la linea command_args con un solo elemento `--tools=read,grep,find,ls,bash`, y pi 0.73.1 rechaza esa forma con `Error: Unknown option: --tools`; acepta `--tools read,grep,find,ls,bash` como dos argumentos. Los coordinadores corrigen el template a mano.

## Goal

_Describe the concrete result this task must produce._

En `deskops/runtime/scion.py`, la funcion `_command_args` emite para el harness pi cada opcion y su valor como dos elementos separados de command_args (`"--tools", "read,grep,find,ls,bash"`). Para los demas harness se conserva la forma `opcion=valor` de hoy, que existe porque la opcion `--allowedTools` de claude es variadica y se tragaria el prompt. La decision se toma por el kind del RuntimeProfileDoc, no por el nombre del rol.

## Scope

_State what is in scope and what is out of scope._

Dentro: `deskops/runtime/scion.py`, `tests/test_scion_runtime.py`, y la mencion en `docs/operator-manual.md` si el manual describe la forma de command_args. Fuera: cambios en scion o en la imagen de pi; otros flags. Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py

## Done When

_Name the observable condition that makes the task complete._

El template generado con `--harness pi` trae command_args con opcion y valor separados; el generado con `--harness claude` no cambia; los tests lo comprueban.
