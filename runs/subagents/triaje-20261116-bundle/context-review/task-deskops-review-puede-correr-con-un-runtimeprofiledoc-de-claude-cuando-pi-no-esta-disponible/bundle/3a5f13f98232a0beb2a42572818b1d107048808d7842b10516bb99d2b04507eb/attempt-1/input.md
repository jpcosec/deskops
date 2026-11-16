FILE:desk/tasks/task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible.md
---
sldb:
  by: agent
  at: '2026-11-16T05:00:47Z'
  authority: generated
  via: save_document_payload
id: task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-002453-suggestion-piloto-scion-fase-1-brechas-del-coordinador-y-del-ejecutor-claude-en-contenedor.md
depends_on: []
pills:
- desk/contexts/pill-zero-context-preflight-precedes-executor.md
files:
- deskops/services/review.py
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
- atom-cheap-zero-context-reviews-test-the-brief-recursively
---

# deskops review puede correr con un RuntimeProfileDoc de claude cuando pi no esta disponible

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del piloto scion fase 1 (2026-11-16), brecha 1: la imagen scion-claude no trae pi, asi que el coordinador dentro del contenedor no puede correr `deskops review preflight/bundle` (engine por defecto runtime-pi-deepseek-flash); hoy los corre el supervisor en el host. deskops/services/review.py arma el argv solo para pi (`binary or 'pi'` y el input como `@<ruta>`).

## Goal

_Describe the concrete result this task must produce._

`deskops review preflight|bundle|node --engine <perfil>` funciona con un RuntimeProfileDoc cuyo binario es claude: el argv usa el modo no interactivo de claude (-p), el modelo del perfil, el system prompt del revisor, sin tools, sin sesion persistida y sin cargar contexto, skills ni MCP del usuario, y el input se entrega por stdin o por archivo segun lo que acepte claude. El manifest registra binario, modelo y flags de aislamiento igual que con pi. El default sigue siendo runtime-pi-deepseek-flash.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/review.py (armado del argv, alrededor de las lineas 166-186), el RuntimeProfileDoc runtime-claude del desk de deskops si hay que ajustar sus campos (con `deskops edit runtime-profile`), tests/test_review_command.py. Se fijan los flags exactos leyendo `claude --help` en robocop2. No entra: instalar pi en la imagen (lo pide la nota al repo scion), cambiar el ritual context-review, elegir el modelo por defecto. Precisiones del preflight 1: claude esta instalado en robocop2 y el ejecutor corre ahi (claude --help para los flags). El input va por stdin (no @ruta). Si runtime-claude no existe o le falta binary/model, se completa con deskops edit runtime-profile (binary claude, model haiku) y si no existe se crea con deskops add runtime-profile. Desk sandbox = un directorio en /dev/shm con git init y deskops init, borrado al terminar. La evidencia de la corrida manual es el run_dir que imprime el comando (manifest.json, output.md) citado en el informe; se acepta si output.md trae las secciones REFORMULACION, AMBIGUEDADES y DRY-RUN. tests/test_review_doc.py solo se corre, no se modifica.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer review.py:150-200 y el modelo RuntimeProfileDoc. 2) Rama por binario: pi (actual) y claude (argv nuevo). 3) Test unitario del argv para un perfil claude (sin llamar al modelo): contiene -p, --model <m>, el system prompt, la desactivacion de tools y no contiene @<ruta>. 4) Prueba manual una vez en robocop2: `deskops review preflight <tarea de prueba> --engine runtime-claude --root .` en un desk sandbox, guardando la salida del run como evidencia.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El test del argv claude pasa; la corrida manual del paso 4 deja un recibo con engine runtime-claude y output con las secciones del revisor.

FILE:desk/contexts/pill-zero-context-preflight-precedes-executor.md
---
# pill-xxx
id: pill-zero-context-preflight-precedes-executor
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:subagents
- topic:preflight
- topic:execution
---

# Guardrail: zero-context preflight precedes executor

## What

_Define the context or guardrail this pill carries._

Before any Executor is dispatched, run one fresh-context subagent against only the TaskDoc and require a step-by-step reformulation of the intended work plus any ambiguity it detects.

## Why

_Explain why this context matters for safe execution._

This cheap comprehension gate proves whether the TaskDoc itself is sufficient. If the subagent cannot restate the intent correctly from the task alone, the real execution bundle is still relying on hidden context or coordinator memory.

## When

_Describe when an agent should apply this pill._

