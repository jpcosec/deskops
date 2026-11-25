FILE:desk/tasks/task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea.md
---
sldb:
  by: agent
  at: '2026-11-21T06:40:37Z'
  authority: generated
  via: save_document_payload
id: task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-003533-suggestion-namespace-de-tags-host-para-marcar-en-qu-m-quina-corre-cada-tarea.md
- desk/inbox/20261116-003602-suggestion-namespace-de-tags-host-para-separar-tareas-de-ui-local-y-backend-robocop2.md
- desk/inbox/20261116-004642-suggestion-namespace-de-tags-host-para-rutear-tareas-por-m-quina-host-local-host-robocop2.md
depends_on: []
pills: []
files:
- deskops/atom_tags.py
- docs/workflow-policy-reference.md
- .sldb/store.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops declara el namespace de tags host para marcar en que maquina corre cada tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Dos notas del 2026-11-16 (IR y deskops), del triaje de drawers e inbox: JP pide que cada TaskDoc diga en que maquina corre. Lo que tiene UI o verificacion en navegador va a la maquina local; suites, build --check, benchmarks, migraciones, scion y revisiones van a robocop2. La via es TaskDoc.tags, pero ningun store del ecosistema declara un namespace para la maquina (deskops no declara tag_namespaces en .sldb/store.yaml; sldb e IR solo tienen domain, layer, system y topic).

## Goal

_Describe the concrete result this task must produce._

La declaracion de tag namespaces que deskops sincroniza en cada desk (deskops/atom_tags.py, alrededor de 159-204, que arma TagNamespace(name=..., anchored_by=...)) agrega host como TagNamespace(name='host', hierarchical=False), usando el modelo sldb.api.stores.tag_namespace.TagNamespace tal cual (campos name, hierarchical, folder_axis, anchored_by). tag_models es global en sldb, asi que TaskDoc entra en tag_models y, para que las tareas existentes no den alertas, se declaran tambien workspace, artifact y source (hierarchical=False). meaning, use_when y do_not_use_when de host van en el registro de atom tags que escribe deskops (DEFAULT_ATOM_TAG_NAMESPACES, mismo formato que las demas entradas): meaning 'maquina donde se ejecuta y valida la tarea'; use_when 'tareas con UI o verificacion en navegador -> host:local; backend, suites, migraciones, scion y revisiones -> host:robocop2'; do_not_use_when 'atoms y pills'. Los valores no se restringen (sldb no tiene enumeraciones). docs/workflow-policy-reference.md, en la seccion '### Tasks', suma una linea: 'TaskDoc.tags may carry host:local or host:robocop2: the machine that runs and validates the task (UI and browser checks run locally; backend on robocop2).' Tras deskops desk update --apply en el desk de deskops, una tarea con host:robocop2 no produce alertas de tag en sldb stores check. Criterio de detencion: si con workspace, artifact y source declarados sldb stores check sigue dando alertas de tag en tareas existentes del desk de deskops, se manda deskops message send --to sldb pidiendo namespaces por modelo y la tarea cierra solo con la documentacion.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/atom_tags.py, la semilla de desk que la usa, docs/workflow-policy-reference.md (una linea que explique el tag host) y un test nuevo o ampliado en tests/ (buscar el test actual de tag namespaces con `grep -rln tag_namespaces tests/`). No entra: taggear las tareas existentes (lo hace cada coordinador despues), restringir valores si sldb no soporta enumeraciones (se documentan). Precisiones del preflight 1: en sldb, tag_namespaces es una lista de {name, hierarchical, folder_axis} y tag_models es una lista GLOBAL de modelos (hoy AtomDoc y ProtoAtomDoc en sldb/.sldb/store.yaml): agregar TaskDoc hace que se validen TODOS sus tags, y las tareas ya usan workspace:, artifact: y source:. Por eso la entrada es: host con hierarchical: false y folder_axis: false, y si TaskDoc entra en tag_models se declaran tambien workspace, artifact y source. Si sldb no admite eso sin alertas en tareas existentes, la tarea se detiene, manda deskops message send --to sldb pidiendo namespaces por modelo, y cierra solo con la parte de documentacion. Textos: meaning 'maquina donde se ejecuta y valida la tarea'; use_when 'tareas con UI o verificacion en navegador -> host:local; backend, suites, migraciones, scion y revisiones -> host:robocop2'; do_not_use_when 'atoms y pills'. Los valores no se restringen (sldb no tiene enumeraciones): se documentan. La tarea de prueba es una creada en el desk sandbox del test. docs/workflow-policy-reference.md es el de este repo (deskops). El test va en tests/test_atom_tags.py (ampliado).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer deskops/atom_tags.py completo y sldb docs/architecture/tags.md. 2) Agregar host a la semilla con tag_models que incluya TaskDoc. 3) Test: desk sandbox, desk update --apply, TaskDoc con host:robocop2, `sldb stores check` sin alerta de tag. 4) Aplicar en el desk de deskops y commitear .sldb/store.yaml.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_tags.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_domain_tree.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops desk update --apply --root . && PYTHONPATH=../sldb/src:. ../.venv/bin/python -m sldb stores check --store .sldb (sin alertas de tag por host)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El store de deskops declara host; una tarea con host:robocop2 no da alertas; el test pasa; la doc lo explica.

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

FILE:deskops/atom_tags.py
from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

import yaml


