---
sldb:
  by: agent
  at: '2026-11-24T02:17:27Z'
  authority: generated
  via: save_document_payload
id: task-cc51-docs-config-vs-code-md-con-la-medicion-de-lineas-de-codigo-frente-a-configuracion-y-el-inventar
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-como-config/dag.yaml
- desk/drawer/plans/deskops-como-config/decisiones.md
depends_on:
- task-jp-fija-n-la-meta-de-lineas-de-python-de-deskops-que-exige-cc51
pills: []
files:
- docs/config-vs-code.md
- CHANGELOG.md
- tests/test_config_vs_code_doc.py
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# CC51: docs/config-vs-code.md con la medicion de lineas de codigo frente a configuracion y el inventario justificado

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC51 (T5.1) del plan deskops-como-config, autorizado; sus dependencias CC30-CC38 estan cerradas.

## Goal

_Describe the concrete result this task must produce._

docs/config-vs-code.md contiene: (1) lineas de Python de deskops/ por directorio de primer nivel con el comando `find deskops -name '*.py' | xargs wc -l` agrupado por directorio, en la base 827f3db7 (re-medida con el mismo comando; si difiere de 18,732 prevalece la re-medicion y se anotan ambas) y en el HEAD de main al momento de medir (se anota el hash: ese es el 'commit de cierre'); (2) inventario de configuracion (modelos, RelationDoc, RuleDoc, ViewDoc, semillas, configuracion de grafo) con su ubicacion; (3) cada archivo de deskops/ aparece una vez en una lista con su categoria: 'configuracion declarada en Python' (p. ej. deskops/models/*.py, que igual cuentan en la medicion), 'codigo justificado' con su razon (P4: closure.py y git, runtime/, materializers/, bootstrap, identity, CLI; hechos de git de CC33; agents de CC34 en el CLI) o 'deuda' con la tarea o nota que la retira. Total del HEAD medido < N (N lo fija JP en la tarea de decision). CHANGELOG con la entrada.

## Scope

_State what is in scope and what is out of scope._

Entra: docs/config-vs-code.md y CHANGELOG.md. No entra: cambiar codigo para bajar lineas (si queda > N, se reporta y se abren tareas de deuda). Precisiones del preflight 1: N no es ambiguedad: lo fija la tarea task.decision de la que depende, y esta tarea no arranca antes. La lista cubre todos los archivos de git ls-files deskops (no solo .py); la medicion de lineas cuenta solo .py. Agrupacion: find deskops -name '*.py' | xargs wc -l, sumado por el primer componente bajo deskops/ (archivos sueltos de deskops/ = 'nivel superior'), con un awk que va en el doc. Categorias: deskops/models/*.py -> configuracion declarada en Python; deskops/data/** y deskops/spec/** -> configuracion; todo lo demas -> codigo justificado (con la razon de P4 si aplica, o una frase propia) o deuda (con la tarea o nota que lo retira). 'Configuracion de grafo' = FILE_RULES, EXCLUSIONS y MATERIALIZATION_TARGETS de deskops/graph/desk_graph.py y los RelationTypeDoc/RuleDoc de deskops/data. CHANGELOG: una linea en la seccion [Unreleased] existente.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) git worktree temporal en 827f3db7 solo para medir, luego removerlo. 2) Medir HEAD. 3) Script de conteo en el doc (comando exacto). 4) Lista por archivo con `git ls-files 'deskops/*.py'`. 5) Test simple que todo archivo de deskops/ aparezca en el doc (tests/test_config_vs_code_doc.py).

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_config_vs_code_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && find deskops -name '*.py' | xargs wc -l | tail -1 (menor que N)

## Done When

_Name the observable condition that makes the task complete._

El doc existe con las dos mediciones, el inventario y la lista completa; el test pasa; el total es < N o la diferencia esta reportada con tareas de deuda.