Apply this whenever an active desk task enters execution and before the real Executor launch.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/execution.md` preparation work and evidence stored under `runs/subagents/<run-dir>/preflight.md`.

## How

_Describe the correct way to apply this guidance._

Pass only when the reformulation reproduces the task intent closely enough to execute without guesswork. If the subagent reports any ambiguity, or misses the intended step sequence, fix the TaskDoc first and rerun the preflight.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not dispatch an Executor when the fresh-context subagent could not restate the TaskDoc without guessing, and do not let coordinator chat memory fill gaps the TaskDoc does not contain.

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

FILE:desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:17Z'
  authority: generated
  via: create_document
id: atom-cheap-zero-context-reviews-test-the-brief-recursively
title: Cheap zero-context reviews test the brief recursively
five_wh_one_plus: how
tags:
- system:deskops
- topic:workflow
- topic:subagents
- topic:context-review
---

# Cheap zero-context reviews test the brief recursively

## Answer

Before promoting or executing work, test the quality of the question with a cheap, ephemeral, zero-context reviewer. Supply only the exact versioned brief and explicitly necessary references: no chat history, previous reviews, oral fixes, persistent memory, automatic skills or context files. The reviewer restates the objective, lists ambiguities, and describes a detailed dry-run of readings, proposed changes, dependencies and validation without executing commands or editing sources. The coordinator compares this with the owner's intent, corrects the written brief and recursively splits oversized nodes into children with explicit dependency edges. Review the root, packages and every leaf, including their interfaces and edges; a root review never covers all descendants. Retry each changed input in a fresh process. Unresolved ambiguity blocks execution; an APTO label is insufficient.

TaskDoc-only preflight and cold-bundle coverage review remain distinct cheap comprehension gates before Executor dispatch. Expert council review, execution and independent implementation testing are separate roles and evidence; expert capability cannot rescue or approve a failed cheap brief review. A transport/quota failure is technical evidence, not proof of ambiguity. Record per-node/input/attempt evidence under runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/: exact input bytes and SHA-256, chosen cheap provider/model/profile and selection reason, command/isolation flags, reformulation/ambiguities/dry-run, coordinator comparison and required edits. Keep TaskDoc-only reformulation in preflight.md. New input or a changed dependency contract invalidates affected reviews; unrelated typos do not invalidate every review. This is a documented gate, not runtime enforcement or human product approval. See [context-review ritual](../../rituals/context-review.md).

FILE:deskops/services/review.py
"""Cold context review service behind ``deskops review`` (GC03).

This replaces the two governed ``context_review.py`` scripts with a CLI command
(plan gates-por-tipo, D10). Every run writes the evidence the ritual asks for
under ``runs/subagents/<run>/context-review/<key>/<input sha256>/attempt-N/``
(``input.md``, ``manifest.json``, ``output.md``, ``stderr.log``, ``receipt.json``)
and one ``ReviewDoc`` receipt under ``desk/reviews/``.

Modes:
  node <plan-dir> [IDS...]   review drawer dag.yaml nodes (contract + neighbours + gates)
  preflight <task>           TaskDoc-only review before dispatch
  bundle <task>              cold bundle: TaskDoc + routed rituals + pills + atoms + files + validation
  status [task | plan-dir]   compare current inputs with recorded reviews; no model call
  dispose <review-id>        write the verdict on one pending receipt
  record <task> --kind K     reproduction/goldens/owner receipt from operator evidence; no model call

Caps (owner, D9): an unchanged input is not reviewed again; ``--max-attempts``
(default 2) refuses another *good* attempt on the same key unless ``--force`` with
``--reason``. Transport failures (non-zero exit, timeout, or output without the
``REFORMULACION`` section) do not count against the cap and are recorded as
``technical_ok: false`` with a ``verdict: incomplete`` / ``reason: technical``
receipt, kept separate from comprehension findings (ritual step 5).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml
from sldb.api.stores.doc_status import doc_status
from sldb.runtime.validation import extract_model_data

from deskops import doc_access
from deskops.config import DeskConfig
from deskops.errors import DomainError
from deskops.errors import UsageError
from deskops.models import ReviewDoc
from deskops.models import RuntimeProfileDoc
from deskops.models import TaskDoc
from deskops.models import BoardDoc


# The verified reviewer profile from desk/rituals/context-review.md step 3 (D4).
SYSTEM = (
    "Revisor barato aislado de un encargo de planificación. Trabajas solo con el input explícito: "
    "sin herramientas, historial ni otras fuentes. No ejecutas nada. Responde en español con estas "
    "secciones exactas: REFORMULACION (propósito, resultado, repo, límites), AMBIGUEDADES (numeradas, "
    'cada una con cita textual del input y qué obligaría a inventar; escribe "ninguna" si no hay), '
    "DRY-RUN (lecturas, cambios previstos, dependencias y validaciones futuras, sin ejecutar), "
    "FUTURO (lo que produce otro nodo o decide un humano, no ambigüedad). "
    "REFORMULACION describe el encargo del nodo, no esta revisión. DRY-RUN describe cómo lo ejecutaría "
    "un ejecutor futuro, hipotéticamente y sin ejecutar nada. Si el nodo es un agregado o paquete no "
    "ejecutable, dilo y además recorre cómo lo cumplen sus hijos, qué transfiere cada uno al siguiente "
    "y cómo se valida el resultado conjunto. Máximo 350 palabras."
)
SELECTION = "deepseek-flash: perfil barato verificado en esta máquina por ritual-context-review (D4)"
MODEL = "deepseek/deepseek-flash"
DEFAULT_ENGINE = "runtime-pi-deepseek-flash"
TIMEOUT = 900
# Receipts ``deskops review record`` writes by hand (no model call); the others come from their command.
# Kinds an operator records by hand. ``preflight`` and ``bundle`` also come from their own
# model review; a hand-recorded one keeps ``engine: human`` so it never reads as a model review.
RECORD_KINDS = ("reproduction", "goldens", "owner", "preflight", "bundle")

# Recorded by hand, ``preflight`` and ``bundle`` name their operator (``--operator``) and say
# why no model reviewed them; they are for desks without a model (CI scenarios, the quickstart),
# not a substitute for ``deskops review preflight|bundle`` on a real desk.
HUMAN_REVIEW_KINDS = ("preflight", "bundle")
NO_MODEL_REASON = "no model available"

KEEP = (
    "id",
    "title",
    "kind",
    "owner_repo",
    "node_role",
    "parent_id",
    "children",
    "scope",
    "acceptance",
    "output_scope",
    "depends_on",
    "requires",
)
BASE = ["context-review-guide.md", "brief.md", "alcance.md", "decisiones.md"]


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _coerce_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


class Bundle:
    """Accumulates the explicit input.md parts and their per-source hashes."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.sources: list[dict[str, Any]] = []
        self.omitted: list[dict[str, Any]] = []

    def add(self, path: str, text: str, projection: str = "whole_file") -> None:
        self.parts.append(f"FILE:{path}\n{text.rstrip()}\n")
        self.sources.append({"path": path, "sha256": _sha(text.encode()), "projection": projection})

    def omit(self, path: str, reason: str, size: int | None = None) -> None:
        record: dict[str, Any] = {"path": path, "reason": reason}
        if size is not None:
            record["size"] = size
        self.omitted.append(record)

    def close(self, instruction: str) -> bytes:
        self.parts.append(f"FILE:instruccion\n{instruction}\n")
        return "".join(part + "\n" for part in self.parts).encode()


def _technical_ok(attempt_dir: Path) -> bool:
    receipt = attempt_dir / "receipt.json"
    if not receipt.exists():
        return False
    try:
        return bool(json.loads(receipt.read_text(encoding="utf-8")).get("technical_ok"))
    except Exception:
        return False


class ReviewService:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"

    # ------------------------------------------------------------------ paths
    def _reviews_dir(self) -> Path:
        return self.desk_root / "reviews"

    def _evidence_root(self, run_name: str) -> Path:
        return self.root / "runs" / "subagents" / run_name / "context-review"

    def _key_attempts(self, key: str) -> list[Path]:
        base = self.root / "runs" / "subagents"
        if not base.exists():
            return []
        return sorted(base.glob(f"*/context-review/{key}/*/attempt-*"))

    def _identity(self) -> str:
        identity = (DeskConfig.load(self.desk_root).project_identity or "").strip()
        if identity and identity != "unknown-project":
            return identity
        return self.root.name

    # ------------------------------------------------------------------ engine
    def _load_engine(self, engine_id: str) -> dict[str, Any]:
        directory = self.desk_root / "runtimes"
        for path in sorted(directory.glob("*.md")) if directory.exists() else []:
            try:
                data = extract_model_data(RuntimeProfileDoc, path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if data.get("id") == engine_id or path.stem == engine_id:
                return data
        raise DomainError(
            f"RuntimeProfileDoc '{engine_id}' not found under {directory}; "
            f"seed it with `deskops init` / `deskops desk update --apply` or write it by hand."
        )

    def _argv(self, engine: dict[str, Any], input_path: Path) -> list[str]:
        argv = [str(engine.get("binary") or "pi")]
        argv += [str(item) for item in (engine.get("extra_args") or [])]
        if engine.get("system_prompt_flag") and engine.get("system_prompt"):
            argv += [str(engine["system_prompt_flag"]), str(engine["system_prompt"])]
        argv.append(f"@{input_path}")
        return argv

    # ------------------------------------------------------------------ tasks
    def _task_path(self, task_id: str) -> Path:
        tasks_dir = self.desk_root / "tasks"
        try:
            return doc_access.resolve_document(self.root, tasks_dir, task_id, "task", recursive=False)
        except FileNotFoundError:
            raise DomainError(f"Task '{task_id}' not found under {tasks_dir}") from None

    def _resolve_task(self, selector: str) -> tuple[Path, str]:
        """The task file a selector names and the task's full id (its frontmatter ``id``, else the
        file stem). Receipts are keyed and anchored on that id, never on the selector as typed:
        ``task-cc37`` would otherwise give ``doc:<Model>:task-cc37``, a subject no rule matches."""
        task_path = self._task_path(selector)
        task_id = str(self._task_payload(task_path).get("id") or "").strip() or task_path.stem
        return task_path, task_id

    def _task_model(self, task_path: Path) -> str:
        store = self.root / ".sldb"
        if not store.exists():
            return "TaskDoc"
        try:
            status = doc_status(store, task_path.relative_to(self.root).as_posix())
        except Exception:
            return "TaskDoc"
        return status.model or "TaskDoc" if status.exists else "TaskDoc"

    def _task_payload(self, task_path: Path) -> dict[str, Any]:
        return extract_model_data(TaskDoc, task_path.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------ bundle
    def _preflight_input(self, task_path: Path, task_id: str) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        rel = task_path.relative_to(self.root).as_posix()
        bundle.add(rel, task_path.read_text(encoding="utf-8"))
        instruction = (
            f"Preflight solo-TaskDoc de la tarea {task_id}: reformula el encargo tal como lo leería "
            "un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y "
            "da el DRY-RUN sin ejecutar nada. No ejecutes nada."
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    def _resolve_pill(self, ref: str) -> Path | None:
        ref = ref.strip()
        if not ref:
            return None
        candidate = Path(ref)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            return candidate
        try:
            return doc_access.resolve_document(self.root, self.desk_root / "contexts", ref, "pill")
        except (FileNotFoundError, ValueError):
            return None

    def _resolve_atom(self, ref: str) -> Path | None:
        ref = ref.strip()
        if not ref:
            return None
        candidate = Path(ref)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            return candidate
        atom_id = ref.removeprefix("atom:")
        matches = [path for path in (self.desk_root / "atoms").rglob("*.md") if path.stem == atom_id]
        if len(matches) == 1:
            return matches[0]
        return None

    def _bundle_input(self, task_path: Path, task_id: str) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        payload = self._task_payload(task_path)

        # 1. TaskDoc
        rel = task_path.relative_to(self.root).as_posix()
        bundle.add(rel, task_path.read_text(encoding="utf-8"))

        # 2. Rituals routed by the Board (desk/tasks/Board.md), in order.
        board_path = self.desk_root / "tasks" / "Board.md"
        rituals: list[str] = []
        if board_path.is_file():
            try:
                board = extract_model_data(BoardDoc, board_path.read_text(encoding="utf-8"))
                rituals = [str(item) for item in (board.get("rituals") or [])]
            except Exception:
                rituals = []
        if rituals:
            for ritual_ref in rituals:
                ritual_path = Path(ritual_ref)
                if not ritual_path.is_absolute():
                    ritual_path = self.root / ritual_path
                if ritual_path.is_file():
                    bundle.add(ritual_path.relative_to(self.root).as_posix(), ritual_path.read_text(encoding="utf-8"))
                else:
                    bundle.omit(ritual_ref, "missing")
        else:
            bundle.omit("desk/tasks/Board.md rituals", "missing")

        # 3. Bound pills (TaskDoc.pills), in order.
        for pill_ref in _coerce_list(payload.get("pills")):
            pill_path = self._resolve_pill(pill_ref)
            if pill_path is not None:
                bundle.add(pill_path.relative_to(self.root).as_posix(), pill_path.read_text(encoding="utf-8"))
            else:
                bundle.omit(pill_ref, "unresolved")

        # 4. Bound atoms (TaskDoc.atoms), in order.
        for atom_ref in _coerce_list(payload.get("atoms")):
            atom_path = self._resolve_atom(atom_ref)
            if atom_path is not None:
                bundle.add(atom_path.relative_to(self.root).as_posix(), atom_path.read_text(encoding="utf-8"))
            else:
                bundle.omit(atom_ref, "unresolved")

        # 5. Files the TaskDoc names, under 60 KB, files only, present.
        for file_ref in _coerce_list(payload.get("files")):
            file_path = Path(file_ref)
            if not file_path.is_absolute():
                file_path = self.root / file_path
            if not file_path.exists():
                bundle.omit(file_ref, "missing")
                continue
            if file_path.is_dir():
                bundle.omit(file_ref, "directory")
                continue
            size = file_path.stat().st_size
            if size >= 60_000:
                bundle.omit(file_ref, "size>=60000", size=size)
                continue
            bundle.add(file_ref, file_path.read_text(encoding="utf-8", errors="replace"))

        # 6. The TaskDoc validation section as the instruction.
        validation = _coerce_list(payload.get("validation"))
        validation_text = "\n".join(f"- {item}" for item in validation) if validation else "(sin validación declarada)"
        instruction = (
            f"Cold-bundle de la tarea {task_id}: con el TaskDoc, los rituales enrutados por el Board, "
            "las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el "
            "encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. "
            "No ejecutes nada.\n\nSección de validación del TaskDoc:\n" + validation_text
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    # ------------------------------------------------------------------ node
    def _load_dag(self, plan_dir: Path) -> tuple[dict, dict]:
        dag_path = plan_dir / "dag.yaml"
        if not dag_path.is_file():
            raise DomainError(f"No dag.yaml in plan directory {plan_dir}")
        try:
            dag = yaml.safe_load(dag_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise DomainError(f"Could not parse {dag_path}: {exc}") from exc
        nodes: dict[str, dict] = {}
        for task in dag.get("tasks") or []:
            nodes[task["id"]] = task
        for package in (dag.get("hierarchy") or {}).get("packages") or []:
            nodes[package["id"]] = package
        root = (dag.get("hierarchy") or {}).get("root")
        if root:
            nodes[root["id"]] = root
        return dag, nodes

    def _plan_nodes(self, dag: dict) -> list[str]:
        order: list[str] = []
        root = (dag.get("hierarchy") or {}).get("root")
        if root:
            order.append(root["id"])
        for package in (dag.get("hierarchy") or {}).get("packages") or []:
            order.append(package["id"])
        for task in dag.get("tasks") or []:
            order.append(task["id"])
        return list(dict.fromkeys(order))

    @staticmethod
    def _contract(node: dict) -> dict:
        return {key: node[key] for key in KEEP if key in node}

    @staticmethod
    def _neighbours(dag: dict, nodes: dict, node: dict) -> tuple[list[dict], dict]:
        tasks = {task["id"]: task for task in dag.get("tasks") or []}
        packages = {package["id"] for package in (dag.get("hierarchy") or {}).get("packages") or []}
        node_id = node["id"]
        if node_id == "ROOT":
            ids = list(node.get("children") or [])
        elif node_id in packages:
            ids = list(node.get("children") or [])
            inside = set(ids)
            for child in ids[:]:
                ids += [x for x in (tasks.get(child) or {}).get("depends_on") or [] if x not in inside]
        else:
            ids = list(node.get("depends_on") or [])
            ids += [task["id"] for task in (dag.get("tasks") or []) if node_id in (task.get("depends_on") or [])]
            ids += [node.get("parent_id") or ""]
        ids = list(dict.fromkeys(item for item in ids if item and item != node_id))
        gates_ids = list(node.get("requires") or [])
        gates_ids += [
            gate for gate, value in (dag.get("gates") or {}).items()
            if isinstance(value, dict) and value.get("produced_by") == node_id
        ]
        gates_ids += [
            gate for gate in (dag.get("gates") or {}) if gate in str(ReviewService._contract(node))
        ]
        return [nodes[item] for item in ids if item in nodes], {
            gate: (dag.get("gates") or {})[gate] for gate in dict.fromkeys(gates_ids) if gate in (dag.get("gates") or {})
        }

    def _node_input(self, plan_dir: Path, dag: dict, nodes: dict, node: dict) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        plan_rel = plan_dir.relative_to(self.root).as_posix()
        for rel in BASE:
            source = plan_dir / rel
            if source.is_file():
                bundle.add(f"{plan_rel}/{rel}", source.read_text(encoding="utf-8"))
            else:
                bundle.omit(f"{plan_rel}/{rel}", "missing")

        node_id = node["id"]
        bundle.add(f"{plan_rel}/dag.yaml#node:{node_id}", yaml.safe_dump(self._contract(node), allow_unicode=True, sort_keys=False), "node_contract")
        neighbours, gates = self._neighbours(dag, nodes, node)
        for neighbour in neighbours:
            bundle.add(f"{plan_rel}/dag.yaml#edge:{neighbour['id']}", yaml.safe_dump(self._contract(neighbour), allow_unicode=True, sort_keys=False), "edge_contract")
        if gates:
            bundle.add(f"{plan_rel}/dag.yaml#gates", yaml.safe_dump(gates, allow_unicode=True, sort_keys=False), "gate_contracts")

        is_aggregate = node_id == "ROOT" or node_id.startswith("PK")
        instruction = (
            f"Revisa el nodo {node_id} siguiendo context-review-guide.md. "
            + (
                "Es un agregado: reformula el resultado sustantivo del paquete y da un DRY-RUN hipotético de "
                "sus hijos en orden, con entradas y salidas entre ellos y la validación conjunta. "
                if is_aggregate
                else ""
            )
            + "Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada."
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    def _find_plan_dir(self, plan_id: str) -> Path | None:
        plans_root = self.desk_root / "drawer" / "plans"
        if not plans_root.exists():
            return None
        for dag_path in sorted(plans_root.rglob("dag.yaml")):
            try:
                dag = yaml.safe_load(dag_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(dag, dict) and dag.get("id") == plan_id:
                return dag_path.parent
        return None

    # ------------------------------------------------------------------ caps
    def _next_attempt_dir(
        self,
        run_name: str,
        key: str,
        input_sha256: str,
        max_attempts: int,
        force: bool,
    ) -> Path | None:
        attempts = self._key_attempts(key)
        prior = [attempt for attempt in attempts if attempt.parent.name == input_sha256]
        if prior and any(_technical_ok(attempt) for attempt in prior) and not force:
            return None  # unchanged input already reviewed
        good = sum(1 for attempt in attempts if _technical_ok(attempt))
        if not prior and good >= max_attempts and not force:
            raise DomainError(
                f"{key}: {good} intentos ya; tope --max-attempts {max_attempts} "
                "(usa --force con --reason si el input cambió de verdad)"
            )
        out = self._evidence_root(run_name) / key / input_sha256 / f"attempt-{len(prior) + 1}"
        out.mkdir(parents=True, exist_ok=True)
        return out

    # ------------------------------------------------------------------ run
    def _run_one(
        self,
        *,
        run_name: str,
        key: str,
        input_data: bytes,
        sources: list[dict],
        omitted: list[dict],
        engine_id: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
        kind: str,
        subject: str,
        subject_ref: str,
        node_id: str | None,
        plan_id: str | None = None,
    ) -> dict[str, Any]:
        input_sha256 = _sha(input_data)
        attempt_dir = self._next_attempt_dir(run_name, key, input_sha256, max_attempts, force)
        if attempt_dir is None:
            return {"key": key, "state": "unchanged", "input_sha256": input_sha256}

        (attempt_dir / "input.md").write_bytes(input_data)
        engine = self._load_engine(engine_id)
        argv = self._argv(engine, attempt_dir / "input.md")
        start = _now()
        try:
            result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
            stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired as exc:
            detail = ""
            if isinstance(getattr(exc, "stderr", None), bytes):
                detail = exc.stderr.decode(errors="replace")
            elif isinstance(getattr(exc, "stderr", None), str):
                detail = exc.stderr or ""
            stdout, stderr, returncode = "", f"timeout after {timeout}s\n{detail}", None
        end = _now()

        (attempt_dir / "output.md").write_text(stdout, encoding="utf-8")
        (attempt_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        technical_ok = returncode == 0 and "REFORMULACION" in stdout

        manifest: dict[str, Any] = {
            "key": key,
            "input_sha256": input_sha256,
            "argv": argv,
            "model": MODEL,
            "profile": engine_id,
            "selection_reason": SELECTION,
            "sources": sources,
            "omitted_sources": omitted,
            "started": start,
            "finished": end,
        }
        if force and reason:
            manifest["retry_reason"] = reason
        (attempt_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        receipt: dict[str, Any] = {
            "key": key,
            "technical_ok": technical_ok,
            "returncode": returncode,
            "input_sha256": input_sha256,
            "output_sha256": _sha(stdout.encode()),
            "start": start,
            "end": end,
        }
        (attempt_dir / "receipt.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        run_dir = attempt_dir.relative_to(self.root).as_posix()
        if technical_ok:
            verdict = "pending"
            review_reason = reason if force else ""
        else:
            verdict = "incomplete"
            review_reason = "technical"

        review_id, review_path = self._write_review(
            kind=kind,
            subject=subject,
            subject_ref=subject_ref,
            engine=engine_id,
            run_dir=run_dir,
            input_sha256=input_sha256,
            output_sha256=receipt["output_sha256"],
            verdict=verdict,
            reason=review_reason,
            node_id=node_id,
            plan_id=plan_id,
        )

        return {
            "key": key,
            "state": "reviewed" if technical_ok else "technical_failure",
            "input_sha256": input_sha256,
            "review_id": review_id,
            "review_path": review_path.relative_to(self.root).as_posix(),
            "run_dir": run_dir,
            "technical_ok": technical_ok,
        }

    def _next_review_number(self, review_dir: Path, kind: str, node: bool) -> int:
        if not review_dir.exists():
            return 1
        prefix = "node-" if node else f"{kind}-"
        matches = [path for path in review_dir.glob(f"{prefix}*.md") if path.stem.startswith(prefix)]
        return len(matches) + 1

    def _write_review(
        self,
        *,
        kind: str,
        subject: str,
        subject_ref: str,
        engine: str,
        run_dir: str,
        input_sha256: str,
        output_sha256: str,
        verdict: str,
        reason: str,
        node_id: str | None,
        plan_id: str | None = None,
        summary: str | None = None,
        actor: str | None = None,
        title: str | None = None,
    ) -> tuple[str, Path]:
        if node_id is not None:
            node_lower = node_id.lower()
            plan_id = plan_id or (subject_ref.split("/dag.yaml#node:", 1)[0].rsplit("/", 1)[-1] if "/" in subject_ref else "")
            review_dir = self._reviews_dir() / f"{plan_id}-{node_lower}"
            n = self._next_review_number(review_dir, kind, node=True)
            review_id = f"review-{plan_id}-{node_lower}-node-{n}"
            title = title or f"Node review of {node_id}"
        else:
            task_id = subject.rsplit(":", 1)[-1].split("@", 1)[0]
            review_dir = self._reviews_dir() / task_id
            n = self._next_review_number(review_dir, kind, node=False)
            review_id = f"review-{task_id}-{kind}-{n}"
            title = title or f"{kind.capitalize()} review of {task_id}"

        path = review_dir / (f"node-{n}.md" if node_id is not None else f"{kind}-{n}.md")
        payload: dict[str, Any] = {
            "id": review_id,
            "title": title,
            "kind": kind,
            "subject": subject,
            "subject_ref": subject_ref,
            "engine": engine,
            "actor": actor or self._identity(),
            "run_dir": run_dir,
            "input_sha256": input_sha256,
            "output_sha256": output_sha256,
            "verdict": verdict,
            "reason": reason,
            "created_at": _now(),
            "disposed_at": "",
            "disposed_by": "",
            "summary": summary if summary is not None else f"{kind} review; engine {engine}; evidence under {run_dir}.",
            "disposition": "",
            "tags": ["workspace:desk"],
        }
        doc_access.create_doc(self.root, path, ReviewDoc, payload, review_id)
        return review_id, path

    # ------------------------------------------------------------------ record
    def record_receipt(
        self, task_id: str, kind: str, evidence: list[str], reason: str, operator: str | None = None
    ) -> dict[str, Any]:
        """A receipt the desk operator records without a model call (reproduction, goldens, owner,
        and preflight or bundle from operator evidence, always with ``engine: human``).

        Every ``evidence`` path must be an existing file inside the root; otherwise nothing is
        written. ``input_sha256`` hashes ``<path>\\n<content>\\n`` of each file, paths POSIX-relative
        to the root, sorted, without repeats (b1); empty without evidence. The verdict stays
        ``pending`` until ``deskops review dispose`` (r4).
        """
        if kind not in RECORD_KINDS:
            raise UsageError(
                f"--kind {kind} is not recorded by hand; use one of {', '.join(RECORD_KINDS)} "
                "(node comes from its own review command)"
            )
        if not (reason and reason.strip()):
            raise UsageError("--reason is required")
        operator = (operator or "").strip()
        if kind in HUMAN_REVIEW_KINDS and not operator:
            raise UsageError(
                f"--kind {kind} recorded by hand requires --operator <name>: the receipt names the "
                f"human who reviewed instead of a model ({NO_MODEL_REASON})"
            )
        paths: list[str] = []
        for raw in evidence:
            candidate = Path(raw)
            if not candidate.is_absolute():
                candidate = self.root / candidate
            resolved = candidate.resolve()
            if not resolved.is_relative_to(self.root) or not resolved.is_file():
                raise DomainError(f"evidence not found: {raw}")
            paths.append(resolved.relative_to(self.root).as_posix())
        paths = sorted(set(paths))
        if not paths and kind != "owner":
            raise UsageError(f"--kind {kind} requires at least one --evidence")

        task_path, task_id = self._resolve_task(task_id)
        subject = f"doc:{self._task_model(task_path)}:{task_id}"
        input_sha256 = ""
        if paths:
            data = b"".join(rel.encode() + b"\n" + (self.root / rel).read_bytes() + b"\n" for rel in paths)
            input_sha256 = _sha(data)
        actor = operator or self._identity()
        summary = f"{kind} receipt recorded by {actor}; evidence: {', '.join(paths) if paths else '(none)'}"
        title = None
        if kind in HUMAN_REVIEW_KINDS:
            summary = (
                f"{kind} receipt recorded by hand by operator {operator}, not by a model review "
                f"(engine human; {NO_MODEL_REASON}); evidence: {', '.join(paths)}"
            )
            title = f"{kind.capitalize()} receipt of {task_id} by operator {operator} ({NO_MODEL_REASON})"
        review_id, review_path = self._write_review(
            kind=kind,
            subject=subject,
            subject_ref="",
            engine="human",
            run_dir="",
            input_sha256=input_sha256,
            output_sha256="",
            verdict="pending",
            reason=reason,
            node_id=None,
            summary=summary,
            actor=actor,
            title=title,
        )
        return {
            "key": f"{task_id}/{kind}",
            "state": "recorded",
            "review_id": review_id,
            "review_path": review_path.relative_to(self.root).as_posix(),
            "evidence": paths,
            "input_sha256": input_sha256,
            "engine": "human",
            "operator": actor,
            "no_model_reason": NO_MODEL_REASON if kind in HUMAN_REVIEW_KINDS else "",
        }

    # ------------------------------------------------------------------ dispose
    def dispose(self, review_id: str, verdict: str, reason: str) -> dict[str, Any]:
        path = self._resolve_review_path(review_id)
        payload = doc_access.read_doc(path, ReviewDoc)
        if (payload.get("verdict") or "pending") != "pending":
            raise DomainError(f"Review '{review_id}' already has verdict '{payload.get('verdict')}'; only a pending review can be disposed.")
        payload["verdict"] = verdict
        payload["reason"] = reason
        payload["disposed_at"] = _now()
        payload["disposed_by"] = self._identity()
        payload["disposition"] = f"Verdict {verdict}: {reason}"
        doc_access.write_doc(self.root, path, ReviewDoc, payload)
        return {
            "review_id": review_id,
            "verdict": verdict,
            "reason": reason,
            "disposed_at": payload["disposed_at"],
            "disposed_by": payload["disposed_by"],
        }

    def _resolve_review_path(self, review_id: str) -> Path:
        reviews_dir = self._reviews_dir()
        matches: list[Path] = []
        for path in sorted(reviews_dir.rglob("*.md")):
            try:
                payload = extract_model_data(ReviewDoc, path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if payload.get("id") == review_id:
                matches.append(path)
        if not matches:
            raise DomainError(f"Review '{review_id}' not found under {reviews_dir}")
        if len(matches) > 1:
            names = ", ".join(str(path.relative_to(self.desk_root)) for path in matches)
            raise DomainError(f"Ambiguous review selector '{review_id}': {names}")
        return matches[0]

    # ------------------------------------------------------------------ status
    def _review_records(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        reviews_dir = self._reviews_dir()
        if not reviews_dir.exists():
            return records
        for path in sorted(reviews_dir.rglob("*.md")):
            try:
                records.append(extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")))
            except Exception:
                continue
        return records

    def _state_for_key(self, key: str, input_data: bytes) -> dict[str, Any]:
        current_sha = _sha(input_data)
        records = [
            record
            for record in self._review_records()
            if self._record_key(record) == key
        ]
        if not records:
            state = "missing"
        else:
            current = [record for record in records if record.get("input_sha256") == current_sha]
            verdicts = {record.get("verdict") for record in current}
            if not current:
                state = "stale"
            elif "accepted" in verdicts:
                state = "accepted"
            elif "rejected" in verdicts:
                state = "rejected"
            elif "pending" in verdicts:
                state = "reviewed"
            else:
                state = "technical_failure"
        return {"key": key, "state": state, "input_sha256": current_sha}

    def _record_key(self, record: dict[str, Any]) -> str:
        subject = str(record.get("subject") or "")
        subject_ref = str(record.get("subject_ref") or "")
        kind = str(record.get("kind") or "")
        if subject:
            task_id = subject.split("@", 1)[0].rsplit(":", 1)[-1]
            return f"{task_id}/{kind}"
        if subject_ref:
            node_id = subject_ref.rsplit("#node:", 1)[-1]
            plan_path = subject_ref.split("#node:", 1)[0]
            plan_dir = Path(plan_path)
            if not plan_dir.is_absolute():
                plan_dir = self.root / plan_dir
            try:
                dag = yaml.safe_load((plan_dir / "dag.yaml").read_text(encoding="utf-8"))
                plan_id = dag["id"]
            except Exception:
                plan_id = plan_path.rsplit("/", 1)[-1]
            return f"{plan_id}/{node_id}"
        return f"unknown/{kind}"

    def status(self, target: str | None) -> list[dict[str, Any]]:
        if target:
            if self._is_plan_dir(target):
                return self._status_plan(target)
            return self._status_task(target)
        # No target: every key that has at least one ReviewDoc.
        keys: list[str] = []
        for record in self._review_records():
            key = self._record_key(record)
            if key not in keys and not key.startswith("unknown/"):
                keys.append(key)
        reports: list[dict[str, Any]] = []
        for key in keys:
            input_data = self._input_for_key(key)
            if input_data is None:
                reports.append({"key": key, "state": "missing", "input_sha256": ""})
            else:
                reports.append(self._state_for_key(key, input_data))
        return reports

    def _is_plan_dir(self, target: str) -> bool:
        plan_dir = Path(target)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        return (plan_dir / "dag.yaml").is_file()

    def _status_task(self, task_id: str) -> list[dict[str, Any]]:
        task_path, task_id = self._resolve_task(task_id)
        reports: list[dict[str, Any]] = []
        for mode, builder in (
            ("preflight", self._preflight_input),
            ("bundle", self._bundle_input),
        ):
            input_data, _, _ = builder(task_path, task_id)
            reports.append(self._state_for_key(f"{task_id}/{mode}", input_data))
        return reports

    def _status_plan(self, plan_dir_str: str) -> list[dict[str, Any]]:
        plan_dir = Path(plan_dir_str)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        dag, nodes = self._load_dag(plan_dir)
        reports: list[dict[str, Any]] = []
        for node_id in self._plan_nodes(dag):
            node = nodes[node_id]
            input_data, _, _ = self._node_input(plan_dir, dag, nodes, node)
            reports.append(self._state_for_key(f"{dag['id']}/{node_id}", input_data))
        return reports

    def _input_for_key(self, key: str) -> bytes | None:
        if "/preflight" in key or "/bundle" in key:
            task_id, _, mode = key.rpartition("/")
            if mode not in {"preflight", "bundle"}:
                return None
            try:
                task_path = self._task_path(task_id)
            except DomainError:
                return None
            builder = self._preflight_input if mode == "preflight" else self._bundle_input
            input_data, _, _ = builder(task_path, task_id)
            return input_data
        # node key <plan-id>/<NODE>
        parts = key.split("/", 1)
        if len(parts) != 2:
            return None
        plan_id, node_id = parts
        plan_dir = self._find_plan_dir(plan_id)
        if plan_dir is None:
            return None
        dag, nodes = self._load_dag(plan_dir)
        node = nodes.get(node_id)
        if node is None:
            return None
        input_data, _, _ = self._node_input(plan_dir, dag, nodes, node)
        return input_data

    # ------------------------------------------------------------------ public run
    def run_task(
        self,
        mode: str,
        task_id: str,
        *,
        run_name: str,
        engine: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
    ) -> dict[str, Any]:
        if force and not (reason and reason.strip()):
            raise UsageError("--force requires --reason (recorded in manifest.json and the ReviewDoc)")
        task_path, task_id = self._resolve_task(task_id)
        model = self._task_model(task_path)
        subject = f"doc:{model}:{task_id}"
        builder = self._preflight_input if mode == "preflight" else self._bundle_input
        input_data, sources, omitted = builder(task_path, task_id)
        return self._run_one(
            run_name=run_name,
            key=f"{task_id}/{mode}",
            input_data=input_data,
            sources=sources,
            omitted=omitted,
            engine_id=engine,
            max_attempts=max_attempts,
            force=force,
            reason=reason,
            timeout=timeout,
            kind=mode,
            subject=subject,
            subject_ref="",
            node_id=None,
        )

    def run_nodes(
        self,
        plan_dir_str: str,
        ids: list[str],
        *,
        run_name: str,
        engine: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
    ) -> list[dict[str, Any]]:
        if force and not (reason and reason.strip()):
            raise UsageError("--force requires --reason (recorded in manifest.json and the ReviewDoc)")
        plan_dir = Path(plan_dir_str)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        dag, nodes = self._load_dag(plan_dir)
        plan_rel = plan_dir.relative_to(self.root).as_posix()
        selected = ids or self._plan_nodes(dag)
        reports: list[dict[str, Any]] = []
        for node_id in selected:
            if node_id not in nodes:
                raise DomainError(f"Unknown node '{node_id}' in {plan_dir / 'dag.yaml'}")
            node = nodes[node_id]
            input_data, sources, omitted = self._node_input(plan_dir, dag, nodes, node)
            reports.append(
                self._run_one(
                    run_name=run_name,
                    key=f"{dag['id']}/{node_id}",
                    input_data=input_data,
                    sources=sources,
                    omitted=omitted,
                    engine_id=engine,
                    max_attempts=max_attempts,
                    force=force,
                    reason=reason,
                    timeout=timeout,
                    kind="node",
                    subject="",
                    subject_ref=f"{plan_rel}/dag.yaml#node:{node_id}",
                    node_id=node_id,
                    plan_id=dag["id"],
                )
            )
        return reports

FILE:tests/test_review_command.py
"""GC03: ``deskops review`` — cold context reviews and their disposition.

Each test runs in a temporary desk with a fake ``pi`` executable placed first on
``PATH``. The fake prints a ``REFORMULACION`` section (or fails) and counts its
invocations, so no test ever calls the real model or touches the network.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from sldb.runtime.validation import extract_model_data

from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
PLAN_SRC = ROOT / "desk" / "drawer" / "plans" / "gates-por-tipo"


FAKE_PI = """#!/usr/bin/env python3
import os
import sys
import time

log = os.environ.get("FAKE_PI_LOG")
if log:
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(" ".join(sys.argv[1:]) + "\\n")

mode = os.environ.get("FAKE_PI_MODE", "ok")
if mode == "fail":
    sys.exit(1)
if mode == "no-reformulacion":
    print("sin seccion")
    sys.exit(0)
if mode == "sleep":
    time.sleep(5)
    print("REFORMULACION\\nDRY-RUN: nada.")
    sys.exit(0)
print(
    "REFORMULACION\\n"
    "Propósito: revisar el encargo.\\n"
    "AMBIGUEDADES: ninguna.\\n"
    "DRY-RUN: leer, proponer, validar, sin ejecutar.\\n"
    "FUTURO: otro nodo o un humano."
)
sys.exit(0)
"""


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, (str(ROOT), env.get("PYTHONPATH"))))
    return env


def _run(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*argv], cwd=root, env=env or _env(), capture_output=True, text=True)


def _deskops(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return _run(root, *CLI, *argv, "--root", str(root), env=env)


@pytest.fixture
def fake_pi(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pi = bin_dir / "pi"
    pi.write_text(FAKE_PI, encoding="utf-8")
    pi.chmod(0o755)
    log = tmp_path / "pi.log"
    monkeypatch.setenv("FAKE_PI_LOG", str(log))
    monkeypatch.setenv("FAKE_PI_MODE", "ok")
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return bin_dir, log


def _pi_calls(log: Path) -> int:
    if not log.exists():
        return 0
    return len([line for line in log.read_text(encoding="utf-8").splitlines() if line.strip()])


def _add_task(root: Path, *, title: str = "X", task_type: str = "task.code") -> str:
    result = _deskops(
        root,
        "add",
        "task",
        "--title",
        title,
        "--goal",
        "review goal",
        "--scope",
        "review scope",
        "--validation",
        "pytest",
        "--task-type",
        task_type,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return f"task-{title.lower().replace(' ', '-')}"


def _attempt_dirs(root: Path, key: str) -> list[Path]:
    base = root / "runs" / "subagents"
    if not base.exists():
        return []
    return sorted(base.glob(f"*/context-review/{key}/*/attempt-*"))


def _review_docs(root: Path) -> list[dict]:
    reviews = root / "desk" / "reviews"
    if not reviews.exists():
        return []
    docs: list[dict] = []
    for path in sorted(reviews.rglob("*.md")):
        docs.append(extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")))
    return docs


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_preflight_writes_attempt_evidence_and_receipt(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 1
    attempt = attempts[0]
    assert attempt.name == "attempt-1"
    for name in ("input.md", "manifest.json", "output.md", "stderr.log", "receipt.json"):
        assert (attempt / name).is_file(), name

    input_bytes = (attempt / "input.md").read_bytes()
    assert input_bytes.decode().startswith("FILE:desk/tasks/task-x.md\n")

    manifest = _json(attempt / "manifest.json")
    assert manifest["input_sha256"] == __import__("hashlib").sha256(input_bytes).hexdigest()
    assert manifest["sources"][0]["path"] == "desk/tasks/task-x.md"
    assert manifest["argv"][0] == "pi"
    assert manifest["argv"][-1].startswith("@")

    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is True
    assert receipt["returncode"] == 0
    assert receipt["input_sha256"] == manifest["input_sha256"]

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "pending"
    assert doc["subject"] == "doc:TaskCodeDoc:task-x"
    assert doc["run_dir"] == attempt.relative_to(root).as_posix()
    assert doc["input_sha256"] == manifest["input_sha256"]
    assert doc["output_sha256"] == receipt["output_sha256"]


def test_unchanged_second_run_is_reviewed_and_does_not_call_the_model(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    calls_after_first = _pi_calls(_log)
    assert calls_after_first == 1

    second = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert second.returncode == 0, second.stdout + second.stderr
    assert "unchanged" in second.stdout
    assert _pi_calls(_log) == calls_after_first
    assert len(_attempt_dirs(root, "task-x/preflight")) == 1

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "reviewed"


def test_edited_goal_is_stale_and_next_run_uses_a_new_sha(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    first_sha = _attempt_dirs(root, "task-x/preflight")[0].parent.name

    edit = _deskops(root, "edit", "task", "task-x", "goal", "goal changed")
    assert edit.returncode == 0, edit.stdout + edit.stderr

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "stale"

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    new_shas = {attempt.parent.name for attempt in attempts}
    assert first_sha in new_shas
    assert len(new_shas) == 2


def test_bundle_includes_rituals_pills_and_files_in_order(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    pill = _deskops(
        root,
        "add",
        "pill",
        "--title",
        "Guardrail",
        "--what",
        "keep layers clean",
        "--why",
        "safety",
        "--when",
        "always",
        "--where",
        "desk",
        "--how",
        "read first",
        "--how-not",
        "skip it",
    )
    assert pill.returncode == 0, pill.stdout + pill.stderr
    assert _deskops(root, "bind", "pill", "task-x", "pill-guardrail").returncode == 0

    doc = root / "docs" / "foo.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# Foo\nsmall file\n", encoding="utf-8")
    edit = _deskops(root, "edit", "task", "task-x", "files", '["docs/foo.md"]')
    assert edit.returncode == 0, edit.stdout + edit.stderr

    assert _deskops(root, "review", "bundle", "task-x", "--run", "test-run").returncode == 0

    attempt = _attempt_dirs(root, "task-x/bundle")[0]
    input_text = (attempt / "input.md").read_text(encoding="utf-8")
    file_headers = [line for line in input_text.splitlines() if line.startswith("FILE:")]
    assert file_headers[0] == "FILE:desk/tasks/task-x.md"
    assert "FILE:desk/rituals/phase.md" in file_headers
    assert "FILE:desk/rituals/execution.md" in file_headers
    assert "FILE:desk/rituals/testing.md" in file_headers
    assert "FILE:desk/rituals/closeout.md" in file_headers
    assert "FILE:desk/contexts/pill-guardrail.md" in file_headers
    assert "FILE:docs/foo.md" in file_headers
    assert file_headers[-1] == "FILE:instruccion"

    # Order: task, rituals, pill, file, instruction.
    ordered = [
        "FILE:desk/tasks/task-x.md",
        "FILE:desk/rituals/phase.md",
        "FILE:desk/rituals/execution.md",
        "FILE:desk/rituals/testing.md",
        "FILE:desk/rituals/closeout.md",
        "FILE:desk/contexts/pill-guardrail.md",
        "FILE:docs/foo.md",
        "FILE:instruccion",
    ]
    assert file_headers == ordered


def test_node_writes_one_review_doc_per_node(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)

    result = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    node_docs = [doc for doc in _review_docs(root) if doc["kind"] == "node"]
    node_ids = [doc["id"] for doc in node_docs]
    assert "review-deskops-gates-por-tipo-gc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-pc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-root-node-1" in node_ids
    for doc in node_docs:
        assert doc["subject"] == ""
        assert doc["subject_ref"].startswith("desk/drawer/plans/gates-por-tipo/dag.yaml#node:")
        assert doc["verdict"] == "pending"


def test_dispose_writes_the_verdict_and_a_second_dispose_fails(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0

    disposed = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "accepted",
        "--reason",
        "looks right",
    )
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "accepted"
    assert doc["reason"] == "looks right"
    assert doc["disposed_at"]
    assert doc["disposed_by"]

    again = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "rejected",
        "--reason",
        "changed my mind",
    )
    assert again.returncode == 1
    assert "already has verdict" in again.stdout


def test_third_good_attempt_on_the_same_key_fails_without_force(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)
    brief = plan_dir / "brief.md"
    log = fake_pi[1]

    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change one\n", encoding="utf-8")
    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    assert _pi_calls(log) == 2

    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change two\n", encoding="utf-8")
    third = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r")
    assert third.returncode == 1
    assert "tope --max-attempts" in third.stdout
    assert _pi_calls(log) == 2


def test_transport_failure_leaves_technical_failure_and_incomplete(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "fail")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is False
    assert receipt["returncode"] == 1

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_output_without_reformulacion_is_a_transport_failure(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "no-reformulacion")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    assert _json(attempt / "receipt.json")["technical_ok"] is False
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_force_requires_reason(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--run", "test-run")
    assert result.returncode == 2
    assert "--force requires --reason" in result.stdout


def test_force_with_reason_retries_the_same_input(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    assert _pi_calls(log) == 1

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--reason", "again", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _pi_calls(log) == 2

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    manifest = _json(attempts[1] / "manifest.json")
    assert manifest["retry_reason"] == "again"
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-2"]
    assert len(docs) == 1
    assert docs[0]["reason"] == "again"


def test_init_and_desk_update_seed_the_deepseek_flash_profile_idempotently(
    tmp_path: Path,
) -> None:
    from deskops.cli.main import main

    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0

    profile = root / "desk" / "runtimes" / "runtime-pi-deepseek-flash.md"
    assert profile.is_file()
    first = profile.read_text(encoding="utf-8")

    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == first

    # An existing profile is never overwritten.
    profile.write_text("# my own profile\n", encoding="utf-8")
    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == "# my own profile\n"


@pytest.mark.parametrize(
    ("receipts", "expected"),
    [
        ([], "missing"),
        ([("old", "accepted"), ("old", "rejected"), ("old", "incomplete")], "stale"),
        ([("current", "incomplete")], "technical_failure"),
        ([("current", "incomplete"), ("current", "pending")], "reviewed"),
        ([("current", "pending"), ("current", "rejected")], "rejected"),
        ([("current", "accepted"), ("current", "rejected"), ("current", "pending"),
          ("current", "incomplete"), ("old", "rejected")], "accepted"),
        ([("old", "accepted"), ("current", "rejected")], "rejected"),
    ],
)
def test_status_classifies_only_current_receipts_without_mutating_evidence(
    lifecycle_desk: Path, receipts: list[tuple[str, str]], expected: str
) -> None:
    from deskops.cli.main import main
    from deskops.services.review import ReviewService, _sha

    root = lifecycle_desk
    assert main([
        "add", "task", "--title", "Status", "--goal", "review goal",
        "--scope", "review scope", "--validation", "pytest", "--task-type", "task.code",
        "--root", str(root),
    ]) == 0
    service = ReviewService(root)
    task_path, task_id = service._resolve_task("task-status")
    input_data, _, _ = service._preflight_input(task_path, task_id)
    for index, (identity, verdict) in enumerate(receipts):
        evidence = root / "runs" / "subagents" / f"receipt-{index}"
        evidence.mkdir(parents=True)
        (evidence / "input.md").write_bytes(input_data if identity == "current" else b"old input\n")
        (evidence / "manifest.json").write_text(json.dumps({"profile": "test", "attempt": index}))
        review_id, _ = service._write_review(
            kind="preflight", subject=f"doc:TaskCodeDoc:{task_id}", subject_ref="",
            engine="test", run_dir=evidence.relative_to(root).as_posix(),
            input_sha256=_sha(input_data) if identity == "current" else _sha(b"old input\n"),
            output_sha256=_sha(b"review output"),
            verdict="pending" if verdict in {"accepted", "rejected"} else verdict, reason="test evidence",
            node_id=None,
        )
        if verdict in {"accepted", "rejected"}:
            service.dispose(review_id, verdict, "test disposition")
    preserved = {
        path: path.read_bytes()
        for directory in (root / "desk" / "reviews", root / "runs")
        if directory.exists() for path in directory.rglob("*") if path.is_file()
    }
    reports = {item["key"]: item for item in service.status("task-status")}
    assert reports["task-status/preflight"] == {
        "key": "task-status/preflight", "state": expected, "input_sha256": _sha(input_data),
    }
    assert reports["task-status/bundle"]["state"] == "missing"
    assert all(path.read_bytes() == content for path, content in preserved.items())


@pytest.mark.parametrize("tracked", [False, True], ids=["plain", "pinned"])
def test_disposed_review_status_uses_task_identity(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], tracked: bool
) -> None:
    root = lifecycle_desk
    if not tracked:
        shutil.rmtree(root / ".sldb")
    _add_task(root, title="Identity")
    result = _deskops(root, "review", "preflight", "task-identity", "--run", "identity")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = _review_docs(root)[0]
    assert doc["subject"].startswith("doc:TaskCodeDoc:task-identity" if tracked else "doc:TaskDoc:task-identity")
    disposed = _deskops(root, "review", "dispose", doc["id"], "--verdict", "accepted", "--reason", "correct")
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    subject = _review_docs(root)[0]["subject"]
    if tracked:
        # GO07 pins the actual stored subject on disposition, not a parser fixture.
        assert "@sha256:" in subject
    else:
        assert "@" not in subject
    for target in [("task-identity",), ()]:
        status = _deskops(root, "review", "status", *target, "--format", "json")
        assert status.returncode == 0, status.stdout + status.stderr
        report = next(item for item in json.loads(status.stdout) if item["key"] == "task-identity/preflight")
        assert report["state"] == "accepted"
    edit = _deskops(root, "edit", "task", "task-identity", "goal", "changed input")
    assert edit.returncode == 0, edit.stdout + edit.stderr
    status = _deskops(root, "review", "status", "task-identity", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    assert next(item for item in json.loads(status.stdout) if item["key"] == "task-identity/preflight")["state"] == "stale"

FILE:instruccion
Cold-bundle de la tarea task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

