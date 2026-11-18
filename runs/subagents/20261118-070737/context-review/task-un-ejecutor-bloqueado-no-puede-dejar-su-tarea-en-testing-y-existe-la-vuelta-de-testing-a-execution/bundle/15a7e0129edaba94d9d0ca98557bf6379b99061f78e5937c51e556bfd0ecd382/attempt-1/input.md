FILE:desk/tasks/task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution.md
---
sldb:
  by: agent
  at: '2026-11-18T07:04:57Z'
  authority: generated
  via: save_document_payload
id: task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution
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
- deskops/lifecycle.py
- deskops/services/tasks.py
- deskops/runtime/scion.py
- deskops/cli/registry.py
- deskops/data/desk_declaration.yaml
- tests/test_lifecycle_graph.py
- tests/test_scion_runtime.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Un ejecutor bloqueado no puede dejar su tarea en testing y existe la vuelta de testing a execution

## Rationale

_Explain why this task exists or the business driver behind it._

El 2026-11-18 un ejecutor scion del desk de sldb entrego BLOQUEADO (necesitaba una decision de diseno), sin codigo, y aun asi corrio `deskops advance task`: la tarea paso a ritual-testing con status active. La transicion task_activates solo mira los recibos preflight y bundle, y no hay ninguna transicion que devuelva una tarea de ritual-testing a ritual-execution. El coordinador tuvo que relanzar con la tarea en un nodo que no corresponde.

## Goal

_Describe the concrete result this task must produce._

Dos cambios.

(1) Transicion de vuelta. La siembra del lifecycle (los archivos de la carpeta `deskops/data/lifecycle` y su lista en `deskops/data/desk_declaration.yaml`) gana una transicion de `RitualDoc:ritual-testing` a `RitualDoc:ritual-execution` con `relation_type: task_returns_to_execution`, sin condicion, con `attributes.sets.status: active`, `attributes.terminal: false` y un atributo nuevo `attributes.manual: true`, mas su archivo de tipo, copiando la forma de `deskops/data/lifecycle/testing-task_hands_to_closeout.md` y `deskops/data/lifecycle/type-task_hands_to_closeout.md`. Una transicion con `manual: true` nunca la toma el avance normal: `deskops advance task <id>` sin opciones se comporta exactamente como hoy. `deskops advance task <id> --back --reason "<texto>"` toma solo transiciones manuales desde el nodo actual; agrega a `history` la cadena `task_returns_to_execution: <texto>` (hoy history guarda solo el relation_type; esta entrada lleva ademas el motivo); corre los post-hooks de esa transicion igual que cualquier avance. `--back` sin `--reason`, o con motivo vacio, sale con codigo 2 y un mensaje; `--reason` sin `--back` sale con codigo 2; `--back` en un nodo sin transicion manual sale bloqueado con el mensaje `no hay transicion de vuelta desde <nodo>`.

(2) Regla del ejecutor. El agents.md del modo executor (funcion `_render_agents_md` de `deskops/runtime/scion.py`) dice que, si el ejecutor termina bloqueado o sin cambios, NO corre `deskops advance task`: escribe el bloqueo en result-summary.md y termina con `sciontool status blocked "<motivo>"`.

El manual (`docs/operator-manual.md`, seccion `Inspect, edit, and advance a task`) documenta `--back --reason` y el atributo `manual`.

## Scope

_State what is in scope and what is out of scope._

Dentro: la carpeta `deskops/data/lifecycle` y `deskops/data/desk_declaration.yaml`, `deskops/lifecycle.py`, `deskops/services/tasks.py`, la opcion en `deskops/cli/registry.py` y el comando que la recibe, `deskops/runtime/scion.py`, `tests/test_lifecycle_graph.py`, `tests/test_scion_runtime.py`, `docs/operator-manual.md`, y los goldens de ayuda que cambien por la opcion nueva. Fuera: aplicar la transicion a desks reales (lo hace despues `deskops desk update --apply` en cada desk). Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- `TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py tests/test_scion_runtime.py` pasa, con tests nuevos sobre un desk desechable de `tmp_path` que comprueban: (a) una tarea en ritual-testing vuelve a ritual-execution con `--back --reason`, queda con status active y su history termina en `task_returns_to_execution: <texto>`; (b) sin `--back`, desde ritual-testing el avance normal sigue yendo a ritual-closeout y nunca toma la transicion manual; (c) los tres casos de codigo 2 y el caso bloqueado; (d) un post-hook declarado en la transicion de vuelta corre; (e) el agents.md del ejecutor contiene `sciontool status blocked`.
- Los goldens de ayuda afectados se regeneran con `pytest -n 4 tests/test_output_goldens.py -k help --update-golden` y se conservan solo los que cambian por la opcion nueva.
- `deskops doctor --root .` sobre un desk recien creado con `deskops init` no informa deriva por la transicion nueva.

## Done When

_Name the observable condition that makes the task complete._

En un desk desechable una tarea en ritual-testing vuelve a ritual-execution con `advance task --back --reason`, y sin `--back` el avance normal no cambia; el agents.md del ejecutor trae la regla del bloqueo.

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

FILE:deskops/lifecycle.py
"""The task lifecycle as a graph in the desk's sldb store.

States are the desk's tracked rituals (``RitualDoc:ritual-execution`` and its siblings).
Transitions are sldb ``RelationDoc`` edges between those rituals, typed by a
``RelationTypeDoc`` whose name is the verb (``task_activates``), with a ``condition``
written as an sldb ``--where`` predicate over the task and the transition's effects in
``attributes``: ``sets`` (the task fields the transition writes, ``status`` today) and
``terminal`` (the task closes), the convention sldb reads (GO09). The six documents are
managed seeds of the package (``deskops/data/desk_declaration.yaml``, templates in
``deskops/data/lifecycle/``): ``deskops init`` and ``deskops desk update --apply`` write
them under ``desk/lifecycle/`` and rewrite a desk's copy that differs.

The activation gate of each factory task type is a ``RuleDoc`` (sldb GO06/GO08), also a
managed seed (``deskops/data/rules/``, written to ``desk/lifecycle/rule-activation-<type>.md``):
``on_transition`` over ``ritual-execution``, with subject ``model <= <TypeDoc>`` so a desk's
subtype inherits it without code, requiring the review receipts the type asks for
(``any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")``) and
the task's dependencies closed (``all(depends_on: status = "closed")``). sldb evaluates those
rules when ``edges_holding`` receives the task as ``document``; an ``error`` finding blocks
every edge and ``edges_blocked`` returns them with the findings ``deskops advance``, ``next``
and ``show`` print.

deskops keeps three things: the states ``deskops next`` describes
(``deskops/spec/workflows/task_lifecycle.yaml``), the call to sldb for the edges whose
condition holds (``sldb.api.edges_holding``) and their effects (``sldb.api.apply_effects``),
and the task's ``history``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from deskops.paths import data_path
from deskops.paths import package_pythonpath

SPEC_PATH = data_path("spec", "workflows", "task_lifecycle.yaml")
LIFECYCLE_DIR = Path("desk") / "lifecycle"
COMPLETE = "complete"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
RITUAL_MODEL = "RitualDoc"
RULE_MODEL = "RuleDoc"
RULE_MODEL_REF = "sldb.models.rule_doc:RuleDoc"


class LifecycleGraphMissing(RuntimeError):
    """The desk's store has no lifecycle graph, or it does not cover a task's state."""


class LifecycleSeedOutOfDate(LifecycleGraphMissing):
    """The edge ``deskops advance`` would take does not carry the package's effect (a desk's
    lifecycle seed older than CC31, ``attributes: {}``): applying it would write a state the
    ``TaskDoc`` validator rejects. Raised before any effect is applied; the fix is
    ``deskops desk update --apply``, which restores the managed seed."""


class HookDefinitionError(RuntimeError):
    """A transition's ``attributes.hooks`` entry is malformed; ``deskops advance`` fails with it
    before persisting anything."""


#: Seconds a post-hook may run unless its entry carries its own ``timeout``.
DEFAULT_HOOK_TIMEOUT = 300


@dataclass(frozen=True, slots=True)
class Hook:
    """One post-hook of a transition: a command (argument list, no shell) run after the transition is persisted."""

    name: str
    run: tuple[str, ...]
    timeout: int = DEFAULT_HOOK_TIMEOUT

    def as_dict(self) -> dict[str, Any]:
        return {"name": self.name, "run": list(self.run), "timeout": self.timeout}


def parse_hooks(raw: Any, relation_doc: str) -> tuple[Hook, ...]:
    """The hooks of ``attributes.hooks`` of the edge authored by ``relation_doc``; raises
    ``HookDefinitionError`` naming the RelationDoc when an entry has no ``name``, no ``run``, a
    ``run`` that is not a list of texts, or a ``timeout`` that is not an integer above zero."""
    if raw in (None, ""):
        return ()
    where = f"{LIFECYCLE_DIR.as_posix()}/{relation_doc}.md"

    def bad(why: str) -> HookDefinitionError:
        return HookDefinitionError(f"Malformed attributes.hooks in {where}: {why}.")

    if not isinstance(raw, list):
        raise bad("hooks must be a list")
    hooks: list[Hook] = []
    for index, entry in enumerate(raw, start=1):
        if not isinstance(entry, dict):
            raise bad(f"entry {index} is not a mapping")
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            raise bad(f"entry {index} has no name")
        run = entry.get("run")
        if not isinstance(run, list) or not run or not all(isinstance(a, str) for a in run):
            raise bad(f"hook '{name}' needs run as a non-empty list of texts")
        timeout = entry.get("timeout", DEFAULT_HOOK_TIMEOUT)
        if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0:
            raise bad(f"hook '{name}' has a timeout that is not an integer above zero")
        hooks.append(Hook(name=name, run=tuple(run), timeout=timeout))
    return tuple(hooks)


def _frontmatter_of(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def hooks_from_text(text: str) -> Any:
    """``attributes.hooks`` of a lifecycle seed's frontmatter text; None when it declares none."""
    attributes = _frontmatter_of(text).get("attributes")
    return attributes.get("hooks") if isinstance(attributes, dict) else None


def provenance_from_text(text: str) -> Any:
    """The ``sldb`` write provenance of a document's frontmatter text; None without it."""
    return _frontmatter_of(text).get("sldb")


def with_hooks(text: str, hooks: Any, provenance: Any = None) -> str:
    """The seed ``text`` with ``attributes.hooks`` set to ``hooks`` (the whole list, in order) and,
    when given, the desk copy's ``sldb`` write provenance (sldb adds it to a document it edits, so
    a copy carrying the hooks has it); the text unchanged when the seed has no frontmatter."""
    front = _frontmatter_of(text)
    if not front:
        return text
    attributes = dict(front.get("attributes") or {})
    attributes["hooks"] = hooks
    front["attributes"] = attributes
    if provenance is not None:
        front = {"sldb": provenance, **front}
    rest = text.split("---", 2)[2]
    return "---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---" + rest


@dataclass(frozen=True, slots=True)
class Transition:
    """One edge of the lifecycle graph leaving ``source``, with its effects as the edge declares them."""

    relation_type: str
    source: str
    target: str
    condition: str
    sets: dict[str, Any] = field(default_factory=dict)
    terminal: bool = False
    #: The name of the ``RelationDoc`` that authors the edge (its file is ``desk/lifecycle/<name>.md``).
    relation_doc: str = ""
    #: The findings of the task's ``on_transition`` rules (sldb GO08), as ``finding_dict`` gives
    #: them: every finding on a blocked edge, only alerts on a holding one, none without a document.
    findings: tuple[dict[str, Any], ...] = ()
    #: ``attributes.hooks`` as the edge declares them, unvalidated (``parse_hooks`` validates).
    raw_hooks: Any = None

    @property
    def hooks(self) -> tuple[Hook, ...]:
        return parse_hooks(self.raw_hooks, self.relation_doc or self.relation_type)

    def hooks_listing(self) -> list[dict[str, Any]]:
        """The declared hooks as plain mappings for display; a malformed entry is shown as far as it reads."""
        raw = self.raw_hooks if isinstance(self.raw_hooks, list) else []
        return [
            {
                "name": str(e.get("name") or ""),
                "run": [str(a) for a in e["run"]] if isinstance(e.get("run"), list) else [],
                "timeout": e.get("timeout", DEFAULT_HOOK_TIMEOUT),
            }
            for e in raw
            if isinstance(e, dict)
        ]

    @property
    def effects(self) -> dict[str, Any]:
        return {"sets": dict(self.sets), "terminal": self.terminal}


@dataclass(frozen=True, slots=True)
class LifecycleSpec:
    """The states of ``task_lifecycle.yaml``: what ``deskops next`` says at each node."""

    entry_node: str
    states: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def rituals(self) -> list[str]:
        return [node for node in (str(state.get("current_node") or "") for state in self.states) if node and node != COMPLETE]


@dataclass(slots=True)
class ReadSnapshot:
    """Reads shared by every task of one read-only pass.

    ``DeskopsOperations.read_snapshot`` opens one; ``transitions_from`` keeps the transitions
    leaving each node in it, ``transition_findings`` the store's rule graph (sldb loads the
    whole index for it, ~3 s on a small desk), the closure service the closeout graph context
    and the operations facade the path, model payload and normalized payload of each task.
    Nothing outlives the pass: the snapshot is dropped when the block closes.
    """

    transitions: dict[str, list["Transition"]] = field(default_factory=dict)
    graph_context: Any = None
    rule_graph: Any = None
    has_rules: bool | None = None
    #: Cache key (resolved path or task id) -> (path, model payload, payload with effective fields).
    task_records: dict[str, tuple[Path, dict[str, Any], dict[str, Any]]] = field(default_factory=dict)
    #: Normalized task payloads, keyed by task id, shared by a task's inherited parents.
    task_payloads: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: Resolved task path -> the ``Model:name`` its on_transition rules use.
    task_documents: dict[str, str | None] = field(default_factory=dict)


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str
    #: The transition taken (set when ``progressed``); ``advance_task`` runs its hooks after persisting it.
    transition: Transition | None = None


def load_lifecycle_spec(path: Path = SPEC_PATH) -> LifecycleSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    states = tuple(state for state in payload.get("states") or [] if isinstance(state, dict))
    if not states:
        raise ValueError(f"Lifecycle spec declares no states: {path}")
    return LifecycleSpec(entry_node=str(payload.get("entry_node") or states[0].get("current_node") or ""), states=states)


# ---------------------------------------------------------------- conditions
def condition_holds(condition: str, payload: dict[str, Any]) -> bool:
    """Whether an sldb ``--where`` condition (predicates joined by `` and ``) holds on a task payload."""
    from sldb.api import where_matches

    return where_matches(condition, payload)


# ---------------------------------------------------------------- the graph
def _store(root: Path) -> Path:
    return root / ".sldb"


def ritual_export_id(ritual_id: str) -> str:
    return f"{RITUAL_MODEL}:{ritual_id}"


def finding_dict(finding: Any) -> dict[str, Any]:
    """An sldb ``Finding`` as the plain mapping ``show --format json`` prints."""
    return {"level": finding.level, "code": finding.code, "subject": finding.subject, "what": finding.what}


def finding_line(finding: dict[str, Any]) -> str:
    """One finding as sldb prints it: ``<level>: [<code>] <node>: <message> | <clause> (seen: ...)``."""
    return f"{finding['level']}: [{finding['code']}] {finding['subject']}: {finding['what']}"


def _transition(node: str, edge: Any) -> Transition:
    """The edge as a transition; ``effects`` (filled by ``edges_holding``) else the declared attributes."""
    attributes = edge.metadata.get("attributes") or {}
    effects = edge.effects or {"sets": attributes.get("sets") or {}, "terminal": attributes.get("terminal")}
    return Transition(
        relation_type=edge.relation,
        source=node,
        target=edge.target.rsplit(":", 1)[-1],
        condition=str(edge.metadata.get("condition") or ""),
        sets=dict(effects.get("sets") or {}),
        terminal=bool(effects.get("terminal")),
        relation_doc=str(edge.metadata.get("relation_doc") or ""),
        findings=tuple(finding_dict(f) for f in (getattr(edge, "findings", None) or ())),
        raw_hooks=attributes.get("hooks"),
    )


def _is_lifecycle_edge(edge: Any) -> bool:
    """An authored edge (a RelationDoc) whose target is a ritual (`sldb://document/RitualDoc:<id>`)."""
    return edge.metadata.get("origin") == "relation_doc" and edge.target.rsplit("/", 1)[-1].startswith(f"{RITUAL_MODEL}:")


def _lifecycle_edges(node: str, edges: list[Any]) -> list[Transition]:
    """The authored edges between rituals, in the order sldb returns them."""
    return [_transition(node, e) for e in edges if _is_lifecycle_edge(e)]


