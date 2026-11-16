FILE:desk/tasks/task-retirar-el-alias-deskops-inbox-docs-y-skills-pasan-a-deskops-message-y-se-borra-el-alias.md
---
sldb:
  by: agent
  at: '2026-11-16T05:04:56Z'
  authority: generated
  via: save_document_payload
id: task-retirar-el-alias-deskops-inbox-docs-y-skills-pasan-a-deskops-message-y-se-borra-el-alias
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
- deskops/cli/registry.py
- docs/operator-manual.md
- docs/faq.md
- .claude/skills/deskops-workflow/SKILL.md
- .claude/skills/deskops-workflow/references/deskops-cli.md
- .claude/skills/deskops-workflow/references/vocabulary.md
- tests/test_message_cli.py
- tests/test_message_delivery.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md
---

# Retirar el alias deskops inbox: docs y skills pasan a deskops message y se borra el alias

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (punto 4). El alias `deskops inbox` esta deprecado a favor de `deskops message` (deskops/cli/registry.py:651, deprecated_for=('message',)). Aun lo nombran docs/operator-manual.md:421 y 425, docs/faq.md:52 y 230 y la skill .claude/skills/deskops-workflow (SKILL.md, references/deskops-cli.md y references/vocabulary.md), que es la skill global por symlink.

## Goal

_Describe the concrete result this task must produce._

Ningun doc ni skill versionado usa `deskops inbox`; el alias, sus goldens de ayuda y sus tests desaparecen.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/registry.py, docs/operator-manual.md, docs/faq.md, deskops/data/faq.md si lo nombra, .claude/skills/deskops-workflow/SKILL.md y references/, goldens de ayuda, tests/test_message_cli.py y tests/test_message_delivery.py (casos de alias). No entra: .pi/skills (no versionado). Precisiones del preflight 1: el reemplazo es deskops message send: 'deskops inbox "<texto>" --kind K --root .' pasa a 'deskops message send "<texto>" --kind K --root .' (sin --to escribe en el propio desk; con --to <repo> en otro). Entra tambien deskops/data/faq.md, .opencode/ y README.md si el grep los muestra. Goldens: los de tests/fixtures/golden/help que nombran el alias (deskops_inbox.txt y los que lo listen como comando), regenerados con pytest --update-golden. Casos de test a borrar = los que invocan 'deskops inbox' o comprueban el aviso de deprecado. El patron de busqueda es grep -rnw 'deskops inbox'.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `grep -rn 'deskops inbox' docs .claude .opencode deskops/data README.md`. 2) Reescribir con deskops message send. 3) Borrar el alias y sus tests. 4) Regenerar goldens.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rnw 'deskops inbox' docs .claude .opencode deskops/data README.md
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_grammar.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El grep queda vacio, `deskops inbox` da error de comando desconocido y los tests pasan.

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

FILE:desk/atoms/workflow-model/atom-cli-mutation-testing-uses-sandbox-desk-roots.md
---
id: atom-cli-mutation-testing-uses-sandbox-desk-roots
title: CLI mutation testing uses sandbox desk roots
five_wh_one_plus: how
tags:
- system:deskops
- topic:testing
- topic:cli
- topic:materialization
---

# CLI mutation testing uses sandbox desk roots

## Answer

When testing or exploring mutating deskops CLI commands, agents should point writes at a disposable sandbox root such as `.tmp/deskops-cli-test` instead of the repository's real `desk/`. This keeps generated tasks, lifecycle documents, inbox notes, and other workflow artifacts out of tracked project surfaces unless the mutation is intentionally changing the real desk.

FILE:docs/operator-manual.md
# deskops Operator Manual

This manual is the end-to-end operational playbook for `deskops`.

It is written for two audiences:

- people who operate a desk by hand
- agents that follow documented commands instead of reconstructing behavior from source

The examples are executable. Every fenced block marked `bash runnable` is
extracted, in document order, by `tests/test_operator_manual.py`. The test runs
the blocks in a throwaway git repository under `pytest`'s `tmp_path`, with an
isolated `HOME`, so the manual cannot drift from the real CLI.

Blocks marked `bash` are illustrative only. They show expected failures,
destructive alternatives, cross-repo targeting, or commands that need an
external runtime such as Herdr.

For the first, shortest walkthrough, read `docs/quickstart.md`. For the CLI's
first-use question index, run `deskops faq`. This manual does not re-document
SLDB; it only covers the deskops workflow surface built on top of SLDB.

## Runnables convention

The runnable walkthrough assumes:

- the current directory is an empty git repository with at least one commit
- `deskops` resolves to this checkout (`tests/test_operator_manual.py` supplies
  a shim so the examples stay spelled `deskops ...`)
- no real `~/.sldb` or user desk is touched

Run one block at a time, or let the test run all blocks in order. State created
by one block is visible to later blocks.

## Machine and repository setup

### Help and bootstrap

`deskops bootstrap` is the machine-level repair path. It verifies that SLDB is
importable, installs it from the sibling checkout only when needed, creates the
global `~/.sldb` store, and registers the deskops model set there.

```bash runnable
deskops --help
deskops bootstrap
```

### Initialize the repository

`deskops init` runs the bootstrap preflight, creates a local `.sldb/` store,
scaffolds `desk/`, and writes the lifecycle graph under `desk/lifecycle/`.

```bash runnable
deskops init .
```

### Orient yourself

```bash runnable
deskops about
deskops faq
deskops faq 1
```

`deskops faq` with no argument lists the available questions. Pass a question
index, slug, or text fragment to print one answer.

### Check desk health

`deskops doctor` reports desk shape, store registration, tracking, and model
validity. `deskops status` is a deprecated alias for the same command.

```bash runnable
deskops doctor --root .
deskops status --root .
```

The report has two parts. **Errors** mean the desk is broken: missing structure,
a tracked document that is gone, a document its model cannot read, an unregistered
model, a store that cannot be read. They make `doctor` exit 1. **Alerts** mean the
store moved under an expected change: a document edited, moved or added by hand, a
model contract that changed. Nothing is broken; register them with
`deskops desk update --apply`. Alerts alone exit 0, and they are always printed.

A task its model rejects (its `status`, `current_node` and `history` are not a state
the lifecycle can produce) is an error of its own, one line per task with the file and
the validator's text, read from the task's frontmatter, while doctor still runs the other
checks (structure, store, models). `sldb stores check` names such a document as
`store/doc-invalid` and goes on; doctor reads that finding too, for a tracked document
under another model, and does not repeat a task its frontmatter listing already named.
A task the legacy migration decides says
`Migrate it with deskops desk update --apply`; any other one says what its owner can
do (`decide its state: deskops closeout supersede --task <id> --reason ... --ref ...`).

`doctor` also compares the desk's managed seeds (the lifecycle graph and its rules
under `desk/lifecycle/`) with the ones the installed deskops ships, by the same
comparison `deskops desk update --apply` makes before rewriting them. Each copy
that differs is one finding, naming the top-level frontmatter fields that differ
(`body` when only the text below the frontmatter does; the `sldb:` write
provenance is named only when nothing else differs):

```text
lifecycle seed out of date: desk/lifecycle/execution-task_activates.md differs from the deskops package (attributes). Fix: deskops desk update --apply
```

It is an **error** when a lifecycle edge's transition fields differ (`source_id`,
`target_id`, `relation_type`, `condition`, `attributes`): `deskops advance` refuses
that edge. Any other difference (a rule, the body or notes of a seed) is an
**alert**. A desk seeded before CC31 has `attributes: {}` on its edges and shows
up here; `deskops desk update --apply` restores the managed seeds.

`doctor` raises one **alert** per absolute path (`/home/...`, `/mnt/...`) in the
frontmatter of a desk document: a path written on one machine does not exist on
another. It never changes the exit code. The store already knows where the
neighbouring repositories are (`.sldb/store.yaml` `links`, read through sldb, plus the
registry entries whose path is relative; the root of a neighbour is the parent of its
linked `.sldb`), so the alert says what the path becomes:

```text
Absolute path: desk/registry/repo-sldb.md path: /home/jp/proyectos/SLDB_1/sldb (becomes ../sldb; fix: deskops doctor --repair)
```

`--repair` rewrites those that resolve, through the desk's sldb transaction: the
`path` of a registry entry becomes a path relative to the repository root, and each
absolute entry of a task's `files` and `references` becomes `<repo-id>:<path>`, the
form `closeout resolved-by` accepts (a path of this repository becomes relative to its
root, without prefix). A path that exists here is placed by the root it falls under; a
path that does not exist (another machine) is placed only when what follows the
ecosystem folder (`SLDB_1`) names one neighbour without ambiguity. Anything else stays
an alert with its reason (no ecosystem folder, no neighbour, ambiguous, no registry
entry for that root, a field other than registry `path`, `files` and `references`).

`--repair` otherwise acts on errors only (it scaffolds structure and registers models). Use it
when you understand the reported errors:

```bash
deskops doctor --root . --repair
```

### Inspect the lifecycle graph

On a fresh desk, `next --diagram` renders the state machine as Mermaid from the
source spec. The states are ritual docs and the transitions are sldb relation
docs.

```bash runnable
deskops next --diagram --root .
```

The rendered edges include their conditions:

- `task_activates` moves a draft task into execution.
- `task_hands_to_closeout` requires a non-empty `validation` field.
- `task_completes` requires `status = 'ready_for_testing'` and verified
  closeout evidence.

## Repository identity and the ecosystem registry

`deskops repo whoami` prints the repository's configured project identity.
`deskops repo register` writes a canonical `RepositoryDoc` into the registry and
tracks it in SLDB.

Register the current repository before sending messages. Message delivery
requires the current repository to resolve through the registry when any
registry entries exist.

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo register "$identity" . --store .sldb --pythonpath .
deskops repo whoami --root .
```

`deskops repo remove <id>` takes a registration out of the registry so the
repository can be registered again, for example after a rename:

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo remove "$identity" --root . --store .sldb
deskops repo register "$identity" . --store .sldb --pythonpath .
```

`deskops add repository` is different: it creates a local repository artifact
under `desk/registry/` for discovery or routing. It is not the canonical
ecosystem registration path. The runnable walkthrough creates one later for a
sibling desk.

Cross-repo targeting uses the registered repository id:

```bash
deskops message send "Need a follow-up" --to sibling-desk --title "Follow-up"
deskops list tasks --include-repos
```

## Desk scaffold, migration, and repair

`deskops desk install` scaffolds only the desk folders and starter docs. It does
not create a store, register a repository, or write the lifecycle graph.

```bash runnable
mkdir -p ../sibling
deskops desk install ../sibling
deskops desk migrate --root ../sibling
deskops desk update --root ../sibling --apply
```

- `desk install <path>` creates `tasks/`, `contexts/`, `rituals/`, `atoms/`,
  `roles/`, `inbox/`, `drawer/`, the starter boards/pills/rituals, and
  `desk/config.json`.
- `desk migrate` adopts a legacy or partial desk non-destructively. It reports
  what it adopted, preserved, or left for manual conversion.
- `desk update` is a dry run by default. Add `--apply` to create a missing
  store, register missing models, and write the lifecycle graph.
- `desk update` also migrates the tasks a desk migrated before CC31 left in a
  state no transition produces: an empty history with a terminal or drawer
  status at a node. The dry run lists them as `Legacy task states to migrate`;
  `--apply` writes them first, one line per changed field
  (`desk/tasks/<task>.md: history [] -> [superseded]`). The table:
  `superseded` gets `history [superseded]` (its node stays); `closed`,
  `resolved`, `done`, `complete` and `cancelled` (pre-lifecycle resolved), and
  `deferred` and `candidate` (drawer), get `current_node ''`, outside the
  lifecycle. A non-terminal status with an empty history (any status that is
  not `draft` nor one of those above, nor a closeout status: `active`,
  `ready_for_testing`, `blocked`...) is backed by no transition, so it gets
  `status draft` at the entry node `ritual-execution` (an empty
  `current_node` stays empty), reported as
  `desk/tasks/<task>.md: status active -> draft` plus
  `current_node <node> -> ritual-execution` when the node moves, and its
  `summary` gets one line in front, `Migrada a draft por deskops desk update:
  estado heredado '<status>' sin history (<YYYY-MM-DD UTC>).`, followed by the
  previous summary. A non-empty history with an incoherent status is not
  migrated. Any other task the model rejects is listed under
  `Invalid task documents (not written)` with the validator's text and what its
  owner can do; it is never written. The migration writes the frontmatter
  directly because the model rejects the state, and validates the new text with
  `TaskDoc`; a task it still rejects is restored. A document sldb names with
  `store/doc-invalid` that the task listing does not cover is reported under
  `Invalid documents (not written)` with the model's rejection. `sldb stores
  check` names invalid documents and goes on, so `--apply` keeps every other
  repair (structure, lifecycle graph, models, tracking, task types, indexes); a
  store check with no JSON and a failing exit code is still an environment
  error. `--apply` exits 0
  when nothing is left and 1 while a task or another invalid document waits
  for its owner (as the dry-run does); a second run migrates nothing.

A dry run exits `1` when it finds divergence:

```bash
deskops desk update --root ../sibling
# Desk divergence report:
# - Missing store: .sldb
# - Unregistered models: ...
# Run with --apply to repair these issues.
```

## Artifact commands

The `add`, `edit`, `list`, and `show` families are generated from the artifact
registry. The same grammar applies to every artifact subject.

### Add artifacts

```bash runnable
deskops add atom --root . \
  --title "Operator manual evidence" \
  --five-wh-one-plus what \
  --answer "The operator manual examples run against the real CLI." \
  --tags system:manual topic:docs

