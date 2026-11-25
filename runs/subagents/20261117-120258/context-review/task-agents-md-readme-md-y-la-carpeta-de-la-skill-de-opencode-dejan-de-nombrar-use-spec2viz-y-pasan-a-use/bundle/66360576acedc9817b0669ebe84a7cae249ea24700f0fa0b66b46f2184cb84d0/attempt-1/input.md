FILE:desk/tasks/task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use.md
---
sldb:
  by: agent
  at: '2026-11-17T01:25:43Z'
  authority: generated
  via: create_document
id: task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-175512-suggestion-seguimiento-de-ir13-cerrado-en-ce66f69e-2421ca29-agents-md-25-rutea-a.md
depends_on: []
pills: []
files:
- AGENTS.md
- README.md
- .opencode/skills/use-spec2viz/SKILL.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
---

# AGENTS.md, README.md y la carpeta de la skill de opencode dejan de nombrar use-spec2viz y pasan a use-specir

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento de la tarea de skills de IR13 (ce66f69e, closeout 2421ca29; nota 20261116-175512). Quedaron fuera de sus files: AGENTS.md rutea a la skill use-spec2viz y README.md cita references/spec2viz-cli.md. Ademas la carpeta .opencode/skills/use-spec2viz tiene name: use-specir en su frontmatter (lo exige specir retirement check), y opencode pide que name coincida con el nombre de la carpeta.

## Goal

_Describe the concrete result this task must produce._

AGENTS.md y README.md nombran la skill use-specir del repo IR en vez de use-spec2viz y de references/spec2viz-cli.md, y la carpeta .opencode/skills/use-spec2viz pasa a .opencode/skills/use-specir (git mv) con su SKILL.md sin cambios de contenido.

## Scope

_State what is in scope and what is out of scope._

Entra: AGENTS.md, README.md y el git mv de la carpeta de la skill de opencode. Sale: .claude/skills/deskops-workflow (ya migrada), el repo IR y menciones historicas de spec2viz (por ejemplo 'spec2viz se archiva'), que se quedan.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep -n spec2viz AGENTS.md README.md. 2) Cambiar cada mencion que instruye a usar use-spec2viz o references/spec2viz-cli.md por use-specir (skills/use-specir/SKILL.md del repo IR). 3) git mv .opencode/skills/use-spec2viz .opencode/skills/use-specir. 4) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -rn use-spec2viz AGENTS.md README.md .opencode (sin coincidencias, rc 1)

## Done When

_Name the observable condition that makes the task complete._

grep de use-spec2viz en AGENTS.md, README.md y .opencode no da nada, la carpeta se llama use-specir y tests/test_skill_cli_drift.py pasa.

FILE:desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md
---
id: atom-code-changes-close-with-tests-and-commit
title: Code changes close with tests and commit
five_wh_one_plus: when
tags:
- system:deskops
- topic:testing
- topic:git
- topic:closeout
---

# Code changes close with tests and commit

## Answer

A task that modifies code is not closed until relevant tests pass and the completed change is recorded in a descriptive git commit.

FILE:AGENTS.md
# Agent Onboarding

This file is the first stop for agents working in this repository. It is a routing document, not the full operator manual.

## Startup Route

Read in this order before changing files:

1. `README.md` for repository purpose, install flow, and tool boundaries.
2. `docs/faq.md` for first-use CLI orientation.
3. `desk/tasks/Board.md` for active routing, board pills, and rituals.
4. The board-routed pills under `desk/contexts/` that match the task.
5. `desk/rituals/phase.md`, `desk/rituals/execution.md`, `desk/rituals/testing.md`, and `desk/rituals/closeout.md` for board/phase and task gates.
6. Relevant atoms under `desk/atoms/`, preferably found through `sldb find` or graph commands rather than raw scanning.

If the active board does not route a task, do not treat fixture-looking files in `desk/tasks/` as real work by default. Use `desk/drawer/tasks/Board.md` for deferred backlog; a drawer item becomes active work only when someone authors the task with `deskops add task --from-drawer <selector> ...`, declaring its closeout evidence (`--task-type` or `--evidence`).

## Skill Route