def transitions_from(root: Path, node: str, *, snapshot: ReadSnapshot | None = None) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology, conditions and effects all come from the graph. The lifecycle graph lives in the
    desk's own store, so only that store's edge index is read (sldb keeps it composed while
    its shards do not move), not the index composed with every linked store.

    With a ``snapshot``, the transitions leaving a node are read once and reused.
    """
    if snapshot is not None:
        if node not in snapshot.transitions:
            snapshot.transitions[node] = transitions_from(root, node)
        return snapshot.transitions[node]
    from sldb.api import edges_from

    return _lifecycle_edges(node, edges_from(_store(root), ritual_export_id(node), include_linked=False))


def transitions_holding(root: Path, node: str, payload: dict[str, Any], document: str | None = None) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` (``sldb.api.edges_holding``),
    each with its effects resolved for that payload. With ``document`` (the task's ``Model:name``
    in the store) the task's ``on_transition`` rules run too: an error finding holds every edge back."""
    from sldb.api import edges_holding

    return _lifecycle_edges(node, edges_holding(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transitions_blocked(root: Path, node: str, payload: dict[str, Any], document: str) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` but that an error
    finding of the task's ``on_transition`` rules blocks (``sldb.api.edges_blocked``), each
    carrying every finding."""
    from sldb.api import edges_blocked

    return _lifecycle_edges(node, edges_blocked(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transition_findings(root: Path, document: str, payload: dict[str, Any], *, snapshot: ReadSnapshot | None = None) -> list[dict[str, Any]]:
    """The findings of the task's ``on_transition`` rules read as ``payload`` (``sldb.api.transition_findings``).

    With a ``snapshot``, the store's rule graph is loaded once and shared by every task read of
    the pass (what ``sldb.api.transition_findings`` does on each call); a store without
    ``RuleDoc`` has no findings and loads nothing."""
    if snapshot is None:
        from sldb.api import transition_findings as sldb_transition_findings

        return [finding_dict(f) for f in sldb_transition_findings(_store(root), document, payload)]
    from sldb.api.rules.rule_graph import rule_graph
    from sldb.api.rules.rule_subjects import resolve_subject
    from sldb.api.rules.rules_on_transition import has_rules
    from sldb.api.rules.rules_on_transition import payload_findings

    if snapshot.has_rules is None:
        snapshot.has_rules = has_rules(_store(root))
    if not snapshot.has_rules:
        return []
    if snapshot.rule_graph is None:
        # The same graph sldb's transition_findings builds: its own index unless the rules
        # may read a linked store (``rule_graph(store, None)``).
        snapshot.rule_graph = rule_graph(_store(root), None)
    graph = snapshot.rule_graph
    return [finding_dict(f) for f in payload_findings(graph, "on_transition", resolve_subject(graph, document), payload)]


def task_document(root: Path, task_path: Path) -> str | None:
    """The ``Model:name`` the desk's store tracks ``task_path`` under (the subject of its rules);
    None for an untracked task or a desk without a store, where no rule runs.

    Reads the store indexes deskops already keeps for the pass (``doc_access.index_entries``)
    instead of opening the store once more for every task.
    """
    from deskops import doc_access

    if not (_store(root) / "core").exists():
        return None
    try:
        entry = doc_access.index_entry(root, task_path)
    except Exception:
        return None
    if entry is None or not entry.model or not entry.name:
        return None
    return f"{entry.model}:{entry.name}"


def lifecycle_transitions(root: Path, spec: LifecycleSpec | None = None) -> list[Transition]:
    """Every transition of the desk's lifecycle graph, ritual by ritual; empty without a store."""
    if not (_store(root) / "core").exists():
        return []
    spec = spec or load_lifecycle_spec()
    return [t for node in spec.rituals for t in transitions_from(root, node)]


def advance(root: Path, payload: dict[str, Any], model: type[Any], spec: LifecycleSpec | None = None, document: str | None = None) -> TransitionResult:
    """Take the first transition out of the task's current node whose condition holds.

    The edge's effects are applied with ``sldb.api.apply_effects`` (``sets`` replaces the
    payload's top-level keys; the result validates against ``model``, the task type's model)
    and, when the edge is ``terminal``, ``current_node`` becomes ``complete``; the relation type
    is appended to ``history``. Mutates ``payload`` and reports what happened; one call takes
    at most one transition. The graph has one edge leaving each ritual, so the order sldb
    returns the holding edges in decides nothing (k4).

    With ``document`` (``task_document``) the task's ``on_transition`` rules run: when an error
    finding holds the edges back, the message lists each finding (rule, clause, node and value
    seen) instead of the edges' conditions.
    """
    from sldb.api import apply_effects

    spec = spec or load_lifecycle_spec()
    node = str(payload.get("current_node") or spec.entry_node)
    status = str(payload.get("status") or "")
    if node == COMPLETE:
        return TransitionResult(COMPLETE, status, False, False, "Task already complete.")
    if not (_store(root) / "core").exists():
        raise LifecycleGraphMissing(
            f"No sldb store at {_store(root)}: run 'deskops init' (or 'deskops desk update --apply' on an "
            "existing store) to create the lifecycle graph that 'deskops advance' reads."
        )
    transitions = transitions_from(root, node)
    if not transitions:
        raise LifecycleGraphMissing(
            f"No lifecycle transition leaves '{node}' in the graph of {_store(root)}. "
            "Run 'deskops desk update --apply' to write the lifecycle graph."
        )
    holding = transitions_holding(root, node, payload, document)
    if not holding:
        payload["current_node"] = node
        blocked = transitions_blocked(root, node, payload, document) if document else []
        findings = [f for t in blocked for f in t.findings if f["level"] == "error"]
        if findings:
            lines = "; ".join(finding_line(f) for f in findings)
            return TransitionResult(node, status, False, True, f"Gate {node} is blocked by its rules: {lines}")
        gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
        return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")
    transition = holding[0]
    target = COMPLETE if transition.terminal else transition.target
    _check_against_package(payload, transition, target)
    transition.hooks  # a malformed hook entry fails here, before the payload changes
    # The model validates the whole new state (TaskDoc's lifecycle coherence): the edge's
    # ``sets``, the history it appends to and the node it leads to are applied together.
    history = [str(item) for item in payload.get("history") or []]
    sets = {**transition.sets, "history": [*history, transition.relation_type], "current_node": target}
    payload.update(apply_effects(payload, {**transition.effects, "sets": sets}, model))
    verb = "Completed" if transition.terminal else "Advanced to"
    return TransitionResult(target, str(payload.get("status") or ""), True, False, f"{verb} {target} via {transition.relation_type}.", transition)


UPDATE_SEEDS = "deskops desk update --apply"


def _check_against_package(payload: dict[str, Any], transition: Transition, target: str) -> None:
    """Refuse an edge whose effect differs from the package's lifecycle table (b6).

    The ``TaskDoc`` validator checks the new state against ``lifecycle_table()``, the package's
    edges; the desk's edge is what ``advance`` applies. When the two differ (a desk seed older
    than CC31 has no ``attributes.sets``), the write would fail inside pydantic without naming
    the edge, so the edge is compared first: same ``relation_type``, same target, same
    ``sets.status``. The table is cached; no file is read here.
    """
    from deskops.models.task_lifecycle import lifecycle_table

    task_id = str(payload.get("id") or "")
    edge_file = f"{LIFECYCLE_DIR.as_posix()}/{transition.relation_doc or transition.relation_type}.md"
    head = f"Cannot advance {task_id} via {transition.relation_type}: the edge {edge_file}"
    tail = f" The desk's lifecycle seeds are out of date: run '{UPDATE_SEEDS}'."
    expected = lifecycle_table().edges.get(transition.relation_type)
    if expected is None:
        raise LifecycleSeedOutOfDate(f"{head} is not a transition of the deskops package lifecycle.{tail}")
    seen = transition.sets.get("status")
    if str(seen or "") != expected.status:
        shown = "missing" if seen in (None, "") else str(seen)
        raise LifecycleSeedOutOfDate(
            f"{head} does not set status {expected.status} (attributes.sets.status is {shown}).{tail}"
        )
    if target != expected.target:
        raise LifecycleSeedOutOfDate(f"{head} does not lead to {expected.target} (it leads to {target}).{tail}")


# ---------------------------------------------------------------- writing the graph
def seed_changes(root: Path, result: Any) -> list[str]:
    """What a desk scaffold did to the lifecycle graph: ``wrote <path>`` and ``rewrote <path>`` lines."""
    root = root.resolve()
    prefix = LIFECYCLE_DIR.as_posix() + "/"
    created = [path.resolve().relative_to(root).as_posix() for path in result.created_paths]
    rewritten = [path.resolve().relative_to(root).as_posix() for path in result.rewritten_paths]
    return [f"wrote {rel}" for rel in created if rel.startswith(prefix)] + [f"rewrote {rel}" for rel in rewritten]


def _ritual_paths(spec: LifecycleSpec) -> dict[str, str]:
    return {f"desk/rituals/{node.removeprefix('ritual-')}.md": node for node in spec.rituals}


def tracked_line(model: str, path: str, spec: LifecycleSpec | None = None) -> str | None:
    """The change line for a lifecycle document the declared includes tracked; None for any other."""
    if path.startswith(LIFECYCLE_DIR.as_posix() + "/"):
        return f"tracked {path}"
    ritual = _ritual_paths(spec or load_lifecycle_spec()).get(path)
    if model == RITUAL_MODEL and ritual:
        return f"tracked {path} as {ritual_export_id(ritual)}"
    return None


def ensure_rule_model(root: Path) -> bool:
    """Register sldb's ``RuleDoc`` in the desk's store when it lacks it (``sldb.api.add_model``);
    True when it was registered now. Tracking an activation rule needs the model, and each
    ``model <= <TypeDoc>`` of a rule's subject needs the type registered, which the deskops
    models always are."""
    from sldb.api import add_model
    from sldb.api import is_model_registered

    if is_model_registered(_store(root), RULE_MODEL):
        return False
    add_model(_store(root), RULE_MODEL_REF, pythonpath=package_pythonpath())
    return True


def write_lifecycle_graph(root: Path) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: writes the managed lifecycle seeds (the graph and the activation rules) and
    restores one the desk changed (``workspace.seed_desk``), registers sldb's relation models
    and ``RuleDoc`` when the store lacks them and tracks the declared desk documents
    (``workspace.apply_desk_includes``): the lifecycle documents and the lifecycle rituals by
    their ids. Any other declared document pending is tracked too and reported in the same way.
    """
    from sldb.api import init_relations
    from sldb.api import is_model_registered

    from deskops.workspace import apply_desk_includes
    from deskops.workspace import pending_desk_includes
    from deskops.workspace import seed_desk

    root = root.resolve()
    changes = seed_changes(root, seed_desk(root, restore_managed=True))
    if not all(is_model_registered(_store(root), name) for name in (RELATION_MODEL, RELATION_TYPE_MODEL)):
        init_relations(_store(root), pythonpath=package_pythonpath())
    ensure_rule_model(root)
    spec = load_lifecycle_spec()
    pending = {path: model for model, path in pending_desk_includes(root)}
    for path in apply_desk_includes(root):
        model = pending.get(path, "")
        changes.append(tracked_line(model, path, spec) or f"tracked {path} as {model}")
    return changes


# Alias de compatibilidad hacia atrás
ensure_lifecycle_graph = write_lifecycle_graph

FILE:deskops/services/tasks.py
"""Task lifecycle service: create, list, show, advance, next, and the task type registry.

TaskDoc reads go only through sldb's ``extract_model_data``; this service never
overlays a regex parse on top of the model. Document storage (read/write/track,
selector resolution, the task payload with its inherited context) is
``deskops.doc_access``; the lifecycle graph is ``deskops.lifecycle``.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops import lifecycle
from deskops.lifecycle import TransitionResult
from deskops.lifecycle_hooks import run_hooks
from deskops.models import BoardDoc
from deskops.models import PillDoc
from deskops.models import TaskDoc
from deskops.models.validation import validated
from deskops.models.task_types import TASK_TYPE_MODELS
from deskops.models.task_types import canonical_task_type_name
from deskops.runtime import Task
from deskops.specs import compile_task_spec
from deskops.workflow.next_actions import match_workflow_state
from deskops.workflow.next_actions import render_workflow_mermaid

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


@dataclass(slots=True)
class TaskBundle:
    task_id: str
    task_path: Path


def registered_task_types(root: Path) -> dict[str, type[Any]]:
    """task_type name -> model class: the factory types plus desk-local types in the store.

    A desk adds its own types as ``desk/models/*.py`` subclasses; ``desk update --apply``
    registers them with ``pythonpath`` = the desk root. Factory types are importable directly
    and are merged in first, so local modules never shadow them.
    """
    registry: dict[str, type[Any]] = dict(TASK_TYPE_MODELS)
    store_dir = root / ".sldb"
    if store_dir.exists():
        try:
            from sldb.api.model_registry.model_reference import resolve_model_ref

            from deskops.bootstrap import SLDBBootstrap

            entries = SLDBBootstrap()._registered_model_entries(store_dir)
            pythonpath = str(doc_access.desk_root(root))
            for name, entry in entries.items():
                if name in registry:
                    continue
                model_ref = getattr(entry, "model_ref", "") or ""
                if not model_ref:
                    continue
                try:
                    cls = resolve_model_ref(model_ref, pythonpath=pythonpath)
                except Exception:
                    continue
                if not isinstance(cls, type) or not issubclass(cls, TaskDoc):
                    continue
                field = cls.model_fields.get("task_type")
                default = getattr(field, "default", None)
                if default not in (None, ""):
                    registry[str(default)] = cls
        except Exception:
            pass
    return registry


class TasksService:
    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger
        self._task_type_registry: dict[str, type[Any]] | None = None

    def registered_task_types(self) -> dict[str, type[Any]]:
        """The task type registry of this desk, read once per service instance."""
        if self._task_type_registry is None:
            self._task_type_registry = registered_task_types(self.root)
        return self._task_type_registry

    # ---------------------------------------------------------------- create
    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        """Write one task and route it on the Board. Its lifecycle is the desk's graph
        (deskops/lifecycle.py), so nothing else is written per task."""
        doc_access.ensure_workspace(self.root)
        # A task's closeout evidence is declared by its type, not written into the task. The
        # task is stored under its type's model so `model <= TaskCodeDoc` finds it.
        raw_task_type = str(raw_payload.get("task_type") or "").strip()
        registry = self.registered_task_types()
        task_type = raw_task_type if raw_task_type in registry else canonical_task_type_name(raw_task_type)
        type_model = registry.get(task_type) or registry.get("task.code") or TaskDoc
        spec = lifecycle.load_lifecycle_spec()
        compiled = compile_task_spec({**raw_payload, "task_type": task_type}, entry_node=spec.entry_node)
        validated(type_model, compiled.task_payload)
        task_id = compiled.task_payload["id"]
        task_path = self._task_path(task_id)

        with doc_access.desk_transaction(self.root):
            doc_access.create_doc(self.root, task_path, type_model, compiled.task_payload, task_id)
            self._append_task_to_board(task_id)
        return TaskBundle(task_id=task_id, task_path=task_path)

    def _append_task_to_board(self, task_id: str) -> None:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_payload = doc_access.read_doc(board_path, BoardDoc)
        task_ref = f"desk/tasks/{task_id}.md"
        tasks = list(board_payload.get("tasks") or [])
        if task_ref not in tasks:
            tasks.append(task_ref)
            board_payload["tasks"] = tasks
            doc_access.write_doc(self.root, board_path, BoardDoc, board_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[doc_access.DocumentRecord, str, bool]:
        doc_access.ensure_workspace(self.root)
        task_path = doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        pill_path = doc_access.resolve_artifact_selector(self.root, "artifact.pill", self.desk_root / "contexts", pill_selector)
        task_payload = doc_access.read_doc(task_path, TaskDoc)
        doc_access.read_doc(pill_path, PillDoc)
        pill_ref = str(pill_path.relative_to(self.root))
        pills = list(task_payload.get("pills") or [])
        record = doc_access.DocumentRecord(kind="task", doc_id=str(task_payload.get("id", task_path.stem)), path=task_path)
        if pill_ref in pills:
            return record, pill_ref, False
        task_payload["pills"] = [*pills, pill_ref]
        doc_access.write_doc(self.root, task_path, TaskDoc, task_payload)
        return record, pill_ref, True

    # ---------------------------------------------------------------- read
    def list_tasks(self) -> list[Task]:
        task_dir = self.desk_root / "tasks"
        if not task_dir.exists():
            if not self.desk_root.exists():
                raise FileNotFoundError(f"Desk root not found at {self.desk_root}. Run 'deskops init' to initialize.")
            return []
        tasks: list[Task] = []
        for path in sorted(task_dir.glob("task-*.md")):
            try:
                tasks.append(doc_access.load_task(self.root, path.stem))
            except Exception as e:
                print(f"Warning: Failed to load task {path}: {e}", file=sys.stderr)
        return tasks

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        """The task and the lifecycle transitions leaving its current node, each with
        whether its condition holds now (empty when the graph is missing or the task is
        complete)."""
        try:
            task_path, payload, effective = self._ops.task_record(task_id)
        except FileNotFoundError:
            return None, []
        task = doc_access.hydrate_task(effective)
        return task, self._lifecycle_gates(task, task_path, payload)

    def _lifecycle_gates(self, task: Task, task_path: Path | None = None, payload: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        if not task.current_node or task.current_node == lifecycle.COMPLETE:
            return []
        try:
            transitions = lifecycle.transitions_from(self.root, task.current_node, snapshot=self._ops.snapshot)
        except Exception:
            return []
        if task_path is None or payload is None:
            task_path, payload, _ = self._ops.task_record(task.id)
        findings = self._transition_findings(task_path, payload)
        # An error finding of the task's on_transition rules holds every edge back (as
        # sldb's edges_holding does), so such a gate does not hold whatever its condition says.
        blocked = any(f.get("level") == "error" for f in findings)
        return [
            {
                "relation_type": t.relation_type,
                "target": lifecycle.COMPLETE if t.terminal else t.target,
                "condition": t.condition,
                "holds": not blocked and lifecycle.condition_holds(t.condition, payload),
                **({"hooks": t.hooks_listing()} if t.raw_hooks else {}),
                **({"findings": findings} if findings else {}),
            }
            for t in transitions
        ]

    def _transition_findings(self, task_path: Path, payload: dict[str, Any]) -> list[dict[str, Any]]:
        """The findings of the task's ``on_transition`` rules (sldb GO08): what blocks the gate
        leaving its node, as ``show`` and ``next`` print them; empty for an untracked task."""
        document = self._ops.task_document(task_path)
        if document is None:
            return []
        try:
            return lifecycle.transition_findings(self.root, document, payload, snapshot=self._ops.snapshot)
        except Exception:
            return []

    def _transition_hooks(self, node: str) -> dict[str, list[dict[str, Any]]]:
        """relation_type -> the post-hooks of each transition leaving ``node`` that declares any."""
        if not node or node == lifecycle.COMPLETE:
            return {}
        try:
            transitions = lifecycle.transitions_from(self.root, node, snapshot=self._ops.snapshot)
        except Exception:
            return {}
        return {t.relation_type: t.hooks_listing() for t in transitions if t.raw_hooks}

    def render_next_action_diagram(self) -> str:
        spec = lifecycle.load_lifecycle_spec()
        return render_workflow_mermaid(spec, lifecycle.lifecycle_transitions(self.root, spec))

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_ref = str(board_path.relative_to(self.root))
        if not task_selector:
            task_refs = list(doc_access.read_doc(board_path, BoardDoc).get("tasks") or [])
            if not task_refs:
                return {
                    "kind": "no_board_task",
                    "board": board_ref,
                    "suggested_commands": [
                        "deskops list tasks --root .",
                        "deskops promote inbox-to-drawer-task <selector> --root .",
                        'deskops add task --root . --title "..." ...',
                    ],
                }
            if len(task_refs) > 1:
                tasks = []
                for task_ref in task_refs:
                    path = self.root / str(task_ref)
                    payload = doc_access.read_doc(path, TaskDoc)
                    tasks.append(
                        {
                            "id": str(payload.get("id") or path.stem),
                            "status": str(payload.get("status") or ""),
                            "title": str(payload.get("title") or ""),
                        }
                    )
                return {
                    "kind": "multiple_board_tasks",
                    "board": board_ref,
                    "tasks": tasks,
                    "suggested_commands": [
                        "deskops next <task-id> --root .",
                        "deskops list tasks --root .",
                    ],
                }
        task_path = self._next_task_path(task_selector, board_path)
        payload = doc_access.resolve_task_payload(self.root, task_path.stem)
        spec = lifecycle.load_lifecycle_spec()
        state = match_workflow_state(spec, str(payload.get("current_node") or ""))
        findings = self._transition_findings(task_path, dict(payload)) if payload.get("current_node") else []
        hooks = self._transition_hooks(str(payload.get("current_node") or ""))
        pills = list(dict.fromkeys([*self._board_pills(board_path), *list(payload.get("effective_pills") or payload.get("pills") or [])]))
        sources = {
            "task": str(task_path.relative_to(self.root)),
            "board": str(board_path.relative_to(self.root)),
            "workflow": "deskops/spec/workflows/task_lifecycle.yaml",
        }
        why = [
            "task selected by explicit selector"
            if task_selector
            else "task selected from the single board route",
            f"current_node {payload.get('current_node', '')} matched workflow state {state['id']} in {sources['workflow']}",
            "pills merged from desk/tasks/Board.md and the task",
            f"source task: {sources['task']}",
            f"source board: {sources['board']}",
            f"source workflow: {sources['workflow']}",
        ]
        return {
            "task": {
                "id": payload["id"],
                "title": payload["title"],
                "status": payload["status"],
                "current_node": payload.get("current_node", ""),
                "task_type": payload.get("task_type", ""),
                "inherits_from": list(payload.get("inherits_from") or []),
            },
            "phase": state["phase"],
            "ritual": state.get("ritual", ""),
            "pills": pills,
            "next_actions": list(state.get("next_actions") or []),
            "advance_when": list(state.get("advance_when") or []),
            "findings": findings,
            **({"hooks": hooks} if hooks else {}),
            "why": why,
            "sources": sources,
        }

    # ---------------------------------------------------------------- advance
    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        try:
            task_path = doc_access.resolve_glob(self.root, self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return None, None
        payload = doc_access.read_doc(task_path, TaskDoc)
        before = copy.deepcopy(payload)

        current_node = str(payload.get("current_node") or "")
        current_status = str(payload.get("status") or "")
        # The edge's effects validate against the task type's model. A task whose task_type is
        # not a registered type (empty or legacy, what `desk update --apply` migrates) validates
        # against TaskDoc, the model it was read with: a typed model's `task_type` literal could
        # not accept it (d4, instead of k5's TaskCodeDoc).
        model = self.registered_task_types().get(str(payload.get("task_type") or "")) or TaskDoc
        result = lifecycle.advance(self.root, payload, model, document=lifecycle.task_document(self.root, task_path))
        if result.progressed and payload.get("current_node") == lifecycle.COMPLETE:
            # The lifecycle graph would close the task. Do not persist it; the
            # only closing entry point is `deskops closeout commit`.
            self.logger.info(f"Task {task_id} reached the closure gate; deferring to closeout commit.")
            restored = {**payload, "current_node": current_node, "status": current_status}
            return doc_access.hydrate_task(restored), self._closure_required(task_id, restored)
        advanced_task = doc_access.hydrate_task(payload)
        if result.progressed:
            doc_access.write_doc(self.root, task_path, TaskDoc, payload)
            transition = result.transition
            failure = (
                run_hooks(self.root, task_id, transition, str(payload.get("current_node") or ""), transition.hooks)
                if transition is not None
                else None
            )
            if failure is not None:
                # Only the task goes back (status, current_node, history); what a hook wrote elsewhere stays.
                doc_access.write_doc(self.root, task_path, TaskDoc, before)
                self.logger.info(f"Hook {failure.hook} failed advancing task {task_id}; the task is back at {current_node}")
                message = failure.finding(transition.relation_type)
                return doc_access.hydrate_task(before), TransitionResult(current_node, current_status, False, True, message)
        self.logger.info(f"Advanced task {task_id} to node {payload.get('current_node')}")
        return advanced_task, result

    @staticmethod
    def _closure_required(task_id: str, payload: dict[str, Any]) -> TransitionResult:
        node = str(payload.get("current_node") or "")
        status = str(payload.get("status") or "")
        message = (
            f"Task {task_id} closes with 'deskops closeout commit --task {task_id} "
            f"--run-dir <runs/subagents/dir>' or 'deskops closeout commit --task {task_id} "
            f"--no-run --reason <why>'."
        )
        return TransitionResult(node, status, False, True, message)

    # ---------------------------------------------------------------- paths
    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _next_task_path(self, task_selector: str | None, board_path: Path) -> Path:
        if task_selector:
            return doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        board_payload = doc_access.read_doc(board_path, BoardDoc)
        task_refs = list(board_payload.get("tasks") or [])
        if not task_refs:
            raise FileNotFoundError("No active tasks routed by desk/tasks/Board.md")
        if len(task_refs) > 1:
            raise ValueError("Multiple active tasks are routed; pass a task selector")
        return self.root / str(task_refs[0])

    def _board_pills(self, board_path: Path) -> list[str]:
        try:
            board_payload = doc_access.read_doc(board_path, BoardDoc)
        except Exception:
            return []
        return [str(pill) for pill in board_payload.get("pills") or []]

FILE:deskops/runtime/scion.py
"""Project a RoleDoc + its RuntimeProfileDoc onto a Scion agent template.

Scion (github.com/GoogleCloudPlatform/scion) launches an agent from a
*template* directory: ``scion-agent.yaml`` plus the prose files it points at
(``system-prompt.md``, ``agents.md``). A template describes the job, never the
environment: the harness-config decides image, auth and concrete model, and
the template only carries a portable model *size alias*.

This module is the Scion counterpart of ``materializers.roles`` (pi agent
files): the RoleDoc stays the tracked source and the template is a
materialization. Pure except for the two writers at the bottom; it never
calls ``scion``. Dispatch (``scion start``) is the supervisor's gesture.

Nothing is dropped silently: every RoleDoc setting the template cannot carry
is written into ``scion-agent.yaml`` as a comment that names the setting and
why it was left out.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

from sldb.runtime.validation import extract_model_data
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.hashing import hash_fields_with_map

from deskops import doc_access
from deskops.materializers.roles import iter_role_doc_paths, load_role_doc
from deskops.materializers.runtime_profiles import build_agent_spec_args, load_runtime_profiles
from deskops.models import RunDoc, TaskDoc

#: RuntimeProfileDoc.kind -> Scion harness-config name. Only ``claude`` and
#: ``gemini`` ship installed; the rest need ``scion harness-config install``
#: (``pi`` needs a bundle of our own; see the scion fork's desk).
HARNESS_BY_KIND: dict[str, str] = {
    "claude": "claude",
    "codex": "codex",
    "antigravity": "antigravity",
    "gemini": "gemini",
    "opencode": "opencode",
    "pi": "pi",
}

#: Scion's portable model size aliases (``local/templates.md``).
MODEL_SIZE_ALIASES: tuple[str, ...] = ("small", "medium", "large", "extra-large")

#: ``medium`` by default: the owner's rule is that subagents never run on the
#: largest tier. Pass ``model_alias`` to change it per template.
DEFAULT_MODEL_ALIAS = "medium"
DEFAULT_MAX_TURNS = 200
DEFAULT_MAX_DURATION = "2h"
#: A coordinator waits blocked on its children and Scion counts that idle time,
#: so the executor's limit would kill it mid-review.
COORDINATOR_MAX_TURNS = 1000
COORDINATOR_MAX_DURATION = "24h"

#: Without this the Hub picks whichever credential it finds; a stale
#: ``CLAUDE_AUTH`` file beats a project token and the agent is not logged in.
HARNESS_AUTH: dict[str, str] = {"claude": "oauth-token"}

#: Auth a ``scion start`` names when nobody chose one: the same default the
#: claude template carries, so a coordinator never launches a subscription
#: child with ``api-key`` (it would ask for ANTHROPIC_API_KEY and not start).
DEFAULT_HARNESS_AUTH = HARNESS_AUTH["claude"]

#: Auth types a template may select (``auth_selectedType``); the harness-config
#: decides which secrets each one needs (claude: oauth-token ->
#: CLAUDE_CODE_OAUTH_TOKEN, auth-file -> the CLAUDE_AUTH credentials file).
HARNESS_AUTH_TYPES: tuple[str, ...] = ("api-key", "oauth-token", "auth-file", "vertex-ai")

TEMPLATE_FILES: tuple[str, ...] = ("scion-agent.yaml", "system-prompt.md", "agents.md")

#: The only keys a Scion runtime context may carry. Paths are absolute and inside
#: ``workspace_root``; ``project`` is the Scion project slug or UUID, never a path.
SCION_CONTEXT_KEYS: tuple[str, ...] = ("project", "workspace_root", "desk_root", "source_root", "sldb_root")

#: Optional container keys: how this machine runs the agent, not where the desk is.
#: ``memory_limit``/``cpu_limit`` become ``resources.limits``; ``shared_paths`` are host
#: paths bound at the same path (e.g. ``/dev/shm``, so tests share the host's tmpfs and
#: its lock files); ``env`` adds static variables (e.g. ``TMPDIR``). Omitted: no change.
SCION_CONTEXT_OPTIONAL_KEYS: tuple[str, ...] = ("memory_limit", "cpu_limit", "shared_paths", "env")

_PROJECT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_MEMORY_RE = re.compile(r"^[0-9]+(\.[0-9]+)?([KMGT]i?)?$")
_CPU_RE = re.compile(r"^[0-9]+(\.[0-9]+)?$")
_ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
#: Variables the context already derives; ``env`` may not redefine them.
_DERIVED_ENV = frozenset(
    {"DESKOPS_DESK_ROOT", "DESKOPS_SOURCE_ROOT", "DESKOPS_SLDB_SOURCE_ROOT", "DESKOPS_WORKSPACE_ROOT",
     "DESKOPS_SCION_PROJECT", "PYTHONPATH"}
)


def _context_absolute_path(key: str, value: object) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"context {key} must be a non-empty absolute path")
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ValueError(f"context {key} must be an absolute path, got '{value}'")
    return path.resolve()


def _validate_container_keys(context: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    """The optional container keys, validated; absent keys are left out."""
    resolved: dict[str, Any] = {}
    if "memory_limit" in context:
        value = context["memory_limit"]
        if not isinstance(value, str) or _MEMORY_RE.fullmatch(value.strip()) is None:
            raise ValueError(f"context memory_limit must be a size such as '6Gi' or '6G', got {value!r}")
        resolved["memory_limit"] = value.strip()
    if "cpu_limit" in context:
        value = context["cpu_limit"]
        if not isinstance(value, str) or _CPU_RE.fullmatch(value.strip()) is None or float(value) <= 0:
            raise ValueError(f"context cpu_limit must be a positive number of cores as a string, got {value!r}")
        resolved["cpu_limit"] = value.strip()
    if "shared_paths" in context:
        value = context["shared_paths"]
        if not isinstance(value, list):
            raise ValueError("context shared_paths must be a list of absolute host paths")
        paths: list[str] = []
        for item in value:
            path = _context_absolute_path("shared_paths", item)
            if not path.exists():
                raise ValueError(f"context shared_paths entry does not exist on this host: {path}")
            if path == workspace_root:
                raise ValueError(f"context shared_paths must not repeat workspace_root: {path}")
            if str(path) not in paths:
                paths.append(str(path))
        resolved["shared_paths"] = paths
    if "env" in context:
        value = context["env"]
        if not isinstance(value, dict):
            raise ValueError("context env must be an object of NAME: value strings")
        env: dict[str, str] = {}
        for name, item in value.items():
            if not isinstance(name, str) or _ENV_NAME_RE.fullmatch(name) is None:
                raise ValueError(f"context env name is not a valid variable name: {name!r}")
            if name in _DERIVED_ENV:
                raise ValueError(f"context env must not redefine {name}; the context derives it")
            if not isinstance(item, str):
                raise ValueError(f"context env {name} must be a string")
            env[name] = item
        resolved["env"] = env
    return resolved


def validate_scion_context(context: dict[str, Any]) -> dict[str, Any]:
    """Validate the five-key runtime context before any template output is written.

    ``project`` is a non-empty Scion slug or UUID. Every other value is an
    absolute directory: ``workspace_root`` contains the rest, ``desk_root``
    contains ``desk/``, ``source_root`` contains the ``deskops`` package and
    ``sldb_root`` is sldb's ``src`` directory. Missing, unknown, relative,
    outside-workspace or invalid paths are refused with no partial defaults.
    """
    if not isinstance(context, dict):
        raise ValueError("Scion context must be a JSON object")
    missing = [key for key in SCION_CONTEXT_KEYS if key not in context]
    unknown = sorted(
        str(key) for key in context if key not in SCION_CONTEXT_KEYS and key not in SCION_CONTEXT_OPTIONAL_KEYS
    )
    if missing:
        raise ValueError(f"Scion context is missing required key(s): {', '.join(missing)}")
    if unknown:
        raise ValueError(f"Scion context has unknown key(s): {', '.join(unknown)}")

    project = context["project"]
    if not isinstance(project, str) or not project.strip():
        raise ValueError("context project must be a non-empty Scion slug or UUID")
    project = project.strip()
    if "/" in project or "\\" in project or project in {".", ".."} or _PROJECT_RE.fullmatch(project) is None:
        raise ValueError(f"context project must be a Scion slug or UUID, not a filesystem path: '{project}'")

    workspace_root = _context_absolute_path("workspace_root", context["workspace_root"])
    if not workspace_root.is_dir():
        raise ValueError(f"context workspace_root is not a directory: {workspace_root}")
    resolved: dict[str, Any] = {"project": project, "workspace_root": str(workspace_root)}
    for key in SCION_CONTEXT_KEYS[2:]:
        path = _context_absolute_path(key, context[key])
        try:
            path.relative_to(workspace_root)
        except ValueError as exc:
            raise ValueError(f"context {key} must be inside workspace_root ({workspace_root}): {path}") from exc
        resolved[key] = str(path)

    if not (Path(resolved["desk_root"]) / "desk").is_dir():
        raise ValueError(f"context desk_root must be the repository root containing desk/: {resolved['desk_root']}")
    if not (Path(resolved["source_root"]) / "deskops").is_dir():
        raise ValueError(f"context source_root must be the repository root containing the deskops package: {resolved['source_root']}")
    if not (Path(resolved["sldb_root"]) / "sldb").is_dir():
        raise ValueError(f"context sldb_root must be the sldb src directory containing the sldb package: {resolved['sldb_root']}")
    resolved.update(_validate_container_keys(context, workspace_root))
    return resolved


def load_scion_context(path: Path) -> dict[str, Any]:
    """Read and validate a JSON context file; nothing is generated before this succeeds."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read Scion context file {path}: {exc}") from exc
    return validate_scion_context(raw)


def task_contract_sha256(markdown: str) -> str:
    """The SLDB ``__contract__`` digest of a task document (no local hash recipe)."""
    try:
        _, field_hashes = hash_fields_with_map(TaskDoc, markdown)
        return contract_hash(TaskDoc, field_hashes)
    except Exception as exc:  # noqa: BLE001 - surface the model's own diagnostic
        raise ValueError(f"cannot read the task contract: {exc}") from exc


def _scion_task_label(task_id: str) -> str:
    """Bound native metadata without altering the canonical task identity."""
    if len(task_id) <= 63 and all(0x20 <= ord(char) <= 0x7E for char in task_id):
        return task_id
    return "t-" + hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:61]


def scion_child_identity(task_path: str | Path, role: str, attempt: int = 1) -> dict[str, Any]:
    """Deterministic Scion child name and labels for one task contract and role.

    Status, history and references never move the identity; the SLDB task
    ``__contract__`` digest does, so a goal/scope/files/validation change does.
    Attempt is exactly 1 or 2: attempt 2 appends ``-a2`` and a third attempt is
    refused. This helper derives identity only; it does not start anything.
    """
    role_name = str(role).strip().lower()
    if role_name not in {"executor", "tester", "specialist"}:
        raise ValueError(f"role must be executor, tester or specialist, got '{role}'")
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt not in {1, 2}:
        raise ValueError(f"attempt must be 1 or 2, got {attempt!r}")

    path = Path(task_path)
    try:
        markdown = path.read_text(encoding="utf-8")
        task_id = str(extract_model_data(TaskDoc, markdown)["id"])
    except Exception as exc:  # noqa: BLE001 - one diagnostic for an unreadable task
        raise ValueError(f"cannot read task {path}: {exc}") from exc
    contract_sha256 = task_contract_sha256(markdown)
    digest = hashlib.sha256(f"{task_id}\0{contract_sha256}\0{role_name}".encode("utf-8")).hexdigest()[:12]
    prefix = {"executor": "deskops-e", "tester": "deskops-t", "specialist": "deskops-s"}[role_name]
    name = f"{prefix}-{digest}" + ("-a2" if attempt == 2 else "")
    return {
        "name": name,
        "task_id": task_id,
        "contract_sha256": contract_sha256,
        "role": role_name,
        "attempt": attempt,
        "labels": {
            "deskops.task_id": _scion_task_label(task_id),
            "deskops.contract_sha256": contract_sha256[:63],
            "deskops.role": role_name,
            "deskops.attempt": str(attempt),
        },
    }


def scion_start_argv(
    identity: dict[str, Any],
    *,
    prompt: str,
    project: str,
    workspace: str,
    template: str,
    harness_auth: str | None = DEFAULT_HARNESS_AUTH,
) -> list[str]:
    """The explicit native Scion start argv for one deterministic child identity.

    ``harness_auth`` is the auth the child's template selects (``auth_selectedType``);
    by default ``oauth-token``, the claude template default. ``None`` leaves
    ``--harness-auth`` out so the child's template decides alone.
    """
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if harness_auth is not None and harness_auth not in HARNESS_AUTH_TYPES:
        raise ValueError(f"harness auth must be one of {HARNESS_AUTH_TYPES}, got '{harness_auth}'")
    argv = [
        "scion",
        "start",
        str(identity["name"]),
        prompt,
        "--type",
        template,
        "--project",
        project,
        "--workspace",
        workspace,
        *(["--harness-auth", harness_auth] if harness_auth is not None else []),
        "--non-interactive",
    ]
    for key, value in (identity.get("labels") or {}).items():
        argv += ["--label", f"{key}={value}"]
    return argv


def pick_harness_config(runtime_kind: str) -> str:
    """Scion harness-config name for a RuntimeProfileDoc kind."""
    try:
        return HARNESS_BY_KIND[runtime_kind]
    except KeyError as exc:
        known = ", ".join(sorted(HARNESS_BY_KIND))
        raise ValueError(f"no Scion harness-config is known for runtime kind '{runtime_kind}' (known: {known})") from exc


def find_role_doc(root: Path, role_id: str) -> tuple[Path, dict[str, Any]]:
    """Locate a tracked RoleDoc by ``id`` or ``name`` (``role-x`` and ``x`` both resolve)."""
    wanted = {role_id, f"role-{role_id}"}
    for path in iter_role_doc_paths(root):
        role_doc = load_role_doc(path)
        if role_doc.get("id") in wanted or role_doc.get("name") in wanted:
            return path, role_doc
    raise ValueError(f"no RoleDoc with id or name '{role_id}' under {root / 'desk' / 'roles'}")


def template_dir_for(root: Path, role_doc: dict[str, Any], out_dir: Path | None = None) -> Path:
    """Default destination: ``<root>/.scion/templates/<role-name>/`` (a Scion project template)."""
    if out_dir is not None:
        return out_dir
    name = str(role_doc.get("name") or role_doc.get("id") or "").strip()
    if not name:
        raise ValueError("Role doc is missing a name")
    return root / ".scion" / "templates" / name


def _yaml_scalar(value: Any) -> str:
    """One-line YAML for a scalar or list: JSON is a YAML subset, and it never wraps."""
    return json.dumps(value, ensure_ascii=False)


def _command_args(role_doc: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    """Role settings that only exist as CLI flags (today: ``tools``).

    Model and system prompt have template fields of their own, the session is
    Scion's, and the profile's ``extra_args`` describe a non-interactive
    invocation (``--print``) that Scion must not inherit. What is left is the
    tools vocabulary, folded through the profile's own flag.
    """
    stripped = dict(profile)
    stripped.update(model_flag="", fallback_models_flag="", system_prompt_flag="", session_flag="", extra_args=[])
    args = list(build_agent_spec_args(role_doc, stripped))
    # Scion puts the task prompt (and more options) after command_args. A variadic
    # flag such as Claude's ``--allowedTools <tools...>`` would swallow the prompt as
    # one more tool, so every flag/value pair is emitted as a single ``flag=value``.
    return [f"{flag}={value}" for flag, value in zip(args[::2], args[1::2], strict=True)]


def scion_template_files(
    role_doc: dict[str, Any],
    profile: dict[str, Any],
    *,
    harness: str,
    model_alias: str = DEFAULT_MODEL_ALIAS,
    task_repo: str | None = None,
    source: str | None = None,
    mode: str | None = None,
    context: dict[str, Any] | None = None,
    harness_auth: str | None = None,
) -> dict[str, str]:
    """Render the three template files as ``{filename: text}``.

    ``source`` is a human-readable provenance line (role path + runtime path)
    written at the top of ``scion-agent.yaml``. ``mode`` picks the
    ``agents.md``: ``executor`` (one bounded task), ``tester`` (independent
    verification), ``specialist`` (leaves the sldb store clean) or ``coordinator`` (owns a desk); by default the selected
    role's own name/id decides, and an explicit mode always wins.

    ``context`` is the optional five-key Scion runtime context. Omitted, the
    CLI and path/environment behavior is preserved; the generated prompt text is
    corrected intentionally rather than kept byte-identical. Supplied, it adds
    the DESKOPS_* environment, a workspace volume and concrete command paths.
    """
    if mode not in (None, "executor", "coordinator", "tester", "specialist"):
        raise ValueError(f"mode must be executor, coordinator, tester or specialist, got '{mode}'")
    if harness_auth is not None and harness_auth not in HARNESS_AUTH_TYPES:
        raise ValueError(f"harness auth must be one of {HARNESS_AUTH_TYPES}, got '{harness_auth}'")
    if model_alias not in MODEL_SIZE_ALIASES:
        raise ValueError(f"model alias must be one of {MODEL_SIZE_ALIASES}, got '{model_alias}'")
    if harness not in HARNESS_BY_KIND.values():
        raise ValueError(f"unknown Scion harness-config '{harness}' (known: {', '.join(sorted(set(HARNESS_BY_KIND.values())))})")

    runtime_context = validate_scion_context(context) if context is not None else None

    role_name = str(role_doc.get("name") or role_doc.get("id") or "role")
    role_id = str(role_doc.get("id") or "")
    if mode:
        resolved_mode = mode
    elif role_name.endswith("-tester") or role_id.endswith("-tester"):
        resolved_mode = "tester"
    elif role_name.endswith("-specialist") or role_id.endswith("-specialist"):
        resolved_mode = "specialist"
    elif (
        "supervisor" in role_name
        or "coordinator" in role_name
        or "supervisor" in role_id
        or "coordinator" in role_id
    ):
        resolved_mode = "coordinator"
    else:
        resolved_mode = "executor"
    description = str(role_doc.get("description") or "").strip()
    body = str(role_doc.get("body") or "").strip()
    unsupported = set(profile.get("unsupported_role_fields") or [])

    lines: list[str] = []
    lines.append(f"# Generated by `deskops runtime template {role_doc.get('id') or role_name} --harness {harness}`.")
    if source:
        lines.append(f"# Source: {source}")
    lines.append("# Edit the RoleDoc / RuntimeProfileDoc and regenerate; do not edit this file by hand.")
    lines.append('schema_version: "1"')
    lines.append(f"description: {_yaml_scalar(description or role_name)}")
    lines.append("agent_instructions: agents.md")
    lines.append("system_prompt: system-prompt.md")
    lines.append(f"default_harness_config: {harness}")

    concrete_model = role_doc.get("model")
    if concrete_model:
        lines.append(
            f"# RoleDoc.model is {_yaml_scalar(concrete_model)}. A template carries a portable size alias; "
            f"the harness-config '{harness}' resolves it to a concrete model (Scion local/templates.md)."
        )
    lines.append(f"model: {model_alias}")
    auth_type = harness_auth or HARNESS_AUTH.get(harness)
    if auth_type:
        lines.append(f"auth_selectedType: {auth_type}")
    coordinator = resolved_mode == "coordinator"
    lines.append(f"max_turns: {COORDINATOR_MAX_TURNS if coordinator else DEFAULT_MAX_TURNS}")
    lines.append(f"max_duration: {COORDINATOR_MAX_DURATION if coordinator else DEFAULT_MAX_DURATION}")

    command_args = _command_args(role_doc, profile)
    if command_args:
        lines.append("# RoleDoc.tools, folded through the runtime profile's tools flag:")
        lines.append(f"command_args: {_yaml_scalar(command_args)}")

    if runtime_context is not None:
        lines.append("# Runtime context from --context-file (absolute paths, no secrets):")
        lines.append("env:")
        for key, value in (
            ("DESKOPS_DESK_ROOT", runtime_context["desk_root"]),
            ("DESKOPS_SOURCE_ROOT", runtime_context["source_root"]),
            ("DESKOPS_SLDB_SOURCE_ROOT", runtime_context["sldb_root"]),
            ("DESKOPS_WORKSPACE_ROOT", runtime_context["workspace_root"]),
            ("DESKOPS_SCION_PROJECT", runtime_context["project"]),
            ("PYTHONPATH", runtime_context["source_root"] + os.pathsep + runtime_context["sldb_root"]),
        ):
            lines.append(f"  {key}: {_yaml_scalar(value)}")
        for key, value in (runtime_context.get("env") or {}).items():
            lines.append(f"  {key}: {_yaml_scalar(value)}")
        lines.append("volumes:")
        for path in (runtime_context["workspace_root"], *(runtime_context.get("shared_paths") or [])):
            lines.append(f"  - source: {_yaml_scalar(path)}")
            lines.append(f"    target: {_yaml_scalar(path)}")
        limits = [(key, runtime_context[f"{key}_limit"]) for key in ("cpu", "memory") if runtime_context.get(f"{key}_limit")]
        if limits:
            lines.append("resources:")
            lines.append("  limits:")
            lines.extend(f"    {key}: {_yaml_scalar(value)}" for key, value in limits)

    omitted: list[str] = []
    fallback_models = role_doc.get("fallback_models") or []
    if fallback_models:
        reason = (
            f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' lists it in unsupported_role_fields"
            if "fallback_models" in unsupported
            else "a Scion template has no field for it"
        )
        omitted.append(f"fallback_models: {_yaml_scalar(list(fallback_models))}  ({reason})")
    tools = role_doc.get("tools") or []
    if tools and not command_args:
        reason = (
            f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' lists it in unsupported_role_fields"
            if "tools" in unsupported
            else f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' declares no tools_flag"
        )
        omitted.append(f"tools: {_yaml_scalar(list(tools))}  ({reason})")
    for key in ("system_prompt_mode", "inherit_project_context", "inherit_skills", "default_context"):
        if key in role_doc and role_doc.get(key) not in (None, ""):
            omitted.append(f"{key}: {_yaml_scalar(role_doc[key])}  (pi agent setting; Scion templates have no equivalent)")
    if omitted:
        lines.append("# Omitted on purpose (nothing is dropped silently):")
        lines.extend(f"#   {item}" for item in omitted)

    agent_yaml = "\n".join(lines) + "\n"
    system_prompt = (body or f"# {role_name}") + "\n"
    if resolved_mode == "coordinator":
        agents_md = _render_coordinator_agents_md(
            role_name, harness, task_repo, runtime_context, child_auth=auth_type or DEFAULT_HARNESS_AUTH
        )
    elif resolved_mode == "tester":
        agents_md = _render_tester_agents_md(role_name, harness, task_repo, runtime_context)
    elif resolved_mode == "specialist":
        agents_md = _render_specialist_agents_md(role_name, harness, task_repo, runtime_context)
    else:
        agents_md = _render_agents_md(role_name, harness, task_repo, runtime_context)
    return {"scion-agent.yaml": agent_yaml, "system-prompt.md": system_prompt, "agents.md": agents_md}


def _example_roots(task_repo: str | None, context: dict[str, str] | None) -> tuple[str, str, str, str]:
    """(workspace, desk_root, source_root, project) for generated command examples."""
    if context is not None:
        return context["workspace_root"], context["desk_root"], context["source_root"], context["project"]
    repo = task_repo or "<repo>"
    return "/workspace", f"/workspace/{repo}", "/workspace/deskops", "<project>"


def _render_coordinator_agents_md(
    role_name: str,
    harness: str,
    task_repo: str | None,
    context: dict[str, str] | None,
    *,
    child_auth: str = DEFAULT_HARNESS_AUTH,
) -> str:
    """Instructions for the long-lived agent that owns one desk.

    ``child_auth`` is the ``--harness-auth`` its ``scion start`` examples name:
    the auth this coordinator's own template selected, ``oauth-token`` by default.

    One coordinator per desk is the shape the owner chose (2026-10-29). It
    mutates modeled workflow state through the CLIs, never implements code,
    dispatches one executor/tester at a time and reconciles before acting.
    """
    repo = task_repo or "<repo>"
    workspace, desk_root, source_root, project = _example_roots(task_repo, context)
    sldb_root = str((context or {}).get("sldb_root", "<sldb_root>"))
    return (
        f"# {role_name}: coordinator of the `{repo}` desk on Scion ({harness})\n"
        "\n"
        "You are the long-lived coordinator of ONE desk. The desk, not your memory, holds the state; every time you\n"
        "wake up, recover the configured current state again. You are the only agent that writes this desk's\n"
        "workflow documents, and you do that with the CLIs, never by editing source code.\n"
        "\n"
        "## Configured current state\n"
        "\n"
        "Use the absolute roots supplied by the template environment; do not infer them from the current cwd.\n"
        "Run implementation and validation commands from the actual desk_root, not from a descriptive repo alias.\n"
        "The source and sldb roots are tool import locations, not task write locations.\n"
        "\n"
        "```bash\n"
        f"cd {desk_root}\n"
        f"deskops show board Board --root {desk_root}\n"
        f"deskops list tasks --root {desk_root}\n"
        f"deskops message list --root {desk_root}\n"
        "git status --short --branch\n"
        f"scion list --project {project} --format json\n"
        "```\n"
        "\n"
        f"The source checkout is `{source_root}`; the sldb source is `{sldb_root}`.\n"
        "A stale, dirty or unreadable state is a finding to report, not a reason to guess.\n"
        "\n"
        "## Each cycle\n"
        "\n"
        "1. **Reconcile ownership first.** Inspect existing executor/tester lanes by exact project, name and labels,\n"
        "   and read their RunDoc and handoff evidence. Distinguish Scion activity from phase: activity=completed\n"
        "   with phase=running means the child completed, so inspect activity=completed first and use phase only as\n"
        "   fallback (Scion v0.2.21 uses activity first). Reconcile your OWN completed or stopped lane before\n"
        "   selecting anything; a restart or successful child completion must not skip your own task or launch a\n"
        "   duplicate. Skip only tasks owned elsewhere. A conflicting owner blocks that task only; unknown or\n"
        "   unavailable Scion state is recorded as a blocker.\n"
        "2. **Select and prepare one leaf.** After reconciling your own lanes, select one dependency-ready unowned\n"
        "   leaf from Board order (the only deterministic tie-breaker). If its preflight or bundle receipt is missing,\n"
        "   run the existing cheap context-review CLI/ritual and adjudicate factual findings: this is routine\n"
        "   coordinator work, not a human blocker. Do not implement until the execution gates pass.\n"
        "3. **Derive identity before dispatch.** For role `executor` or `tester`, compute the child name as\n"
        "   `deskops-e-<12hex>` or `deskops-t-<12hex>`, where the 12 hex are SHA256 of\n"
        "   `task_id + NUL + contract_sha256 + NUL + role`. `contract_sha256` is the SLDB TaskDoc `__contract__`\n"
        "   digest, not a raw file hash. Attempt 1 uses the base name; attempt 2 appends `-a2`; there is no attempt 3.\n"
        "   Labels are `deskops.task_id`, `deskops.contract_sha256`, `deskops.role`, `deskops.attempt`. The runtime\n"
        "   helper `scion_child_identity(task_path, role, attempt)` returns this name and label set.\n"
        "   Copy the helper labels exactly: native values must be printable ASCII and at most 63 characters.\n"
        "   The contract label is the 63-hex prefix; invalid/long task-id labels use a bounded hash descriptor.\n"
        "   Full task id and full canonical contract hash remain in TaskDoc/RunDoc and name derivation; never\n"
        "   paste the full 64-hex hash as a native label or change the canonical contract to fit labels.\n"
        "4. **Reuse or write intent, then start.** A matching RunDoc is reused without rewriting it; only a missing\n"
        "   intent calls the runtime template to create the in_progress RunDoc. Its summary says launch intent, not\n"
        "   proof of start. Write that intent before the native Scion start; a retry gets a new run_dir. Never\n"
        "   overwrite a previous attempt's RunDoc or evidence. One executor or tester per repository at a time.\n"
        "5. **Dispatch the executor.** Build the prompt from `deskops show task <id> --root <desk_root>`: task id and\n"
        "   contract, repository, exact scope, validation, evidence, assigned run_dir/attempt and prohibitions. Tell the executor to run\n"
        f"   implementation and validation from `{desk_root}`. The executor implements one bounded task and does not\n"
        "   close it. Template artifacts and evidence stay under the assigned desk runs directory, never /tmp:\n"
        "\n"
        "```bash\n"
        f"RUN_DIR={desk_root}/runs/subagents/<run>\n"
        f"deskops runtime template role-deskops-executor --root {source_root} --out \"$RUN_DIR/scion-template\" \\\n"
        f"  --mode executor --task <task-id> --agent deskops-e-<12hex> --task-root {desk_root} --run-dir runs/subagents/<run>\n"
        f"scion start deskops-e-<12hex> \"<task prompt>\" --type deskops-executor --project {project} \\\n"
        f"  --workspace {workspace} --harness-auth {child_auth} --non-interactive \\\n"
        "  --label deskops.task_id=<helper-task-label> --label deskops.contract_sha256=<helper-contract-label> \\\n"
        "  --label deskops.role=executor --label deskops.attempt=1\n"
        f"sciontool status blocked \"waiting on deskops-e-<12hex>\"\n"
        "```\n"
        "\n"
        "   One executor per repository at a time; different repositories may run in parallel.\n"
        "   The executor itself runs `deskops advance task` on its task once its evidence is written; you do not\n"
        "   advance that transition. If it signalled `blocked` with an `advance` finding or a failed post-hook,\n"
        "   the task is back at its previous node: read the finding and the hook log it names, and decide the retry.\n"
        "6. **Test independently.** When activity=completed, verify that the executor's advance happened with\n"
        f"   `deskops show task <id> --root {desk_root}` (status and current_node changed) and inspect its handoff\n"
        "   before testing. Dispatch a\n"
        "   fresh tester with role-deskops-tester, `--mode tester`, its own `deskops-t-<12hex>` identity and a run dir\n"
        f"   ending in `-testing`. Tell it to run validation from `{desk_root}`. The tester proves the contract and\n"
        "   guardrails; it does not implement or close.\n"
        "\n"
        "```bash\n"
        f"TEST_RUN={desk_root}/runs/subagents/<run>-testing\n"
        f"deskops runtime template role-deskops-tester --root {source_root} --out \"$TEST_RUN/scion-template\" \\\n"
        f"  --mode tester --task <task-id> --agent deskops-t-<12hex> --task-root {desk_root} --run-dir runs/subagents/<run>-testing\n"
        f"scion start deskops-t-<12hex> \"<test prompt>\" --type deskops-tester --project {project} \\\n"
        f"  --workspace {workspace} --harness-auth {child_auth} --non-interactive \\\n"
        "  --label deskops.task_id=<helper-task-label> --label deskops.contract_sha256=<helper-contract-label> \\\n"
        "  --label deskops.role=tester --label deskops.attempt=1\n"
        "```\n"
        "\n"
        "7. **Close explicitly and continue.** Review the evidence and diff, then run\n"
        f"   `deskops closeout verify --task <id> --root {desk_root}` and\n"
        f"   `deskops closeout commit --task <id> --run-dir <run> --paths <scoped implementation, evidence and review paths> --root {desk_root}`.\n"
        "   Never use `git add -A` or stage unrelated work. A failed tester cannot support closeout: request one\n"
        "   bounded correction and a fresh test, preserving the failure evidence, with at most two\n"
        "   implementation/test cycles per task contract. Reconcile the phase, then reconcile ownership and select again.\n"
        f"   Stop each completed child with `scion stop <name> --project {project}`. Do not push.\n"
        "\n"
        "## Bounds and human decisions\n"
        "\n"
        "- Never rerun an accepted review with unchanged input. Bound technical retries to 2 attempts per unchanged\n"
        "  input and report the exact blocker instead of looping broadly.\n"
        "- Answer ordinary factual and implementation questions from the task and source evidence; do not\n"
        "  blanket-surface every question. Escalate only unresolved owner decisions, real ownership conflicts,\n"
        "  external credentials/permissions, or genuine human decisions.\n"
        "- Waiting for a child uses Scion activity/completion notifications (already subscribed); do not poll in a\n"
        "  loop. Only a genuine human decision uses `sciontool status ask_user \"<question>\"`.\n"
        "\n"
        "## Completion\n"
        "\n"
        "- Only after all authorized work is closed, declared evidence verified and required phase integration/commit\n"
        "  done, write the final evidence summary and call `sciontool status task_completed \"<one-line summary>\"`.\n"
        "- If externally blocked, persist the exact blocker and signal `sciontool status blocked \"<blocker>\"`.\n"
        "- Only an actual owner decision uses `ask_user`.\n"
        "\n"
        "## Never\n"
        "\n"
        "- Never implement code, edit source files or hand-edit a tracked desk document; use `deskops` / `sldb` CLIs\n"
        "  for modeled workflow mutations (`--help` first).\n"
        f"- Never write outside `{workspace}` except `runs/` evidence inside the configured desk root.\n"
        "- Never duplicate a running or completed child, create attempt 3, or overwrite prior RunDoc evidence.\n"
        "- Never decide for the owner: releases, policy, model design, anything a note marks as theirs.\n"
    )


def _render_tester_agents_md(
    role_name: str,
    harness: str,
    task_repo: str | None,
    context: dict[str, str] | None,
) -> str:
    """Independent verification instructions, intentionally separate from the executor."""
    _workspace, desk_root, source_root, project = _example_roots(task_repo, context)
    repo_line = (
        f"- Your task lives in the repository at `{desk_root}` (`{task_repo}` is descriptive only)."
        if task_repo
        else f"- Your task lives in the repository at `{desk_root}`."
    )
    return (
        f"# {role_name}: independent tester on Scion ({harness})\n"
        "\n"
        "You are an independent tester. You do not implement or fix the task; you prove whether the\n"
        "executor's handoff satisfies the task contract and its guardrails.\n"
        "\n"
        "## Tester scope\n"
        "\n"
        f"{repo_line}\n"
        "- Test one bounded task only. Do not route the board, edit implementation, alter tests, or close the task.\n"
        "- Confirm the incoming contract names the intended result, touched surfaces and guardrails to prove.\n"
        f"- Run every validation command from `{desk_root}`. `{source_root}` is the tool import source, not a task\n"
        "  write location. Persist evidence under the assigned `runs/subagents/<run>-testing/` directory.\n"
        "\n"
        "## Recover state first\n"
        "\n"
        "```bash\n"
        f"cd {desk_root}\n"
        f"deskops show board Board --root {desk_root}\n"
        f"deskops show task <task-id> --root {desk_root}\n"
        f"deskops next <task-id> --root {desk_root}\n"
        "git status --short --branch\n"
        "```\n"
        "\n"
        "## Verify\n"
        "\n"
        "- Read the executor's `result-summary.md`, `validation.log` and changed-file list before trusting a green\n"
        "  exit code.\n"
        "- Run the smallest task-specific validation first, then the negative or boundary checks the task and pills\n"
        "  imply. Report stale or missing tests instead of treating them as proof.\n"
        "- Record exact commands and genuine outputs. A failed check is a blocker for closeout, not something to fix\n"
        "  in this role.\n"
        "\n"
        "## Completion\n"
        "\n"
        "- Write `result-summary.md` with the task id, role `tester`, run id/session, validations, pass/fail,\n"
        "  guardrails proven, stale/missing tests and any follow-up.\n"
        "- Hand back to the coordinator. Do not run `deskops closeout`; the coordinator closes only after reviewing\n"
        "  your evidence and a passing independent test.\n"
        "- Say you are done with `sciontool status task_completed \"<one-line pass/fail summary>\"`: Scion wakes the\n"
        "  coordinator on that status.\n"
        f"\nProject: `{project}`. Runtime: `{harness}`.\n"
    )


def _render_specialist_agents_md(
    role_name: str,
    harness: str,
    task_repo: str | None,
    context: dict[str, str] | None,
) -> str:
    """Store-cleaning specialist: mechanical sldb repairs only, notes for the rest."""
    _workspace, desk_root, _source_root, project = _example_roots(task_repo, context)
    return (
        f"# {role_name}: sldb store specialist on Scion ({harness})\n"
        "\n"
        "You leave the desk's sldb store clean. You repair only mechanical findings and report the rest.\n"
        "\n"
        "## Scope\n"
        "\n"
        f"- Work from the desk root `{desk_root}` (`DESKOPS_DESK_ROOT`): `cd {desk_root}` first.\n"
        "- Use exactly the run_dir the coordinator wrote in your start prompt; never invent a different\n"
        "  timestamp directory. Create it if missing.\n"
        "\n"
        "## 1. Check\n"
        "\n"
        "```bash\n"
        f"cd {desk_root}\n"
        "RUN_DIR=<run_dir from the start prompt>; mkdir -p \"$RUN_DIR\"\n"
        "sldb stores check --store .sldb --format json > \"$RUN_DIR/stores-check-before.json\"\n"
        "deskops doctor --root . > \"$RUN_DIR/doctor-before.txt\"\n"
        "```\n"
        "\n"
        "## 2. Repair (only these four commands define \"mechanical\")\n"
        "\n"
        "- `sldb docs track <path>`: a Markdown file under `desk/` the check reports as unregistered.\n"
        "- `sldb docs update <path>`: a registered document whose file changed outside the CLI. It registers the\n"
        "  file as it is; you never change its text.\n"
        "- `sldb docs untrack <id>`: an indexed document whose file no longer exists.\n"
        "- `sldb stores rebuild-index --store .sldb`: the check reports a stale derived index.\n"
        "\n"
        "## 3. Everything else: leave a note, touch nothing\n"
        "\n"
        "Any finding those four commands do not fix (lost anchors included, and anything that would need you to\n"
        "change a document's text) is not touched. Send one note per finding:\n"
        "\n"
        "```bash\n"
        "deskops message send \"<finding verbatim and affected document>\" --kind unclear \\\n"
        "  --title \"store: <document id, or file path if it has no id>\" --root .\n"
        "```\n"
        "\n"
        "## 4. Re-check and report\n"
        "\n"
        "```bash\n"
        "sldb stores check --store .sldb --format json > \"$RUN_DIR/stores-check-after.json\"\n"
        "```\n"
        "\n"
        "Write `$RUN_DIR/result-summary.md` with: findings before, commands run, findings after, notes sent.\n"
        "\n"
        "## Forbidden\n"
        "\n"
        "- Editing files by hand, touching code or tests.\n"
        "- `git commit` and `git add`: changes stay uncommitted for the coordinator.\n"
        "- `deskops closeout` and `deskops advance task`.\n"
        "\n"
        "## Completion\n"
        "\n"
        "- Say you are done with `sciontool status task_completed \"<one-line summary>\"`.\n"
        f"\nProject: `{project}`. Runtime: `{harness}`.\n"
    )


def _render_agents_md(
    role_name: str,
    harness: str,
    task_repo: str | None,
    context: dict[str, str] | None,
) -> str:
    _workspace, desk_root, source_root, project = _example_roots(task_repo, context)
    repo_line = (
        f"- Your task lives in the repository `{task_repo}` at `{desk_root}` (the alias is descriptive only). Write only there."
        if task_repo
        else f"- Your task lives in the repository at `{desk_root}`. Write only there; the other repositories are context."
    )
    return (
        f"# {role_name} on Scion ({harness})\n"
        "\n"
        "You are a deskops executor running as a Scion agent. The desk, not your memory, holds the state.\n"
        "\n"
        "## Scope\n"
        "\n"
        f"{repo_line}\n"
        "- One bounded task. Do not route the board, touch other tasks, or close the task yourself.\n"
        f"- Run implementation and validation from `{desk_root}`. `{source_root}` is the tool import source, not a\n"
        "  task write location.\n"
        "- The CLIs are `deskops` and `sldb`; learn them with `--help`. Never edit a tracked desk document by hand.\n"
        "\n"
        "## Recover state first\n"
        "\n"
        "```bash\n"
        f"cd {desk_root}\n"
        f"deskops show board Board --root {desk_root}\n"
        f"deskops show task <task-id> --root {desk_root}\n"
        f"deskops next <task-id> --root {desk_root}\n"
        "git status --short --branch\n"
        "```\n"
        "\n"
        "## Evidence\n"
        "\n"
        "Use the exact run_dir assigned by the coordinator; never invent a different timestamp directory.\n"
        "Snapshot the state inside that assigned run_dir and preserve its existing RunDoc intent.\n"
        "`deskops closeout commit --run-dir` refuses a run dir without `board.txt` and `git-status.txt`:\n"
        "\n"
        "```bash\n"
        'RUN_DIR=runs/subagents/<assigned-run>; mkdir -p "$RUN_DIR"\n'
        f"deskops show board Board --root {desk_root} > \"$RUN_DIR/board.txt\"\n"
        f"deskops show task <task-id> --root {desk_root} > \"$RUN_DIR/task.txt\"\n"
        f"deskops next <task-id> --root {desk_root} > \"$RUN_DIR/next.txt\"\n"
        f"deskops graph missing --root {desk_root} > \"$RUN_DIR/graph.txt\"\n"
        f"git status --short --branch > \"$RUN_DIR/git-status.txt\"\n"
        "```\n"
        "\n"
        "- Then `validation.log` (the exact command and its exit code) and `result-summary.md`.\n"
        "- `result-summary.md` is the handoff: what you did, what you ran, what the supervisor must review.\n"
        "- Run the smallest relevant validation first.\n"
        "\n"
        "## When done\n"
        "\n"
        "- Leave scoped implementation changes uncommitted and clearly described in `result-summary.md`; the coordinator\n"
        "  stages the deliverable and evidence through `deskops closeout commit`. Do not commit or close the task yourself.\n"
        "- With the evidence written, ask to advance your task before you finish:\n"
        "\n"
        "```bash\n"
        f"deskops advance task <task-id> --root {desk_root}\n"
        "```\n"
        "\n"
        "  Run it once, right before `sciontool status task_completed`. The transition may run post-hooks the desk\n"
        "  declared (`deskops next` lists them). If `advance` is blocked or a hook fails (it exits non-zero and the task\n"
        "  stays where it was), put that finding line in `result-summary.md` and signal\n"
        "  `sciontool status blocked \"<the finding line>\"` instead of `task_completed`.\n"
        "  Advancing is the only lifecycle step you take: never close the task, commit or touch other tasks.\n"
        "- Say you are done with `sciontool status task_completed \"<one-line summary>\"`: Scion wakes the coordinator\n"
        "  on that status, not on `blocked`.\n"
        f"\nProject: `{project}`.\n"
    )


def materialize_scion_template(
    root: Path,
    role_id: str,
    *,
    harness: str | None = None,
    out_dir: Path | None = None,
    model_alias: str = DEFAULT_MODEL_ALIAS,
    task_repo: str | None = None,
    mode: str | None = None,
    context: dict[str, Any] | None = None,
    harness_auth: str | None = None,
) -> Path:
    """Write the template for ``role_id`` and return its directory.

    The runtime profile is the one matching the role's ``kind`` unless
    ``harness`` names another installed kind; ``harness`` also decides
    ``default_harness_config``. ``context`` is validated before any output.
    """
    role_path, role_doc = find_role_doc(root, role_id)
    profiles = load_runtime_profiles(root)
    kind = harness or str(role_doc.get("kind") or "")
    profile = profiles.get(kind) or profiles.get(str(role_doc.get("kind") or ""))
    if profile is None:
        raise ValueError(f"no RuntimeProfileDoc for kind '{kind}' under {root / 'desk' / 'runtimes'}")
    harness_name = pick_harness_config(kind)
    source = f"{role_path.relative_to(root).as_posix()} + desk/runtimes/{profile.get('id', kind)}.md"
    files = scion_template_files(
        role_doc,
        profile,
        harness=harness_name,
        model_alias=model_alias,
        task_repo=task_repo,
        source=source,
        mode=mode,
        context=context,
        harness_auth=harness_auth,
    )
    target = template_dir_for(root, role_doc, out_dir)
    target.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (target / name).write_text(text, encoding="utf-8")
    return target


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-")


def record_scion_run(
    root: Path,
    *,
    task_id: str,
    role_id: str,
    kind: str,
    agent_slug: str,
    run_dir: str | None = None,
    outcome: str = "in_progress",
    summary: str = "",
) -> Path:
    """Write the in_progress intent RunDoc for one Scion dispatch.

    The RunDoc lives at ``<run_dir>/run.md`` so the evidence directory and its
    record travel together. It is written before a native Scion start, so it
    records intent, not proof of start. An existing RunDoc is never overwritten:
    attempts and their evidence are immutable, and a new attempt gets a new
    run_dir and ``-a2`` identity.
    """
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_dir = run_dir or f"runs/subagents/{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{_slug(task_id)}"
    run_id = f"run-{_slug(agent_slug)}"
    payload = {
        "id": run_id,
        "title": f"Scion agent {agent_slug} on {task_id}",
        "summary": summary or (
            f"Launch intent for `scion start {agent_slug}` from role {role_id} ({kind}); "
            "intent, not proof of start."
        ),
        "task_id": task_id,
        "role_id": role_id,
        "kind": kind,
        "run_dir": run_dir,
        "herdr_pane_id": "",
        "session_path": f"scion://agent/{agent_slug}",
        "session_sha256": "",
        "started_at": now,
        "ended_at": "" if outcome == "in_progress" else now,
        "outcome": outcome,
        "commit_sha": "",
        "tags": ["system:deskops", "runtime:scion"],
    }
    path = root / Path(run_dir) / "run.md"
    if path.exists():
        raise ValueError(
            f"RunDoc already exists at {path}: attempts and evidence are immutable; "
            "use a new run_dir and the attempt-2 identity instead of overwriting it"
        )
    doc_access.create_doc(root, path, RunDoc, payload, run_id)
    return path

FILE:deskops/data/desk_declaration.yaml
# The desk a fresh repository gets: what `deskops init`, `deskops desk install`, `deskops desk
# update --apply` and the first desk operation create when it is missing (CC36, DP3).
#
# This is an sldb StoreDeclaration (`sldb.api.StoreDeclaration`) restricted to `folders`,
# `seeds` and `include`; deskops reads it, renders every seed for the desk at hand and passes
# the result in process to `sldb.api.scaffold_store` (`deskops.workspace.seed_desk`):
#
# - `{desk_name}` in a `file:` template or in a `document:` payload is replaced with the
#   project directory's name (`str.replace`, no other placeholder exists);
# - `file:` sources are read from `deskops/data/` (`templates/` for the desk's own files,
#   `lifecycle/` for the lifecycle graph);
# - `document:` seeds are rendered through their deskops model, as the Board and the review
#   runtime profile always were; the runtime profile's `system_prompt` is not data here: it
#   is `deskops.services.review.SYSTEM`, injected while the declaration is built.
#
# A desk's own files are `if_missing` seeds: a desk that already has the file keeps its own.
# The task lifecycle graph (CC31, GO09) is `managed`: the three RelationTypeDoc and the three
# RelationDoc under `desk/lifecycle/` are deskops' documents, written from `lifecycle/` and
# rewritten whenever a desk's copy differs (`deskops desk update --apply` reports it). Each
# RelationDoc carries the transition's effects in `attributes`: `sets` (the fields written on
# the task when the edge is taken) and `terminal` (the task closes). The activation gate of
# each factory task type (CC32, GO06/GO08) is a `managed` RuleDoc too, written from `rules/`
# to `desk/lifecycle/rule-activation-<type>.md`: `on_transition` over `ritual-execution`, with
# subject `model <= <TypeDoc>` so a desk subtype inherits it, it requires the review receipts
# the type asks for (accepted and intact) and the task's dependencies closed; sldb evaluates
# it when `deskops advance` asks for the holding edges. The closeout gate of each factory type
# (CC33b) is the same kind of managed RuleDoc, written from `rules/` to
# `desk/lifecycle/rule-closeout-<type>.md`: `on_transition` over `ritual-closeout`, it requires
# the evidence receipts `deskops closeout verify` writes (kinds in `rules/closeout-evidence.yaml`),
# accepted and intact, and `deskops closeout commit` evaluates it; the two
# `rule-closeout-alert-*.md` are `on_write` alerts over the task's own fields. The `include` rules say
# which desk documents `deskops desk update --apply` tracks under which model
# (`sldb.api.stores.apply_declaration.apply_includes`): the lifecycle documents, the rules,
# the three lifecycle rituals by their ids (`RitualDoc:ritual-<x>`, what the graph's edges
# name), the seeded Board (`BoardDoc:Board`) and phase ritual (`RitualDoc:ritual-phase`), which
# the selectors resolve through the store (CC35b d1), and one glob per desk folder. The tasks
# are tracked by their own paths.
folders:
- desk/tasks
- desk/contexts
- desk/rituals
- desk/atoms
- desk/roles
- desk/inbox
- desk/reviews
- desk/drawer
- desk/runtimes
- desk/materializations
- desk/steps
- desk/registry
- desk/faq
seeds:
- path: desk/config.json
  mode: if_missing
  file: templates/config.json
- path: desk/tasks/Board.md
  mode: if_missing
  track: false
  document:
    model: BoardDoc
    name: board-001
    payload:
      id: board-001
      title: '{desk_name} Board'
      scope: desk
      purpose: Route the active execution set for {desk_name}.
      tasks: []
      pills:
      - desk/contexts/pills.md
      rituals:
      - desk/rituals/phase.md
      - desk/rituals/execution.md
      - desk/rituals/testing.md
      - desk/rituals/closeout.md
      notes: Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.
      tags:
      - workspace:desk
- path: desk/contexts/pills.md
  mode: if_missing
  file: templates/contexts/pills.md
- path: desk/rituals/phase.md
  mode: if_missing
  file: templates/rituals/phase.md
- path: desk/rituals/execution.md
  mode: if_missing
  file: templates/rituals/execution.md
- path: desk/rituals/testing.md
  mode: if_missing
  file: templates/rituals/testing.md
- path: desk/rituals/closeout.md
  mode: if_missing
  file: templates/rituals/closeout.md
- path: desk/drawer/README.md
  mode: if_missing
  file: templates/drawer/README.md
- path: desk/atoms/tag-namespaces.yaml
  mode: if_missing
  file: templates/atoms/tag-namespaces.yaml
- path: desk/runtimes/runtime-pi-deepseek-flash.md
  mode: if_missing
  track: false
  document:
    model: RuntimeProfileDoc
    name: runtime-pi-deepseek-flash
    payload:
      id: runtime-pi-deepseek-flash
      title: Pi deepseek-flash isolated reviewer
      status: active
      kind: pi
      binary: pi
      model_flag: --model
      fallback_models_flag: ''
      fallback_models_join: comma
      tools_flag: ''
      tools_join: comma
      system_prompt_flag: --system-prompt
      system_prompt_delivery: inline
      session_flag: ''
      extra_args:
      - --provider
      - deepseek
      - --model
      - deepseek-flash
      - --thinking
      - low
      - --offline
      - --no-session
      - --no-context-files
      - --no-skills
      - --no-extensions
      - --no-prompt-templates
      - --no-tools
      - --print
      unsupported_role_fields: []
      notes: 'Verified cheap profile for ritual-context-review step 3 (D4): offline, no session/context/skills/extensions/prompt-templates/tools.'
      summary: Isolated cheap reviewer profile (pi deepseek-flash) used by `deskops review`.
      tags:
      - system:deskops
- path: desk/lifecycle/type-task_activates.md
  mode: managed
  file: lifecycle/type-task_activates.md
- path: desk/lifecycle/type-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/type-task_hands_to_closeout.md
- path: desk/lifecycle/type-task_completes.md
  mode: managed
  file: lifecycle/type-task_completes.md
- path: desk/lifecycle/execution-task_activates.md
  mode: managed
  file: lifecycle/execution-task_activates.md
- path: desk/lifecycle/testing-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/testing-task_hands_to_closeout.md
- path: desk/lifecycle/closeout-task_completes.md
  mode: managed
  file: lifecycle/closeout-task_completes.md
- path: desk/lifecycle/rule-activation-task-code.md
  mode: managed
  file: rules/rule-activation-task-code.md
- path: desk/lifecycle/rule-activation-task-docs.md
  mode: managed
  file: rules/rule-activation-task-docs.md
- path: desk/lifecycle/rule-activation-task-debug.md
  mode: managed
  file: rules/rule-activation-task-debug.md
- path: desk/lifecycle/rule-activation-task-refactor.md
  mode: managed
  file: rules/rule-activation-task-refactor.md
- path: desk/lifecycle/rule-activation-task-decision.md
  mode: managed
  file: rules/rule-activation-task-decision.md
- path: desk/lifecycle/rule-activation-task-aggregate.md
  mode: managed
  file: rules/rule-activation-task-aggregate.md
- path: desk/lifecycle/rule-activation-task-external.md
  mode: managed
  file: rules/rule-activation-task-external.md
- path: desk/lifecycle/rule-closeout-task-code.md
  mode: managed
  file: rules/rule-closeout-task-code.md
- path: desk/lifecycle/rule-closeout-task-docs.md
  mode: managed
  file: rules/rule-closeout-task-docs.md
- path: desk/lifecycle/rule-closeout-task-debug.md
  mode: managed
  file: rules/rule-closeout-task-debug.md
- path: desk/lifecycle/rule-closeout-task-refactor.md
  mode: managed
  file: rules/rule-closeout-task-refactor.md
- path: desk/lifecycle/rule-closeout-task-decision.md
  mode: managed
  file: rules/rule-closeout-task-decision.md
- path: desk/lifecycle/rule-closeout-task-aggregate.md
  mode: managed
  file: rules/rule-closeout-task-aggregate.md
- path: desk/lifecycle/rule-closeout-task-external.md
  mode: managed
  file: rules/rule-closeout-task-external.md
- path: desk/lifecycle/rule-closeout-alert-implicit-code.md
  mode: managed
  file: rules/rule-closeout-alert-implicit-code.md
- path: desk/lifecycle/rule-closeout-alert-pill-graduation.md
  mode: managed
  file: rules/rule-closeout-alert-pill-graduation.md
include:
- model: RelationTypeDoc
  glob: desk/lifecycle/type-*.md
- model: RelationDoc
  paths:
  - desk/lifecycle/execution-task_activates.md
  - desk/lifecycle/testing-task_hands_to_closeout.md
  - desk/lifecycle/closeout-task_completes.md
- model: RuleDoc
  glob: desk/lifecycle/rule-activation-*.md
- model: RuleDoc
  glob: desk/lifecycle/rule-closeout-*.md
- model: BoardDoc
  paths:
  - desk/tasks/Board.md
- model: RitualDoc
  paths:
  - path: desk/rituals/phase.md
    name: ritual-phase
  - path: desk/rituals/execution.md
    name: ritual-execution
  - path: desk/rituals/testing.md
    name: ritual-testing
  - path: desk/rituals/closeout.md
    name: ritual-closeout
- model: BoardDoc
  glob: desk/tasks/board-*.md
- model: PillDoc
  glob: desk/contexts/pill-*.md
- model: RitualDoc
  glob: desk/rituals/ritual-*.md
- model: AtomDoc
  glob: desk/atoms/atom-*.md
- model: ProtoAtomDoc
  glob: desk/atoms/proto-*.md
- model: RoleDoc
  glob: desk/roles/*.md
- model: RepositoryDoc
  glob: desk/registry/*.md
- model: StepDoc
  glob: desk/steps/*.md
- model: DeskFAQDoc
  glob: desk/faq/*.md

FILE:tests/test_lifecycle_graph.py
from __future__ import annotations

from deskops import doc_access

from pathlib import Path

import pytest

from deskops import lifecycle
from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations
from deskops.paths import package_pythonpath
from tests.activation_receipts import accept_receipts

LIFECYCLE_TEMPLATES = Path(__file__).resolve().parents[1] / "deskops" / "data" / "lifecycle"
RULE_TEMPLATES = Path(__file__).resolve().parents[1] / "deskops" / "data" / "rules"
RELATION_DOCS = ("execution-task_activates", "testing-task_hands_to_closeout", "closeout-task_completes")


def _run(argv: list[str]) -> tuple[int, str]:
    import contextlib
    import io

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(argv)
    return code, buffer.getvalue()


def _lifecycle_tree(root: Path) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in sorted((root / "desk" / "lifecycle").glob("*.md"))}


def _managed_templates() -> dict[str, bytes]:
    """What `desk/lifecycle/` holds: the graph's six documents and the activation rules (CC32)."""
    return {p.name: p.read_bytes() for folder in (LIFECYCLE_TEMPLATES, RULE_TEMPLATES) for p in folder.glob("*.md")}


def _task(operations: DeskopsOperations, title: str, **extra: object) -> str:
    payload = {
        "title": title,
        "goal": "g",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest"],
        **extra,
    }
    return operations.create_task_bundle(payload).task_id


def test_the_lifecycle_graph_lives_in_the_store_as_rituals_and_relation_docs(lifecycle_desk: Path) -> None:
    from sldb.api import doc_exists

    store = lifecycle_desk / ".sldb"
    for ritual in ("ritual-execution", "ritual-testing", "ritual-closeout"):
        assert doc_exists(store, f"RitualDoc/{ritual}")
    for name in ("task_activates", "task_hands_to_closeout", "task_completes"):
        assert doc_exists(store, f"RelationTypeDoc/type-{name}")
    edges = lifecycle.transitions_from(lifecycle_desk, "ritual-testing")
    assert [(e.relation_type, e.target, e.condition) for e in edges] == [
        ("task_hands_to_closeout", "ritual-closeout", "nonempty(validation)")
    ]
    closing = lifecycle.transitions_from(lifecycle_desk, "ritual-closeout")
    assert closing[0].target == "ritual-closeout" and closing[0].terminal, "completion is a self-loop"


def test_write_lifecycle_graph_is_idempotent(lifecycle_desk: Path) -> None:
    assert lifecycle.write_lifecycle_graph(lifecycle_desk) == []
    assert _lifecycle_tree(lifecycle_desk) == _managed_templates()


def test_the_seeds_declare_the_effects_of_each_transition_and_one_edge_per_ritual(lifecycle_desk: Path) -> None:
    """GO09: each RelationDoc carries `attributes.sets.status` and `terminal`; `task_completes` is the
    terminal one. One edge leaves each ritual, so the order sldb returns holding edges in decides
    nothing (k4, n3)."""
    from sldb.models.relation_doc import RelationDoc
    from sldb.runtime.validation import extract_model_data

    edges = {
        name: extract_model_data(RelationDoc, (lifecycle_desk / "desk" / "lifecycle" / f"{name}.md").read_text(encoding="utf-8"))
        for name in RELATION_DOCS
    }
    assert {name: edge["attributes"] for name, edge in edges.items()} == {
        "execution-task_activates": {"sets": {"status": "active"}, "terminal": False},
        "testing-task_hands_to_closeout": {"sets": {"status": "ready_for_testing"}, "terminal": False},
        "closeout-task_completes": {"sets": {"status": "closed"}, "terminal": True},
    }
    sources = [edge["source_id"] for edge in edges.values()]
    assert sorted(sources) == sorted(f"RitualDoc:{node}" for node in lifecycle.load_lifecycle_spec().rituals)
    assert len(set(sources)) == len(sources), "one edge leaves each ritual"
    for node in lifecycle.load_lifecycle_spec().rituals:
        assert len(lifecycle.transitions_from(lifecycle_desk, node)) == 1, node


def test_desk_update_apply_rewrites_a_relation_doc_without_attributes_and_then_changes_nothing(
    lifecycle_desk: Path,
) -> None:
    """A RelationDoc of the version before GO09 (no `attributes`) differs from the managed seed:
    `desk update` names it, `--apply` rewrites and reports it, and a second run changes nothing."""
    import re

    edge = lifecycle_desk / "desk" / "lifecycle" / "testing-task_hands_to_closeout.md"
    old_version = re.sub(r"^attributes:\n(?:  .*\n)+", "", edge.read_text(encoding="utf-8"), flags=re.M)
    edge.write_text(old_version, encoding="utf-8")
    assert "attributes" not in edge.read_text(encoding="utf-8") and "relation_type: task_hands_to_closeout" in old_version

    code, out = _run(["desk", "update", "--root", str(lifecycle_desk)])
    assert code == 1
    assert "- Lifecycle documents to rewrite: desk/lifecycle/testing-task_hands_to_closeout.md" in out

    code, out = _run(["desk", "update", "--root", str(lifecycle_desk), "--apply"])
    assert code == 0, out
    assert "Lifecycle graph: rewrote desk/lifecycle/testing-task_hands_to_closeout.md" in out
    assert edge.read_bytes() == (LIFECYCLE_TEMPLATES / edge.name).read_bytes()
    assert lifecycle.transitions_from(lifecycle_desk, "ritual-testing")[0].sets == {"status": "ready_for_testing"}

    before = _lifecycle_tree(lifecycle_desk)
    code, out = _run(["desk", "update", "--root", str(lifecycle_desk), "--apply"])
    assert (code, out.strip()) == (0, "Desk is up to date.")
    assert _lifecycle_tree(lifecycle_desk) == before
    assert main(["doctor", "--root", str(lifecycle_desk)]) == 0


def test_a_desk_edge_whose_sets_differ_from_the_package_is_refused_before_the_write(lifecycle_desk: Path) -> None:
    """The effect is the edge's, but the task's lifecycle is checked against the package's edges
    (CC37 a1: ``desk update --apply`` restores a managed edge a desk changed). An edge edited
    through sldb's API to set another status makes ``advance`` refuse the transition before any
    write: since the advance/doctor task.debug (d2) the refusal is ``LifecycleSeedOutOfDate``,
    naming the edge and ``desk update --apply``, instead of the model's ValidationError. The task
    stays as it was; no YAML of the package changes."""
    from sldb.api import save_document_payload
    from sldb.models.relation_doc import RelationDoc
    from sldb.runtime.validation import extract_model_data

    spec_before = lifecycle.SPEC_PATH.read_bytes()
    edge = lifecycle_desk / "desk" / "lifecycle" / "execution-task_activates.md"
    payload = extract_model_data(RelationDoc, edge.read_text(encoding="utf-8"))
    payload["attributes"]["sets"]["status"] = "in_review"
    save_document_payload(lifecycle_desk / ".sldb", "RelationDoc", "execution-task_activates", payload, pythonpath=package_pythonpath())

    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "Declared effect")  # the first desk operation scaffolds only what is missing
    accept_receipts(lifecycle_desk, task_id)
    with pytest.raises(lifecycle.LifecycleSeedOutOfDate) as excinfo:
        operations.advance_task(task_id)

    assert "does not set status active (attributes.sets.status is in_review)" in str(excinfo.value)
    assert "deskops desk update --apply" in str(excinfo.value)
    stored = doc_access.read_doc(lifecycle_desk / "desk" / "tasks" / f"{task_id}.md", TaskDoc)
    assert (stored["status"], stored["current_node"], stored["history"]) == ("draft", "ritual-execution", [])
    assert lifecycle.SPEC_PATH.read_bytes() == spec_before
    assert "in_review" not in lifecycle.SPEC_PATH.read_text(encoding="utf-8")


def test_advance_walks_the_graph_and_sets_status_per_transition(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "Walk the graph")
    accept_receipts(lifecycle_desk, task_id)

    task, result = operations.advance_task(task_id)
    assert (task.current_node, task.status, result.progressed) == ("ritual-testing", "active", True)

    task, result = operations.advance_task(task_id)
    assert (task.current_node, task.status) == ("ritual-closeout", "ready_for_testing")

    task, result = operations.advance_task(task_id)
    assert result.blocked and not result.progressed
    # Without the evidence receipts closeout verify writes, the type's closeout rule holds
    # task_completes back (CC33b) and the message names the rule and its clause.
    assert "rules/rule-closeout-task-code" in result.message, "the blocking rule is named"
    assert 'fact = "tests"' in result.message
    payload = doc_access.read_doc(lifecycle_desk / "desk" / "tasks" / f"{task_id}.md", TaskDoc)
    assert payload["history"] == ["task_activates", "task_hands_to_closeout"]


def test_testing_gate_needs_validation(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "No validation", validation=[])
    accept_receipts(lifecycle_desk, task_id)
    operations.advance_task(task_id)

    task, result = operations.advance_task(task_id)

    assert result.blocked
    assert task.current_node == "ritual-testing"


def test_show_task_reports_the_gates_leaving_the_current_node(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "Show gates")
    accept_receipts(lifecycle_desk, task_id)
    operations.advance_task(task_id)

    _task_obj, gates = operations.show_task(task_id)

    assert gates == [
        {"relation_type": "task_hands_to_closeout", "target": "ritual-closeout", "condition": "nonempty(validation)", "holds": True}
    ]


def test_advance_without_a_lifecycle_graph_says_how_to_get_one(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    task_id = _task(operations, "No graph")

    with pytest.raises(lifecycle.LifecycleGraphMissing, match="deskops init"):
        operations.advance_task(task_id)


# ---------------------------------------------------------------- post-hooks of a transition
HOOKS_EDGE = "testing-task_hands_to_closeout"


def _declare_hooks(root: Path, hooks: object) -> None:
    """Put ``attributes.hooks`` on the testing edge through sldb, as a desk declares them."""
    import contextlib
    import io
    import json

    from sldb.cli import main as sldb_main

    attributes = {"sets": {"status": "ready_for_testing"}, "terminal": False, "hooks": hooks}
    with contextlib.redirect_stdout(io.StringIO()):
        code = sldb_main(["fields", "update", f"docs/RelationDoc/{HOOKS_EDGE}/attributes", json.dumps(attributes), "--store", str(root / ".sldb")])
    assert code == 0


def _task_at_testing(root: Path) -> tuple[DeskopsOperations, str, Path]:
    operations = DeskopsOperations(root)
    task_id = _task(operations, "Hooks")
    accept_receipts(root, task_id)
    operations.advance_task(task_id)
    return operations, task_id, root / "desk" / "tasks" / f"{task_id}.md"


def _state(path: Path) -> dict[str, object]:
    payload = doc_access.read_doc(path, TaskDoc)
    return {key: payload.get(key) for key in ("status", "current_node", "history")}


def test_hooks_run_in_order_after_the_transition_with_env_and_leave_a_log(lifecycle_desk: Path) -> None:
    _declare_hooks(
        lifecycle_desk,
        [
            {"name": "first", "run": ["sh", "-c", 'echo "$DESKOPS_TASK_ID|$DESKOPS_TRANSITION|$DESKOPS_FROM_NODE|$DESKOPS_TO_NODE|$DESKOPS_ROOT" > first.txt; pwd > cwd.txt']},
            {"name": "second", "run": ["sh", "-c", "test -f first.txt && echo said-out && echo said-err >&2"]},
        ],
    )
    operations, task_id, task_path = _task_at_testing(lifecycle_desk)

    task, result = operations.advance_task(task_id)

    assert result.progressed and task.current_node == "ritual-closeout"
    assert "current_node: ritual-closeout\n" in task_path.read_text(encoding="utf-8")
    root = lifecycle_desk.resolve()
    assert (root / "first.txt").read_text().strip() == f"{task_id}|task_hands_to_closeout|ritual-testing|ritual-closeout|{root}"
    assert (root / "cwd.txt").read_text().strip() == str(root)
    logs = list((root / "runs" / "hooks" / task_id).glob("task_hands_to_closeout-*.log"))
    assert len(logs) == 1
    assert __import__("re").fullmatch(r"task_hands_to_closeout-\d{8}T\d{6}Z\.log", logs[0].name)
    text = logs[0].read_text()
    assert text.index("== hook first") < text.index("== hook second")
    assert "result: exit 0" in text and "said-out" in text and "said-err" in text


def test_a_failing_hook_restores_the_task_stops_the_chain_and_advance_names_it(lifecycle_desk: Path) -> None:
    _declare_hooks(
        lifecycle_desk,
        [
            {"name": "boom", "run": ["sh", "-c", "echo partial; echo nope >&2; exit 3"]},
            {"name": "never", "run": ["sh", "-c", "echo x > never.txt"]},
        ],
    )
    operations, task_id, task_path = _task_at_testing(lifecycle_desk)
    before = _state(task_path)

    code, out = _run(["advance", "task", task_id, "--root", str(lifecycle_desk)])

    assert code == 1
    assert _state(task_path) == before
    assert not (lifecycle_desk / "never.txt").exists()
    line = next(l for l in out.splitlines() if l.startswith("Message: "))
    assert "error: [" in line and "hook 'boom'" in line and "codigo de salida 3" in line
    log = next((lifecycle_desk / "runs" / "hooks" / task_id).glob("*.log"))
    assert f"runs/hooks/{task_id}/{log.name}" in line
    assert "partial" in log.read_text() and "nope" in log.read_text()
    assert "Current node: ritual-testing" in out


def test_a_hook_that_exceeds_its_timeout_fails_with_the_timeout_in_place_of_the_code(lifecycle_desk: Path) -> None:
    _declare_hooks(lifecycle_desk, [{"name": "slow", "run": ["sleep", "5"], "timeout": 1}])
    operations, task_id, task_path = _task_at_testing(lifecycle_desk)
    before = _state(task_path)

    code, out = _run(["advance", "task", task_id, "--root", str(lifecycle_desk)])

    assert code == 1 and _state(task_path) == before
    assert "hook 'slow'" in out and "timeout tras 1 s" in out


@pytest.mark.parametrize(
    "hooks",
    [
        [{"run": ["true"]}],
        [{"name": "n"}],
        [{"name": "n", "run": "true"}],
        [{"name": "n", "run": ["true", 3]}],
        [{"name": "n", "run": ["true"], "timeout": 0}],
        [{"name": "n", "run": ["true"], "timeout": "5"}],
    ],
)
def test_a_malformed_hook_entry_fails_advance_before_persisting_and_names_the_relation_doc(lifecycle_desk: Path, hooks: object) -> None:
    import contextlib
    import io

    _declare_hooks(lifecycle_desk, hooks)
    operations, task_id, task_path = _task_at_testing(lifecycle_desk)
    before = task_path.read_bytes()

    err = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
        code = main(["advance", "task", task_id, "--root", str(lifecycle_desk)])

    assert code == 1
    assert task_path.read_bytes() == before
    assert f"desk/lifecycle/{HOOKS_EDGE}.md" in err.getvalue()
    assert not (lifecycle_desk / "runs" / "hooks").exists()


def test_desk_update_keeps_the_hooks_doctor_does_not_report_them_and_next_and_show_list_them(lifecycle_desk: Path) -> None:
    hooks = [
        {"name": "b-second", "run": ["true"]},
        {"name": "a-first", "run": ["sh", "-c", "exit 0"], "timeout": 9},
    ]
    _declare_hooks(lifecycle_desk, hooks)
    operations, task_id, _task_path = _task_at_testing(lifecycle_desk)
    edge = lifecycle_desk / "desk" / "lifecycle" / f"{HOOKS_EDGE}.md"

    code, out = _run(["doctor", "--root", str(lifecycle_desk)])
    assert "lifecycle seed out of date" not in out, out

    # The package seed changes under the hooks: the rewrite copies the desk's list whole, in order.
    edge.write_text(edge.read_text(encoding="utf-8").replace("status: ready_for_testing", "status: active"), encoding="utf-8")
    code, out = _run(["desk", "update", "--apply", "--root", str(lifecycle_desk)])
    assert code == 0, out
    assert f"rewrote desk/lifecycle/{HOOKS_EDGE}.md" in out
    assert lifecycle.parse_hooks(lifecycle.hooks_from_text(edge.read_text(encoding="utf-8")), HOOKS_EDGE) == (
        lifecycle.Hook("b-second", ("true",), 300),
        lifecycle.Hook("a-first", ("sh", "-c", "exit 0"), 9),
    )
    assert "status: ready_for_testing" in edge.read_text(encoding="utf-8")

    code, out = _run(["doctor", "--root", str(lifecycle_desk)])
    assert "lifecycle seed out of date" not in out, out

    code, out = _run(["next", task_id, "--root", str(lifecycle_desk)])
    assert "Post-hooks:\n- task_hands_to_closeout:\n  - b-second: true\n  - a-first: sh -c exit 0\n" in out
    _task_obj, gates = operations.show_task(task_id)
    assert [h["name"] for h in gates[0]["hooks"]] == ["b-second", "a-first"]
    code, out = _run(["show", "task", task_id, "--root", str(lifecycle_desk)])
    assert "post-hook b-second: true" in out


def test_the_package_seeds_declare_no_hooks() -> None:
    for path in LIFECYCLE_TEMPLATES.glob("*.md"):
        assert lifecycle.hooks_from_text(path.read_text(encoding="utf-8")) is None, path.name

FILE:tests/test_scion_runtime.py
"""RoleDoc + RuntimeProfileDoc -> Scion agent template, against this repo's real desk."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.main import main
from deskops.materializers.runtime_profiles import load_runtime_profiles
from deskops.models import RunDoc, TaskDoc
from deskops.runtime.scion import (
    TEMPLATE_FILES,
    find_role_doc,
    load_scion_context,
    materialize_scion_template,
    pick_harness_config,
    record_scion_run,
    scion_child_identity,
    scion_start_argv,
    scion_template_files,
    validate_scion_context,
)
from sldb.runtime.validation import extract_model_data, render_model_markdown
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.hashing import hash_fields_with_map


@pytest.fixture(scope="module")
def executor() -> dict:
    _, role_doc = find_role_doc(ROOT, "role-deskops-executor")
    return role_doc


@pytest.fixture(scope="module")
def profiles() -> dict[str, dict]:
    return load_runtime_profiles(ROOT)


def test_harness_for_every_tracked_runtime_kind(profiles: dict[str, dict]) -> None:
    for kind in profiles:
        assert pick_harness_config(kind)
    with pytest.raises(ValueError, match="no Scion harness-config"):
        pick_harness_config("emacs")


def test_find_role_doc_accepts_id_and_name() -> None:
    by_id = find_role_doc(ROOT, "role-deskops-executor")[1]
    by_name = find_role_doc(ROOT, "deskops-executor")[1]
    assert by_id == by_name
    with pytest.raises(ValueError, match="no RoleDoc"):
        find_role_doc(ROOT, "role-nobody")


def test_claude_template_is_portable_and_loud_about_omissions(executor: dict, profiles: dict[str, dict]) -> None:
    files = scion_template_files(executor, profiles["claude"], harness="claude", source="desk/roles/x.md")
    assert set(files) == set(TEMPLATE_FILES)

    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["schema_version"] == "1"
    assert agent["default_harness_config"] == "claude"
    assert agent["model"] == "medium"  # size alias, never the concrete RoleDoc model
    assert agent["auth_selectedType"] == "oauth-token"  # never left to whatever credential the Hub finds
    assert agent["agent_instructions"] == "agents.md"
    assert agent["system_prompt"] == "system-prompt.md"
    assert agent["max_turns"] and agent["max_duration"]
    assert "image" not in agent  # environment keys belong to the harness-config

    text = files["scion-agent.yaml"]
    assert "# Source: desk/roles/x.md" in text
    assert executor["model"] in text  # the concrete model is named in a comment
    assert "fallback_models" in text and "unsupported_role_fields" in text  # dropped, but said so
    assert files["system-prompt.md"].strip() == executor["body"].strip()
    assert "Write only there" in files["agents.md"]
    assert "deskops closeout" in files["agents.md"]


def test_pi_template_targets_the_pi_harness_config(executor: dict, profiles: dict[str, dict]) -> None:
    files = scion_template_files(executor, profiles["pi"], harness="pi", model_alias="small", task_repo="sldb")
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["default_harness_config"] == "pi"
    assert agent["model"] == "small"
    assert "auth_selectedType" not in agent
    assert "repository `sldb`" in files["agents.md"]


def test_supervisor_role_gets_coordinator_instructions(profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")
    agents = files["agents.md"]
    assert "coordinator of the `deskops` desk" in agents
    assert "One executor per repository at a time" in agents
    assert "Do not push" in agents and "Never decide for the owner" in agents
    # the executor text is not in it, and an explicit mode overrides the name
    assert "You are a deskops executor" not in agents
    forced = scion_template_files(supervisor, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in forced["agents.md"]
    with pytest.raises(ValueError, match="mode must be"):
        scion_template_files(supervisor, profiles["claude"], harness="claude", mode="boss")


def test_statuses_are_ones_sciontool_has_and_wake_the_coordinator(executor: dict, profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    coordinator = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")
    worker = scion_template_files(executor, profiles["claude"], harness="claude", task_repo="deskops")
    for text in (coordinator["agents.md"], worker["agents.md"]):
        statuses = set(re.findall(r"sciontool status (\w+)", text))
        assert statuses <= {"ask_user", "blocked", "task_completed"}, statuses
    assert "sciontool status task_completed" in worker["agents.md"]  # blocked would not wake the coordinator

    # A coordinator idles blocked on its children; the executor's limit would kill it.
    assert yaml.safe_load(coordinator["scion-agent.yaml"])["max_duration"] == "24h"
    assert yaml.safe_load(worker["scion-agent.yaml"])["max_duration"] == "2h"


def test_the_executor_asks_to_advance_before_completing_and_the_coordinator_only_verifies(executor: dict, profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    coordinator = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")["agents.md"]
    worker = scion_template_files(executor, profiles["claude"], harness="claude", task_repo="deskops")["agents.md"]

    advance, done = worker.index("deskops advance task <task-id>"), worker.index('sciontool status task_completed "<one-line summary>"')
    assert advance < done
    assert "sciontool status blocked" in worker[advance:done] and "result-summary.md" in worker[advance:done]
    assert "never close the task, commit or touch other tasks" in worker

    assert "deskops advance task" in coordinator and "you do not\n   advance that transition" in coordinator
    assert "deskops show task <id>" in coordinator and "status and current_node changed" in coordinator


def test_tools_fold_into_command_args_when_the_profile_has_a_flag(profiles: dict[str, dict]) -> None:
    role = {"id": "role-x", "name": "x", "description": "d", "kind": "claude", "model": "", "tools": ["Read", "Bash"], "body": "# x"}
    agent = yaml.safe_load(scion_template_files(role, profiles["claude"], harness="claude")["scion-agent.yaml"])
    # One token per pair: Scion appends the prompt after command_args, and a variadic
    # flag (Claude's --allowedTools <tools...>) followed by a bare value would eat it.
    assert agent["command_args"] == ["--allowedTools=Read", "--allowedTools=Bash"]


def test_bad_alias_and_bad_harness_are_refused(executor: dict, profiles: dict[str, dict]) -> None:
    with pytest.raises(ValueError, match="model alias"):
        scion_template_files(executor, profiles["claude"], harness="claude", model_alias="huge")
    with pytest.raises(ValueError, match="unknown Scion harness-config"):
        scion_template_files(executor, profiles["claude"], harness="emacs")


def test_materialize_writes_the_three_files(tmp_path: Path) -> None:
    target = materialize_scion_template(ROOT, "deskops-executor", harness="claude", out_dir=tmp_path / "t")
    assert target == tmp_path / "t"
    assert sorted(p.name for p in target.iterdir()) == sorted(TEMPLATE_FILES)
    assert "Source: desk/roles/deskops-executor.md + desk/runtimes/runtime-claude.md" in (target / "scion-agent.yaml").read_text()


def test_cli_runtime_template(tmp_path: Path, capsys) -> None:
    code = main(["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude", "--out", str(tmp_path / "t")])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "Scion template:" in out and "scion start" in out
    assert (tmp_path / "t" / "scion-agent.yaml").exists()


def test_cli_task_root_puts_the_rundoc_next_to_the_task(tmp_path: Path, capsys) -> None:
    task_root = tmp_path / "other-repo"
    task_root.mkdir()
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--out", str(tmp_path / "t"), "--task", "task-x", "--agent", "agent-x", "--task-root", str(task_root),
    ])
    out = capsys.readouterr().out
    assert code == 0, out
    runs = list((task_root / "runs" / "subagents").glob("*-task-x/run.md"))
    assert len(runs) == 1, out

    # An agent that already made its own evidence dir: the RunDoc points there.
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--out", str(tmp_path / "t"), "--task", "task-x", "--agent", "agent-y", "--task-root", str(task_root),
        "--run-dir", "runs/subagents/20261029-000000-task-x",
    ])
    assert code == 0, capsys.readouterr().out
    doc = extract_model_data(RunDoc, (task_root / "runs/subagents/20261029-000000-task-x/run.md").read_text(encoding="utf-8"))
    assert doc["run_dir"] == "runs/subagents/20261029-000000-task-x" and doc["id"] == "run-agent-y"
    assert not list((ROOT / "runs" / "subagents").glob("*-task-x"))  # nothing written into the roles' repo
    assert extract_model_data(RunDoc, runs[0].read_text(encoding="utf-8"))["id"] == "run-agent-x"


def test_cli_task_without_agent_is_an_error(tmp_path: Path, capsys) -> None:
    code = main(["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--out", str(tmp_path / "t"), "--task", "task-x"])
    captured = capsys.readouterr()
    assert code != 0
    assert "--task and --agent go together" in captured.out + captured.err


def test_record_scion_run_writes_a_rundoc_that_roundtrips(tmp_path: Path) -> None:
    path = record_scion_run(
        tmp_path,
        task_id="task-close-serve",
        role_id="role-deskops-executor",
        kind="claude",
        agent_slug="sldb-close-serve",
        run_dir="runs/subagents/20261029-000000-task-close-serve",
    )
    assert path == tmp_path / "runs/subagents/20261029-000000-task-close-serve/run.md"
    data = extract_model_data(RunDoc, path.read_text(encoding="utf-8"))
    assert data["id"] == "run-sldb-close-serve"
    assert data["task_id"] == "task-close-serve"
    assert data["session_path"] == "scion://agent/sldb-close-serve"
    assert data["outcome"] == "in_progress" and data["ended_at"] == ""
    assert "intent, not proof of start" in data["summary"]
    assert data["tags"] == ["system:deskops", "runtime:scion"]


def test_record_scion_run_never_overwrites_a_previous_attempt(tmp_path: Path) -> None:
    run_dir = "runs/subagents/20261029-000000-task-close-serve"
    record_scion_run(
        tmp_path,
        task_id="task-close-serve",
        role_id="role-deskops-executor",
        kind="claude",
        agent_slug="deskops-e-abc123abc123",
        run_dir=run_dir,
    )
    original = (tmp_path / run_dir / "run.md").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="immutable"):
        record_scion_run(
            tmp_path,
            task_id="task-close-serve",
            role_id="role-deskops-executor",
            kind="claude",
            agent_slug="deskops-e-abc123abc123-a2",
            run_dir=run_dir,
        )
    assert (tmp_path / run_dir / "run.md").read_text(encoding="utf-8") == original


def _task_payload(**updates) -> dict:
    payload = {
        "id": "task-contract-identity",
        "title": "Identity test task",
        "status": "draft",
        "summary": "",
        "tags": ["workspace:desk", "artifact:task"],
        "current_node": "ritual-execution",
        "history": [],
        "references": ["tests/test_scion_runtime.py"],
        "depends_on": [],
        "pills": [],
        "files": ["deskops/runtime/scion.py"],
        "task_type": "task.code",
        "inherits_from": [],
        "inherit_acceptance_context": False,
        "atoms": [],
        "why": "Test why.",
        "goal": "Test goal.",
        "scope": "Test scope.",
        "implementation_path": "Test implementation.",
        "validation": ["pytest tests/test_scion_runtime.py"],
        "done_when": "The test passes.",
    }
    payload.update(updates)
    return payload


def _write_task(tmp_path: Path, name: str, **updates) -> Path:
    path = tmp_path / f"{name}.md"
    path.write_text(render_model_markdown(TaskDoc, _task_payload(**updates)) + "\n", encoding="utf-8")
    return path


def test_identity_uses_the_canonical_sldb_contract_digest(tmp_path: Path) -> None:
    path = _write_task(tmp_path, "task")
    markdown = path.read_text(encoding="utf-8")
    _, fields = hash_fields_with_map(TaskDoc, markdown)
    expected_contract = contract_hash(TaskDoc, fields)
    expected_name = "deskops-e-" + hashlib.sha256(
        f"task-contract-identity\0{expected_contract}\0executor".encode("utf-8")
    ).hexdigest()[:12]

    identity = scion_child_identity(path, "executor")
    assert identity["contract_sha256"] == expected_contract
    assert identity["name"] == expected_name
    assert identity["labels"] == {
        "deskops.task_id": "task-contract-identity",
        "deskops.contract_sha256": expected_contract[:63],
        "deskops.role": "executor",
        "deskops.attempt": "1",
    }
    assert scion_child_identity(path, "tester")["name"].startswith("deskops-t-")

    attempt_2 = scion_child_identity(path, "executor", attempt=2)
    assert attempt_2["name"] == expected_name + "-a2"
    assert attempt_2["labels"]["deskops.attempt"] == "2"
    for bad in (0, 3, True):
        with pytest.raises(ValueError, match="attempt must be 1 or 2"):
            scion_child_identity(path, "executor", attempt=bad)
    with pytest.raises(ValueError, match="role must be"):
        scion_child_identity(path, "coordinator")


def test_identity_ignores_status_history_and_references_but_moves_with_contract(tmp_path: Path) -> None:
    entry = scion_child_identity(_write_task(tmp_path, "entry"), "executor")
    active = scion_child_identity(
        _write_task(
            tmp_path,
            "active",
            status="active",
            current_node="ritual-testing",
            history=["task_activates"],
            references=["other.md"],
            summary="Different summary",
            tags=["workspace:desk", "artifact:task", "state:changed"],
        ),
        "executor",
    )
    finished = scion_child_identity(
        _write_task(
            tmp_path,
            "finished",
            status="closed",
            current_node="complete",
            history=["task_activates", "task_hands_to_closeout", "task_completes"],
            references=[],
        ),
        "executor",
    )
    assert entry["name"] == active["name"] == finished["name"]
    assert entry["contract_sha256"] == active["contract_sha256"] == finished["contract_sha256"]

    changed_goal = scion_child_identity(_write_task(tmp_path, "goal", goal="A changed goal."), "executor")
    changed_scope = scion_child_identity(_write_task(tmp_path, "scope", scope="A changed scope."), "executor")
    assert changed_goal["name"] != entry["name"]
    assert changed_scope["contract_sha256"] != entry["contract_sha256"]


def test_start_argv_carries_explicit_project_workspace_auth_and_labels(tmp_path: Path) -> None:
    identity = scion_child_identity(_write_task(tmp_path, "task"), "tester")
    argv = scion_start_argv(
        identity,
        prompt="Verify the contract.",
        project="sldb-1",
        workspace="/workspace",
        template="deskops-tester",
    )
    assert argv[:4] == ["scion", "start", identity["name"], "Verify the contract."]
    assert "--type" in argv and argv[argv.index("--type") + 1] == "deskops-tester"
    assert "--project" in argv and argv[argv.index("--project") + 1] == "sldb-1"
    assert "--workspace" in argv and argv[argv.index("--workspace") + 1] == "/workspace"
    assert "--harness-auth" in argv and argv[argv.index("--harness-auth") + 1] == "oauth-token"
    assert "--non-interactive" in argv
    labels = {argv[index + 1].split("=", 1)[0]: argv[index + 1].split("=", 1)[1] for index, item in enumerate(argv) if item == "--label"}
    assert labels == identity["labels"]


def _context(tmp_path: Path) -> tuple[dict, dict[str, Path]]:
    workspace = tmp_path / "workspace"
    desk_root = workspace / "repo"
    source_root = workspace / "source"
    sldb_root = workspace / "sldb" / "src"
    for path in (desk_root / "desk", source_root / "deskops", sldb_root / "sldb"):
        path.mkdir(parents=True)
    context = {
        "project": "sldb-1",
        "workspace_root": str(workspace),
        "desk_root": str(desk_root),
        "source_root": str(source_root),
        "sldb_root": str(sldb_root),
    }
    return context, {
        "workspace": workspace,
        "desk": desk_root,
        "source": source_root,
        "sldb": sldb_root,
    }


def test_context_emits_environment_volume_and_concrete_examples(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(
        supervisor, load_runtime_profiles(ROOT)["claude"], harness="claude", mode="coordinator", context=context
    )
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["env"] == {
        "DESKOPS_DESK_ROOT": str(paths["desk"]),
        "DESKOPS_SOURCE_ROOT": str(paths["source"]),
        "DESKOPS_SLDB_SOURCE_ROOT": str(paths["sldb"]),
        "DESKOPS_WORKSPACE_ROOT": str(paths["workspace"]),
        "DESKOPS_SCION_PROJECT": "sldb-1",
        "PYTHONPATH": f"{paths['source']}:{paths['sldb']}",
    }
    assert agent["volumes"] == [{"source": str(paths["workspace"]), "target": str(paths["workspace"])}]
    agents = files["agents.md"]
    for fragment in (
        f"--root {paths['desk']}",
        f"--project sldb-1",
        f"--workspace {paths['workspace']}",
        "--type deskops-executor",
        "--type deskops-tester",
        "--harness-auth oauth-token",
        "--non-interactive",
        "--mode tester",
        "scion_child_identity(task_path, role, attempt)",
    ):
        assert fragment in agents


def test_omitted_context_keeps_the_template_without_env_or_volumes() -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, load_runtime_profiles(ROOT)["claude"], harness="claude")
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert "env" not in agent and "volumes" not in agent
    assert "coordinator of the `<repo>` desk" in files["agents.md"]


def test_context_rejects_missing_unknown_relative_and_out_of_workspace_paths(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    assert validate_scion_context(context)["project"] == "sldb-1"

    with pytest.raises(ValueError, match="missing required key"):
        validate_scion_context({key: value for key, value in context.items() if key != "sldb_root"})
    with pytest.raises(ValueError, match="unknown key"):
        validate_scion_context({**context, "secret": "nope"})
    with pytest.raises(ValueError, match="absolute path"):
        validate_scion_context({**context, "desk_root": "repo"})
    with pytest.raises(ValueError, match="inside workspace_root"):
        validate_scion_context({**context, "desk_root": str(tmp_path / "outside")})
    with pytest.raises(ValueError, match="slug or UUID"):
        validate_scion_context({**context, "project": str(paths["workspace"])})
    with pytest.raises(ValueError, match="containing desk/"):
        validate_scion_context({**context, "desk_root": str(paths["workspace"])})
    with pytest.raises(ValueError, match="containing the deskops package"):
        validate_scion_context({**context, "source_root": str(paths["workspace"])})
    with pytest.raises(ValueError, match="sldb src directory"):
        validate_scion_context({**context, "sldb_root": str(paths["source"])})


def test_context_container_keys_emit_limits_shared_paths_and_env(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    shared = tmp_path / "shm"
    shared.mkdir()
    context.update(
        memory_limit="6Gi",
        cpu_limit="4",
        shared_paths=[str(shared), str(shared)],
        env={"TMPDIR": str(shared)},
    )
    _, executor_role = find_role_doc(ROOT, "role-deskops-executor")
    files = scion_template_files(
        executor_role, load_runtime_profiles(ROOT)["claude"], harness="claude", mode="executor", context=context
    )
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["resources"] == {"limits": {"cpu": "4", "memory": "6Gi"}}
    assert agent["volumes"] == [
        {"source": str(paths["workspace"]), "target": str(paths["workspace"])},
        {"source": str(shared), "target": str(shared)},
    ]
    assert agent["env"]["TMPDIR"] == str(shared)
    assert agent["env"]["DESKOPS_SCION_PROJECT"] == "sldb-1"


def test_context_without_container_keys_has_no_resources(tmp_path: Path) -> None:
    context, _ = _context(tmp_path)
    _, executor_role = find_role_doc(ROOT, "role-deskops-executor")
    files = scion_template_files(
        executor_role, load_runtime_profiles(ROOT)["claude"], harness="claude", mode="executor", context=context
    )
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert "resources" not in agent
    assert len(agent["volumes"]) == 1 and "TMPDIR" not in agent["env"]


def test_harness_auth_selects_the_template_auth_type(tmp_path: Path) -> None:
    _, executor_role = find_role_doc(ROOT, "role-deskops-executor")
    profile = load_runtime_profiles(ROOT)["claude"]
    default = yaml.safe_load(scion_template_files(executor_role, profile, harness="claude")["scion-agent.yaml"])
    assert default["auth_selectedType"] == "oauth-token"
    chosen = yaml.safe_load(
        scion_template_files(executor_role, profile, harness="claude", harness_auth="auth-file")["scion-agent.yaml"]
    )
    assert chosen["auth_selectedType"] == "auth-file"
    with pytest.raises(ValueError, match="harness auth"):
        scion_template_files(executor_role, profile, harness="claude", harness_auth="password")

    out_dir = tmp_path / "tpl"
    assert main(
        ["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
         "--out", str(out_dir), "--harness-auth", "auth-file"]
    ) == 0
    assert yaml.safe_load((out_dir / "scion-agent.yaml").read_text(encoding="utf-8"))["auth_selectedType"] == "auth-file"


def test_start_auth_follows_the_template_never_a_fixed_api_key(tmp_path: Path) -> None:
    identity = scion_child_identity(_write_task(tmp_path, "task"), "executor")
    common = dict(prompt="Do the task.", project="sldb-1", workspace="/workspace", template="deskops-executor")
    chosen = scion_start_argv(identity, **common, harness_auth="auth-file")
    assert chosen[chosen.index("--harness-auth") + 1] == "auth-file"
    assert "--harness-auth" not in scion_start_argv(identity, **common, harness_auth=None)
    with pytest.raises(ValueError, match="harness auth"):
        scion_start_argv(identity, **common, harness_auth="password")

    context, _ = _context(tmp_path)
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    profile = load_runtime_profiles(ROOT)["claude"]
    for auth, expected in ((None, "oauth-token"), ("auth-file", "auth-file")):
        agents = scion_template_files(
            supervisor, profile, harness="claude", mode="coordinator", context=context, harness_auth=auth
        )["agents.md"]
        assert agents.count(f"--harness-auth {expected} --non-interactive") == 2
        assert "--harness-auth api-key" not in agents

    out_dir = tmp_path / "coordinator"
    assert main(
        ["runtime", "template", "role-deskops-supervisor", "--root", str(ROOT), "--harness", "claude",
         "--mode", "coordinator", "--out", str(out_dir), "--harness-auth", "auth-file"]
    ) == 0
    written = (out_dir / "agents.md").read_text(encoding="utf-8")
    assert written.count("--harness-auth auth-file") == 2 and "api-key" not in written
    assert yaml.safe_load((out_dir / "scion-agent.yaml").read_text(encoding="utf-8"))["auth_selectedType"] == "auth-file"


def test_context_rejects_bad_container_keys(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    with pytest.raises(ValueError, match="memory_limit"):
        validate_scion_context({**context, "memory_limit": "lots"})
    with pytest.raises(ValueError, match="cpu_limit"):
        validate_scion_context({**context, "cpu_limit": "0"})
    with pytest.raises(ValueError, match="absolute path"):
        validate_scion_context({**context, "shared_paths": ["shm"]})
    with pytest.raises(ValueError, match="does not exist"):
        validate_scion_context({**context, "shared_paths": [str(tmp_path / "missing")]})
    with pytest.raises(ValueError, match="must not repeat workspace_root"):
        validate_scion_context({**context, "shared_paths": [str(paths["workspace"])]})
    with pytest.raises(ValueError, match="must not redefine PYTHONPATH"):
        validate_scion_context({**context, "env": {"PYTHONPATH": "/x"}})
    with pytest.raises(ValueError, match="valid variable name"):
        validate_scion_context({**context, "env": {"BAD-NAME": "x"}})
    with pytest.raises(ValueError, match="must be a string"):
        validate_scion_context({**context, "env": {"TMPDIR": 3}})


def test_load_context_validates_json_and_cli_writes_nothing_on_failure(tmp_path: Path, capsys) -> None:
    context, _ = _context(tmp_path)
    valid = tmp_path / "context.json"
    valid.write_text(json.dumps(context), encoding="utf-8")
    assert load_scion_context(valid)["desk_root"] == validate_scion_context(context)["desk_root"]

    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps({key: value for key, value in context.items() if key != "project"}), encoding="utf-8")
    out_dir = tmp_path / "out"
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT),
        "--harness", "claude", "--out", str(out_dir), "--context-file", str(invalid),
    ])
    captured = capsys.readouterr()
    assert code != 0
    assert "missing required key" in captured.out + captured.err
    assert not out_dir.exists()


def test_tester_mode_is_autodetected_and_explicit_mode_wins() -> None:
    profiles = load_runtime_profiles(ROOT)
    _, tester = find_role_doc(ROOT, "role-deskops-tester")
    auto = scion_template_files(tester, profiles["claude"], harness="claude", task_repo="deskops")
    assert "independent tester" in auto["agents.md"]
    assert "## Tester scope" in auto["agents.md"]
    assert "## Completion" in auto["agents.md"]
    assert "You are a deskops executor" not in auto["agents.md"]
    assert "Do not run `deskops closeout`" in auto["agents.md"]

    _, executor = find_role_doc(ROOT, "role-deskops-executor")
    forced = scion_template_files(executor, profiles["claude"], harness="claude", mode="tester")
    assert "independent tester" in forced["agents.md"]
    explicit = scion_template_files(tester, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in explicit["agents.md"]

    id_tester = {"id": "role-x-tester", "name": "custom reviewer", "description": "d", "kind": "claude", "body": "# t"}
    assert "independent tester" in scion_template_files(id_tester, profiles["claude"], harness="claude")["agents.md"]
    not_tester = {"id": "role-x", "name": "tester", "description": "d", "kind": "claude", "body": "# t"}
    assert "You are a deskops executor" in scion_template_files(not_tester, profiles["claude"], harness="claude")["agents.md"]

    id_coordinator = {"id": "role-x-coordinator", "name": "custom lead", "description": "d", "kind": "claude", "body": "# t"}
    coordinator = scion_template_files(id_coordinator, profiles["claude"], harness="claude")
    assert "coordinator of the" in coordinator["agents.md"]
    explicit_executor = scion_template_files(id_coordinator, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in explicit_executor["agents.md"]


def _normalized(text: str) -> str:
    return " ".join(text.split())


def test_coordinator_reconciles_activity_own_lanes_and_reviews_before_dispatch() -> None:
    profiles = load_runtime_profiles(ROOT)
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    agents = _normalized(
        scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")["agents.md"]
    )
    assert "Never answer an executor's or tester's question" not in agents
    for fragment in (
        "activity=completed with phase=running means the child completed",
        "inspect activity=completed first and use phase only as fallback",
        "Reconcile your OWN completed or stopped lane",
        "must not skip your own task",
        "If its preflight or bundle receipt is missing",
        "routine coordinator work, not a human blocker",
        "do not blanket-surface every question",
        "closeout verify --task <id>",
        "--paths <scoped implementation, evidence and review paths>",
        "Never use `git add -A`",
        "Only an actual owner decision uses `ask_user`",
        "sciontool status task_completed",
        "Do not push.",
    ):
        assert fragment in agents, fragment
    assert "/tmp/scion" not in agents


def test_all_three_modes_receive_the_actual_context_roots(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    profiles = load_runtime_profiles(ROOT)
    roles = {
        "role-deskops-executor": "executor",
        "role-deskops-tester": "tester",
        "role-deskops-supervisor": "coordinator",
    }
    for role_id, mode in roles.items():
        _, role = find_role_doc(ROOT, role_id)
        files = scion_template_files(role, profiles["claude"], harness="claude", context=context)
        agents = files["agents.md"]
        assert str(paths["desk"]) in agents, mode
        assert str(paths["source"]) in agents, mode
        assert f"cd {paths['desk']}" in agents, mode
        assert "/tmp/scion" not in agents, mode
        agent = yaml.safe_load(files["scion-agent.yaml"])
        assert agent["env"]["DESKOPS_DESK_ROOT"] == str(paths["desk"]), mode


def test_cli_tester_mode_and_context_file_are_available(tmp_path: Path, capsys) -> None:
    context, paths = _context(tmp_path)
    context_file = tmp_path / "context.json"
    context_file.write_text(json.dumps(context), encoding="utf-8")
    out_dir = tmp_path / "tester-template"
    code = main([
        "runtime", "template", "role-deskops-tester", "--root", str(ROOT),
        "--harness", "claude", "--out", str(out_dir), "--context-file", str(context_file),
    ])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "independent tester" in (out_dir / "agents.md").read_text(encoding="utf-8")
    agent = yaml.safe_load((out_dir / "scion-agent.yaml").read_text(encoding="utf-8"))
    assert agent["env"]["DESKOPS_DESK_ROOT"] == str(paths["desk"])


def test_executor_preserves_assigned_run_and_coordinator_commit_boundary(executor, profiles) -> None:
    agents = scion_template_files(executor, profiles["pi"], harness="pi", task_repo="example")["agents.md"]
    assert "Use the exact run_dir assigned by the coordinator" in agents
    assert "preserve its existing RunDoc intent" in agents
    assert "$(date" not in agents
    assert "graph.txt" in agents
    assert "Do not commit or close the task yourself" in agents


def test_omitted_context_keeps_legacy_tool_root_separate_from_task_repo(profiles) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, profiles["pi"], harness="pi", task_repo="example")
    assert "cd /workspace/example" in files["agents.md"]
    assert "--root /workspace/deskops" in files["agents.md"]
    assert "env:" not in files["scion-agent.yaml"]


@pytest.mark.parametrize("task_id", ["task-" + "a" * 58, "task-" + "b" * 59, "task-construcción"])
def test_native_labels_fit_scion_without_changing_canonical_identity(tmp_path, task_id) -> None:
    path = _write_task(tmp_path, "native-labels", id=task_id)
    identity = scion_child_identity(path, "executor")
    labels = identity["labels"]
    assert identity["task_id"] == task_id
    assert len(identity["contract_sha256"]) == 64
    assert labels["deskops.contract_sha256"] == identity["contract_sha256"][:63]
    assert len(labels) <= 16
    assert all(len(k) <= 63 and len(v) <= 63 for k, v in labels.items())
    assert all(all(0x20 <= ord(c) <= 0x7E for c in key + value) for key, value in labels.items())
    if len(task_id) <= 63 and task_id.isascii():
        assert labels["deskops.task_id"] == task_id
    else:
        assert labels["deskops.task_id"] == "t-" + hashlib.sha256(task_id.encode()).hexdigest()[:61]
    expected = hashlib.sha256(f"{task_id}\0{identity['contract_sha256']}\0executor".encode()).hexdigest()[:12]
    assert identity["name"] == "deskops-e-" + expected


def test_specialist_mode_writes_the_three_files_with_the_repair_contract(tmp_path: Path, capsys) -> None:
    out_dir = tmp_path / "t"
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--mode", "specialist", "--out", str(out_dir),
    ])
    assert code == 0, capsys.readouterr().out
    assert sorted(p.name for p in out_dir.iterdir()) == sorted(TEMPLATE_FILES)
    agents = (out_dir / "agents.md").read_text(encoding="utf-8")
    for needle in (
        "sldb stores check", "deskops doctor", "sldb docs track", "sldb docs update",
        "sldb docs untrack", "sldb stores rebuild-index", "deskops message send",
    ):
        assert needle in agents
    forbidden = agents.split("## Forbidden", 1)[1].split("## Completion", 1)[0]
    assert "deskops closeout" in forbidden and "deskops advance task" in forbidden
    assert "You are a deskops executor" not in agents


def test_specialist_role_name_resolves_the_mode_and_unknown_mode_still_fails() -> None:
    profiles = load_runtime_profiles(ROOT)
    role = {"id": "role-x", "name": "x-specialist", "description": "d", "kind": "claude", "body": "# s"}
    files = scion_template_files(role, profiles["claude"], harness="claude")
    assert "sldb store specialist" in files["agents.md"]
    by_id = {"id": "role-x-specialist", "name": "x", "description": "d", "kind": "claude", "body": "# s"}
    assert "sldb store specialist" in scion_template_files(by_id, profiles["claude"], harness="claude")["agents.md"]
    with pytest.raises(ValueError, match="mode must be"):
        scion_template_files(role, profiles["claude"], harness="claude", mode="bogus")


def test_specialist_identity_uses_the_s_prefix(tmp_path: Path) -> None:
    identity = scion_child_identity(_write_task(tmp_path, "task"), "specialist")
    assert re.fullmatch(r"deskops-s-[0-9a-f]{12}", identity["name"])
    assert identity["role"] == "specialist"

FILE:instruccion
Cold-bundle de la tarea task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- `TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py tests/test_scion_runtime.py` pasa, con tests nuevos sobre un desk desechable de `tmp_path` que comprueban: (a) una tarea en ritual-testing vuelve a ritual-execution con `--back --reason`, queda con status active y su history termina en `task_returns_to_execution: <texto>`; (b) sin `--back`, desde ritual-testing el avance normal sigue yendo a ritual-closeout y nunca toma la transicion manual; (c) los tres casos de codigo 2 y el caso bloqueado; (d) un post-hook declarado en la transicion de vuelta corre; (e) el agents.md del ejecutor contiene `sciontool status blocked`.
- Los goldens de ayuda afectados se regeneran con `pytest -n 4 tests/test_output_goldens.py -k help --update-golden` y se conservan solo los que cambian por la opcion nueva.
- `deskops doctor --root .` sobre un desk recien creado con `deskops init` no informa deriva por la transicion nueva.

