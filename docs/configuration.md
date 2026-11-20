# deskops Configuration Map

In deskops, *configuration* is not a settings file. It is a set of **documents and models** that
deskops ships in its package and copies into every desk, and that `sldb` evaluates. To change how
a desk behaves you change one of those documents, you do not change deskops code.

This page says, for each piece of configuration, where it lives in the package, where it lives in
the desk, and what `sldb` runs with it. Two recipes at the end declare a new task type and a new
view; `tests/test_docs_recipes.py` runs both in a temporary desk, so they cannot drift from the CLI.
For the rules themselves read `docs/workflow-policy-reference.md`; for the commands, the
operator manual (`docs/operator-manual.md`).

## The rule of thumb

| You want to... | Change | Then run |
|---|---|---|
| add a task type | a `TaskDoc` subclass in `desk/models/*.py` and its `RuleDoc` | `deskops desk update --apply` |
| change when a task may start or close | the `RuleDoc` in `desk/lifecycle/rule-*.md` | `deskops desk update --apply` |
| see data a new way | a `ViewDoc` in the desk | `sldb views run <name> --store .sldb` |
| change a package default for every desk | the file under `deskops/data/` | `deskops desk update --apply` in each desk |

A *managed* file (the lifecycle graph and the factory rules) is deskops' document: `desk update
--apply` rewrites a desk's copy that differs from the package's. A desk file with a name of its own
(your rule, your model) is never rewritten.

## The map

| Piece | In the package | In the desk | What sldb runs |
|---|---|---|---|
| Models and task types | `deskops/models/*.py` (`task_types.py` has the seven factory types) | `desk/models/*.py` for your own types | `sldb.api.add_model` registers each class in `.sldb`; `model <= TaskCodeDoc` selects a type and its subtypes |
| ReviewDoc and receipts | `deskops/models/review.py` | `desk/reviews/` (one document per receipt) | sldb pins `subject` to the reviewed document's contract hash and derives `anchor_state` (`intact`, `changed`, `lost`) when it composes the edge index |
| RelationDoc and `attributes` | `deskops/data/lifecycle/*.md` | `desk/lifecycle/{type,execution,testing,closeout}-*.md` (managed) | `edges_holding` lists the edges whose `condition` holds; `apply_effects` writes the edge's `attributes.sets` on the task; `attributes.terminal` closes it |
| RuleDoc of activation | `deskops/data/rules/rule-activation-<type>.md` | `desk/lifecycle/rule-activation-<type>.md` | an `on_transition` rule over `ritual-execution`; `deskops advance` evaluates it on the task |
| RuleDoc of closeout | `deskops/data/rules/rule-closeout-<type>.md` and `closeout-evidence.yaml` | `desk/lifecycle/rule-closeout-<type>.md` | an `on_transition` rule over `ritual-closeout`; `deskops closeout commit` evaluates it over the receipts `closeout verify` wrote |
| Consistency | `deskops/models/task_lifecycle.py` | nothing: it is part of the `TaskDoc` model | a validator sldb runs on every write, so a task with an impossible `status`/`current_node`/`history` is refused |
| ViewDoc | `deskops/data/views/{board,task}.md` | your own, e.g. `desk/views/<name>.md` | `sldb.api.run_view` evaluates the sections; `sldb views run`, `GET /views/<name>` |
| Graph configuration | `deskops/graph/` (extraction of declared edges, checks, export) | the `atoms:` frontmatter of docs and the `references` of tasks | sldb composes them into the edge index that `deskops graph` and `sldb edges` read |
| Seeds and templates | `deskops/data/desk_declaration.yaml`, `deskops/data/templates/` | `desk/config.json`, rituals, pills, the Board | `sldb.api.scaffold_store` creates the desk's folders and seeds; `if_missing` seeds keep a desk's own file |

Notes on each row:

- **Models.** A task type is a model, not a string in a field. `TaskDoc` keeps `task_type: str` so
  old documents still read; each subclass fixes it with a `Literal` default. A subtype inherits
  the gates of its ancestors and can only add to them.
- **Receipts.** `deskops review` writes a receipt with `verdict: pending`; `deskops review dispose`
  writes the verdict. The activation rules read them through the `^subject` edge.
- **RelationDoc.** One relation leaves each ritual. Its `attributes` carry `sets` (fields written on
  the task when the edge is taken) and `terminal` (the task closes). They are data: changing a
  transition's effect is editing the document.
- **Activation and closeout rules.** Both are `RuleDoc`s with `subject: model <= <TypeDoc>`, so a
  rule written for a type also applies to every subtype. The evidence kinds each type closes with
  are data too (`closeout-evidence.yaml`).
- **Consistency.** Only `deskops advance` and `deskops closeout` change a task's lifecycle fields.
- **ViewDoc.** The `board` and `task` views ship in the package store and reach a desk through its
  link. A view of your own is a `ViewDoc` tracked in the desk's store.
- **Seeds.** `desk_declaration.yaml` is an sldb `StoreDeclaration` (`folders`, `seeds`, `include`).
  `include` says which desk documents `desk update --apply` tracks, and under which model.

## Recipe: declare a new task type

Goal: a type `task.runbook` that cannot start until it names at least one file in `files`. The
rule is deliberately small; any condition over the task's fields, its receipts or its dependencies
works the same way (see the factory rules in `desk/lifecycle/`).

### 1. The model

A `TaskDoc` subclass in `desk/models/`. It fixes `task_type` with a `Literal` default. Extend
`TaskDoc` directly for a new type; extend a factory type (for instance `TaskCodeDoc`) to inherit
its gates and add yours.

```python recipe:desk/models/runbook_types.py
from typing import Literal

from pydantic import Field

from deskops.models import TaskDoc


class TaskRunbookDoc(TaskDoc):
    """task.runbook: a runbook change; it starts only once it names the file it edits."""

    task_type: Literal["task.runbook"] = Field(default="task.runbook", description="Runbook task.")
```

### 2. The activation rule

A `RuleDoc` named `rule-activation-<type>.md` in `desk/lifecycle/`. `subject` names the family,
`where` restricts it to the node the rule guards, `moment: on_transition` makes `deskops advance`
evaluate it, and `severity: error` makes a failing condition hold the edge back.

```markdown recipe:desk/lifecycle/rule-activation-task-runbook.md
---
subject: model <= TaskRunbookDoc
where: current_node = "ritual-execution"
condition: 'files != []'
severity: error
moment: on_transition
message: Una tarea task.runbook se activa cuando declara al menos un archivo en files.
---

# Activación de task.runbook
```

### 3. Register both and create a task

`desk update --apply` imports `desk/models/*.py`, registers each `TaskDoc` subclass with sldb
(`pythonpath` is `desk/`) and tracks the rule, because `rule-activation-*.md` matches an `include`
glob of the desk declaration.

```bash recipe
deskops desk update --apply --root .
deskops add task --title "Runbook uno" --goal g --scope s --task-type task.runbook --root .
```

### 4. See the task blocked

`sldb rules explain` evaluates one rule on one document: exit 0 when true, 1 when false. `deskops
advance` asks the same question when it looks for the edge to take.

```bash recipe-fails
sldb rules explain rule-activation-task-runbook TaskRunbookDoc:task-runbook-uno --store .sldb --pythonpath desk
```

```bash recipe-fails
deskops advance task task-runbook-uno --root .
```

The second command exits 1 and prints `Gate ritual-execution is blocked by its rules` followed by
the rule's message and the clause it saw fail (`files != []`, seen `[]`).

### 5. Satisfy the rule and activate

`deskops edit task` imports the task's model, so it needs `desk/` on `PYTHONPATH` for a desk-local
type. Once the rule holds, `advance` takes `task_activates`.

```bash recipe
PYTHONPATH=desk deskops edit task task-runbook-uno files '["docs/runbook.md"]' --root .
sldb rules explain rule-activation-task-runbook TaskRunbookDoc:task-runbook-uno --store .sldb --pythonpath desk
deskops advance task task-runbook-uno --root .
```

The explain now prints `true` and `advance` prints `Advanced to ritual-testing via task_activates.`

To close the type the same way, add a `rule-closeout-task-runbook.md` (`where: current_node =
"ritual-closeout"`) over the receipts `deskops closeout verify` writes. A desk type reads the
evidence kinds of its nearest factory ancestor; a type that extends `TaskDoc` directly declares its
own rule.

## Recipe: declare a new view

A view is a `ViewDoc`: named sections, each one selecting documents by model and path and listing
the fields to return. The format is the one of `deskops/data/views/board.md`. This one lists the
runbook tasks grouped by node.

### 1. The document

```markdown recipe:desk/views/runbooks.md
---
id: runbooks
name: runbooks
nodes: []
relations: []
direction: both
notation: ''
layout: {}
params: []
sections:
- key: runbooks
  select:
    model: TaskRunbookDoc
    path_glob: desk/tasks/**/*.md
  fields:
  - id
  - title
  - current_node
  - files
  group_by: current_node
  group_order:
  - ritual-execution
  - ritual-testing
  - ritual-closeout
