FILE:desk/tasks/task-los-rituales-context-review-y-phase-nombran-deskops-review-y-la-regla-de-activacion-como-gate-de-la.md
---
sldb:
  by: agent
  at: '2026-11-17T01:36:10Z'
  authority: generated
  via: create_document
id: task-los-rituales-context-review-y-phase-nombran-deskops-review-y-la-regla-de-activacion-como-gate-de-la
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/gates-por-tipo/dag.yaml
depends_on: []
pills: []
files:
- desk/rituals/context-review.md
- desk/rituals/phase.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
---

# los rituales context-review y phase nombran deskops review y la regla de activacion como gate de la tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GC08 del plan congelado gates-por-tipo (desk/drawer/plans/gates-por-tipo/dag.yaml), el unico nodo de ese plan que sigue vigente tras el triaje del 2026-11-16. El ritual context-review todavia describe la revision barata con el comando pi a mano (el perfil pi --provider deepseek ... en su linea 18) y guarda la reformulacion en runs/subagents/<run-dir>/preflight.md; el ritual phase describe su gate sin la regla de activacion. Desde CC31-CC33 eso lo hacen deskops review preflight|bundle|dispose con un RuntimeProfileDoc (default runtime-pi-deepseek-flash) y las reglas rule-activation-<tipo> de desk/lifecycle, como ya dicen docs/operator-manual.md y el quickstart.

## Goal

_Describe the concrete result this task must produce._

desk/rituals/context-review.md describe la revision de contexto como deskops review preflight y deskops review bundle (con --engine <perfil> y el default runtime-pi-deepseek-flash), su recibo en desk/reviews/<tarea>/ y su disposicion con deskops review dispose; desk/rituals/phase.md nombra la regla rule-activation-<tipo> como el gate que deja pasar una tarea a ejecucion. Ninguno de los dos instruye correr pi a mano.

## Scope

_State what is in scope and what is out of scope._

Entra: los pasos de context-review que hoy describen el comando pi manual y el archivo preflight.md del run dir, y el gate de phase. Los rituales se cambian con deskops edit ritual <id> <campo> <valor> --root . (nunca a mano). Sale: los otros rituales, las reglas de desk/lifecycle, docs/ (ya estan al dia) y el plan gates-por-tipo (se retira aparte).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) deskops show ritual context-review --root . y deskops show ritual phase --root . para ver campos y pasos. 2) Reescribir los pasos afectados con deskops edit ritual, tomando la redaccion de docs/operator-manual.md sobre deskops review. 3) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops show ritual context-review --root . (sin 'pi --provider' ni 'preflight.md' como instruccion)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops doctor --root . (sin hallazgos nuevos sobre rituales)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py

## Done When

_Name the observable condition that makes the task complete._

context-review y phase nombran deskops review preflight|bundle|dispose y la regla de activacion, no instruyen pi manual, doctor no da hallazgos nuevos y tests/test_skill_cli_drift.py pasa.

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

FILE:desk/rituals/context-review.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:18Z'
  authority: generated
  via: create_document
# ritual-xxx
id: ritual-context-review
# Ordered prose steps; not document references
steps:
- '1. Map the multilevel DAG: root, packages, leaves and dependency edges. Start with
  the question at the current node; review every node and its edges, not only the
  root.'
- '2. Save input.md as an explicit concatenation of FILE:<path> headers and UTF-8
  texts in documented order. Hash the exact saved bytes with SHA-256, without additional
  normalization. Evidence directory: runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/.'
- '3. Launch a new ephemeral process for each attempt. On this machine the verified
  profile is: pi --provider deepseek --model deepseek-flash --thinking low --offline
  --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates
  --no-tools --system-prompt <reviewer-role> --print @<input.md>. Save the command,
  provider/model/profile and reason for cheap selection. No --continue or --resume.
  Record isolation flags and supplied input as operational evidence; this does not
  assert knowledge of provider internal memory.'
