FILE:desk/tasks/task-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal-sin-wor.md
---
sldb:
  by: agent
  at: '2026-11-16T06:04:24Z'
  authority: generated
  via: save_document_payload
id: task-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal-sin-wor
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261104-180658-suggestion-cambios-solo-de-desk-van-directo-en-el-checkout-principal-nunca-en-un-worktree.md
depends_on: []
pills: []
files:
- .opencode/skills/use-deskops/SKILL.md
- docs/operator-manual.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La guia versionada de deskops dice que los cambios solo de desk van en el checkout principal, sin worktree

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de JP (2026-11-04, desde MEPU): crear una tarea, mandar notas, editar un campo o hacer un closeout se hace con deskops en el checkout principal del repo, sobre su rama de integracion: ponerse al dia con el remoto, git add solo de los archivos de desk/ y .sldb que toco deskops (nunca git add -A), commit con [skip ci] y push; los worktrees son para cambios de codigo que pasan por PR. Ya esta en .claude/skills/deskops-workflow/SKILL.md (lineas 80-85); falta en la guia de opencode y en el manual.

## Goal

_Describe the concrete result this task must produce._

La regla aparece en ingles, igual en ambos archivos: en .opencode/skills/use-deskops/SKILL.md y en docs/operator-manual.md (subseccion nueva '### Desk-only changes' al final de la seccion '## Desk scaffold, migration, and repair'). Texto: 'Desk-only changes go straight on the main checkout, never in a worktree. Creating a task, sending inbox notes, editing a field or committing a closeout is done with deskops in the repo main checkout on its integration branch: sync with the remote first, git add only the desk/ and .sldb files deskops touched (never git add -A: other sessions may have uncommitted work there), commit with [skip ci] and push. Worktrees are for code changes that go through a PR.'

## Scope

_State what is in scope and what is out of scope._

Entra: .opencode/skills/use-deskops/SKILL.md y docs/operator-manual.md. No entra: un aviso de deskops al correr dentro de un worktree secundario (la nota lo pide 'si aplica'; se descarta en este triaje), .pi/skills (no versionado).

## Implementation Path

_Outline the expected implementation route or affected surface._

Copiar el parrafo de .claude/skills/deskops-workflow/SKILL.md:80-85 adaptado a cada archivo y correr los tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_operator_manual.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n 'Desk-only changes go straight on the main checkout' .opencode/skills/use-deskops/SKILL.md docs/operator-manual.md (una linea por archivo)

## Done When

_Name the observable condition that makes the task complete._

El grep encuentra la regla en ambos archivos y los dos tests pasan.

FILE:.opencode/skills/use-deskops/SKILL.md
---
name: use-deskops
description: Comprehensive global deskops workflow skill. Use when working in this repository's desk/, task lifecycle, atoms, pills, rituals, graph surfaces, or deskops CLI.
---

# Use Deskops

Deskops is the workflow-domain layer for repository-local operational knowledge and execution.

Use this global skill when the task involves:

- `desk/` workflow surfaces.
- Tasks, boards, drawer work, inbox notes, pills, rituals, the lifecycle graph, atoms, or repository registry docs.
- Desk discovery, graph checks, task advancement, promotion, closeout, or workflow automation.
- Understanding how this repo's CLI maps to the project knowledge model.

## What deskops owns

Deskops owns the workflow domain built on top of SLDB.

It owns:

- active and deferred workflow surfaces under `desk/`
- task routing through `desk/tasks/Board.md`
- rituals, pills, atoms, and the lifecycle graph (`desk/lifecycle/`)
- repo-local workflow commands such as `deskops add`, `deskops list`, `deskops show`, `deskops promote`, `deskops advance task`, and `deskops graph`
- operational rules for intake, promotion, execution, testing, closeout, and phase gates

It does **not** own generic structured-document infrastructure. That belongs to SLDB.

## Mandatory read route

Before changing files, recover state from repo artifacts in this order:

1. `AGENTS.md`
2. `README.md`
3. `docs/faq.md`
4. `desk/tasks/Board.md`
5. matching board-routed pills in `desk/contexts/`
6. `desk/rituals/phase.md`
7. `desk/rituals/execution.md`
8. `desk/rituals/testing.md`
9. `desk/rituals/closeout.md`
10. relevant atoms under `desk/atoms/`

Prefer semantic discovery over blind scanning when possible:

```bash
sldb find title --in physical --store .sldb --pythonpath .
sldb find topic:atoms --in semantic --store .sldb --pythonpath .
deskops graph missing
```

## Workflow model

The project logic is:

- **tasks** are bounded units of work
- **boards** route active tasks and shared pills
- **pills** are reusable execution truths, not one-per-task notes
- **atoms** are durable knowledge and architecture truths
- **rituals** define the gates for execution, testing, closeout, and phases
- **drawer tasks** are deferred repo-local work not yet promoted to the active board
- **inbox notes** are incoming unclear or external input, not the default place for new repo-local project work

