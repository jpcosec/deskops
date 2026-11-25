---
sldb:
  by: agent
  at: '2026-11-25T22:51:56Z'
  authority: generated
  via: save_document_payload
id: task-el-ci-de-deskops-vuelve-a-verde-y-baja-de-1h30-a-menos-de-20-minutos
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- .github/workflows/tests.yml
- desk/tasks/task-la-suite-de-deskops-baja-su-ram-por-worker-y-declara-en-que-maquina-y-con-cuantos-workers-corre.md
depends_on: []
pills: []
files:
- tests/test_output_goldens.py
- .sldb/store.yaml
- .github/workflows/tests.yml
- pyproject.toml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El CI de deskops vuelve a verde y baja de 1h30 a menos de 20 minutos

## Rationale

_Explain why this task exists or the business driver behind it._

El workflow tests de main falla en todas las corridas desde el 22-11 y cada una tarda entre 1,5 y 2,5 h; el PR #12 se integró con el CI en rojo. Run 45486095078: en 3.13 falla test_output_goldens::test_help_goldens (golden help/deskops_add_atom.txt); en 3.12 pasan los tests (1398) pero falla 'sldb stores build --check' por rules/builtin:tag_namespace:domain (domain:knowledge-management sin CrossroadDoc.path que lo ancle), que también falla en local. La suite corre en serie: 4993 s.

## Goal

_Describe the concrete result this task must produce._

El workflow tests de main pasa en 3.12 y 3.13 y tarda menos de 20 minutos.

## Scope

_State what is in scope and what is out of scope._

Entra: .github/workflows/tests.yml, el golden de help de add atom (o hacer el test independiente de la versión de argparse), el anclaje o el retiro del tag domain:knowledge-management y paralelizar pytest en CI (pytest-xdist con un -n acorde a la RAM del runner, ver la tarea de la suite de 6 GB). Sale: reescribir tests lentos uno por uno.

## Implementation Path

_Outline the expected implementation route or affected surface._

Causas verificadas el 25-11: (A) tests/test_output_goldens.py:123, el regex _SHORT_OPTION_METAVAR_RE no normaliza los alias largo+largo que 3.13 escribe distinto; (B) .sldb/store.yaml incluye los AtomDoc (líneas 139-143) antes que el CrossroadDoc (145), así que el tag domain:knowledge-management se valida antes de que exista su namespace. 1) Normalizar A en el test, sin regenerar goldens a mano. 2) Ordenar B (CrossroadDoc antes que AtomDoc). 3) pytest-xdist en el CI con -n acorde a la RAM del runner y concurrency: cancel-in-progress. 4) Medir una corrida real.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_output_goldens.py
- sldb stores build --check --store .sldb
- gh run list -R jpcosec/deskops --workflow tests --limit 1 muestra success en menos de 20 minutos

## Done When

_Name the observable condition that makes the task complete._

Una corrida del workflow tests sobre main termina en success en 3.12 y 3.13 en menos de 20 minutos.