- '4. Instruct the non-executing reviewer to restate the objective and scope, enumerate
  ambiguities and produce a detailed dry-run: which supplied sources it would read,
  proposed edits, dependency/interface implications, commands it would run later and
  expected validation outcomes. It may name commands but must not run them, inspect
  unsupplied sources or edit files.'
- 5. Save output and coordinator comparison with owner intent, including missing guardrails,
  required textual corrections and disposition. A word such as APTO is never sufficient.
  Keep transport/quota/unavailable-model failures separately from comprehension findings;
  stop or retry an available cheap model with explicit reason, without expert rescue.
- 6. Use misunderstandings as feedback on the brief. Correct its text; split oversized
  or ambiguous nodes recursively into coherent children and explicit dependency edges.
  Review root, packages and all leaves, plus contracts across edges. Do not execute
  while ambiguity remains unresolved.
- 7. Retry the revised explicit input in a new process, with no prior review or oral
  fixes injected. A new input or changed dependency contract invalidates affected
  reviews, including dependent nodes whose supplied contract changed; unrelated typos
  do not revoke every review. Preserve previous attempts for traceability.
- '8. Before Executor dispatch, run two separate cheap roles under this protocol:
  TaskDoc-only preflight (save reformulation also at runs/subagents/<run-dir>/preflight.md),
  then cold-bundle coverage using TaskDoc, routed instructions/rituals, bound pills,
  linked atoms/files and validation targets supplied explicitly. The coordinator accepts
  both comparisons before dispatch.'
- 9. Only reviewed ready leaves may enter the execution ritual. Expert council review
  of design, an Executor implementation and a fresh independent Tester are separate
  gates; none substitutes for cheap comprehension or human product decisions.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:context-review
---

# Cheap recursive zero-context brief review

## Purpose

_Explain why this ritual exists._

Test whether a cheap isolated reviewer understands the written question before planning, promotion or execution. Durable rule: [source atom](../atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md). This ritual is a documentary gate; it adds no lifecycle state or runtime enforcement.

## Trigger

_State when this ritual should start._

Run while drafting or revising a plan, root, package or leaf, before promotion or execution and again when its explicit input or dependency contract changes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The coordinator names the node, exact versioned brief, explicit dependencies/interfaces and expected intent. Large nodes can still be drafts; they need not be promoted to receive review.
- The supplied context is minimal: exact brief plus only necessary explicitly supplied references, with a documented order and paths. No chat history, previous outputs, oral corrections, persistent memory or automatically loaded context/skills.
- A cheap available provider/model is selected with a recorded reason and profile. Do not claim global minimum price without measurement; do not replace a failed cheap reviewer with an expert to obtain approval.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every required root/package/leaf review has exact input/hash, provider/model/profile and selection reason, command/isolation evidence, reformulation, ambiguities, detailed non-executing dry-run, coordinator comparison and required changes.
- The coordinator compares understanding with intent rather than accepting a verdict token; no unresolved ambiguity remains before execution.
- Each attempt used a new process without history, memory, automatic skills/context or reviewer tools. TaskDoc-only and cold-bundle evidence remain separate.
- Changed node inputs and dependency contracts invalidate the affected reviews; review coverage is explicit by node/revision, never inferred from council approval or plan structure.

## Failure Modes

_List common mistakes this ritual prevents._

- Asking an expert council to compensate for an unclear brief, or treating APTO/structural PASS as comprehension or execution authorization.
- Reviewing only the root or whole large DAG and claiming every descendant passed.
- Letting a reviewer execute the dry-run or loading implicit chat history, skills, memory or previous corrections.
- Retrying in the same session, fabricating node evidence, or marking pending reviews approved.
- Confusing transport/quota failures with ambiguous intent, or replacing cheap review with execution/testing.

## Completion

_Describe what completion looks like._

For the reviewed node/version, the coordinator has accepted a faithful reformulation and detailed dry-run with no unresolved ambiguity; all required descendant and interface reviews are traceable. This proves brief comprehension only. Promotion, execution, independent testing, product decisions and closeout retain their own gates.

