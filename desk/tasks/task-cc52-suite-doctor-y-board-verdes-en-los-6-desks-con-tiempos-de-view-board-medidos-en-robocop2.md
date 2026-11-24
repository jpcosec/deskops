---
sldb:
  by: agent
  at: '2026-11-24T18:27:20Z'
  authority: generated
  via: save_document_payload
id: task-cc52-suite-doctor-y-board-verdes-en-los-6-desks-con-tiempos-de-view-board-medidos-en-robocop2
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-como-config/dag.yaml
depends_on:
- task-cc51-docs-config-vs-code-md-con-la-medicion-de-lineas-de-codigo-frente-a-configuracion-y-el-inventar
pills: []
files:
- docs/config-vs-code.md
- tests/
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# CC52: suite, doctor y Board verdes en los 6 desks, con tiempos de view board medidos en robocop2

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC52 (T5.2) del plan deskops-como-config, autorizado; dependencias CC30-CC38 cerradas. Una parte previa (view board < 2,5 s) se cerro en fd28aba3; la meta de este nodo es < 1 s en caliente.

## Goal

_Describe the concrete result this task must produce._

Una tabla en docs/config-vs-code.md (seccion Verificacion) y en el TaskDoc con, para deskops, sldb, spec2viz, scion, pron y graph_ui (en /mnt/ssd/proyectos/SLDB_1/<repo>, graph_ui en UIs/graph_ui): `deskops desk update` (dry-run, sin --apply en desks ajenos), `deskops doctor`, `deskops view board`, `sldb stores check` y `sldb rules check`, con rc y resumen. Suite completa de deskops y de sldb con -n 4: sin fallas nuevas contra main. Tiempos de `deskops view board --root .` en el desk de deskops: 3 corridas en frio (antes de cada una se borran /mnt/ssd/proyectos/SLDB_1/deskops/.sldb_cache y ${XDG_CACHE_HOME:-$HOME/.cache}/sldb) y 3 en caliente; se reportan medianas; caliente < 1 s.

## Scope

_State what is in scope and what is out of scope._

Entra: solo lectura en los 5 desks ajenos (lo que falle ahi se manda con `deskops message send --to <repo>`); en deskops, desk update --apply si el dry-run lo pide, y arreglos de codigo que la verificacion delate, cada uno en su commit con su test (pueden tocar deskops/ y tests/). Host robocop2. No entra: arreglar desks ajenos, la UI en navegador. Precisiones del preflight 1: --apply en deskops solo si el dry-run reporta divergencias, y se commitea aparte. Protocolo de tiempos: en frio, borrar las dos caches antes de cada una de las 3 corridas; en caliente, una corrida de calentamiento descartada y luego 3 seguidas. El resumen por comando es rc + numero de errores y de alertas. graph_ui vive en /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui y su id para --to es graph_ui. Solo se arreglan en deskops las fallas cuya causa este en codigo de deskops; las demas se reportan por inbox al repo dueño.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Bucle por desk con los 5 comandos y `/usr/bin/time -f %e`. 2) Suites. 3) Mediciones de view board. 4) Tabla en el doc. 5) Notas a desks ajenos con hallazgos.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea
- cd /mnt/ssd/proyectos/SLDB_1/sldb && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests
- cd /mnt/ssd/proyectos/SLDB_1/deskops && for i in 1 2 3; do /usr/bin/time -f %e deskops view board --root . >/dev/null; done (mediana caliente < 1 s)

## Done When

_Name the observable condition that makes the task complete._

La tabla de 6 desks y los tiempos estan en el doc y en el TaskDoc; suites sin fallas nuevas; hallazgos ajenos enviados por inbox.