from deskops.models.atom import ATOM_TAG_PATTERN

NAMESPACE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
# The tag form is the model's (AtomDoc.tags); this is the same pattern with the namespace named.
TAG_PATTERN = re.compile(ATOM_TAG_PATTERN.replace("^[a-z][a-z0-9_]*:", "^(?P<namespace>[a-z][a-z0-9_]*):"))

DEFAULT_ATOM_TAG_NAMESPACES: dict[str, dict[str, Any]] = {
    "system": {
        "meaning": "System, project, or tool the atom belongs to.",
        "use_when": "The atom is about a specific system.",
        "do_not_use_when": "The tag is only a general topic.",
        "examples": ["system:deskops", "system:sldb"],
    },
    "topic": {
        "meaning": "Subject area discussed by the atom.",
        "use_when": "The atom is about a conceptual topic.",
        "do_not_use_when": "The atom describes a reusable implementation shape.",
        "examples": ["topic:atoms", "topic:composition"],
    },
    "layer": {
        "meaning": "Architectural layer where the atom applies.",
        "use_when": "The atom is scoped to a layer of the system.",
        "do_not_use_when": "The tag names only a broad topic or system.",
        "examples": ["layer:document-model", "layer:runtime", "layer:cli"],
    },
    "domain": {
        "meaning": "Problem domain or durable area of concern.",
        "use_when": "The atom belongs to a reusable problem domain.",
        "do_not_use_when": "A more specific system, topic, layer, or pattern tag applies.",
        "examples": ["domain:knowledge-management", "domain:task-execution"],
    },
}


def default_registry_path(root: Path) -> Path:
    return root / "desk" / "atoms" / "tag-namespaces.yaml"