---

# Runbooks del desk
```

### 2. Track it and run it

A desk's store does not register `ViewDoc` (the package's own views come through the store link), so
the first view of a desk registers the model; after that, tracking is one command per view.
`deskops desk update --apply` does not track views: it has no `include` for them.

```bash recipe
sldb models add sldb.models.notation.view_doc:ViewDoc --store .sldb
sldb docs track desk/views/runbooks.md --model ViewDoc --name runbooks --store .sldb
sldb views run runbooks --store .sldb
```

The result groups the task by node (`ritual-testing` holds `TaskRunbookDoc:task-runbook-uno` once
the first recipe ran). `sldb views list --store .sldb` lists the views by name, and `sldb serve`
answers `GET /views/runbooks`. `deskops view` has fixed subcommands (`board`, `task`, `drawer`,
`inbox`, `agents`): a view of your own is read with `sldb views run`.

## Where is the rule for X?

| X | File in the desk |
|---|---|
| when a task of type T may start | `desk/lifecycle/rule-activation-<T>.md` |
| what a task of type T needs to close | `desk/lifecycle/rule-closeout-<T>.md` (kinds: `deskops/data/rules/closeout-evidence.yaml`) |
| what each transition does to the task | `desk/lifecycle/<node>-<verb>.md`, `attributes` |
| which task types exist | `deskops/models/task_types.py` and `desk/models/*.py` |
| what a receipt is | `deskops/models/review.py`; the receipts are in `desk/reviews/` |
| what the desk starts with | `deskops/data/desk_declaration.yaml` |

To read why a rule holds or not, `sldb rules explain <rule> <Model>:<id> --store .sldb --pythonpath
desk`; to read why a task does not advance, `deskops next <task> --root .`.