FILE:desk/rituals/phase.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:20Z'
  authority: generated
  via: update_document
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 1. Apply [ritual-context-review](context-review.md) cheaply and recursively to the
  root, packages and every leaf with their dependency interfaces. Compare reformulation,
  ambiguities and detailed non-executing dry-run with intent; correct briefs and split
  large nodes into children and edges before selecting ready leaves.
- 1. Identify the ready dependency layer of tasks whose prerequisites are satisfied
  and whose planned changes do not overlap operationally.
- '1. Confirm each task has a fresh execution context bundle: the task doc, board-routed
  instructions, bound pills, linked atoms, linked files, and validation targets.'
- 1. Run the execution ritual for each task in the phase before implementation begins.
- 1. Execute phase tasks in parallel when the environment supports it, or in isolated
  fresh contexts when parallelism is unavailable.
- 1. Require each task to close with its own targeted validation and atomic task commit
  before considering the phase complete.
- 1. When all phase tasks are closed, run shared integration or end-to-end validation
  for the combined layer.
- 1. Fix interaction regressions uncovered by the phase-level validation before phase
  closeout.
- '1. Reconcile the pill set touched by the phase: retire stale pills, merge or delete
  redundant pills, and promote durable residue into atoms and materializations.'
- 1. Capture newly discovered tasks, dependencies, or next-phase pills before advancing.
- 1. Create one descriptive phase-closing commit for the integration and reconciliation
  pass.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:phases
---

# Phase ritual for dependency-layer execution

## Purpose

_Explain why this ritual exists._

Run one horizontal dependency layer of tasks as the workflow unit above individual task execution, then close that layer with integration validation, pill reconciliation, and next-phase preparation. Review decomposition under [ritual-context-review](context-review.md) before selecting leaves; this adds no lifecycle state.

## Trigger

_State when this ritual should start._

Start during decomposition of the multilevel DAG, before promotion or selection of a ready non-overlapping layer; close the layer only after every task closes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The board's active tasks and dependencies are explicit.
- The ready phase has been identified as a non-overlapping layer.
- Each task has a named context bundle and validation target.
- Phase-level validation expectations are known.
- A pill reconciliation pass is planned for phase closeout.
- Ready leaves and their governing root/package contracts have current accepted cheap context reviews; expert council verdicts and topological order do not satisfy this gate.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every task in the phase executed from fresh context.
- Every task closed with its own tests and its own commit.
- Shared phase validation passed after task integration.
- Regressions caused by task interaction were fixed before advancing.
- Pills touched by the phase were reconciled as stale, redundant, durable, or still active.
- Durable residue from pills was promoted into atoms and materializations when needed.
- Newly discovered work for later phases was captured explicitly.
- The phase closeout has its own descriptive commit.
- Cheap reviews are evidenced by node/input/attempt under ritual-context-review; changed inputs or dependency contracts invalidated affected reviews and retries used new processes.

## Failure Modes

_List common mistakes this ritual prevents._

- Starting a phase without identifying the actual dependency layer.
- Treating a semantic milestone as a phase even when tasks still depend on one another.
- Letting tasks share one long-lived execution context instead of fresh task-specific bundles.
- Advancing to the next phase after isolated task tests without integration validation.
- Carrying stale or overlapping pills forward because each task closed independently.
- Hiding phase-level regressions inside later task commits instead of closing the layer explicitly.
- Selecting leaves from a root-only or expert-reviewed plan without recursive cheap reviews; treating hierarchy or structural PASS as execution authorization.

## Completion

_Describe what completion looks like._

The current dependency layer is integrated, reconciled, and committed, and the board is ready to start the next phase.

FILE:instruccion
Cold-bundle de la tarea task-los-rituales-context-review-y-phase-nombran-deskops-review-y-la-regla-de-activacion-como-gate-de-la: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops show ritual context-review --root . (sin 'pi --provider' ni 'preflight.md' como instruccion)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops doctor --root . (sin hallazgos nuevos sobre rituales)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py