deskops add pill --root . \
  --title "Pattern: Manual examples stay runnable" \
  --summary "Executable documentation." \
  --what "What." --why "Why." --when "When." --where "Where." \
  --how "How." --how-not "How not." \
  --tags topic:docs

deskops add ritual --root . \
  --title "Manual ritual" \
  --purpose "Purpose." --trigger "Trigger." --completion "Completion."

deskops add board --root . \
  --title "Manual board" --scope "Scope." --purpose "Purpose."

deskops add materialization --root . \
  --title "Manual materialization" \
  --source-atoms atom-operator-manual-evidence \
  --target-kind board \
  --target-identity desk/tasks/Board.md \
  --intent "Document the CLI." \
  --validation pytest

deskops add repository --root . \
  --name "Sibling desk" --path ../sibling --description "Sibling sandbox."

deskops add faq-doc --root . --title "Manual FAQ" --body "FAQ body."

deskops add step --root . \
  --title "Manual step" --action "Action." --outcome "Outcome."

deskops add inbox-note --root . \
  --kind suggestion \
  --created-at "2026-01-01T00:00:00" \
  --status open \
  --title "Manual inbox note" \
  --body "Promote this note."
```

Required and commonly used flags per subject:

| Subject | Required flags | Common extras |
|---|---|---|
| `task` | `--title` | `--why`, `--goal`, `--scope`, `--task-type` (default `task.code`), `--implementation-path`, `--done-when`, `--validation`, `--from-drawer`, `--depends-on`, `--evidence` (adds kinds only), `--inherits-from`, `--atom`, `--inherit-acceptance-context` |
| `pill` | `--what`, `--why`, `--when`, `--where`, `--how`, `--how-not` | `--summary`, `--tags` |
| `ritual` | `--purpose`, `--trigger`, `--completion` | `--preconditions`, `--steps`, `--validation`, `--failure-modes`, `--tags` |
| `board` | `--scope`, `--purpose` | `--tasks`, `--pills`, `--rituals`, `--notes`, `--tags` |
| `atom` | `--five-wh-one-plus`, `--answer` | `--title`, `--tags`, `--provenance` |
| `materialization` | `--target-kind`, `--target-identity`, `--intent` | `--source-atoms`, `--validation`, `--tags`, `--provenance` |
| `repository` | `--name`, `--description` | `--path`, `--status`, `--tags` |
| `inbox-note` | `--kind`, `--created-at`, `--status`, `--body` | `--sender-project`, `--target-project`, `--title`, `--acknowledged-by`, `--acknowledged-at` |
| `faq-doc` | `--body` | `--title` |
| `step` | `--action`, `--outcome` | `--title`, `--tags` |

`--validation`, `--depends-on`, `--atom`, and similar list flags accept repeated
or space-separated values. Put them last in a command when mixing with another
multi-value flag, because argparse consumes following tokens until the next
flag.

`--from-yaml <file>` loads the payload from YAML for every `add` subject.

`--evidence <kind>...` adds closeout evidence kinds to the type's (`tests`,
`commit`, `atom`, `materialization`, `document`, `external`); it cannot remove
one the type requires. Without `--task-type` the type is `task.code`. See Closeout.

### List artifacts

Plural subjects list all documents of a type. `--format json` is available on
every list command. `list tasks --include-repos` also follows task boards
registered as sibling repositories.

```bash runnable
deskops list atoms --root .
deskops list pills --root .
deskops list rituals --root .
deskops list boards --root .
deskops list materializations --root .
deskops list repositories --root .
deskops list faq-docs --root .
deskops list steps --root .
deskops list inbox-notes --root .
```

### Show artifacts

Singular subjects show one document by exact id, filename, stem, or a unique
slug fragment. `--format json` is available.

```bash runnable
deskops show atom atom-operator-manual-evidence --root .
deskops show pill pill-pattern-manual-examples-stay-runnable --root .
deskops show ritual ritual-manual-ritual --root .
deskops show board board-manual-board --root .
deskops show materialization materialization-manual-materialization --root .
deskops show repository repo-sibling-desk --root .
deskops show faq-doc faq-manual-faq --root .
deskops show step step-manual-step --root .
deskops show inbox-note inbox-note-manual-inbox-note --root .
```

### Edit artifacts

The edit grammar is:

```text
deskops edit <subject> <selector> <field> <value> [--root .]
```

Field names accept hyphens in place of underscores. Values are parsed like SLDB
field values, so JSON lists and quoted strings work. The document is re-rendered
through its model.

A section field of text whose template carries an italic placeholder paragraph
(`_Outline the expected implementation route or affected surface._` in a task,
`_Describe the incoming message with enough evidence to triage._` in an inbox
note) gets it from the template on every render, so `edit` drops from the value
any paragraph that is exactly that field's placeholder. Passing the raw section
text back with a new paragraph leaves one placeholder, the same value twice leaves
the same file, and a value that is only the placeholder empties the field. The
phrase inside a longer paragraph, a quote, a list or a code block is content and
stays. The placeholders are read from the model's template, never from a list.

```bash runnable
deskops edit atom atom-operator-manual-evidence title "Operator manual evidence (edited)" --root .
deskops edit pill pill-pattern-manual-examples-stay-runnable summary "Edited summary." --root .
deskops edit ritual ritual-manual-ritual summary "Edited summary." --root .
deskops edit board board-manual-board notes "Edited notes." --root .
deskops edit materialization materialization-manual-materialization intent "Edited intent." --root .
deskops edit repository repo-sibling-desk status maintenance --root .
deskops edit faq-doc faq-manual-faq body "Edited FAQ body." --root .
deskops edit step step-manual-step outcome "Edited outcome." --root .
deskops edit inbox-note inbox-note-manual-inbox-note body "Edited inbox body." --root .
```

The same subjects exist for `add`, `edit`, `list`, and `show`; `list` uses
plural names and `show` uses singular names.

## Inbox, messages, and drawer

### Send, list, read, and acknowledge messages

`deskops message` is the canonical cross-desk surface. Files are written to the
target desk's `desk/inbox/` as timestamped Markdown notes. Acknowledging closes
the note but keeps the file as the trace.

```bash runnable
deskops message send "Please clarify the manual example." \
  --kind unclear --title "Manual message" --root .
deskops message list --root .
deskops message read manual-message --root .
deskops message ack manual-message --root .
```

`deskops inbox` is a deprecated alias for the same storage. Its flag grammar
(`--list`, `--show`, `--ack`) still works:

```bash runnable
deskops inbox --list --root .
```

`--to <repo>` targets another registered repository. `--from <project>` overrides
the resolved sender identity (`--sender` is the deprecated `inbox` spelling).
`--desk-root` targets an explicit desk directory. `--format json|yaml` prints
the result for machines.

### Promote an inbox note to a drawer candidate

Inbox notes are intake. Promotion turns one note into a loose deferred candidate
under `desk/drawer/tasks/`, removes the inbox file, and records the new
candidate on the drawer board. The candidate is not yet an active task.

```bash runnable
deskops promote inbox-to-drawer-task manual-inbox-note --root .
```

`--title <text>` overrides the candidate title.

### Remove a drawer entry

`deskops drawer remove` removes the file, its tracking, and its drawer-board
bullets. It refuses when an active task records the entry in `from_drawer`
unless `--force` is passed. Any other reference to the entry is left as it is.
Each file that holds one is reported on stderr as
`alert: <entry> still referenced by <file>`, and the exit code does not change.
These references are what `sldb.api.referrers` finds over the desk graph: a
drawer-board bullet in another form, such as `` `tasks/<id>.md` ``, or a task
that names the entry. `deskops closeout` reports the files that still name the
closed task in the same way.

```bash runnable
deskops message send "Remove this candidate." \
  --kind suggestion --title "Removable candidate" --root .
deskops promote inbox-to-drawer-task removable-candidate --root .
deskops drawer remove task-removable-candidate --root .
```

### Retire any other desk document

`deskops retire` removes one obsolete file under `desk/` that has no dedicated
verb (pills, inbox notes, steps, roles, runtimes, FAQ docs, materializations,
leftovers), with a reason and a `--ref` that resolves to an ancestor commit or
an existing path. The declared fields that name the document lose that entry
in the transaction that deletes it. For a pill, these are the `pills` of the
Board and of every task. A mention in prose, such as a path in a task body, is
never rewritten, so retire refuses while one remains unless `--force` is passed.
Both kinds of reference are what `sldb.api.referrers` finds: the store's field
index, and the mention patterns of the desk graph. Tasks, drawer entries, atoms, and registry
entries keep their own verbs: `closeout`, `drawer remove`, `atoms delete`,
`repo remove`.

```bash runnable
deskops retire desk/steps/step-manual-step.md --root . \
  --reason "The manual step was only an example" \
  --ref "$(git rev-parse HEAD)"
```

## Tasks

### Author a task from a drawer candidate

There is no direct drawer-to-active promotion. A person or agent authors the
active task explicitly and records the drawer file with `--from-drawer`. The
drawer file is kept for manual cleanup. Like every task, its type declares its
closeout evidence: `--task-type task.docs` declares `commit` and `document`.

When the `files` of a task name another repository of the desk's registry
(`deskops repo register`), `add task` prints one more line after creating it, and
creates it all the same (it never blocks and does not change the type):

```text
Files of <task-id> belong to repository <repo-id>; if the work lives there consider task_type task.external or a mirror task in its desk.
```

A file belongs to another repository when it is `<repo-id>:<path>` with a registered
id, an absolute path under that repository's registered root, or a relative path that
starts at the parent folder (`../<repo>/...`) and resolves under it. Anything else is
local. Only `files` count, not `references`; the line is not printed for `task.external`
or when every file is local. `deskops doctor` lists the same line as an alert for each
open task (not closed, resolved, done, complete, superseded or cancelled) that is not
`task.external` and has such files; it does not change doctor's exit code.

```bash runnable
deskops add task --root . \
  --title "Close a manual task" \
  --task-type task.docs \
  --why "Why." \
  --goal "Goal." \
  --scope "Scope." \
  --implementation-path "Path." \
  --done-when "Done." \
  --from-drawer task-manual-inbox-note \
  --validation "pytest tests/test_manual_smoke.py"
```

### Bind reusable context pills

Pills are reusable atomic context, not one-to-one task artifacts. Bind the ones
whose `when`, `where`, and `how_not` match the task.

```bash runnable
deskops bind pill task-close-a-manual-task \
  pill-pattern-manual-examples-stay-runnable --root .
```

### Inspect, edit, and advance a task

`next <task>` explains the next valid workflow action without mutating the
task; `next <task> --why` adds why this task and these actions were selected. `show task` prints the lifecycle gates and whether each holds.

```bash runnable
deskops list tasks --root .
deskops show task task-close-a-manual-task --root .
deskops next task-close-a-manual-task --root .
deskops edit task task-close-a-manual-task scope "Edited scope." --root .
deskops review record task-close-a-manual-task --kind preflight --operator "Manual operator" \
  --evidence desk/tasks/task-close-a-manual-task.md --reason "Contract read; nothing ambiguous" --root .
