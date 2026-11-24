---
sldb:
  by: agent
  at: '2026-11-24T18:27:58Z'
  authority: generated
  via: save_document_payload
id: task-el-skill-deskops-workflow-y-vocabulary-md-explican-que-la-suite-completa-y-el-push-son-de-la-fase-y
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill.md
depends_on:
- task-integrate-por-lote-una-sola-integracion-por-desk-con-todo-lo-cerrado-pendiente-un-tip-una-suite-un-g
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El skill deskops-workflow y vocabulary.md explican que la suite completa y el push son de la fase y cada tarea solo corre su validacion dirigida

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill (JP 2026-11-23): .claude/skills/deskops-workflow/SKILL.md no menciona la integracion por fase y references/vocabulary.md define fase solo como capa de dependencias; un agente no sabe que la suite completa y el push son de la fase.

## Goal

_Describe the concrete result this task must produce._

SKILL.md explica como se declaran las fases en el Board al descomponer el DAG y que la integracion (suite completa, grafo, store, push y commit de cierre de fase) es de la fase, mientras cada tarea cierra con su validacion dirigida; vocabulary.md define fase como capa de dependencias declarada en el Board y unidad de integracion; los comandos citados existen en la ayuda del CLI.

## Scope

_State what is in scope and what is out of scope._

.claude/skills/deskops-workflow/SKILL.md, references/vocabulary.md y las copias del skill que el repo mantiene en sincronia (opencode u otras), mas el test de deriva entre skill y CLI si aplica. Fuera: codigo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer ritual-phase, pill-007 y los comandos nuevos de fases e integrate. 2) Redactar las secciones. 3) Correr el test de deriva del skill.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp pytest -q tests/test_skill_cli_drift.py

## Done When

_Name the observable condition that makes the task complete._

SKILL.md y vocabulary.md tienen las secciones; el test de deriva del skill contra el CLI pasa.