Load the global surface skill that matches the work before changing files. Workflow roles such as supervisor, executor, and tester are system-prompt concerns, not repo-local skills:

- `use-deskops` for `desk/` surfaces, tasks, drawer work, pills, rituals, the lifecycle graph, repo registry, and workflow operations.
- `use-sldb` for `StructuredNLDoc` models, reversible Markdown markers, `.sldb` stores, document tracking, model registration, rendering, extraction, or field operations. The authoritative global Pi skill lives in the sibling `../sldb/.pi/skills/use-sldb/`.
- `use-kgdb` for graph contracts, graph snapshots, nodes, edges, provenance, `deskops graph build`, `deskops graph missing`, or graph runtime validation.
- `use-spec2viz` for diagram specs, Mermaid/projection outputs, and generated diagram surfaces under `docs/diagrams/`.
- `customize-opencode` only for opencode configuration, `.opencode/` agents, skills, plugins, MCP servers, permissions, or `AGENTS.md`/opencode routing changes.

For Pi in this repo, prefer the project skills under `.pi/skills/`.

## Core Boundaries

- `deskops/` contains Python implementation code.
- `desk/` contains workflow document data: tasks, pills, rituals, atoms, inbox notes, drawer items, and the lifecycle graph (`desk/lifecycle/`).
- SLDB owns structured Markdown infrastructure, model contracts, reversible templates, stores, field queries, and safe document edits.
- KGDB owns graph contracts and graph runtime validation.
- Spec2viz owns structured diagram sources and generated diagram projections.

Docs are human-facing materializations of atoms, not the durable source of truth by themselves. When adding or changing a substantive rule in `docs/`, first capture it in one or more atoms under `desk/atoms/`, then make the doc reflect those atoms.

Do not add desk-local field documents to duplicate SLDB field behavior. If an expected SLDB path fails, capture the gap in the sibling `sldb` repo inbox first, then route an explicit desk task before building a deskops workaround.

## Working Rules

- Start with ambiguity review. If a task would require improvisation, record or resolve the ambiguity before implementation.
- New unrouted repo-local project work starts in `desk/drawer/tasks/`, not `desk/inbox/`. Reserve inbox for incoming notes, unclear external input, or cross-repo intake.
- Commit the drawer task creation before authoring the active task. Commit the authored task (`deskops add task --from-drawer ...`) before implementation.
- Keep one coherent deliverable per task.
- Treat active work as a dependency graph: tasks are atomic units, phases are the current horizontal layer of non-overlapping ready tasks, and the next phase does not begin until the current phase passes its closeout ritual.
- For active desk tasks, run the execution-ritual fresh-context subagent review before implementation. Each task should execute in its own fresh subagent context bundle: the task doc, routed instructions, bound pills, linked atoms, linked files, and validation targets. Use additional subagents for broad exploration when the task is non-trivial.
- Correction: pills are not 1:1 with tasks.
- Treat pills as reusable atomic truths, not one-to-one task artifacts.
- Bind relevant pills by checking `when`, `where`, and `how_not`, not just titles.
- Do not skip from implementation to closeout. Pass execution, testing, and closeout gates explicitly.
- Keep changes small and scoped. Do not clean unrelated dirty worktree changes.
- For mutating CLI exploration or UX testing, write to a disposable sandbox desk such as `.tmp/deskops-cli-test`, not the repo's real `desk/`, unless the task is intentionally changing the tracked desk.
- Every closed task ends with its own atomic commit, made by `deskops closeout commit` after `closeout verify` checks exactly the evidence the task declared at creation (printed as declared X; found Y). `closeout supersede` and `closeout retire` are the closes for a vanished subject or a pre-lifecycle resolution.
- When every task in a phase is closed, run the phase ritual: execute shared integration validation, reconcile pills, capture newly discovered work, and make the phase-closing commit before starting the next phase.

## Validation

Minimum validation for code changes:

```bash
pytest
```

For CLI changes, also run the affected command directly, for example:

```bash
python -m deskops --help
deskops faq
```

For graph or store work, prefer semantic checks:

```bash
sldb stores check --store .sldb
deskops graph missing
```

## Selected Source Documents