deskops review dispose review-task-close-a-manual-task-preflight-1 --verdict accepted --reason "Contract reviewed by the operator" --root .
deskops advance task task-close-a-manual-task --root .
deskops advance task task-close-a-manual-task --root .
```

A task leaves `ritual-execution` only with the review receipts its type asks for
(here `task.docs`: an accepted `preflight` on the task's current contract, so it
is recorded after the last edit). This sandbox has no reviewer model, so the
operator records a human receipt (`engine: human`, `no model available`; see
[Cold context reviews](#cold-context-reviews)); a desk where the model runs uses
`deskops review preflight`. The two advances move the task from `draft` to `active` and then
`ready_for_testing`. `advance` stops at `ritual-closeout`; it never closes a
task. When no outgoing transition condition holds, it exits non-zero and names
the blocked gate.

Before applying an edge, `advance` checks it against the lifecycle the installed
deskops ships: same `relation_type`, same target ritual and same
`attributes.sets.status`. An edge that differs (a desk seeded before CC31 has
`attributes: {}`) would write a state the task model rejects, so `advance` stops
first, exits 1 and leaves the task unchanged:

```text
Error: Cannot advance task-x via task_activates: the edge desk/lifecycle/execution-task_activates.md does not set status active (attributes.sets.status is missing). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.
```

`deskops doctor` reports the same seed; `deskops desk update --apply` restores it.

There is no manual override: a transition fires only when its condition
holds, and a blocked task stays where it is while `advance` names the gate.
Closing is `deskops closeout commit` for work that was done, `closeout
resolved-by` for work that already entered the history (for example through a
PR) before the closeout, `closeout supersede` when the task's subject no longer
exists, and `closeout retire` for a task resolved before the ritual lifecycle.

## Closeout

A task's type declares the evidence that closes it (`task.code`: tests + commit + atom|materialization; `task.docs` and `task.decision`: commit + document; `task.external`: external; `task.aggregate`: children + commit; `task.refactor`: task.code's evidence plus goldens). `--evidence` only adds kinds to the type's, never removes one. `deskops closeout verify`
checks exactly that set for a board-routed task, nothing more and nothing less,
and prints `esta tarea declaró X; encontré Y` (declared X; found Y):

| Evidence | What counts |
|---|---|
| `tests` | an existing `.py` file under `tests/`, optionally with `::node`, or a `pytest <path>` reference |
| `atom` / `materialization` | one gate: an atom reference, or graph/materialization coverage or a routed follow-up reference for every path in `files`; exempt in a desk without local atom documents |
| `commit` | a lowercase 7-40 character commit id resolving to `HEAD` or an ancestor |
| `document` | an existing `.md`, `.rst`, `.txt`, `.adoc`, or `.yaml` file in `references` or `files`, outside `tests/` and `desk/tasks/` |
| `external` | an `http(s)` URL in `references`, for work tracked outside the repository |

Changed `.py` files in a task that did not declare `tests` print a visible alert
without blocking. A task created before the field existed is gated as code and
alerted to declare its evidence with
`deskops edit task <id> closeout_evidence '["commit", "document"]'`.

Verify before adding evidence. It exits `1` and prints the missing gates:

```bash
deskops closeout verify --root . --task task-close-a-manual-task
```

The manual task was authored with `--task-type task.docs`, so its type declares
`commit` and `document`: the gate asks for no test file. The example still writes
`tests/test_manual_smoke.py` because the task's `--validation` names it, and
the `pytest ...` reference is extra context the gate does not read. The atom
file is the document evidence. The commit reference must already exist, so use
an earlier commit such as the repository seed or the authoring commit. The
closing commit does not exist yet.

```bash runnable
mkdir -p tests
cat > tests/test_manual_smoke.py <<'EOF'
def test_manual_smoke():
    assert True
EOF

commit="$(git rev-parse HEAD)"
deskops edit task task-close-a-manual-task references \
  "[\"desk/atoms/atom-operator-manual-evidence.md\", \"pytest tests/test_manual_smoke.py::test_manual_smoke\", \"$commit\"]" \
  --root .
deskops edit task task-close-a-manual-task files \
  '["desk/atoms/atom-operator-manual-evidence.md"]' --root .
deskops closeout verify --root . --task task-close-a-manual-task
```

`deskops closeout commit` creates the closing commit itself. It offers two
routes:

- `--run-dir runs/subagents/<dir>` links the commit to subagent run evidence
  and adds `Task-Id`, `Run-Dir`, `Run-Id`, and `Session-Sha256` trailers.
- `--no-run --reason "<why>"` closes manually and adds `Task-Id`,
  `Closeout-Mode: manual`, and `Closeout-Reason` trailers.

Either route removes the task bundle from `desk/tasks/`, removes it from
`desk/tasks/Board.md`, records the commit in `runs/subagents/index.jsonl`, and
commits only the paths it staged. Unrelated staged work stays staged. `--paths`
accepts files and directories.

```bash runnable
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --no-run --reason "Operator manual runnable example" \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

A subagent-run closeout instead looks like:

```bash
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --run-dir runs/subagents/20260101-120000-task-close-a-manual-task \
  --run-id 6046eaef \
  --session ~/.pi/agent/sessions/<dir>/6046eaef/run-0/session.jsonl \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

### Supersede or retire a task

Two closes skip the evidence gates because no work is being proven.
`closeout supersede` closes a task whose subject no longer exists. `closeout
retire` removes a task whose status is already `resolved`, `closed`, `done`,
`complete` or `cancelled`, as pre-lifecycle tasks are, or `superseded`,
`deferred` or `candidate` with an empty history (what a desk migrated before
CC31 left; a `superseded` task with only its `superseded` record, what
`desk update --apply` makes of it, too). Retire reads the task's frontmatter, so it also removes a task its
model rejects. `closeout supersede` also closes a task
its model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads and writes the frontmatter, with the same
commit and trailers. Both close one invalid task while others remain invalid:
sldb names the others with `store/doc-invalid` and goes on. Both need `--reason` and at least one
`--ref` (an ancestor commit; supersede also accepts an existing path), make
exactly one closing commit with `Closeout-Mode: superseded` or
`Closeout-Mode: legacy-resolved` trailers, and take the task off the Board.

```bash runnable
deskops add task --root . \
  --title "Superseded manual task" \
  --task-type task.docs \
  --goal "Goal." --scope "Scope." --validation "pytest"
deskops closeout supersede --root . \
  --task task-superseded-manual-task \
  --reason "The feature this task targeted was removed before any work started" \
  --ref "$(git rev-parse HEAD)"
```

```bash
deskops closeout retire --root . \
  --task task-already-resolved \
  --reason "Resolved before the ritual lifecycle existed" \
  --ref 3900ad4
```

### Close a task whose work already entered the history

`closeout resolved-by` closes a task whose work was already committed, for
example merged through a PR, before anyone ran its closeout. It does not ask for
an atom per changed file. Its evidence is a `--reason`, at least one `--ref`
that is a commit at HEAD or an ancestor (further refs may be ancestor commits or
http(s) URLs, such as the PR), and at least one `--test` that the tests gate
accepts for the task's `files`. A ref or test that does not resolve is refused
and nothing is written. It makes exactly one closing commit with
`Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and
one `Closeout-Test` per test; the task is marked `resolved` (history
`resolved-by`) and leaves the Board. `--paths` adds paths to the closing commit
and `--message` replaces its subject. Like supersede, it also closes a task its
model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads the task's `files` and history from the
frontmatter, applies the same ref and test gates, writes `status: resolved` and
the `resolved-by` record into the frontmatter (validated with `TaskDoc`, restored
if it fails) and makes the same closing commit with the same trailers. With a
store, each of the three closes its invalid task while another one of the same
model remains invalid: sldb names it with `store/doc-invalid` and goes on, so
the tasks can be closed one after the other. Tasks that are not the one being
closed can also be migrated with `deskops desk update --apply` or decided by
hand.

```bash
deskops closeout resolved-by --root . \
  --task task-fix-thing \
  --reason "The fix entered main through PR #42 before the closeout" \
  --ref 9f64f0f --ref https://example.com/org/repo/pull/42 \
  --test tests/test_fix_thing.py
```