Key rules:

- New unrouted repo-local work starts in `desk/drawer/tasks/`, not `desk/inbox/`.
- Author drawer work as an active task (`deskops add task --from-drawer <selector> ...`) before implementation; there is no drawer-to-task promotion.
- Keep one coherent deliverable per task.
- Do not skip execution, testing, or closeout gates.
- `deskops advance task` stops at the closeout node; close only with `deskops closeout commit` (`--run-dir` or `--no-run --reason`).
- Every task declares its closeout evidence at creation (`--task-type` or `--evidence`); `deskops closeout verify` checks exactly that, and every closed task ends with its own atomic commit (`closeout commit`, or `closeout supersede`/`closeout retire`, which skip the evidence gates).
- When a whole ready dependency layer closes, run the phase ritual before starting the next layer.
- Docs are human-facing materializations of atoms, not the only durable source of truth.

## Task-state recovery commands

Use direct CLI commands instead of improvising from chat state:

```bash
deskops show board Board --root .
deskops list tasks --root .
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
git status --short --branch
```

If the task changes graph or store semantics, also use:

```bash
sldb stores check --store .sldb
deskops graph build --root .
deskops graph missing --root .
```

## CLI surface

Common deskops commands:

```bash
deskops --help
deskops faq
deskops bootstrap
deskops init .
deskops add task --root . --title "..." --task-type task.code --goal "..." --scope "..."
deskops add atom --root . --title "..." --answer "..." --five-wh-one-plus what
deskops list tasks --root .
deskops list atoms --root .
deskops show task <task-id> --root .
deskops show atom <atom-id> --root .
deskops add task --root . --from-drawer <drawer-selector> --task-type task.docs --title <title> --goal <goal> --scope <scope> --validation <check>
deskops bind pill <task-id> <pill-selector> --root .
deskops advance task <task-id> --root .
deskops closeout commit --task <task-id> --run-dir runs/subagents/<run-dir> --root .
deskops closeout commit --task <task-id> --no-run --reason "<why>" --root .
deskops closeout verify --task <task-id> --root .
deskops graph build --root .
deskops graph missing --root .
deskops repo register ...
deskops desk install .
```

CLI usage rules:

- Use `deskops ...`, not `bash deskops ...`.
- Prefer local repo-root execution instead of unnecessary `--root .` in prose, but include `--root .` in explicit workflow instructions when clarity matters.
- For CLI mutation or UX experiments, use a disposable sandbox desk such as `.tmp/deskops-cli-test` unless the task intentionally changes the tracked desk.

## Role logic

Workflow roles are **global/system-prompt concerns**, not repo-local skills:

- supervisor: routes, dispatches, reviews evidence, and enforces closeout gates
- executor: implements one bounded task
- tester: proves the intended contract and pill guardrails

Repo-local skills should stay focused on surfaces and tools. Do not reintroduce workflow-role prompts as auto-discovered project skills.

`subagent-execution` may still exist as a narrow repo-local helper for launching bounded worker lanes.

## Atoms, pills, and docs

Use these distinctions consistently:

- Put durable architecture or policy in atoms.
- Put reusable execution guardrails in pills.
- Put active routed work in tasks.
- Put deferred candidate work in drawer tasks.
- Treat docs under `docs/` as materializations of atom truth.

When a doc rule changes materially, update the relevant atom first, then reflect it in the doc.

## When to load other skills

- Load `use-sldb` for `StructuredNLDoc` models, tracked Markdown, reversible markers, `.sldb` stores, document tracking, field operations, rendering, extraction, or model changes.
- Load `use-kgdb` for graph contracts, graph snapshots, provenance, node/edge behavior, or graph runtime validation.
- Load `use-specir` (IR repo, `skills/use-specir/SKILL.md`; replaces the retired `use-spec2viz`) for structured diagram specs and generated diagram projections.
- Load `customize-opencode` only for opencode config, `.opencode/` agents, skills, plugins, MCP servers, permissions, or routing configuration.

## Validation

Minimum repo validation:

```bash
pytest
```

For CLI work, also run the affected commands directly, for example:

```bash
python -m deskops --help
deskops faq
```

For graph or store work, prefer semantic checks:

```bash
sldb stores check --store .sldb
deskops graph missing
```

## Anti-patterns

Do not:

- invent alternate workflow categories when repo docs already define them
- treat unrouted `desk/tasks/` files as active by default
- bypass the board, pills, or rituals because the task seems familiar
- use ad hoc file edits where SLDB should own the structured-document operation
- skip from implementation straight to closeout
- treat role prompts as repo-local skills

FILE:instruccion
Cold-bundle de la tarea task-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal-sin-wor: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_operator_manual.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n 'Desk-only changes go straight on the main checkout' .opencode/skills/use-deskops/SKILL.md docs/operator-manual.md (una linea por archivo)