- `README.md`
- `docs/quickstart.md`
- `docs/operator-manual.md`
- `docs/faq.md`
- `docs/atoms.md`
- `docs/workflow-policy-reference.md`
- `docs/how-to-test-ux-cli.md`
- `.pi/skills/use-deskops/SKILL.md`
- `../sldb/.pi/skills/use-sldb/SKILL.md`
- `docs/agent-system-prompts/README.md`
- `.opencode/skills/use-deskops/SKILL.md` (parallel copy)
- `.opencode/skills/use-sldb/SKILL.md` (parallel copy)
- `desk/tasks/Board.md`
- `desk/drawer/tasks/Board.md`
- `desk/rituals/phase.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/contexts/pill-001-task-closure-commit.md`
- `desk/contexts/pill-005-subagent-execution.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/atoms/workflow-model/atom-first-safe-action-follows-read-route.md`
- `desk/atoms/workflow-model/atom-clean-agents-start-from-minimum-workflow-set.md`
- `desk/atoms/workflow-model/atom-agents-read-by-decision-need.md`
- `desk/atoms/workflow-model/atom-agents-read-through-semantic-tools.md`
- `desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md`
- `desk/atoms/workflow-model/atom-clean-subagent-ambiguity-review.md`
- `desk/atoms/workflow-model/atom-phase-gates-prevent-agent-skipping.md`
- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-cli-mutation-testing-uses-sandbox-desk-roots.md`
- `desk/atoms/atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly.md`

The end-to-end manual is `docs/operator-manual.md`; `docs/quickstart.md` is the shortest walkthrough.

FILE:README.md
---
atoms:
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-deskops-owns-workflow-not-document-infrastructure
  role: documents
- id: atom-sldb-is-read-write-edit-surface
  role: documents
- id: atom-spec2viz-mirrors-sldb-for-diagrams
  role: documents
- id: atom-cli-should-match-spoken-workflow-language
  role: documents
- id: atom-desk-test-root-precedence-is-explicit
  role: documents
---
# deskops

Source atoms are declared in the YAML frontmatter.

Workflow-domain instance built on top of `sldb`.

This repo owns the operational surfaces that should not live inside generic `sldb` infrastructure: `desk/`, deferred drawer work, workflow-native models, pills, rituals, atoms, and materializers.

Understanding `deskops` requires understanding `sldb` first: `sldb` owns structured Markdown infrastructure for querying, writing, and editing modeled documents, while `deskops` owns the workflow-domain instance built on top of it.

## Layout

- `desk/` - active and deferred workflow surfaces
- `docs/` - durable deskops-specific documentation
- `tests/` - workflow-domain tests

Durable guides currently include:

- `docs/quickstart.md`
- `docs/operator-manual.md`
- `docs/faq.md`
- `docs/workflow-policy-reference.md`
- `docs/atoms.md`
- `docs/how-to-report.md`
- `docs/how-to-test-ux-cli.md`

Pi/project agent guidance includes:

- `.pi/skills/use-deskops/SKILL.md`
- `.pi/skills/deskops-task-lifecycle/SKILL.md`
- `.pi/skills/deskops-inbox-coordination/SKILL.md`
- `.pi/skills/deskops-health-and-drift/SKILL.md`
- `../sldb/.pi/skills/use-sldb/SKILL.md`
- `docs/agent-system-prompts/README.md`

Parallel opencode copies also exist under `.opencode/skills/`.

Claude Code uses `.claude/skills/deskops-workflow/` (`SKILL.md` plus `references/deskops-cli.md`,
`references/spec2viz-cli.md` and `references/vocabulary.md`). This is the versioned copy: on each machine,
`~/.claude/skills/deskops-workflow` is a symlink to it, so the skill is the same in every repo that uses deskops
and on every machine that pulls this repo:

```bash
ln -sfn "$(pwd)/.claude/skills/deskops-workflow" ~/.claude/skills/deskops-workflow
```

Edit the skill here, not in `~/.claude/skills/`, and commit it with the CLI change it documents.

## SLDB Boundary

`sldb` owns reusable structured-document infrastructure:

- `StructuredNLDoc` model contracts
- reversible Markdown templates using `⸢rev•field⸥` markers
- structured document creation and updates
- field extraction from Markdown into model payloads
- field-level query, update, append, clean, create, and remove commands
- section ownership for fields
- store tracking, integrity hashes, recovery, and composition primitives

`deskops` owns workflow-domain surfaces:

- active tasks and boards
- rituals, the task lifecycle graph (rituals as states, sldb relations as gated transitions), and gates
- transient pills and inbox notes
- durable atoms and materializers
- drawer triage for deferred work

Fields are already first-class in `sldb`. Do not create desk-local field documents just to make fields reusable, queryable, writable, or editable. Use `sldb docs`, `sldb fields`, `sldb sections`, `sldb ast`, and tracked document payloads for that.

Use `sldb` as the preferred write/edit path for modeled Markdown: `sldb docs create`, `sldb docs update`, `sldb fields update`, `sldb fields append`, `sldb fields clean`, and `sldb fields remove` should be preferred over ad hoc file edits whenever the document is tracked by a `StructuredNLDoc` model.

If that SLDB path does not work, capture the failure in the sibling `sldb` repo's inbox with the failing command, expected behavior, actual behavior, and relevant model/document references. Do not silently bypass SLDB or reimplement the missing field/document behavior inside `deskops` before the SLDB issue is recorded.

`deskops/spec/fields/` may define artifact schema vocabulary for the deskops compiler, but `desk/fields/` should not become a human-facing workflow surface or duplicate SLDB's field model.

Model changes should use SLDB's model workflow where possible:

- `sldb models add <model-ref> --store .sldb --pythonpath .`
- `sldb models template edit <ModelName> --input <template.md> --store .sldb --pythonpath .`
- `sldb models fields add <ModelName> <field> --type <type> --description <text> --store .sldb --pythonpath .`
- `sldb models fields remove <ModelName> <field> --store .sldb --pythonpath .`
- `sldb models validate <ModelName> --store .sldb --pythonpath .`
- `sldb models validate <ModelName> --promote --store .sldb --pythonpath .`

Use physical search for concrete names, paths, field paths, document names, and section titles:

```bash
sldb find title --in physical --store .sldb --pythonpath .
sldb find desk/atoms --in physical --store .sldb --pythonpath .
```

Use semantic search for model semantics, document tags, and meaning-oriented discovery:

```bash
sldb find topic:atoms --in semantic --store .sldb --pythonpath .
sldb find type.knowledge.atom --in semantic --store .sldb --pythonpath .
```

Use `--in both` when unsure, and `--global` when the local store should include linked/federated stores.

Maintain the semantic store with:

```bash
sldb stores check --store .sldb
sldb stores update --store .sldb --pythonpath .
sldb stores build --check --store .sldb
```

## Spec2viz Boundary

`spec2viz` owns structured diagram generation in the same way `sldb` owns structured Markdown operations.

Use `spec2viz` when a diagram has or should have a structured YAML source. The YAML spec is the source of truth; Mermaid, PlantUML, SVG, or other rendered outputs are projections.

Use `spec2viz` for:

- validating structured diagram specs
- rendering human-facing diagrams from semantic YAML
- keeping diagrams aligned with their underlying architecture/process model
- avoiding hand-maintained duplicate Mermaid or PlantUML surfaces

Common commands:

```bash
spec2viz validate <diagram-spec.yaml>
spec2viz render <diagram-spec.yaml> --backend mermaid --out <output-dir>
spec2viz render <diagram-spec.yaml> --out <output-dir>
spec2viz schema --out spec2viz.schema.json
```

For `docs/diagrams/`, prefer this rule:

- structured YAML specs are editable source
- `.mmd`, PlantUML, SVG, or rendered diagram files are generated projections
- if a generated diagram is wrong, fix the YAML source or the renderer, not only the generated output
- if `spec2viz` cannot express or render the needed diagram, capture the gap in the sibling `spec2viz` repo's inbox before creating a deskops-specific workaround

The intended parallel is:

- `sldb`: structured data plus model contract -> Markdown document and field/query/edit surface
- `spec2viz`: structured diagram spec plus diagram contract -> rendered visual artifact

Both exist to reduce drift by making the structured source explicit and regenerating the human-facing projection from it.

## Install

Install `deskops` from this repo checkout:

```bash
pip install -e .[dev]
```

If `sldb` is not already available on the machine, `deskops` can bootstrap it from the sibling checkout at `../sldb`.

The store under `.sldb/core/` is derived and not versioned; `.sldb/store.yaml` declares it. After cloning, build it once:

```bash
sldb stores build --store .sldb
```

Recommended first-use flow:

```bash
deskops bootstrap
deskops init .
deskops add task --title "First task" --task-type task.docs --goal "..." --scope "..." --validation "..."
```

`deskops add task --task-type` names the type (default `task.code`): the task's type declares the evidence `deskops closeout` will verify (`docs/quickstart.md` walks through it).

`deskops bootstrap` will:

- install or repair `sldb` from the sibling checkout when it is missing
- initialize the global store at `~/.sldb` when needed
- register the `deskops` models into that global store

`deskops init <path>` will:

- ensure the bootstrap prerequisites are ready
- create a local `.sldb/` store under the target repo when missing
- scaffold `desk/` when missing

## Per-project desk config precedence

Each desk can declare tracked shared config in `desk/config.json` and optional machine-local overrides in `desk/config.local.json`.

For root/sandbox resolution, precedence is authoritative:

1. explicit CLI flag such as `--root`
2. `DESKOPS_TEST_ROOT`
3. `desk/config.local.json`
4. `desk/config.json`
5. built-in defaults

`desk/config.local.json` is intended for disposable local overrides such as sandbox settings; tracked shared expectations such as `versions.desk_format` belong in `desk/config.json`.

## CLI

Run the installed entrypoint as `deskops`, or use the module form from this repo checkout.

```bash
deskops --help
python -m deskops --help
```

Current commands (`deskops --help` is authoritative; `docs/operator-manual.md` documents every verb):

- `deskops about`, `deskops faq` - orientation
- `deskops doctor` (`deskops status` is a deprecated alias)
- `deskops bootstrap`, `deskops init`
- `deskops message send/list/read/ack`
- `deskops promote inbox-to-drawer-task`, `deskops drawer remove`, `deskops retire`, `deskops issue close/list`
- `deskops add/edit/list/show <artifact>` - tasks, pills, rituals, boards, atoms, materializations, repositories, inbox-notes, faq-docs, steps
- `deskops bind pill`, `deskops next`, `deskops advance task`
- `deskops closeout commit/supersede/retire/verify`
- `deskops repo register/whoami/remove`
- `deskops desk install/migrate/replace/update`
- `deskops atoms ...` (namespaces, crossroads, protoatoms, create/split/merge/delete/validate/reorganize/tree)
- `deskops graph build/neighbors/missing/reflect`
- `deskops materialize`, `deskops drift check`
- `deskops runtime init/status/attach/stop/workers/supervise/template`

## Testing

```bash
pytest
```

FILE:.opencode/skills/use-spec2viz/SKILL.md
---
name: use-specir
description: Remission. spec2viz is retired (IR13); diagram specs, renderers, the catalog and generated diagram projections are now handled with specIR's `specir` command and sldb. Load the use-specir skill of the IR repo.
---

# use-spec2viz → use-specir

spec2viz is retired (IR13). This file stays only so that whoever loads the old `use-spec2viz` path
finds where the guidance went. The skill to use is `use-specir`, in the IR repo:
`skills/use-specir/SKILL.md` (sibling checkout: `../IR/skills/use-specir/SKILL.md`). The
command-by-command correspondence is `docs/spec2viz/correspondencia-cli.md` in that repo.

Short map:

- render / validate / lint / schema of a spec → `specir diagram render|validate|lint|schema`
- catalog HTML → `specir catalog build`
- catalog sync / check → `sldb notations sync --catalog [--check]`
- serving the catalog's annotations → `sldb serve`
- spec from a graph or Python source → `sldb notations from-graph`

Deskops conventions that still hold: diagram docs live under `docs/diagrams/`, rendered files are
projections reproducible from their source spec, and durable knowledge goes into atoms/specs first.

FILE:instruccion
Cold-bundle de la tarea task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -rn use-spec2viz AGENTS.md README.md .opencode (sin coincidencias, rc 1)