When the task's code entered another repository (a task.code of a coordinating
desk whose code lives in a sibling repo), qualify the ref and the test with that
repository's id: `--ref <repo-id>:<sha>` and `--test <repo-id>:<test path>`.
The id is looked up in the desk's own registry, `desk/registry/repo-*.md`,
written by `deskops repo register`. The reference is cut at its first `:`: when
what comes before it is a registered id, the rest is checked in that
repository's registered root, with the same rules as a local reference (a
lowercase commit id that is its HEAD or an ancestor; an existing `.py` file
under one of its `tests/` directories, optionally with a pytest `::node`). The
task's `files` do not widen where another repository's tests live. A prefix
that is not a registered id (or a reference without `:`) is checked locally as
before, and a prefix naming the desk itself (its `project_identity`, or a
registered repository whose root is the desk's root) is local. A registered
repository whose root is missing on this machine refuses the close with
`Registered repository <id> is not at <path> on this machine.` and writes
nothing. The closing commit is the same, made in the desk's repository, and its
`Closeout-Ref` and `Closeout-Test` trailers keep each reference as written
(`Closeout-Ref: infra:87671716`). `closeout verify`, `closeout commit` and
`closeout supersede` still accept only local evidence.

```bash
deskops repo register infra --path /srv/infra --id infra --store .sldb
deskops closeout resolved-by --root . \
  --task task-wire-infra \
  --reason "The code entered infra through PR #7" \
  --ref infra:87671716 --ref https://example.com/org/infra/pull/7 \
  --test infra:tests/test_wire.py
```

## Issues

Issues are plain Markdown files under `desk/issues/` or
`desk/drawer/issues/`. They are intentionally not modeled documents.
`deskops issue list` filters by `open`, `closed`, or `all`. `deskops issue close`
rewrites the status and appends a `## Resolution` section; it never deletes the
file.

```bash runnable
mkdir -p desk/issues
cat > desk/issues/issue-manual-example.md <<'EOF'
# Manual example issue

## Status

open

## Problem

The manual needs an issue example.
EOF

deskops issue list --root .
deskops issue close issue-manual-example --reason "Manual example" --ref . --root .
deskops issue list --status closed --root .
```

### Replace text in an unmodeled desk file

`deskops desk replace` edits a file under `desk/` that no `deskops edit`
subject reaches (issue bodies, drawer notes, role prompts, the tag namespace
file). `--old` must occur exactly `--count` times (default 1); a modeled
document is refused and pointed at its `edit` verb. The write is sldb's
`replace_text` inside the desk transaction: a store-tracked file (a role prompt)
must still validate under its model after the replacement, or nothing is written
and the command exits 1 with `Refusing to replace in <path>: ...`.

```bash runnable
deskops desk replace desk/issues/issue-manual-example.md --root . \
  --old "The manual needs an issue example." \
  --new "The manual has an issue example."
```

## Atoms

Atoms are the durable knowledge layer. The `atoms` commands cover namespaces,
protoatoms, typed atoms, crossroads, domain trees, provenance-preserving
creation, splitting, merging, deletion, and validation.

### Namespaces, crossroads, and the domain tree

A domain tag such as `domain:manual.docs` needs a written crossroad for every
parent path, created top-down. Crossroads describe what hangs below a path.
sldb checks it (and that every atom or protoatom namespace is declared) as its
tag family, from the declaration `deskops init` and `deskops desk update --apply`
write in `.sldb/store.yaml`; a desk without a store checks neither. See
`docs/atoms.md` ("Who checks the namespaces and the domain parents").

```bash runnable
deskops atoms add-namespace manual \
  --meaning "Manual-only tags" \
  --use-when "Operator manual examples" \
  --do-not-use-when "Durable knowledge" \
  --example manual:example --root .

deskops atoms crossroad manual \
  --title "Manual domain" --content "Root of manual examples." --root .
deskops atoms crossroad manual.docs \
  --title "Manual docs" --content "Documentation children." --root .

deskops atoms proto proto-manual \
  --title "Manual proto" --content "Free text." \
  --tag domain:manual.docs --root .

deskops atoms tree --root .
```

### Type a protoatom

`atoms type` converts a protoatom into a tracked model document and keeps the
protoatom as a redirect stub. For `AtomDoc`, pass `--content-field answer`
because `AtomDoc` has no `content` field.

```bash runnable
deskops atoms type proto-manual \
  --model AtomDoc \
  --id atom-typed-manual \
  --content-field answer \
  --data '{"title":"Typed manual atom","five_wh_one_plus":"what"}' \
  --root .
```

### Create an atom from a source

`atoms create` preserves exact provenance from a pill field, a missing graph
finding, or a diagram source.

```bash runnable
deskops atoms create atom-from-manual-pill \
  --five-wh-one-plus what \
  --from-pill pill-pattern-manual-examples-stay-runnable \
  --root .
```

Other source routes:

```bash
deskops atoms create atom-from-graph \
  --five-wh-one-plus what \
  --from-graph source-id->target-id \
  --graph .deskops/graph.json --root .

deskops atoms create atom-from-diagram \
  --five-wh-one-plus what \
  --from-diagram docs/diagrams/example/source.mmd --root .
```

### Merge, delete, and validate

Merge rewrites every reference to the source atom so that it names the target,
in the same transaction as the merge. It covers fields such as a task's
`atoms`, `atom:atom-<source>` anywhere in a task or issue, and a bare
`atom-<source>` under a Related Atoms heading. The source stays as a redirect
stub. `atoms delete` and `atoms split` find the same references. `atoms split` is not shown here: since CC35a sldb
refuses headings inside a field, so a sectioned atom cannot be written through
the CLI (see the drawer entry
task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field).

```bash runnable
deskops add atom --root . \
  --title "Merge source manual atom" \
  --five-wh-one-plus what \
  --answer "One."
deskops add atom --root . \
  --title "Merge target manual atom" \
  --five-wh-one-plus what \
  --answer "Two."
deskops atoms merge atom-merge-source-manual-atom \
  --into atom-merge-target-manual-atom --root .

deskops add atom --root . \
  --title "Delete manual atom" \
  --five-wh-one-plus what \
  --answer "Temporary."
deskops atoms delete atom-delete-manual-atom --root .

deskops atoms validate --all --root .
deskops list atoms --root .
deskops show atom atom-typed-manual --root .
```

`list atoms` and `show atom` are the current spellings; `atoms list` and
`atoms show` are deprecated aliases. `atoms delete` refuses to delete an atom with inbound references
unless `--force` is passed.

### Reorganize atoms by tag namespace

`atoms reorganize` moves atoms into folders derived from the
`atom_folder_axis` configured in `desk/config.json`. Without that config it
exits non-zero:

```bash
deskops atoms reorganize --dry-run --root .
# Error: No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize.
```

Configure one namespace, then run it:

```json
{ "atom_folder_axis": "object" }
```

```bash
deskops atoms reorganize --dry-run --root .
deskops atoms reorganize --root .
```

## Graph

The graph surface builds a KGDB snapshot, shows one node's neighbors, reports
missing declared targets, and writes review-only self-reflection findings.

```bash runnable
deskops graph build --root . --output .deskops/graph.json
deskops graph neighbors atom:atom-from-manual-pill --root . --graph .deskops/graph.json
deskops graph missing --root . --graph .deskops/graph.json
deskops graph reflect --root . --graph .deskops/graph.json
```

`graph missing` exits `1` when a declared target does not resolve. For example,
a materialization whose `--target-identity` names a file that does not exist as
a graph node is reported as `missing_declared_target`.

`graph reflect` writes `.sldb/runtime/self_reflection_findings.json` and only
reports findings; it does not edit desk documents.

## Roles, materialization, and drift

Role docs under `desk/roles/` are materialized into pi-agent files.
`deskops materialize` writes them to `~/.pi/agent/agents/` by default; `--out`
overrides the directory. `deskops drift check` compares rendered output with
the installed files and also checks runtime-profile bindings.

A role with `kind: pi` needs a matching `RuntimeProfileDoc` under
`desk/runtimes/`. Without it, drift reports a missing runtime profile.

```bash runnable
cat > desk/roles/manual-role.md <<'EOF'
---
id: role-manual-example
name: manual-example
description: Example role for the operator manual.
kind: pi
model: example-model
fallback_models: []
tools: []
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Manual example role

Act as the example role.
EOF

mkdir -p desk/runtimes
cat > desk/runtimes/runtime-pi.md <<'EOF'
---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: --tools
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: file
session_flag: --session
extra_args: []
unsupported_role_fields:
- fallback_models
tags:
- system:manual
---

# Pi runtime

## Summary

Pi agent runtime profile.

## Notes

Example profile.
EOF

deskops materialize --root . --out .pi-agent
deskops drift check --root . --out .pi-agent
```

`drift check` exits `1` on any finding. A mismatch names the installed file and
the role doc it was rendered from.

## Runtime and Herdr

The `runtime` commands manage a live Herdr Space. They need a `herdr`
executable and are not part of the runnable walkthrough.

```bash
# Initialize or reuse this desk's Herdr Space.
deskops runtime init --root .
deskops runtime init --root . --agents

# Inspect, focus, and close the Space.
deskops runtime status --root .
deskops runtime attach --root .
deskops runtime stop --root .

# List live agents machine-wide.
deskops runtime workers
deskops runtime workers --format json

# Block on one agent's lifecycle and report blocked/done settles.
deskops runtime supervise deskops-executor --root .
deskops runtime supervise deskops-executor --max-iterations 1 --timeout-ms 30000

# Materialize a RoleDoc + RuntimeProfileDoc as a Scion agent template
# (.scion/templates/<role-name>/: scion-agent.yaml, system-prompt.md, agents.md).
deskops runtime template deskops-executor --root .
deskops runtime template deskops-executor --root . --harness claude \
  --mode executor --task task-fix-thing --agent deskops-e-0123456789ab

# A tester is its own role and mode, with separate scope and completion rules.
deskops runtime template deskops-tester --root . --harness claude \
  --mode tester --task task-fix-thing --agent deskops-t-0123456789ab \
  --task-root . --run-dir runs/subagents/20261110-120000-task-fix-thing-testing
```

`runtime template` needs no live Herdr Space: it writes the template files from
the role and runtime-profile docs. `--mode executor` writes the agents.md for one
bounded task, `--mode tester` writes the independent verification instructions,
and `--mode coordinator` writes it for an agent that owns a desk. An explicit
mode always wins; otherwise only the selected role's own name/id is inspected
(a name or id ending in `-tester` chooses tester; a selected name or id naming a
supervisor/coordinator chooses coordinator; anything else executor). With
`--task` and `--agent` it also records the in_progress RunDoc launch intent under
`runs/subagents/`; its summary says it is intent, not proof of start.
`--task-root` names the repository whose desk owns the task (default `--root`)
and `--run-dir` points at the evidence directory. An existing RunDoc is reused
for reconciliation but never overwritten: a retry gets a new run_dir, and
attempts and their evidence are immutable.

`--context-file` accepts JSON with exactly `project`, `workspace_root`,
`desk_root`, `source_root` and `sldb_root`. `project` is a non-empty Scion slug
or UUID, never a filesystem path; the other four are absolute directories inside
`workspace_root`, where `desk_root` contains `desk/`, `source_root` contains the
`deskops` package and `sldb_root` is sldb's `src` directory. Missing, unknown,
relative, out-of-workspace or invalid values are refused before any template is
written. A valid context emits `DESKOPS_DESK_ROOT`, `DESKOPS_SOURCE_ROOT`,
`DESKOPS_SLDB_SOURCE_ROOT`, `DESKOPS_WORKSPACE_ROOT`, `DESKOPS_SCION_PROJECT`
and `PYTHONPATH=source_root:sldb_root`, plus a volume whose source and target are
`workspace_root`. It carries no secrets. Omitting the flag preserves CLI, path
and environment compatibility; the corrected prompt text is intentionally not
byte-identical to the faulty earlier wording.

Four optional container keys describe how this machine runs the agent:
`memory_limit` (a size such as `6Gi`) and `cpu_limit` (cores, such as `2`) are
written as `resources.limits`; `shared_paths` is a list of absolute host paths
bound at the same path (for example `/dev/shm`, so tests share the host tmpfs and
`/dev/shm/sldb1-tests.lock`); `env` adds static variables such as
`TMPDIR=/dev/shm` and may not redefine the derived ones. Omitted, nothing changes.

The coordinator derives a stable child identity from the task contract:
`deskops-e-<12hex>` for an executor or `deskops-t-<12hex>` for a tester, where
the hex is SHA-256 of `task_id + NUL + contract_sha256 + NUL + role`.
`contract_sha256` is the SLDB `TaskDoc.__contract__` digest. Attempt 1 uses the
base name, attempt 2 appends `-a2`, and there is no attempt 3; labels are
`deskops.task_id`, `deskops.contract_sha256`, `deskops.role` and
`deskops.attempt`. The runtime helper `scion_child_identity(task_path, role,
attempt)` returns that name and label set, and `scion_start_argv` builds the
explicit native start argv. These helpers only derive identity/argv; native
Scion orchestration remains Scion, not a DeskOps scheduler.

Native labels must be printable ASCII and at most 63 characters. The helper
preserves the full canonical task id and 64-hex contract hash in its returned
identity and name derivation; `deskops.contract_sha256` carries the 63-hex prefix.
A long or non-ASCII task-id label uses a bounded hash descriptor while TaskDoc
and RunDoc retain the full id. Copy the helper label map exactly rather than
pasting a full 64-hex digest into `--label`.

The generated coordinator reconciles its own existing executor/tester lanes and
completed handoffs before selecting new work; a restart or successful child
completion must not skip its own task or duplicate a child. It reads Scion
activity first and phase only as fallback, because the native bridge can report
`activity=completed` while `phase=running`. A dependency-ready task missing its
preflight/bundle receipt is routine work: run the cheap context review and
adjudicate factual findings before dispatch. Implementation and validation run
from the configured `desk_root`, with template artifacts and evidence under the
assigned desk `runs/` path rather than `/tmp`. Closeout runs
`deskops closeout verify`, reviews the diff, and commits only scoped
implementation/evidence/review paths with `closeout commit --paths` (never
`git add -A`). The coordinator signals `task_completed` only after all authorized
work is closed, declared evidence verified and required phase integration/commit
done; an external blocker is recorded and signalled as blocked, and only an
actual owner decision uses `ask_user`.

`runtime supervise` never answers a blocked agent's prompt and never advances a
task on a done settle. A human or supervisor decides what happens next.

## Cold context reviews

`deskops review` runs the cheap isolated reviewer from
`desk/rituals/context-review.md` and writes the receipts (`ReviewDoc`) under
`desk/reviews/`. The default engine is the `runtime-pi-deepseek-flash` profile
seeded under `desk/runtimes/` by `deskops init` and `deskops desk update --apply`;
`--engine` picks any other `RuntimeProfileDoc` under `desk/runtimes/`. Every run
also writes ritual evidence under
`runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/`.

The reviewer is an external model process, so these examples are illustrative
only; they are not part of the runnable walkthrough.

```bash
deskops review preflight task-fix-thing --root .
deskops review bundle task-fix-thing --root .
deskops review node desk/drawer/plans/gates-por-tipo GC03 --root .
deskops review status task-fix-thing --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

An unchanged input is not reviewed again; a second run does not call the model.
`review status` compares the SHA-256 of the exact current builder input bytes
with all receipts for the key. No receipts means `missing`; receipts with no
matching input mean `stale`, regardless of their old verdict. Among matching
receipts, priority is `accepted`, `rejected`, `pending` (reported as `reviewed`),
then `incomplete` (reported as `technical_failure`). A current accepted
receipt therefore survives later rejected or failed attempts. Task subjects
use the same task id whether plain or pinned with a SHA-256 anchor. Status
preserves receipts and run evidence and does not change lifecycle gates.
See [the source atom](../desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md).

`--max-attempts` (default 2) caps the good
attempts per key; `--force --reason` is the only way to re-review a key whose
input already has a good attempt. A transport failure (non-zero exit, timeout,
or output without `REFORMULACION`) is recorded with `technical_ok: false` and a
`verdict: incomplete` / `reason: technical` receipt, kept separate from
comprehension findings.

Reproduction, goldens and owner receipts are not produced by a model: whoever
operates the desk records them with the evidence they checked, and disposes of
them like any other receipt.

```bash
deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .
deskops review record task-fix-thing --kind owner --reason "approved by the owner" --root .
```

`record` writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor`
from the desk identity, and the evidence paths in `summary`. Each `--evidence` is
an existing file inside the root; anything else fails with
`Error: evidence not found: <path>` (exit 1) and writes nothing. `reproduction`
and `goldens` need at least one `--evidence`; `owner` may carry only `--reason`.
`input_sha256` is the SHA-256 of `<path>\n<content>\n` for each evidence file,
paths relative to the root, sorted and without repeats (empty without evidence).
`--kind` accepts `reproduction`, `goldens`, `owner`, `preflight` and `bundle`;
`node` comes from its own command. `deskops review dispose <review-id>` writes
the verdict.

A desk with no model to run the reviewer (the CI scenarios, the quickstart) can
still activate a task: whoever operates it records the `preflight` and `bundle`
receipts by hand. `--operator <name>` is required for those two kinds; without
it the command fails and writes nothing. The receipt keeps `engine: human`,
names the operator as its `actor`, and says `no model available` in its title
and `summary`, so nobody mistakes it for a model review. It is not a stand-in
for `deskops review preflight|bundle` on a desk where the model runs.

```bash
deskops review record task-fix-thing --kind preflight --operator "Ana" --evidence desk/tasks/task-fix-thing.md --reason "read the contract; no ambiguity" --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

## Verb coverage

This table maps every CLI verb to the section that documents it.

| Verb | Section |
|---|---|
| `about` | Orient yourself |
| `doctor`, `status` | Check desk health |
| `faq` | Orient yourself |
| `bootstrap` | Help and bootstrap |
| `init` | Initialize the repository |
| `inbox` | Inbox, messages, and drawer |
| `message send/list/read/ack` | Send, list, read, and acknowledge messages |
| `promote inbox-to-drawer-task` | Promote an inbox note to a drawer candidate |
| `drawer remove` | Remove a drawer entry |
| `retire` | Retire any other desk document |
| `issue close/list` | Issues |
| `add task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Add artifacts |
| `edit ...` | Edit artifacts |
| `bind pill` | Bind reusable context pills |
| `next`, `next --why`, `next --diagram` | Inspect the lifecycle graph; Inspect, edit, and advance a task |
| `list tasks/pills/rituals/boards/atoms/materializations/repositories/inbox-notes/faq-docs/steps` | List artifacts |
| `show task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Show artifacts |
| `advance task` | Inspect, edit, and advance a task |
| `repo register/whoami/remove` | Repository identity and the ecosystem registry |
| `desk install/migrate/update` | Desk scaffold, migration, and repair |
| `desk replace` | Replace text in an unmodeled desk file |
| `atoms add-namespace/list/reorganize/show/validate/create/delete/split/merge/crossroad/proto/type/tree` | Atoms |
| `graph build/neighbors/missing/reflect` | Graph |
| `materialize` | Roles, materialization, and drift |
| `drift check` | Roles, materialization, and drift |
| `closeout verify/commit` | Closeout |
| `closeout supersede/retire` | Supersede or retire a task |
| `closeout resolved-by` | Close a task whose work already entered the history |
| `runtime init/status/attach/stop/workers/supervise/template` | Runtime and Herdr |
| `review node/preflight/bundle/status/dispose/record` | Cold context reviews |

FILE:docs/faq.md
---
atoms:
- id: atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
  role: documents
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-deskops-owns-workflow-not-document-infrastructure
  role: documents
- id: atom-cli-should-match-spoken-workflow-language
  role: documents
- id: atom-inbox-is-coordination-intake
  role: documents
- id: atom-drawers-feed-tasks-through-promotion
  role: documents
- id: atom-available-tasks-are-board-routed-work
  role: documents
---
# deskops FAQ

Source atoms are declared in the YAML frontmatter.

This FAQ is the first-use orientation layer for `deskops`.

`deskops` is the workflow-domain layer that sits on top of `sldb`. It owns the operational workspace surfaces in `desk/`, including tasks, pills, rituals, inbox notes, deferred drawer work, and the repo registry helpers.

## How do I run the CLI correctly?

Use the installed console script `deskops ...`.

You can also run the module form `python -m deskops ...` from this repo checkout.

Do not run `bash deskops ...`. `deskops` is a CLI entrypoint, not a shell script.

Examples:

```bash
deskops --help
deskops faq
python -m deskops --help
```

## What does this repo provide today?

deskops provides a spec-driven artifact pipeline: YAML specs under `deskops/spec/` define every artifact model, fields, and operational behavior. The compiler turns specs into sldb docs at runtime. The CLI is partially derived from specs.

### Core CLI commands

- `deskops about` — short overview and first-use orientation
- `deskops bootstrap` — machine-level sldb and global-store setup
- `deskops init` — initialize a repo-local `.sldb/` plus `desk/`
- `deskops faq` — first-use help (this document)
- `deskops message` — send, list, read, and acknowledge cross-desk messages (`deskops inbox` is a deprecated alias)
- `deskops promote` — move inbox notes into loose drawer candidates (`inbox-to-drawer-task`); drawer items become tasks only by authoring them with `deskops add task --from-drawer`
- `deskops bind pill` — bind a context pill to an active task through the modeled task surface
- `deskops graph` — build graph snapshots, inspect neighbors, check missing references, and write review-only reflection reports
- `deskops repo register` — canonical repository registration in the ecosystem desk registry, tracked through SLDB
- `deskops desk install` — scaffold a desk surface in a target repository (`desk migrate`, `desk update`, `desk replace` maintain it)
- `deskops doctor` — check the desk: errors that break it apart from alerts that only moved (`deskops status` is a deprecated alias)
- `deskops add`, `edit`, `list`, `show` — create, change one field of, list, and inspect modeled desk artifacts
- `deskops next`, `advance` — show the next valid action for a task, and move it through the lifecycle graph
- `deskops closeout` — verify a task's declared evidence and make its closing commit; also `supersede` and `retire`
- `deskops drawer`, `issue`, `retire` — manage deferred drawer entries, close and list issues, retire obsolete desk documents
- `deskops atoms` — atom namespaces, protoatoms, crossroads, the domain tree, validation and reorganization
- `deskops runtime`, `materialize`, `drift` — live Herdr agents and Scion templates, installed role prompts, and drift between them

### Spec-driven artifact commands

**Add artifacts** — `deskops add <artifact> [--flags...]`

Creates structured artifact docs from spec templates. Spec fields populate the artifact model's own fields; they do not create separate desk field-instance documents.

Supported artifact types:

| Subject | Description | Key flags |
|---|---|---|
| `task` | Actionable task, walked through the desk's lifecycle graph | `--title`, `--goal`, `--scope`, and `--task-type` or `--evidence` (one is required: it declares the closeout evidence) |
| `pill` | Reusable context document | `--title`, `--what`, `--why` |
| `ritual` | Repeatable procedure template | `--title`, `--purpose`, `--steps` |
| `board` | Task coordination surface | `--title`, `--scope`, `--purpose` |
| `atom` | Durable architectural concept | `--title`, `--five-wh-one-plus`, `--answer` |
| `materialization` | Projection of atoms into a code, test, doc, or board target | `--target-kind`, `--target-identity`, `--intent`, `--source-atoms` |
| `repository` | Local repository artifact doc; not canonical ecosystem registration | `--name`, `--path`, `--status` |
| `inbox-note` | Incoming project message | `--kind`, `--title`, `--body` |
| `faq-doc` | FAQ entry | (spec-defined flags) |
| `step` | Procedure step | `--title`, `--action`, `--outcome` |

**List artifacts** — `deskops list <artifacts>`

Lists all docs of a given type:

```
deskops list tasks
deskops list atoms
deskops list pills
deskops list inbox-notes
deskops list repositories
...
```

**Show artifacts** — `deskops show <artifact> <doc-id>`

Displays one artifact doc with its model fields:

```
deskops show atom atom-001
deskops show task task-021
deskops show repository repo-deskops
```

**Advance tasks** — `deskops advance task <task-id>`

Fires the next lifecycle transition for the task. The lifecycle is part of the desk's sldb graph: the states are the rituals `ritual-execution`, `ritual-testing` and `ritual-closeout`, and each transition is an sldb `RelationDoc` between two rituals with a `--where` condition on the task (`deskops init` and `deskops desk update --apply` write them under `desk/lifecycle/`). `advance` fires the first transition leaving the task's `current_node` whose condition holds, sets the status it declares, and stops with the blocked gate named when none holds. It stops at `ritual-closeout`: it never closes the task. A task closes only through `deskops closeout`: `closeout commit --task <task-id> --run-dir <runs/subagents/dir>` or `closeout commit --task <task-id> --no-run --reason <why>` for work that was done, `closeout supersede` when the task's subject no longer exists, and `closeout retire` for a task resolved before the ritual lifecycle (both take `--reason` and `--ref`, skip the evidence gates, and still make one closing commit). `deskops show task` lists those gates and whether each holds; `deskops next --diagram` draws the graph.

For a board-routed task, `closeout commit` runs `deskops closeout verify` first. The gate checks exactly the evidence the task declared in `closeout_evidence` when it was created (`--task-type` declares the type's evidence: `task.code` and `task.debug` declare `tests`, `commit`, `atom|materialization`; `task.docs` and `task.decision` declare `commit`, `document`; `task.external` declares `external`; `--evidence` only adds kinds to the type's) and prints `esta tarea declaró X; encontré Y` (declared X; found Y). `tests` needs an existing `.py` file under `tests/`, optionally with `::node` or in the `pytest <path>` form; `commit` a lowercase hex commit id that resolves to `HEAD` or an ancestor; `atom|materialization` is one gate with two ways to pass: an atom reference, or a link for every path in the task's `files` (a materialization/graph link to an atom, or a routed follow-up reference under `desk/tasks`, `desk/drawer/tasks`, or `desk/drawer/issues`), and it is exempt when the desk has no local atom documents (a missing, empty, or README-only atoms directory qualifies); `document` an existing document file in `references` or `files`; `external` an `http(s)` URL in `references`. Changed `.py` files in a task without declared `tests` print a visible alert but do not block. The commit reference must already exist when the gate runs, so point it at an earlier commit such as the task's authoring commit; the closing commit does not exist yet.

**Promote inbox notes** — `deskops promote inbox-to-drawer-task <selector>`

Moves a project-addressed message into the drawer as a loose, deferred candidate, and removes it from the inbox and from the store:

```
deskops promote inbox-to-drawer-task <inbox-note-selector>
```

There is no promotion from the drawer to an active task. The drawer holds loosely shaped material; an active task is a fully authored task document routed by the board. A drawer item becomes active work only when someone authors the task explicitly. `--from-drawer` records the drawer file in the task's own `from_drawer` field, which later edits to `references` cannot overwrite; the drawer file itself is kept and cleaned up by hand. Like any task, its type declares its closeout evidence:

```
deskops add task --root . --from-drawer <drawer-selector> --task-type task.docs --title "..." --goal "..." --scope "..." --validation "..."
```

### Generated CLI surface

The `add`, `edit`, `list`, and `show` subcommands for spec-driven artifacts (atoms, pills, rituals, boards, repositories, inbox-notes, faq-docs, steps) are automatically generated from the artifact registry. When a new artifact type is added to `ARTIFACT_SUBJECTS` in `deskops/operations.py`, subcommands and `--flag` generation follow automatically.

For repository registration, prefer `deskops repo register`. It is the canonical ecosystem registration path because it anchors the repository document in the configured SLDB store. `deskops add repository` only creates a local `desk/registry/repo-*.md` artifact through the generic spec-driven add path.

The models under `deskops.models` and the materializers under `deskops.materializers` are also importable from Python.

Durable workflow guidance lives under `docs/`, including:

- `docs/quickstart.md`
- `docs/operator-manual.md`
- `docs/workflow-policy-reference.md`
- `docs/atoms.md`
- `docs/how-to-report.md`
- `docs/how-to-test-ux-cli.md`
- `docs/faq.md` (this file)

## What is the relationship between `deskops` and `sldb`?

`sldb` is the infrastructure layer.

`deskops` is the workflow-domain layer built on top of that infrastructure. It depends on `sldb` for structured document contracts, validation, store resolution, and tracked-document operations.

## How do I install it for local use?

Install `deskops` from this repo checkout.

```bash
pip install -e .[dev]
```

If `sldb` is not already installed, keep the sibling checkout at `../sldb` and run:

```bash
deskops bootstrap
```

That bootstrap flow installs or repairs `sldb`, creates `~/.sldb` when needed, and registers the deskops model set there.

If you only need the runtime package instead of the dev extras, `pip install -e .` is enough.

## Do I need `--root .` when I am already in the repo?

Usually no.

When you run `deskops` from the target repo root, the local desk is the implied default. Prefer the shorter local form in human-facing examples:

```bash
deskops list tasks
deskops show task task-fix-thing
deskops advance task task-fix-thing
```

Use `--root` when you are intentionally overriding the local default, for example in cross-repo commands, sandbox tests, scripts, or unusual working-directory setups.

## What should I run first in a repo?

Use `deskops init` from the target repo root.

```bash
deskops init .
```

This command ensures `sldb` is available, creates a local `.sldb/` store if it does not already exist, and scaffolds `desk/` if needed.

## Is a store required?

Not for every command.

- `deskops faq` does not require a store.
- `deskops message` can write directly into a repo-local `desk/inbox/` without a store if you pass `--desk-root` or run it from the target project.
- `deskops bootstrap` creates or repairs the global `~/.sldb` store and registers the deskops models there.
- `deskops repo register` and any auto-tracking behavior depend on a resolvable `sldb` store.

If no store is available, commands that depend on registry lookup or tracked-document registration will fail until you provide `--store` or run them from the right project context.

## What is the `desk/` directory for?

`desk/` is the operational workspace for the repo.

It holds active execution surfaces such as task docs, context pills, rituals, inbox notes, and deferred drawer work that should not become permanent documentation by default.

Durable knowledge should eventually land in code, tests, docs, or git history rather than staying only in `desk/`.

## How do I log an unclear point or suggestion?

Use `deskops message send`.

Examples:

```bash
deskops message send "The install flow still leaves a partial scaffold when registration fails" --kind unclear
deskops message send "Add explicit install examples to the README" --kind suggestion --title "README install examples"
deskops message list
deskops message read readme-install-examples
```

Use `--kind unclear` for unresolved confusion and `--kind suggestion` for proposed improvements.

The older `deskops inbox` flag grammar still works as a deprecated alias.

## How do I target another repo's desk?

There are three main targeting modes:

- run inside the target repo so the default local `desk/` is used
- pass `--desk-root` with an explicit desk path
- pass `--to` to resolve a repository through the ecosystem registry, optionally with `--store`

If you use `--to`, the target repository must already be registered and discoverable from the chosen store context.

## How do I route sibling repo tasks without copying them?

Register sibling repositories as local repository artifacts, then ask `list tasks` to include repo-routed boards:

```bash
deskops add repository --name "SLDB" --path ../sldb --description "Structured document infrastructure."
deskops list tasks --include-repos
```

`--include-repos` reads `desk/registry/repo-*.md`, resolves each registered repository path, opens that repo's `desk/tasks/Board.md`, and lists only the task files routed by that board. It does not copy sibling task files into the current repo and it does not require those task files to be tracked in SLDB.

This keeps the boundary clear: `deskops` is the current implementation of the broader `opsys` workflow layer, while SLDB remains the modeled Markdown/store layer. Cross-repo mutation, advancement, and closeout are intentionally separate future workflow decisions.

## What does `repo register` do?

It writes a repository registration document into the ecosystem desk registry and tracks it through `sldb` when the `RepositoryDoc` model is registered.

This command is for cross-repo discovery inside the workflow ecosystem, not for generic package publishing.

## What does `desk install` do right now?

It scaffolds a minimal repo-local `desk/` surface in a target repository.

The scaffold creates local `tasks/`, `contexts/`, `rituals/`, `inbox/`, `drawer/`, `atoms/`, and `roles/` directories plus `config.json` and starter files for the board, pills, rituals, the atom tag namespaces, and the drawer README.

It does not create the `.sldb/` store or the lifecycle graph that `deskops advance` reads; run `deskops init` for that.

It does not auto-register the repository in an ecosystem registry. If you want cross-repo registry discovery, run `deskops repo register ...` as a separate step once the target repo is ready.

## What does `deskops bootstrap` do?

It is the machine-level first-use repair command.

When `sldb` is missing, it installs or repairs it from the sibling `../sldb` checkout. It then initializes the global `~/.sldb` store if needed and registers the deskops model set there.

## What does `deskops init` do?

It is the repo-level first-use command.

It runs the bootstrap preflight, creates a local `.sldb/` store in the target repo if one does not already exist, and scaffolds `desk/` if it is missing.

## How do I organize atoms into folders by a tag namespace?

Set `atom_folder_axis` in `desk/config.json` to one registered tag namespace, for example:

```json
{ "atom_folder_axis": "object" }
```

Behavior (see `desk/atoms/atom-atom-folder-axis-is-one-configurable-tag-namespace.md`):

- `deskops add atom` with one `object:<value>` tag lands in `desk/atoms/<value>/`; dot-notation nests (`object:mepu.licitaciones` → `desk/atoms/mepu/licitaciones/`).
- Atoms without an axis tag, and desks without the config, stay flat (fully backwards compatible).
- Multiple axis values on one atom are rejected with an explicit error.
- `deskops list atoms --axis-value <value>` filters by the axis value; the axis value is shown in list output.
- `deskops atoms reorganize [--dry-run]` idempotently moves existing atoms into their axis folders and retargets tracked paths in the `.sldb` store.

## How do I validate changes in this repo?

Run the test suite from the repo root.

```bash
pytest
```

For CLI work, also run the relevant command directly, for example:

```bash
python -m deskops --help
deskops faq
```

FILE:.claude/skills/deskops-workflow/SKILL.md
---
name: deskops-workflow
description: This skill should be used when a repository has a top-level desk/ directory, or when the user asks to "add a task", "check the board", "advance a task", "create a pill", "create an atom", "promote from the drawer", "create or update a diagram spec", "render a diagram", "validate a spec", "build the architecture catalog", "agregar tarea", "revisar el board", "avanzar tarea", "crear un pill", "crear un atom", "promover del drawer", "renderizar diagrama", "validar spec", or otherwise mentions deskops, spec2viz, sldb, desk/, atoms, pills, routines, the desk board, or a diagram/spec YAML source. It forces use of the `deskops` and `spec2viz` CLIs instead of hand-editing desk/ files or generated diagram outputs, and enforces following the spec -> atoms|diagrams -> tasks|pills -> code|documental-projection pipeline instead of ad hoc workflow habits.
---

# deskops + spec2viz Workflow

> Where this skill lives: the deskops repo (`jpcosec/opsys`), `.claude/skills/deskops-workflow/`.
> `~/.claude/skills/deskops-workflow` is a symlink to that folder. Edit it in the repo and commit it there;
> see the deskops README, «Pi/project agent guidance».

`deskops` and `spec2viz` are CLI-driven layers for structured project workflow and structured
diagrams. `deskops` sits on top of `sldb` (structured-Markdown document infrastructure) and owns
tasks, routines, pills, atoms, drawer, and board. `spec2viz` owns diagrams the same way: a YAML
spec is the source of truth, and every rendered Mermaid/PlantUML/Vega/D2/HTML file is a generated
projection of it. Both CLIs are on PATH as `deskops` and `spec2viz` — always run `--help` on an
unfamiliar subcommand instead of guessing flags.

## The pipeline this skill enforces

Work in a deskops-managed repo flows through one pipeline. Do not skip stages or substitute a
hand-written file for a stage's generated artifact:

1. **Spec** — a structured YAML source (a deskops artifact spec or a spec2viz diagram spec).
   This is where intent and structure get declared first.
2. **Atoms | Diagrams** — durable knowledge units (`deskops atoms ...`) and rendered diagrams
   (`spec2viz diagram render` / `spec2viz catalog build`) derive from specs and decisions. Atoms
   answer exactly one 5W1H question each; diagrams are visual projections, never hand-authored
   Mermaid/PlantUML files maintained in parallel with a spec.
3. **Tasks | Pills** — routed, gated work (`deskops add task`, `deskops advance task`, the
   `desk/tasks/Board.md`) consumes atoms and diagrams as context. Pills (`deskops add pill`,
   `deskops bind pill`) carry transient, task/phase-bound knowledge needed to execute correctly.
4. **Code | Documental projection** — implementation closes with tests and a commit
   (`deskops closeout commit` when a run-dir exists). Generated docs/diagrams/materializations are
   projections of atoms and specs — if one is wrong, fix the atom/spec/renderer, never patch the
   generated file directly.

A pill that stabilizes into durable knowledge must graduate into an atom
(`deskops add atom`) instead of being left as a permanent pill. Work that is not yet ready to
execute belongs in the drawer or inbox. Inbox notes move into the drawer with
`deskops promote inbox-to-drawer-task`; a drawer item never becomes a task directly — the drawer is
loose by design and a task is a fully authored, compiled bundle. Author the task in full with
`deskops add task ... --from-drawer <selector>`, which records the drawer file in the task's own
`from_drawer` field and keeps it for manual cleanup. Never jump straight to code.

## Hard rules

- **Orient before acting.** At the start of any non-trivial work in a repo with `desk/`, run
  `deskops status --root .` and `deskops list tasks --root .` (or read `desk/tasks/Board.md`)
  before inventing a plan. Routed work already tracked there takes priority over ad hoc scope.
- **Never hand-write or hand-edit modeled `desk/` artifacts** (tasks, pills, atoms, routines,
  boards, inbox notes, repositories, faq-docs, steps, conditions, operators, checklists, hooks,
  edges, rituals). Create them with `deskops add <kind> ...` and change one field at a time with
  `deskops edit <kind> <selector> <field> <value> --root .`. If the CLI cannot express something
  needed, log it with `deskops inbox "<gap>" --kind unclear --root .` instead of bypassing the
  model with a raw file edit.
- **Never hand-edit a generated diagram.** `.mmd`, `.puml`, `.svg`, and generated `.html` catalog
  files are projections. Fix the YAML diagram spec (or the renderer, if the gap is systemic) and
  re-run `spec2viz diagram render` / `spec2viz catalog build`. Validate before rendering:
  `spec2viz diagram validate <spec.yml>`.
- **Advance tasks through the CLI, not by editing status fields.** Use
  `deskops advance task <selector> --root .` and check what is next with
  `deskops next <selector> --root .` rather than manually flipping a task's phase/status text.
- **Bind context explicitly.** Attach a pill to a task with `deskops bind pill <task> <pill> --root .`
  instead of referencing it only in prose. Bind atoms to a task via `--atom` on `deskops add task`
  or a follow-up edit, so the task's context is queryable, not implicit.
- **Promote deliberately, author tasks explicitly.** Move an inbox note into the drawer with
  `deskops promote inbox-to-drawer-task`. There is no drawer-to-task promotion: write the task
  yourself with `deskops add task --from-drawer <selector> --title ... --goal ... --scope ...
  --validation ...`, then remove the drawer item by hand once the task supersedes it. Do not
  silently start implementing something that only exists as an inbox note, a drawer item, or a
  chat request.
- **Close code changes with tests and a commit.** Run the task's validation command, then commit.
  If a `runs/subagents/<run-dir>` exists for the task, prefer
  `deskops closeout commit --root . --task <task> --run-dir <dir> ...` over a plain `git commit`,
  since it stamps the commit with task/run trailers deskops can trace later.
- **Check consistency instead of assuming it.** Use `deskops doctor --root .`,
  `deskops drift check --root .`, and `deskops graph missing --root .` when something looks
  inconsistent, before manually reconciling files by hand.
- **Desk-only changes go straight on the main checkout, never in a worktree** (JP, 2026-11-04).
  Creating a task, sending inbox notes, editing a field or committing a closeout is done with
  `deskops` in the repo's main checkout on its integration branch (e.g. `dev`): sync with the
  remote branch first, `git add` only the `desk/` files deskops touched (never `git add -A`: other
  sessions may have uncommitted work there), commit with `[skip ci]` and push. Worktrees are for code
  changes that go through a PR; a worktree just to document a task is ceremony.
- **Bootstrap once per machine, init once per repo.** If `deskops`/`sldb` or a local `.sldb/`
  store are missing, run `deskops bootstrap` then `deskops init .` — do not scaffold `desk/`
  by copying files from another repo.

## Quick command map

| Intent | Command |
|---|---|
| Orient in a repo | `deskops status --root .`, `deskops about` |
| See routed work | `deskops list tasks --root .`, `deskops show task <id> --root .` |
| Create a task | `deskops add task --root . --title ... --goal ... --scope ... --validation ...` |
| Advance a task | `deskops advance task <id> --root .` / `deskops next <id> --root .` |
| Create/bind a pill | `deskops add pill --root . --what ... --why ... --when ... --where ... --how ... --how-not ...` then `deskops bind pill <task> <pill> --root .` |
| Create an atom | `deskops add atom --root . --five-wh-one-plus <what\|why\|how\|how_not\|when\|where\|for_whom> --answer ...` |
| Promote / author work | `deskops promote inbox-to-drawer-task <selector> --root .`, then `deskops add task --root . --from-drawer <selector> --title ... --goal ... --scope ... --validation ...` (no drawer-to-task promotion) |
| Validate a diagram spec | `spec2viz diagram validate <spec.yml>` |
| Render a diagram | `spec2viz diagram render <spec.yml> --out <dir> [--renderer mermaid\|plantuml\|vega\|d2\|antonia-html\|json]` |
| Build a diagram catalog | `spec2viz catalog build --config <catalog.yml> --out <out.html>` |
| Close a task's code | run the task's validation, then `deskops closeout commit --root . --task <id> --run-dir <dir> ...` (or plain commit if no run-dir) |
| Check consistency | `deskops doctor --root .`, `deskops drift check --root .`, `deskops graph missing --root .` |

## Additional resources

- `references/deskops-cli.md` — full `deskops` subcommand reference (all `add`/`edit`/`list`/`show`
  kinds, `atoms`, `graph`, `promote`, `closeout`, `repo`, `desk`).
- `references/spec2viz-cli.md` — full `spec2viz` subcommand reference (`diagram`, `catalog`,
  renderers, schema export, legacy aliases).
- `references/vocabulary.md` — precise definitions of task/routine/phase/board, drawer/promotion,
  pill-vs-atom lifecycle, and the spec2viz mirror-of-sldb relationship, for when the mental model
  itself (not just a command) needs grounding.

FILE:.claude/skills/deskops-workflow/references/deskops-cli.md
# deskops CLI reference

Captured from `deskops --help` and per-subcommand `--help`. Run `deskops <command> --help` (or
`deskops <command> <subcommand> --help`) to confirm current flags before relying on this file —
the CLI evolves.

Top-level: `deskops {about,doctor,status,faq,bootstrap,init,inbox,promote,add,edit,bind,next,list,show,advance,repo,desk,atoms,graph,drift,materialize,closeout}`

Most subcommands take `--root <path>` to target a repository other than the current directory.
Selectors (task ids, pill ids, atom ids, etc.) accept an exact id, filename, stem, or unique slug
fragment.

## Setup

- `deskops bootstrap` — install/repair the sibling `sldb` checkout, create `~/.sldb`, register
  deskops models in the global store. Run once per machine.
- `deskops init .` — ensure bootstrap prerequisites, create a local `.sldb/` store, scaffold
  `desk/` if missing. Run once per repo.
- `deskops desk install .` — scaffold a minimal `desk/` without touching the local store.
- `deskops repo register` — canonically register a repository in the ecosystem registry and track
  it in SLDB.
- `deskops repo context` — manage repository contexts.

## Orientation

- `deskops about` — short overview and first-use commands.
- `deskops status --root .` — current workspace/workflow status.
- `deskops faq` — browse the first-use FAQ by question.
- `deskops doctor --root . [--repair]` — detect (and optionally non-destructively repair) broken
  desk states.
- `deskops drift check --root .` — detect drift between atoms and their materializations.
- `deskops graph missing --root . [--graph <path>]` — report missing graph targets / dangling
  declared references.
- `deskops graph neighbors` — incoming/outgoing neighbors for one graph node.
- `deskops graph trace` — trace a graph node to its root sources.
- `deskops graph reflect --root . [--graph <path>]` — write review-only self-reflection findings
  for a graph snapshot.
- `deskops graph build` — build the KGDB graph snapshot runtime artifact.

## Inbox and drawer promotion

- `deskops inbox "<message>" --kind {unclear,suggestion} --title "<title>" --root .` — log a note.
- `deskops inbox --list --root .` / `deskops inbox --show <selector> --root .` — list/show notes.
- `deskops promote inbox-to-drawer-task <selector> --root . [--title ...]` — promote an inbox note
  into a deferred drawer task candidate.
- There is no drawer-to-task promotion. A drawer item becomes a task only by authoring it with
  `deskops add task --from-drawer <selector> ...` (see below); the drawer file is kept and cleaned
  up by hand.

## Creating artifacts (`deskops add <kind> ...`)

Kinds: `task, condition, operator, checklist, hook, edge, routine, pill, ritual, board, atom,
repository, inbox-note, faq-doc, step`. Any kind accepts `--from-yaml <file>` or an inline JSON
payload instead of individual flags.

- `deskops add task --root . --title "..." --goal "..." --scope "..." \
  --implementation-path "..." --done-when "..." --validation "pytest" [more --validation ...] \
  [--why "..."] [--depends-on task-a task-b] [--task-type design|implementation|test|reflection|closeout] \
  [--inherits-from task-x] [--atom atom-id ...] [--inherit-acceptance-context] \
  [--from-drawer <drawer-path|stem|fragment>]`
  Creates the task, its routine, and primitive checklists/conditions/operators/edges, and adds a
  board entry. `--from-drawer` records the source drawer file in the task's `from_drawer` field
  (not in `references`, which `edit task` replaces wholesale); it does not copy content or delete
  the drawer file.
- `deskops add pill --root . --what "..." --why "..." --when "..." --where "..." --how "..." \
  --how-not "..." [--title "..."] [--summary "..."] [--tags namespace:value ...]`
  All six of `--what/--why/--when/--where/--how/--how-not` are required.
- `deskops add atom --root . --five-wh-one-plus {what,why,how,how_not,when,where,for_whom} \
  --answer "..." [--title "..."] [--tags namespace:value ...] [--provenance <url-or-path>]`
  One atom answers exactly one 5W1H question.
- Other kinds (`routine`, `ritual`, `board`, `repository`, `inbox-note`, `faq-doc`, `step`,
  `condition`, `operator`, `checklist`, `hook`, `edge`) follow the same `--root`/`--from-yaml`
  pattern; run `deskops add <kind> --help` for kind-specific flags before use.

## Editing one field (`deskops edit <kind> <selector> <field> <value> --root .`)

Kinds: `task, pill, ritual, board, atom, repository, inbox-note, faq-doc, step`. Values are parsed
through SLDB's field-value parser and the document is re-rendered from its model — this is the
correct way to change a single field without hand-editing Markdown.

Example: `deskops edit pill pill-keep-layers-clean how-not "Do not bypass the guardrail." --root .`

## Binding context

- `deskops bind pill <task-selector> <pill-selector> --root .` — updates the task's modeled
  `pills` list through the artifact layer.

## Listing and showing

- `deskops list {tasks,routines,conditions,operators,checklists,hooks,edges,pills,rituals,boards,
  atoms,repositories,inbox-notes,faq-docs,steps} --root .`
- `deskops show {task,routine,condition,operator,checklist,hook,edge,pill,ritual,board,atom,
  repository,inbox-note,faq-doc,step} <selector> --root .`
- `deskops atoms list --root . [--format text|json]`
- `deskops atoms show <selector> --root .`
- `deskops atoms new --root .` — interactive/guided atom creation.
- `deskops atoms validate <selector> --root .` — validate an atom's materializations.
- `deskops atoms add-namespace` — add an extensible atom tag namespace to
  `desk/atoms/tag-namespaces.yaml`.

## Advancing work

- `deskops advance task <selector> --root .` — walk a task through execution, testing, and
  closeout gates when its checklist conditions pass. This is the only supported way to move a
  task's runtime status.
- `deskops next [<selector>] --root . [--diagram]` — show the next valid workflow action for a
  task without mutating it; `--diagram` renders the workflow state machine as Mermaid from its
  source spec (useful for understanding the gate structure itself).

## Closeout

- `deskops materialize --root .` — materialize workflow artifacts (regenerate human-facing docs
  from atoms/models).
- `deskops closeout commit --root . --task <task-id> --run-dir runs/subagents/<dir> \
  [-m "<subject>"] [--paths path1 path2 ...] [--run-id <id>] [--session <session.jsonl>]`
  Creates the tool-made closing commit linked to run evidence; stamps Task-Id/Run-Dir/Run-Id/
  Session-Sha256 trailers and records the commit hash back into `runs/subagents/index.jsonl`.
  Prefer this over a bare `git commit` whenever a run-dir exists for the task.
- `deskops closeout {commit,supersede,retire,resolved-by,verify}` — pick the verb by why the task closes
  (run `deskops closeout <verb> --help`; never conclude a task "can't be closed" without checking all five):
  - `supersede --task <id> --reason "..." --ref <commit|path>` — the task was replaced or its subject no
    longer exists (work never done). Skips the evidence gates; makes one closing commit with
    Closeout-Mode: superseded and removes the task from the Board.
  - `resolved-by --task <id> ...` — the work already entered history; names an ancestor commit and a test.
  - `retire` — a task resolved before the ritual lifecycle.
  - `verify --task <id>` — check declared evidence without committing.
  `deskops retire <path>` (top-level) is for other desk documents (inbox notes, pills, steps…), not tasks.

FILE:.claude/skills/deskops-workflow/references/vocabulary.md
# deskops + spec2viz vocabulary

Precise definitions for the nouns these tools use. Consult this when a command's *purpose*, not
just its flags, is unclear — for example, before deciding whether something belongs in a pill or
an atom, or whether a diagram spec or its rendered output is the thing to edit.

## Layering

- **sldb** owns structured-Markdown infrastructure in general: modeled document contracts,
  reversible templates, field-level query/update/append/clean/create/remove, section ownership,
  semantic + physical search, store integrity. It has no opinion on workflow or diagrams.
- **deskops** is the workflow-domain instance built on sldb: tasks, routines, pills, atoms,
  drawer, board, rituals, hooks. It owns *what work is happening and why*.
- **spec2viz** is the diagram-domain mirror of the same idea: a diagram's YAML spec plus its
  contract compiles to a rendered visual artifact, exactly as an sldb model plus a template
  compiles to a Markdown document. It owns *what things look like*.

Both exist to keep a human-facing surface (a Markdown doc, a rendered diagram) from drifting
silently away from its structured source. The fix for a wrong output is always upstream: the
model/field for docs, the YAML spec/renderer for diagrams — never the generated file itself.

## Tasks, routines, phases, board

- A **task** (`desk/tasks/task-*.md`) is one unit of routed work: title, goal, scope,
  implementation path, done-when rule, validation command(s), optional dependencies and bound
  atoms/pills.
- A **routine** is the directed graph of checklists, operators, conditions, and edges that gates a
  task's progress. `deskops advance task` walks the task through this graph; it is the only
  supported way to change a task's runtime status.
- A **phase** is *not* a standalone document — it is a horizontal dependency layer of the task
  graph inside the board: tasks whose prerequisites are already satisfied and whose planned
  changes do not operationally overlap, so they can run in parallel. Phases have execution
  meaning, not business meaning.
- The **board** (`desk/tasks/Board.md`) routes active work; it is the entry point for "what should
  happen next," ahead of inventing new scope.

## Drawer, inbox, promotion

- The **inbox** is coordination intake: external needs, unclear requests, suggestions
  (`deskops inbox`). It routes toward work; it is not itself work.
- The **drawer** (`desk/drawer/`) holds future, uncertain, or loosely shaped work — features,
  issues, questions — that is deliberately *not* active. It only becomes active execution when
  explicitly authored as a routed task: there is no drawer-to-task promotion, because the drawer
  is loose and a task is a compiled, fully authored bundle. Write the task with
  `deskops add task --from-drawer <selector> ...`, which records the drawer file in the task's
  `from_drawer` field.
  Treat anything still in inbox/drawer as not-yet-authorized to implement.

## Pills vs. atoms

- A **pill** is transient, task- or phase-bound context: not-yet-incorporated knowledge needed to
  execute a specific bugfix/feature/migration correctly, or a pointer to already-settled
  atoms/code/docs/specs. A pill can be reused across several tasks as long as it stays atomic and
  applicable, and is attached explicitly with `deskops bind pill`.
- An **atom** is the stable documentation core: one durable answer to exactly one 5W1H question
  (what/why/how/how_not/when/where/for_whom), tagged with namespaced semantic tags
  (`system:x`, `topic:y`). Every durable doc, spec rationale, README section, or diagram
  explanation should either be an atom or a human-facing *materialization* of selected atoms.
- The lifecycle rule: once a pill's knowledge stabilizes and should outlive its task, it must be
  distilled into an atom (`deskops add atom`) so future specs/code/docs can comply with the
  durable ruling instead of depending on an old, task-scoped pill. A pill that never stabilizes
  and never gets used again should be deleted, not left indefinitely.

## Specs, diagrams, catalogs

- A **diagram spec** is a semantic YAML file (sequence, state, component, activity, deployment,
  matrix, or ast) validated against Pydantic models, then compiled to a renderer-agnostic IR
  before rendering. It is the source of truth.
- A **rendered diagram** (`.mmd`, `.puml`, `.svg`, Vega JSON, D2, `antonia-html`) is a projection
  of that spec through one renderer. If a rendered diagram is wrong, the fix is the spec (if the
  structure is wrong) or the renderer (if the spec is right but the output is malformed) — never
  a hand-patch of the rendered file, since the next render would silently discard the patch.
- A **catalog** aggregates many diagram specs (via a legacy `vistas.yml` registry or a
  hierarchical `diagram-store` config that can nest other stores) into one filterable HTML bundle,
  optionally cross-linked to atoms via `--atoms-dir`.
- Diagrams double as a **design surface**: their sections and labeled edges reveal candidate
  atoms, document references, routines, hooks, tests, and CLI nouns — read them for that signal
  rather than only for final output.

## Closeout discipline

A code change is not done when it merely works. Closeout means: validation command passed, bound
pills/guardrails satisfied, stale task/context docs updated or removed, the task removed from
`Board.md` once complete, and one coherent commit made (`deskops closeout commit` when a run-dir
exists, otherwise a descriptive plain commit). Skipping straight from "tests pass" to "next task"
without this reconciliation is how boards and atoms drift from reality.

FILE:tests/test_message_cli.py
"""Canonical `deskops message` transport surface.

`deskops message {send|list|read|ack}` is the cross-desk coordination CLI.
`deskops inbox` remains as a deprecated alias and keeps its legacy flag
grammar; both route to `deskops.cli.commands.message.MessageCLI`.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TESTS = Path(__file__).resolve().parent
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))

from deskops.cli.main import main
from test_cli import _setup_inbox_identity_env


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv], cwd=root, capture_output=True, text=True
    )


def _sldb_stores_check(store_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_path)],
        capture_output=True,
        text=True,
    )


def _init_repos(tmp_path: Path) -> tuple[Path, Path]:
    repos = []
    for name in ("repo-a", "repo-b"):
        repo = tmp_path / name
        repo.mkdir()
        result = _cli(repo, "init", str(repo))
        assert result.returncode == 0, result.stderr or result.stdout
        repos.append(repo)
    return repos[0], repos[1]


def _deliver(repo_a: Path, repo_b: Path, title: str) -> tuple[Path, dict]:
    result = _cli(
        repo_a,
        "message",
        "send",
        "A note for repo B.",
        "--title",
        title,
        "--kind",
        "suggestion",
        "--root",
        str(repo_b),
        "--format",
        "json",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    notes = list((repo_b / "desk" / "inbox").glob("*.md"))
    assert len(notes) == 1
    return notes[0], json.loads(result.stdout)


def test_message_help_documents_transport_verbs(capsys) -> None:
    assert main(["message", "--help"]) == 0
    output = " ".join(capsys.readouterr().out.split())
    assert "{send,list,read,ack}" in output
    assert "deskops message send" in output


def test_inbox_alias_is_announced_as_deprecated(capsys) -> None:
    assert main(["inbox", "--help"]) == 0
    output = " ".join(capsys.readouterr().out.split())
    assert "Deprecated: use `deskops message send|list|read|ack`" in output


def test_inbox_alias_warns_and_matches_message_list(tmp_path: Path, capsys) -> None:
    alias_result = main(["inbox", "--list", "--root", str(tmp_path)])
    alias_capture = capsys.readouterr()
    canonical_result = main(["message", "list", "--root", str(tmp_path)])
    canonical_capture = capsys.readouterr()

    assert alias_result == canonical_result == 0
    assert alias_capture.out == canonical_capture.out
    assert alias_capture.err == "Deprecated: use `deskops message`\n"
    assert canonical_capture.err == ""


def test_message_send_list_read_ack_roundtrip(tmp_path: Path, monkeypatch, capsys) -> None:
    sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(sender_repo)

    assert main(
        [
            "message",
            "send",
            "Please acknowledge this message.",
            "--title",
            "Transport verbs",
            "--kind",
            "suggestion",
            "--to",
            "target-repo",
            "--store",
            str(store_path),
            "--format",
            "json",
        ]
    ) == 0
    delivered = json.loads(capsys.readouterr().out)
    assert delivered["sender_project"] == "sender-repo"
    assert delivered["target_project"] == "target-repo"

    note = next((target_repo / "desk" / "inbox").glob("*.md"))
    monkeypatch.chdir(target_repo)

    assert main(
        ["message", "list", "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    listed = json.loads(capsys.readouterr().out)
    assert [item["id"] for item in listed["notes"]] == [note.stem]

    assert main(
        ["message", "read", note.stem, "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    read = json.loads(capsys.readouterr().out)
    assert read["status"] == "open"
    assert "Please acknowledge this message." in read["body"]

    assert main(
        ["message", "ack", note.stem, "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    acked = json.loads(capsys.readouterr().out)
    assert acked["status"] == "closed"
    assert acked["acknowledged_by"] == "target-repo"


def test_message_list_reports_empty_inbox(tmp_path: Path, monkeypatch, capsys) -> None:
    _sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(target_repo)

    assert main(["message", "list", "--root", str(target_repo), "--store", str(target_repo / ".sldb")]) == 0
    assert "No messages." in capsys.readouterr().out


def test_message_delivery_tracks_note_in_target_repo_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    repo_a, repo_b = _init_repos(tmp_path)
    note, payload = _deliver(repo_a, repo_b, "Tracked in the target store")

    assert payload["target_project"] == "repo-b"
    assert payload["verified"] is True
    assert doc_status(repo_a / ".sldb", note.stem).status == "missing"
    tracked = doc_status(repo_b / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout


def test_message_ack_refreshes_note_tracked_in_target_repo_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Acknowledged in the target store")

    result = _cli(
        repo_b,
        "message",
        "ack",
        note.stem,
        "--root",
        str(repo_b),
        "--format",
        "json",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    acked = json.loads(result.stdout)
    assert acked["status"] == "closed"
    assert acked["acknowledged_by"] == "repo-b"
    assert doc_status(repo_b / ".sldb", note.stem).status == "ok"
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout
    assert doc_status(repo_a / ".sldb", note.stem).status == "missing"


def test_message_ack_restores_note_when_tracking_fails(tmp_path: Path, monkeypatch) -> None:
    from sldb.api import doc_status
    from sldb.core.exceptions import SLDBStoreError

    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Restored when tracking fails")
    original = note.read_bytes()

    def failing_save(*_args, **_kwargs):
        raise SLDBStoreError("simulated refresh failure")

    # The ack is `Transaction.update` of the tracked note: the store's save step fails.
    monkeypatch.setattr("sldb.api.documents.transaction_ops.save_document_payload", failing_save)
    monkeypatch.chdir(repo_b)

    assert main(["message", "ack", note.stem, "--root", str(repo_b)]) == 1
    assert note.read_bytes() == original
    assert doc_status(repo_b / ".sldb", note.stem).status == "ok"
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout


def test_message_list_uses_store_when_no_root_is_given(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    """`--store` alone anchors the desk, so the old root default cannot mask it."""
    repo = tmp_path / "store-repo"
    inbox = repo / "desk" / "inbox"
    inbox.mkdir(parents=True)
    note = inbox / "20260101-000000-suggestion-stored.md"
    note.write_text(
        "---\nkind: suggestion\nsender_project: sender\ntarget_project: store-repo\n"
        "created_at: 2026-01-01T00:00:00\nstatus: open\ntitle: Stored note\n---\n\n"
        "# Stored note\n\nBody.\n",
        encoding="utf-8",
    )
    store = repo / ".sldb"
    (store / "core").mkdir(parents=True)
    (store / "core" / "store_index.yaml").write_text("{}\n", encoding="utf-8")

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    assert main(["message", "list", "--store", str(store), "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert [item["id"] for item in payload["notes"]] == [note.stem]


def test_message_ack_rejects_a_fragment_that_matches_two_notes(tmp_path: Path) -> None:
    """2026-10-19: `message ack 20261019-120241` acked 20261019-120253, whose title quoted it."""
    repo_a, repo_b = _init_repos(tmp_path)
    first, _ = _deliver(repo_a, repo_b, "sldb ci en verde")
    prefix = first.stem.split("-suggestion-")[0]
    result = _cli(
        repo_a, "message", "send", "Corrected hashes.", "--title", f"correccion de mi nota {prefix}",
        "--kind", "suggestion", "--root", str(repo_b),
    )
    assert result.returncode == 0, result.stderr or result.stdout
    (second,) = [path for path in (repo_b / "desk" / "inbox").glob("*.md") if path != first]
    assert prefix in second.stem

    ambiguous = _cli(repo_b, "message", "ack", prefix, "--root", str(repo_b))

    assert ambiguous.returncode == 2, ambiguous.stdout + ambiguous.stderr
    output = ambiguous.stdout + ambiguous.stderr
    assert first.stem in output and second.stem in output
    for note in (first, second):
        assert "status: open" in note.read_text(encoding="utf-8")

    exact = _cli(repo_b, "message", "ack", first.stem, "--root", str(repo_b))

    assert exact.returncode == 0, exact.stdout + exact.stderr
    assert "status: closed" in first.read_text(encoding="utf-8")
    assert "status: open" in second.read_text(encoding="utf-8")

FILE:tests/test_message_delivery.py
"""Message delivery must not depend on the target desk registering the sender.

These are the three failures reported on 2026-10-18:

* a target without ``project_identity`` refused the note,
* a sender was resolved against the target's registry (so a repo that only
  registered itself made every foreign sender unresolvable),
* ``ack`` stopped finding the repo itself once its registry registered some
  other repo.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.models import InboxNoteDoc
from deskops.models import RepositoryDoc
from sldb.runtime.validation import render_model_markdown


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv], cwd=root, capture_output=True, text=True
    )


def _init_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    result = _cli(path, "init", str(path))
    assert result.returncode == 0, result.stderr or result.stdout
    return path


def _register(repo: Path, repo_id: str, repo_path: str) -> None:
    registry_dir = repo / "desk" / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": repo_id,
        "name": repo_id,
        "path": repo_path,
        "status": "active",
        "description": f"Repository for {repo_id}.",
        "tags": [],
    }
    (registry_dir / f"repo-{repo_id}.md").write_text(
        render_model_markdown(RepositoryDoc, payload) + "\n", encoding="utf-8"
    )


def _store_snapshot(repo: Path) -> dict[str, bytes]:
    store = repo / ".sldb"
    return {
        path.relative_to(store).as_posix(): path.read_bytes()
        for path in sorted(store.rglob("*"))
        if path.is_file()
    }


def _write_note(repo: Path, stem: str, *, target_project: str) -> Path:
    inbox = repo / "desk" / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": "suggestion",
        "sender_project": "sender-repo",
        "target_project": target_project,
        "created_at": "2026-01-01T00:00:00",
        "status": "open",
        "title": "Ack me",
        "body": "Please acknowledge this note.",
    }
    note = inbox / f"{stem}.md"
    note.write_text(render_model_markdown(InboxNoteDoc, payload) + "\n", encoding="utf-8")
    return note


def test_send_to_target_without_project_identity_uses_directory_name(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender-repo")
    target = _init_repo(tmp_path / "TraderBot")
    (target / "desk" / "config.json").write_text("{}\n", encoding="utf-8")

    result = _cli(
        sender,
        "message",
        "send",
        "A note for an unconfigured desk.",
        "--title",
        "No identity",
        "--root",
        str(target),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["sender_project"] == "sender-repo"
    assert payload["target_project"] == "TraderBot"
    assert "no project_identity" in result.stderr
    assert len(list((target / "desk" / "inbox").glob("*.md"))) == 1


def test_send_resolves_sender_from_sender_repo_not_target_registry(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender-repo")
    target = _init_repo(tmp_path / "target-repo")
    # The target's local registry knows only itself, exactly like the reported case.
    _register(target, "target-repo", str(target))

    without_from = _cli(
        sender,
        "message",
        "send",
        "Sender comes from the sending repo.",
        "--title",
        "No sender override",
        "--root",
        str(target),
        "--format",
        "json",
    )
    with_from = _cli(
        sender,
        "message",
        "send",
        "Sender comes from the sending repo.",
        "--title",
        "Explicit sender",
        "--from",
        "sender-repo",
        "--root",
        str(target),
        "--format",
        "json",
    )

    assert without_from.returncode == 0, without_from.stderr or without_from.stdout
    assert with_from.returncode == 0, with_from.stderr or with_from.stdout
    assert json.loads(without_from.stdout)["sender_project"] == "sender-repo"
    assert json.loads(with_from.stdout)["sender_project"] == "sender-repo"
    assert json.loads(without_from.stdout)["target_project"] == "target-repo"


def test_send_with_root_tracks_only_in_target_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    sender = _init_repo(tmp_path / "repo-a")
    target = _init_repo(tmp_path / "repo-b")
    before = _store_snapshot(sender)

    result = _cli(
        sender,
        "message",
        "send",
        "A note addressed through --root.",
        "--title",
        "To a root",
        "--root",
        str(target),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["verified"] is True
    assert _store_snapshot(sender) == before
    note = next((target / "desk" / "inbox").glob("*.md"))
    tracked = doc_status(target / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    assert doc_status(sender / ".sldb", note.stem).status == "missing"


def test_send_to_registered_repo_tracks_only_in_target_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    sender = _init_repo(tmp_path / "repo-a")
    target = _init_repo(tmp_path / "repo-b")
    _register(sender, "repo-b", str(target))
    before = _store_snapshot(sender)

    result = _cli(
        sender,
        "message",
        "send",
        "A note addressed through --to.",
        "--title",
        "To a registered repo",
        "--to",
        "repo-b",
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["verified"] is True
    assert _store_snapshot(sender) == before
    note = next((target / "desk" / "inbox").glob("*.md"))
    tracked = doc_status(target / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    assert doc_status(sender / ".sldb", note.stem).status == "missing"


def test_legacy_inbox_repo_tracks_only_in_target_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    sender = _init_repo(tmp_path / "repo-a")
    target = _init_repo(tmp_path / "repo-b")
    _register(sender, "repo-b", str(target))
    before = _store_snapshot(sender)

    result = _cli(
        sender,
        "inbox",
        "A note addressed through the deprecated alias.",
        "--title",
        "Legacy repo alias",
        "--repo",
        "repo-b",
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["verified"] is True
    assert _store_snapshot(sender) == before
    note = next((target / "desk" / "inbox").glob("*.md"))
    tracked = doc_status(target / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    assert doc_status(sender / ".sldb", note.stem).status == "missing"


def test_ack_falls_back_to_config_when_registry_lacks_itself(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "graph-repo")
    # Registering somebody else used to hide the repo's own identity from ack.
    _register(repo, "graph_ui", str(tmp_path / "elsewhere"))
    note = _write_note(repo, "20260101-000000-suggestion-ackme", target_project="graph-repo")

    result = _cli(
        repo,
        "message",
        "ack",
        note.stem,
        "--root",
        str(repo),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["status"] == "closed"
    assert payload["acknowledged_by"] == "graph-repo"
    assert payload["target_project"] == "graph-repo"

FILE:instruccion
Cold-bundle de la tarea task-retirar-el-alias-deskops-inbox-docs-y-skills-pasan-a-deskops-message-y-se-borra-el-alias: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rnw 'deskops inbox' docs .claude .opencode deskops/data README.md
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_grammar.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