def ensure_default_namespaces(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_registry(path, {"namespaces": DEFAULT_ATOM_TAG_NAMESPACES})


def load_namespaces(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    namespaces = loaded.get("namespaces") or {}
    if not isinstance(namespaces, dict):
        raise ValueError(f"Invalid atom tag namespace registry at {path}")
    return dict(namespaces)


def add_namespace(
    path: Path,
    namespace: str,
    *,
    meaning: str,
    use_when: str,
    do_not_use_when: str,
    examples: list[str],
) -> None:
    namespace = namespace.strip()
    if not NAMESPACE_PATTERN.fullmatch(namespace):
        raise ValueError("Namespace must match ^[a-z][a-z0-9_]*$.")

    path.parent.mkdir(parents=True, exist_ok=True)
    registry = {"namespaces": load_namespaces(path)}
    if namespace in registry["namespaces"]:
        raise ValueError(f"Atom tag namespace '{namespace}' already exists.")

    for example in examples:
        match = TAG_PATTERN.fullmatch(example)
        if match is None or match.group("namespace") != namespace:
            raise ValueError(f"Example '{example}' must use namespace '{namespace}'.")

    registry["namespaces"][namespace] = {
        "meaning": meaning,
        "use_when": use_when,
        "do_not_use_when": do_not_use_when,
        "examples": examples,
    }
    _write_registry(path, registry)


def axis_values(tags: list[str], axis: str) -> list[str]:
    """Return the sorted unique values carried by tags of the axis namespace."""
    values: set[str] = set()
    for tag in tags:
        match = TAG_PATTERN.fullmatch(str(tag))
        if match is not None and match.group("namespace") == axis:
            values.add(str(tag).split(":", 1)[1])
    return sorted(values)


def folder_axis_value(tags: list[str], axis: str) -> str | None:
    """Return the single folder-axis value for an atom, or None when absent.

    Raises ValueError when the atom carries more than one value of the axis
    namespace, because the physical folder placement must be deterministic.
    """
    values = axis_values(tags, axis)
    if len(values) > 1:
        raise ValueError(
            f"Atom carries multiple '{axis}' axis values: {', '.join(values)}. "
            f"The folder axis requires exactly one '{axis}:<value>' tag; "
            "remove the extra axis tags or split the atom."
        )
    return values[0] if values else None


def axis_folder(value: str) -> Path:
    """The folder an axis value places an atom in: sldb's ``tag_folder`` (``a.b`` -> ``a/b``).

    An empty segment (``a..b``, ``a.``) is a ``ValueError``; the atom model never lets one in
    (``check_atom_tags``).
    """
    from sldb.api import tag_folder

    return Path(tag_folder(value))


# --- The tag declaration of the store (CC35d resto, e1) ------------------------------------
#
# ``desk/atoms/tag-namespaces.yaml`` is the desk's registry; the store declares the same
# namespaces in ``.sldb/store.yaml`` (``tag_namespaces``), and sldb checks them as the rule
# family ``builtin:tag_namespace:<name>`` (docs/architecture/tags.md in sldb). The file wins:
# ``sync_tag_declaration`` rewrites the declaration only when it differs.

#: The models whose tags the family checks: atoms and protoatoms (the protoatom exists to hang
#: from a domain). Tasks, pills and the rest carry namespaces the registry does not declare.
TAG_MODELS = ["AtomDoc", "ProtoAtomDoc"]
#: A ``domain:a.b`` tag is anchored by the CrossroadDoc whose ``path`` is ``a.b``.
DOMAIN_ANCHOR = {"model": "CrossroadDoc", "field": "path", "value": "bare"}
_SEEN = "(seen: "


def tag_store(root: Path) -> Path | None:
    """The desk's store, or None when the repository has none (then nothing is checked)."""
    from sldb.store.layout import store_exists

    store = Path(root) / ".sldb"
    return store if store_exists(store) else None


def wanted_tag_declaration(root: Path) -> tuple[list[Any], list[str]]:
    """``(tag_namespaces, tag_models)`` the store must declare for the registry file.

    ``folder_axis`` is not declared: the atom folder axis is ``desk/config.json``'s
    ``atom_folder_axis``, which ``config.local.json`` may override per machine, and the
    committed ``store.yaml`` must not depend on the machine.
    """
    from sldb.api import TagNamespace

    from deskops.models.atom import DOMAIN_NAMESPACE

    root = Path(root)
    namespaces = [
        TagNamespace(name=name, anchored_by=dict(DOMAIN_ANCHOR) if name == DOMAIN_NAMESPACE else None)
        for name in sorted(load_namespaces(default_registry_path(root)))
    ]
    return namespaces, list(TAG_MODELS) if namespaces else []


def sync_tag_declaration(root: Path, *, apply: bool = True) -> bool:
    """Whether the store's tag declaration differs from ``tag-namespaces.yaml``; with ``apply``,
    rewrite it (sldb's ``save_declaration``). Idempotent: a second run finds nothing to do.

    A store without ``store.yaml`` (``deskops init`` creates none) starts from the declaration its
    index implies (sldb's ``declare_store``) once there is a namespace to declare.
    """
    from sldb.api.stores.declare_store import declare_store
    from sldb.api.stores.store_declaration import declaration_path
    from sldb.api.stores.store_declaration import load_declaration
    from sldb.api.stores.store_declaration import save_declaration

    root = Path(root)
    store = tag_store(root)
    if store is None:
        return False
    namespaces, models = wanted_tag_declaration(root)
    if declaration_path(store).is_file():
        current = load_declaration(store)
    elif namespaces:
        current = None
    else:
        return False
    if current is not None and current.tag_namespaces == namespaces and current.tag_models == models:
        return False
    if apply:
        base = current if current is not None else declare_store(store, Path(root).resolve())
        save_declaration(store, base.model_copy(update={"tag_namespaces": namespaces, "tag_models": models}))
    return True


# --- Bridge until sldb H4 ---------------------------------------------------------------
#
# Puente hasta sldb H4 (q18: create/track evalúan on_write). sldb's ``create_document`` and
# ``track_document_file`` do not evaluate ``on_write``, so the family cannot refuse a document
# deskops is about to create, and a CrossroadDoc carries no tag for it to check. Until they do,
# deskops refuses before writing from sldb's data only: the declared namespaces
# (``tag_namespaces``), the anchors (``tag_tree``) and what each tag requires
# (``TagNamespace.required``). Without a store or a declaration nothing is checked.


def declared_namespaces(store: Path) -> dict[str, Any]:
    """The namespaces the store declares, by name (``sldb.api.tag_namespaces``)."""
    from sldb.api import TagNamespace
    from sldb.api import tag_namespaces

    return {item["name"]: TagNamespace(**item) for item in tag_namespaces(store)}


def _anchored(store: Path, namespace: str) -> set[str]:
    from sldb.api import tag_tree

    found: set[str] = set()
    pending = list(tag_tree(store, namespace)["roots"])
    while pending:
        node = pending.pop()
        if node["document"] is not None:
            found.add(node["tag"])
        pending.extend(node["children"])
    return found


def refuse_undeclared_namespaces(root: Path, tags: list[str]) -> None:
    """Refuse a tag whose namespace the store does not declare (bridge until sldb H4)."""
    store = tag_store(root)
    declared = declared_namespaces(store) if store is not None else {}
    if not declared:
        return
    for tag in tags:
        namespace = str(tag).split(":", 1)[0]
        if ":" in str(tag) and namespace not in declared:
            raise ValueError(f"Unknown atom tag namespace '{namespace}' for tag '{tag}'.")


def unanchored_tags(root: Path, tags: list[str]) -> list[str]:
    """The tags ``tags`` require (``TagNamespace.required``) that no document anchors, top-down
    and once each; empty without a store or without anchored namespaces (bridge until sldb H4)."""
    store = tag_store(root)
    declared = declared_namespaces(store) if store is not None else {}
    missing: list[str] = []
    for name, namespace in declared.items():
        own = [str(tag) for tag in tags if str(tag).split(":", 1)[0] == name]
        if namespace.anchored_by is None or not own:
            continue
        anchored = _anchored(store, name)
        for tag in own:
            missing += [need for need in namespace.required(tag) if need not in anchored and need not in missing]
    return missing


def refuse_unanchored_domains(root: Path, tags: list[str]) -> None:
    """Refuse domain tags whose path lacks a written crossroad for some prefix (bridge until
    sldb H4); the message names the crossroads to write, top-down."""
    missing = [tag.split(":", 1)[1] for tag in unanchored_tags(root, tags)]
    if missing:
        commands = "; ".join(f"deskops atoms crossroad {path} --title ... --content ..." for path in missing)
        raise ValueError(
            f"Write the parent first: no written crossroad for {', '.join(missing)}. Every domain path "
            f"needs a crossroad that describes its children; create them top-down: {commands}"
        )


def refuse_unplaced_tags(root: Path, tags: list[str]) -> None:
    """The bridge for a document about to be created: declared namespaces, then anchored domains."""
    refuse_undeclared_namespaces(root, tags)
    refuse_unanchored_domains(root, tags)


# --- The family's findings, in deskops' words ----------------------------------------------


def tag_findings(root: Path) -> dict[str, dict[str, list[str]]]:
    """The findings of sldb's ``tag_check`` by document path (absolute, as ``str``), split in
    ``namespace`` (an undeclared namespace) and ``anchor`` (a domain path without crossroad),
    with the texts ``atoms validate`` printed before sldb checked them. Empty without a store or
    a declaration. Only the documents the store tracks are checked.
    """
    from sldb.api import tag_check

    store = tag_store(root)
    if store is None or not declared_namespaces(store):
        return {}
    base = Path(root).resolve()
    found: dict[str, dict[str, list[str]]] = {}
    for finding in tag_check(store):
        if not finding.document or _SEEN not in finding.what:
            continue
        seen = json.loads(finding.what.split(_SEEN, 1)[1][:-1])
        record = found.setdefault(str(base / finding.document), {"namespace": [], "anchor": []})
        if "missing" in seen:
            record["anchor"] += [
                f"no written crossroad for domain path '{tag.split(':', 1)[1]}'" for tag in seen["missing"]
            ]
        else:
            record["namespace"] += [
                f"Unknown atom tag namespace '{seen['namespace']}' for tag '{tag}'." for tag in seen["tags"][:1]
            ]
    return found


def _write_registry(path: Path, registry: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(registry, sort_keys=True), encoding="utf-8")

FILE:docs/workflow-policy-reference.md
---
atoms:
- id: atom-cheap-zero-context-reviews-test-the-brief-recursively
  role: documents
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-phase-gates-prevent-agent-skipping
  role: documents
- id: atom-code-changes-close-with-tests-and-commit
  role: documents
- id: atom-available-tasks-are-board-routed-work
  role: documents
- id: atom-drawers-feed-tasks-through-promotion
  role: documents
- id: atom-pills-carry-transitional-task-knowledge
  role: documents
- id: atom-pills-are-reusable-across-tasks
  role: documents
- id: atom-pills-end-as-atoms-docs-or-deletion
  role: documents
- id: atom-phases-are-dependency-layers-of-tasks
  role: documents
- id: atom-phase-closeout-reconciles-pills-and-next-work
  role: documents
- id: atom-tasks-enable-zero-context-subagents
  role: documents
- id: atom-task-board-phases
  role: documents
- id: atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
  role: documents
---
# Workflow Policy Reference

Source atoms are declared in the YAML frontmatter.

This reference summarizes the current workflow policy used by `deskops`.

> **No task is complete without the closeout evidence it declared at creation and its own closing commit. No phase is complete without integration validation and pill reconciliation.**

## Quick Links

- [Task Management](../desk/tasks/Board.md) - Active tasks
- [Pills Reference](../desk/contexts/pills.md) - Context pill format
- [Deferred Work](../desk/drawer/README.md) - Waiting items
- [Context Review Ritual](../desk/rituals/context-review.md) - Cheap recursive brief comprehension
- [Phase Ritual](../desk/rituals/phase.md) - Dependency-layer execution and closeout
- [Configuration map](configuration.md) - Where each rule, model and view lives, and how to declare a new task type or view

---

## Core Model

### Tasks

A task is the atomic workflow unit.

- One coherent deliverable.
- May depend on other tasks.
- Executes in a fresh subagent context.
- Declares how it activates and how it closes by choosing a task type (`deskops add task --task-type`); the type's activation rule names the review receipts it needs, the type's closeout rule names the evidence receipts it closes with, and the task closes only when `deskops closeout verify` has written them accepted and intact, with its own atomic closing commit. `--evidence` only adds kinds to the type's floor, never removes one the type requires.

#### Task types

A task type is a model: a `TaskDoc` subclass registered in the store. `model <= <Tipo>` names the type's family (including its subtypes); a subtype inherits the gates of its ancestors and can only add, never remove.

| Type | Extends | Activation receipts | Closeout evidence |
|---|---|---|---|
| `task.code` | `TaskDoc` | `preflight` + `bundle` | `tests` + `commit` + `atom\|materialization` |
| `task.docs` | `TaskDoc` | `preflight` | `commit` + `document` |
| `task.debug` | `TaskDoc` | `preflight` + `reproduction` | `tests` + `commit` + `atom\|materialization` |
| `task.refactor` | `task.code` | `preflight` + `bundle` + `goldens` | `task.code` + `goldens` |
| `task.decision` | `TaskDoc` | `owner` | `commit` + `document` |
| `task.aggregate` | `TaskDoc` | none (its dependencies closed; `children` is not a field yet) | `commit` (no `children` clause until `TaskAggregateDoc` has a children field) |
| `task.external` | `TaskDoc` | `preflight` | `external` (URL) |

`atom|materialization` is one gate with two alternatives. `commit` means a commit reachable from `HEAD`. The closeout column is data, `deskops/data/rules/closeout-evidence.yaml` (task type -> kinds): `deskops closeout verify` reads it to choose the producers it runs and `deskops add task` reads it as the floor `--evidence` adds to; a desk subtype reads its nearest factory ancestor's entry. A desk adds its own subtypes in `desk/models/*.py`; `deskops desk update --apply` registers them and migrates legacy `task_type` strings (`code`/`implementation`/`test` → `task.code`; `docs`/`spec`/`design` → `task.docs`; `external` → `task.external`; empty → `task.code`).

#### Activation rules

The activation gate of a type is not Python: it is a `RuleDoc` (sldb GO06/GO08) the desk carries under `desk/lifecycle/rule-activation-<type>.md`, a managed seed of the deskops package (`deskops/data/rules/`, declared in `deskops/data/desk_declaration.yaml` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply`; a desk's copy that differs is rewritten and a second run changes nothing). Every rule is `on_transition`, `severity: error`, applies `where current_node = "ritual-execution"` and has the subject `model <= <TypeDoc>`, so a desk subtype (`desk/models/*.py`) inherits it without code and a desk can add its own `RuleDoc` with a narrower subject to add a clause. A receipt counts when a `ReviewDoc` of that `kind` has the task as `subject`, `verdict: accepted` and `anchor_state: intact` (sldb pins `subject` with the task's contract hash when the receipt is saved and recomputes the state on every read: editing `goal`, `scope`, `files`, `validation`, `done_when`, `title` or `implementation_path` leaves it `changed`).

| Rule | Subject | Condition | Message |
|---|---|---|---|
| `rule-activation-task-code` | `model <= TaskCodeDoc` | `any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") and any(^subject: … kind = "bundle") and all(depends_on: status = "closed")` | Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. |
| `rule-activation-task-docs` | `model <= TaskDocsDoc` | `any(^subject: … kind = "preflight") and all(depends_on: status = "closed")` | Una tarea task.docs se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. |
| `rule-activation-task-debug` | `model <= TaskDebugDoc` | `any(^subject: … kind = "preflight") and any(^subject: … kind = "reproduction") and all(depends_on: status = "closed")` | Una tarea task.debug se activa con recibos preflight y reproduction aceptados e intactos y sus dependencias cerradas. |
| `rule-activation-task-refactor` | `model <= TaskRefactorDoc` | `any(^subject: … kind = "goldens")` (the `task.code` rule already applies to the family) | Una tarea task.refactor se activa, además de lo que pide task.code, con un recibo goldens aceptado e intacto. |
| `rule-activation-task-decision` | `model <= TaskDecisionDoc` | `any(^subject: … kind = "owner") and all(depends_on: status = "closed")` | Una tarea task.decision se activa con un recibo owner aceptado e intacto y sus dependencias cerradas. |
| `rule-activation-task-aggregate` | `model <= TaskAggregateDoc` | `all(depends_on: status = "closed")` | Una tarea task.aggregate se activa con sus dependencias cerradas. |
| `rule-activation-task-external` | `model <= TaskExternalDoc` | `any(^subject: … kind = "preflight") and all(depends_on: status = "closed")` | Una tarea task.external se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. |

`…` abbreviates `anchor_state = "intact" and verdict = "accepted" and`. A dependency that closed no longer exists as a task document, so `all(depends_on: …)` omits it. `deskops review` writes `preflight`, `bundle` and `node` receipts; `reproduction`, `goldens` and `owner` have no command yet.

`deskops advance` passes the task to sldb as the `document` of its `on_transition` rules: when an `error` finding holds the edge back, the message lists each finding (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: {...}) (witness: ...)`) instead of the edge's condition; a gate held back only by its own condition (`ritual-testing`, `ritual-closeout`) keeps the message `Gate <node> is not complete (...)`. `deskops show task` prints the same findings under each lifecycle gate (`blocked by:`; `findings` in `--format json`) and `deskops next` under `Blocked by:`. A blocked task is not a status: it stays `draft` at `ritual-execution` with the blocked edge visible in `show` and `next`.

#### Closeout rules

The closeout gate of a type is a `RuleDoc` too (CC33b): `desk/lifecycle/rule-closeout-<type>.md`, a managed seed of `deskops/data/rules/` declared and tracked like the activation rules. Every rule is `on_transition`, `severity: error`, applies `where current_node = "ritual-closeout"` (the source of `task_completes`, whose own condition is only `status = "ready_for_testing"`) and has the subject `model <= <TypeDoc>`. It asks, per kind of the table, for an evidence receipt `deskops closeout verify` writes (CC33a): `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")`, with `atom|materialization` as an `or` of the two.

| Rule | Subject | Clauses (receipts accepted and intact) |
|---|---|---|
| `rule-closeout-task-code` | `model <= TaskCodeDoc` | `tests`, `commit`, `atom` or `materialization` |
| `rule-closeout-task-docs` | `model <= TaskDocsDoc` | `commit`, `document` |
| `rule-closeout-task-debug` | `model <= TaskDebugDoc` | `tests`, `commit`, `atom` or `materialization` |
| `rule-closeout-task-refactor` | `model <= TaskRefactorDoc` | `any(^subject: kind = "goldens" and anchor_state = "intact" and verdict = "accepted")` (the receipt of `deskops review record --kind goldens`; the `task.code` rule already applies to the family) |
| `rule-closeout-task-decision` | `model <= TaskDecisionDoc` | `commit`, `document` |
| `rule-closeout-task-aggregate` | `model <= TaskAggregateDoc` | `commit` |
| `rule-closeout-task-external` | `model <= TaskExternalDoc` | `external` |

The closing order is fixed: `deskops closeout verify` runs the producers and writes the receipts (`accepted` or `rejected`); `deskops closeout commit` writes none and evaluates the rule on the task read at `ritual-closeout`. When an error finding holds it back the commit is not made and the output lists each finding (`- error: [rules/rule-closeout-<type>] ...`) and says to run `deskops closeout verify --task <id>`; editing a contract field after verify leaves the receipts `changed`, so the rule blocks again until verify writes new ones. `deskops show task` and `deskops next` show the same findings on the `task_completes` gate. The board view runs verify read-only.

When the atom|materialization gate passes without a linking document (a desk without local atoms, coverage only by a routed follow-up, or a skill guard test), verify writes an accepted `atom` receipt whose `value` is `exempt: <why the gate passed>`, so the rule needs no special case. `--evidence` (the task's `closeout_evidence`) only adds kinds (DA5): an added kind is verified and gets its receipt, and when it fails verify reports it as the alert `added_closeout_evidence_not_verified` without blocking; an added kind outside the vocabulary is the alert `unknown_closeout_evidence`.

#### Tests evidence from a suite in another language

The `tests` evidence is always a `.py` file: a reference counts only when it names an existing `.py` file under a `tests/` directory of the repository (or one the task declares in `files`). A repository whose suite is written in another language (vitest, go test, ...) does not change the gate; it declares its suite with a short pytest file that runs it through `deskops.testing.foreign_suites.run_foreign_suite`, and cites that file in the task's `references`.

`run_foreign_suite(command, *, cwd, timeout=None, env=None)` runs `command` (an argument list, no shell) in `cwd` (required, `str` or `Path`). Exit code 0 passes; a non-zero exit code, an executable that is not found or a `timeout` (seconds; `None` is no limit) calls `pytest.fail` with a plain-text message naming the command, the cwd, the exit code or the cause, and the last 200 lines of stdout and then of stderr. `env` replaces the whole environment, as in `subprocess`; `None` inherits it (merge `os.environ` yourself when you need both). The module exports the canonical commands `VITEST = ["npx", "vitest", "run"]` and `GO_TEST = ["go", "test", "./..."]`. The deskops CLI never imports it; it is meant for test files only.

Vitest (`tests/test_vitest_suite.py`):

```python
from pathlib import Path

from deskops.testing.foreign_suites import VITEST, run_foreign_suite


def test_vitest_suite() -> None:
    run_foreign_suite(VITEST, cwd=Path(__file__).resolve().parents[1])
```

Go (`tests/test_go_suite.py`):

```python
from pathlib import Path

from deskops.testing.foreign_suites import GO_TEST, run_foreign_suite


def test_go_suite() -> None:
    run_foreign_suite(GO_TEST, cwd=Path(__file__).resolve().parents[1])
```

The task then lists `tests/test_vitest_suite.py` (or `tests/test_go_suite.py`) in `references`, and `deskops closeout verify` counts it as `tests` evidence. From the root of a repository without its own Python environment, run it with the machine's deskops installation and a throwaway pytest through `uv`:

```bash
uv run --no-project --with pytest --with-editable /mnt/ssd/herramientas/deskops \
  python -m pytest -q tests/test_vitest_suite.py
```

`--with-editable` points at the deskops checkout the machine's `deskops` tool is installed from (on this machine `/mnt/ssd/herramientas/deskops`); that checkout must include `deskops/testing/`.

#### Commit evidence from another repository

When a task's code entered another repository, its `commit` evidence is a reference of the form `<repo-id>:<sha>` in the task's `references` (for example `deskops:4a7707a5`). `deskops closeout verify` counts it, and `deskops closeout resolved-by --ref` accepts it, after two steps:

1. The `<repo-id>` is resolved first in the desk's own registry (`desk/registry/repo-*.md`, under `--root`) and, when that registry does not list it, in the ecosystem registry (`$DESKOPS_ECOSYSTEM_REGISTRY`, else `~/setup/desk/registry`), the same fallback `deskops message send --to` uses. When both list the id, the desk's registry wins. A prefix equal to the desk's own `project_identity`, or a repository whose root is the desk's root, is local: the `<sha>` is checked in this repository.
2. The `<sha>` is checked in that repository's registered root with the same rule as a local commit: a lowercase hex id (7 to 40 characters) that `git rev-parse --verify <sha>^{commit}` resolves and that is HEAD or an ancestor of its HEAD.

A reference that does not resolve does not count and raises nothing: an unknown repo-id, an id the ecosystem registry lists twice (or a registry that cannot be read), a sha that does not exist there or is not an ancestor of its HEAD. A registered root that is not on this machine does not count either: verify reports the commit gate as not found with `Registered repository <id> is not at <path> on this machine.`, and `resolved-by` refuses the close with that message. The evidence receipt records the full id as `<repo-id>:<full sha>`.

Only the commit evidence reads the ecosystem registry. A `resolved-by --test <repo-id>:<test path>` still resolves `<repo-id>` in the desk's own registry alone, and the tests gate of verify is unchanged.

Two rules over the task's own fields are `on_write` alerts, `subject: model <= TaskDoc`: `rule-closeout-alert-implicit-code` (`has(task_type) or nonempty(closeout_evidence)`: a task that predates types is gated as code) and `rule-closeout-alert-pill-graduation` (`not nonempty(pills) or any(references: model <= AtomDoc)`: a task that binds pills references the atom they graduate to). The other field checks stay in verify because the rule language has no quantifier over the elements of a list value: the closeout evidence vocabulary (`deskops add task --evidence` refuses an unknown kind), `python_changes_without_declared_tests` and the http(s) shape of an `external` reference.

### Task lifecycle graph

A task moves through the desk's lifecycle graph, which lives in the desk's sldb store: every state is a tracked ritual (`RitualDoc:ritual-execution`, `ritual-testing`, `ritual-closeout`) and every transition is a `RelationDoc` under `desk/lifecycle/`, typed by a `RelationTypeDoc` named by the verb (`task_activates`, `task_hands_to_closeout`, `task_completes`). Each `RelationDoc` declares the whole transition: its `condition` (an sldb `--where` predicate over the task, such as `nonempty(validation)`) and its effects in `attributes`, following sldb's transition convention (GO09): `sets` names the task fields the transition writes (`status: active`, `ready_for_testing`, `closed`) and `terminal: true` marks the transition that closes the task (`task_completes`).

`deskops advance task` asks sldb which edges leaving the task's current node hold (`sldb.api.edges_holding`, with the task as `document` so its activation rule runs), takes that edge, applies its effects with `sldb.api.apply_effects` (validated against the task type's model), sets `current_node: complete` when the edge is terminal and appends the relation type to the task's `history`. One edge leaves each ritual, so nothing depends on the order sldb returns edges in. A blocked task stays where it is with the gate named. The terminal transition is never persisted by `advance`: the only closing entry point is `deskops closeout commit`. `deskops next` reads only the states of `deskops/spec/workflows/task_lifecycle.yaml` (ritual, next actions, `advance_when`); `deskops next --diagram` draws the desk's graph.

The six lifecycle documents and the seven activation rules are managed seeds of the deskops package (`deskops/data/desk_declaration.yaml`, templates in `deskops/data/lifecycle/` and `deskops/data/rules/`). `deskops init` and `deskops desk update --apply` write them, track them (with the three lifecycle rituals by their ids) and rewrite a desk's copy that differs from the package's: `desk update` lists it under `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote <path>`, and a second run changes nothing. Every other scaffold only creates what is missing. Changing a transition's effect means changing the `RelationDoc` through sldb; no YAML of deskops has to change, and the next `desk update --apply` restores the package's version.

#### Lifecycle consistency (CC37)

A task's `status`, `current_node`, `history` and `task_type` are checked together by a validator of the `TaskDoc` model (`deskops/models/task_lifecycle.py`). sldb applies it on every write: `deskops` itself, `sldb fields update`, `sldb docs update`, `sldb serve` `/save` and transactions. So a write that leaves a task inconsistent is refused with the validator's message, whatever path it takes. A task is consistent in one of these states:

- **Entry:** `current_node` is the entry node, `history` is empty and `status` is `draft`.
- **After transitions:** the last `history` item is the transition that leads to `current_node`, and `status` is what that transition `sets` (`active`, then `ready_for_testing`). The table comes from the package's `RelationDoc`s, not from the desk's store.
- **Closed by closeout:** `superseded` after `superseded`, `resolved` after `resolved-by`, and `closed` after `task_completes`. `closeout supersede` and `closeout resolved-by` record the first two from any node, also on a task the model rejects (they write its frontmatter), and a store lets them close one invalid task while another of the same model remains (sldb names it `store/doc-invalid` and goes on). `closed` is never persisted by `advance`; `closeout commit` removes the task.
- **Outside the lifecycle**, with no `current_node` and empty history: `draft`, a drawer task's `deferred`, and the pre-lifecycle statuses that `closeout retire` removes (`resolved`, `closed`, `done`, `complete`).

`task_type` matches the document's model: each typed model accepts only its own type, and the generic `TaskDoc` accepts an empty or unregistered type. `deskops desk update --apply` does not write an inconsistent task. It reports the task with the reason sldb gives. Only `deskops advance` and `deskops closeout` change a task's lifecycle fields; `deskops edit task` refuses them (GC06).

### Phases

Tasks form an execution dependency graph.

A **phase** is one horizontal dependency layer in that graph:

- task prerequisites are already satisfied
- tasks are ready at the same time
- planned operational changes do not overlap
- tasks may run in parallel when the environment supports it

A phase has execution meaning, not business meaning. It is the workflow unit above individual tasks and below the whole board.

### Boards

The board is the routing surface for active work.

- It names the active tasks.
- It routes board-wide pills and rituals.
- Its current ready dependency layer is the current phase.

---

## Cheap Context Review and Fresh Subagents

Before promoting or executing a draft, plan, package or leaf, run the [context-review ritual](../desk/rituals/context-review.md). It tests the quality of the written question with a cheap reviewer: faithful reformulation, explicit ambiguities and a detailed dry-run of proposed readings, changes, validation and dependencies. The reviewer names intended commands without executing them or editing sources.

Supply the exact versioned brief and only necessary explicit references. Use a new ephemeral process for every attempt, without chat history, earlier reviews, oral fixes, persistent memory, automatic context/skills or tools. Record the chosen cheap provider/model/profile and reason; an expert cannot rescue a failed cheap comprehension gate. The ritual specifies the verified Pi isolation profile and per-node evidence layout.

The coordinator compares understanding with intent, corrects the written brief and recursively decomposes large nodes into children and explicit edges. Review root, packages, every leaf and dependency interfaces before selecting ready leaves. A root-only review does not cover descendants. Unresolved ambiguity blocks execution. Changed input or a changed dependency contract invalidates affected reviews; retries use a new process. Technical transport/quota failures are recorded separately from ambiguity.

Before Executor dispatch, preserve two distinct cheap roles: TaskDoc-only preflight (also saved in `runs/subagents/<run-dir>/preflight.md`) and cold-bundle coverage. The explicit execution bundle contains task, board-routed instructions/rituals, bound pills, linked atoms/files and validation targets. Neither review executes implementation. Expert council review, Executor work, independent Tester validation and human product approval remain separate gates; a word such as APTO or structural PASS grants none of them.

Evidence lives at `runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/`: exact input bytes/hash, model/profile/selection, command/isolation, reformulation/ambiguities/dry-run, coordinator comparison and required edits. These are process records, not runtime enforcement or a new lifecycle state. Each active task then executes in its own fresh context, and an independent Tester validates implementation. The coordinator integrates outputs and enforces task/phase closeout. Do not carry unrelated tasks through one long-lived context.

---

## Pill Lifecycle

Pills are temporary execution aids, but they are not task-specific instances. Correction: pills are not 1:1 with tasks.

```text
Draft or refresh reusable pills -> bind pills to tasks opportunistically -> execute tasks ->
close tasks -> reconcile pills at phase closeout ->
keep / delete / merge / graduate to atoms -> prepare next phase pills
```

At phase closeout, classify touched pills explicitly:

- **still active** - keep for the next phase
- **stale** - delete or retire
- **redundant** - merge or remove duplicates
- **durable** - promote the stabilized residue into atoms first
- **materialization-worthy** - land resulting changes in code, specs, or docs as needed

Do not let durable knowledge remain pill-only once it stabilizes. Do not create a new pill just because a new task exists; create or update a pill only when there is a reusable atomic truth worth rebinding.

---

## Ritual Stack

### 1. Phase Ritual

Before starting a ready dependency layer:

```text
0. REVIEW   -> Review root/packages/leaves and edges cheaply; correct briefs and decompose.
1. IDENTIFY -> Select reviewed ready non-overlapping leaves.
2. BUNDLE   -> Confirm each task has its fresh context bundle.
3. EXECUTE  -> Run the execution ritual per task.
4. CLOSE    -> Require each task to close with its declared evidence and a task commit.
5. VALIDATE -> Run phase-level integration or end-to-end checks.
6. REGRESS  -> Fix interaction regressions.
7. RECONCILE-> Audit pills; delete, merge, or graduate them.
8. SURFACE  -> Capture newly discovered tasks and next-phase pills.
9. COMMIT   -> Make the phase-closing commit.
```

### 2. Task Execution Ritual

For each task in the phase:

```text
1. INIT   -> Confirm task scope, files, pills, validation, and declared closeout evidence.
2. REVIEW -> Accept cheap TaskDoc-only preflight, then separate cheap cold-bundle coverage.
3. BIND   -> Bind every relevant pill.
4. IMPLEMENT -> Make only task-scoped changes.
5. HANDOFF   -> Open an explicit testing handoff.
```

### 3. Task Testing Ritual

```text
1. CHECK  -> Confirm the intended contract and pill guardrails.
2. UPDATE -> Fix stale tests or add missing ones.
3. RUN    -> Execute the smallest relevant scope first.
4. EXPAND -> Run broader checks when shared behavior changed.
5. HANDOFF-> Open an explicit closeout handoff.
```

### 4. Task Closeout Ritual

```text
1. VERIFY -> Run `deskops closeout verify`: it checks the type's evidence (declared X;
             found Y) and writes the evidence receipts the closeout rule reads.
2. CLEAN  -> Remove stale task-local context when appropriate.
3. DELETE -> Remove the resolved task from active routing.
4. COMMIT -> Close with `deskops closeout commit`: it evaluates the type's closeout rule
             on those receipts and writes none; `closeout supersede` when the
             subject no longer exists, `closeout retire` for a pre-lifecycle resolution.
5. WAIT   -> If this was the last task in the phase, do not start the next phase until phase closeout passes.
```

---

## Commit Rules

### Task commit

Every closed task gets its own atomic commit, made by `deskops closeout commit`, `closeout supersede`, or `closeout retire`. The evidence it must show is its type's (plus any kind `--evidence` added at creation), as receipts `deskops closeout verify` wrote and the type's closeout rule accepts.

### Phase commit

When all tasks in a phase are closed, make one separate descriptive phase commit for:

- integration fixes
- pill reconciliation
- captured next work
- board/phase bookkeeping

Do not hide unfinished task work inside a phase commit.

---

## Anti-Patterns

- Starting implementation before identifying the ready phase.
- Treating semantic milestones as phases when tasks still depend on each other.
- Running multiple unrelated tasks through one stale context.
- Closing tasks without the evidence they declared or without a dedicated task commit.
- Starting the next phase after isolated green task tests without integration validation.
- Carrying stale or overlapping pills forward because each task passed independently.
- Leaving durable rules only in pills instead of promoting them into atoms.
- Skipping newly discovered task capture at phase closeout.

FILE:instruccion
Cold-bundle de la tarea task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_tags.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_domain_tree.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops desk update --apply --root . && PYTHONPATH=../sldb/src:. ../.venv/bin/python -m sldb stores check --store .sldb (sin alertas de tag por host)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

