FILE:desk/tasks/task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0.md
---
sldb:
  by: agent
  at: '2026-11-16T05:02:26Z'
  authority: generated
  via: save_document_payload
id: task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0
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
- deskops/cli/commands/desk.py
- tests/test_cli.py
- tests/fixtures/golden/scaffold/update.json
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-desk-update-crea-desk-reviews-vac-o-y-git-no-lo-guarda-en-un-clon-limpio-el-dry-run-vuelve-a-dar-missing-desk-structure-desk-reviews.md
---

# desk update deja de exigir desk/reviews/ vacio y en un clon limpio el dry-run da rc 0

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (worker de graph_ui, 2026-11-10, commit d98fcea): `deskops desk update --apply` crea desk/reviews/ vacio; git no versiona directorios vacios, y en un clon limpio `deskops desk update` (dry-run) vuelve a reportar 'Missing desk structure: desk/reviews/' con rc 1. Sigue hoy en deskops/cli/commands/desk.py:231-232. doctor no lo exige (deskops/cli/commands/doctor.py:66-70). El servicio de reviews crea su carpeta al escribir (deskops/services/review.py, mkdir con parents=True).

## Goal

_Describe the concrete result this task must produce._

desk update ya no cuenta desk/reviews/ como estructura faltante; la carpeta se crea cuando se escribe el primer recibo. En un repo nuevo: `deskops init .`, commit, clon limpio, `deskops desk update --root <clon>` da rc 0.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/desk.py (quitar el chequeo de desk/reviews/), el golden tests/fixtures/golden/scaffold/update.json si cambia, y tests/test_cli.py. No entra: agregar .gitkeep.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Quitar las lineas 231-232. 2) Verificar que review.py crea desk/reviews al escribir el primer recibo. 3) Test en tests/test_cli.py con git init, init, commit, clone y desk update dry-run rc 0. Precisiones del preflight 1: el codigo a quitar es el if que agrega 'desk/reviews/' a missing_desk_files en deskops/cli/commands/desk.py. El golden scaffold/update.json se actualiza solo si su contenido nombra desk/reviews. El test usa tmp_path, subprocess con git init -b main, deskops init, git add/commit, git clone a otro tmp_path y deskops desk update --root <clon> sin --apply; espera rc 0.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El test del clon limpio pasa con rc 0 y el primer recibo crea desk/reviews/.

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

FILE:deskops/cli/commands/desk.py
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from sldb.api import add_model
from sldb.api import remove_model
from sldb.api import track_document_file
from sldb.api import untrack_document
from sldb.api import update_store_indexes

from deskops.atom_tags import sync_tag_declaration
from deskops.workspace import ensure_target_directory
from deskops.workspace import inspect_desk
from deskops.workspace import legacy_task_states
from deskops.workspace import migrate_legacy_task_states
from deskops.doctor_findings import invalid_document_findings
from deskops.workspace import migrate_desk
from deskops.workspace import migrate_task_types
from deskops.workspace import apply_desk_includes
from deskops.workspace import pending_local_task_type_models
from deskops.workspace import pending_task_type_migration
from deskops.workspace import pending_desk_includes
from deskops.workspace import register_local_task_type_models
from deskops.workspace import seed_desk
from deskops.bootstrap import SLDBBootstrap, MODEL_REFS
from deskops.errors import DeskopsEnvironmentError
from deskops.paths import package_pythonpath
import deskops.models as models

#: The deskops FAQ model used to be registered with the same name sldb uses for its
#: own model. sldb federates models by name, so the old name must be migrated.
LEGACY_FAQ_MODEL = "FAQDoc"
LEGACY_FAQ_MODEL_REF = "deskops.models:FAQDoc"
FAQ_MODEL = "DeskFAQDoc"
FAQ_MODEL_REF = "deskops.models:DeskFAQDoc"


def legacy_faq_model_pending(entries: dict[str, Any]) -> bool:
    """Whether a store still registers the old deskops FAQ model name."""
    entry = entries.get(LEGACY_FAQ_MODEL)
    return entry is not None and getattr(entry, "model_ref", None) == LEGACY_FAQ_MODEL_REF


def moved_model_contracts(root: Path, entries: dict[str, Any]) -> list[str]:
    """Registered deskops models whose store contract no longer matches this checkout."""
    from sldb.store.hashing import hash_model_contract
    from sldb.store.io import load_models_index

    moved: list[str] = []
    for name, entry in sorted(entries.items()):
        model_ref = getattr(entry, "model_ref", "") or ""
        model_type = getattr(models, name, None)
        models_index = getattr(entry, "models_index", None)
        if not model_ref.startswith("deskops.models:") or model_type is None or not models_index:
            continue
        try:
            stored = load_models_index(root / models_index).contract_hash
        except Exception:
            continue
        if stored != hash_model_contract(model_type):
            moved.append(name)
    return moved


def migrate_legacy_faq_model(root: Path, *, pythonpath: str | None = None) -> list[str]:
    """Move an existing store from `FAQDoc` to `DeskFAQDoc`, keeping its documents.

    sldb exposes no model rename, so this registers the new name, retracks every
    document the old model owns, and removes the old entry with its document
    records. The Markdown files are never touched, so they stay byte-identical.
    """
    from sldb.store.io import load_documents_index
    from sldb.store.io import load_models_index

    store_dir = root / ".sldb"
    pythonpath = pythonpath or package_pythonpath()
    bootstrap = SLDBBootstrap()
    entries = bootstrap._registered_model_entries(store_dir)
    if not legacy_faq_model_pending(entries):
        return []

    changes: list[str] = []
    if FAQ_MODEL not in entries:
        add_model(store_dir, FAQ_MODEL_REF, pythonpath=pythonpath)
        changes.append(f"registered {FAQ_MODEL}")

    # The old class no longer exists, so its documents are read from the indexes
    # instead of resolving the model reference.
    legacy_entry = entries[LEGACY_FAQ_MODEL]
    legacy_index = load_models_index(root / legacy_entry.models_index)
    old_documents = load_documents_index(root / legacy_index.documents_index).documents
    tracked: set[str] = set()
    new_entry = bootstrap._registered_model_entries(store_dir).get(FAQ_MODEL)
    if new_entry is not None:
        new_index = load_models_index(root / new_entry.models_index)
        tracked = {document.name for document in load_documents_index(root / new_index.documents_index).documents}
    for document in old_documents:
        if document.name in tracked:
            continue
        track_document_file(store_dir, FAQ_MODEL, root / document.path, name=document.name, pythonpath=pythonpath, force=True)
        changes.append(f"tracked {document.name} as {FAQ_MODEL}")

    remove_model(store_dir, LEGACY_FAQ_MODEL, pythonpath=pythonpath, untrack_documents=True)
    changes.append(f"removed {LEGACY_FAQ_MODEL}")
    return changes


class DeskCLI:
    """Handle desk workspace scaffolding and rituals."""

    def run(self, args: Any) -> int:
        if args.desk_command == "install":
            return self.install(args)
        if args.desk_command == "migrate":
            return self.migrate(args)
        if args.desk_command == "replace":
            return self.replace(args)
        if args.desk_command == "update":
            return self.update(args)
        return 1

    def replace(self, args: Any) -> int:
        from deskops.services.replace import replace_text

        result = replace_text(
            Path(args.root),
            args.path,
            args.old,
            args.new,
            count=args.count,
        )
        print(f"Replaced {result.replacements} occurrence(s) in {result.path}")
        return 0

    def install(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        desk_dir = target_path / "desk"
        print(f"Scaffolding local desk at {desk_dir}...")
        result = seed_desk(target_path)
        for path in result.created_paths:
            print(f"Wrote {path}")
        for path in result.rewritten_paths:
            print(f"Rewrote {path}")

        if (target_path / ".sldb").exists():
            from deskops.lifecycle import write_lifecycle_graph

            for change in write_lifecycle_graph(target_path):
                print(f"Lifecycle graph: {change}")
        else:
            print("No .sldb store yet: run 'deskops init' to create it and the lifecycle graph that 'deskops advance' reads.")
        print("Scaffold complete.")
        print("Register the repo separately with 'deskops repo register ...' when you are ready.")
        return 0

    def migrate(self, args: Any) -> int:
        target_path = Path(args.root).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        result = migrate_desk(target_path)
        print(f"Desk migration report for {target_path}:")

        print("Adopted:")
        if result.adopted:
            for item in result.adopted:
                print(f"- {item}")
        else:
            print("- none")

        print("Preserved:")
        if result.preserved:
            for item in result.preserved:
                print(f"- {item}")
        else:
            print("- none")

        print("Still manual:")
        if result.still_manual:
            for item in result.still_manual:
                print(f"- {item}")
        else:
            print("- none")

        return 0

    def update(self, args: Any) -> int:
        root = Path(args.root).resolve()
        apply = getattr(args, "apply", False)

        desk_dir = root / "desk"
        store_dir = root / ".sldb"

        from deskops import lifecycle

        inspection = inspect_desk(root)

        # Tasks with a pre-CC31 lifecycle state: the model rejects them, and sldb with them every
        # other read of the store, so --apply migrates them first, from the frontmatter (d1).
        if apply and desk_dir.exists():
            migrated_lines, invalid_tasks = migrate_legacy_task_states(root)
            if migrated_lines:
                print("Migrating legacy task states...")
                for line in migrated_lines:
                    print(f"- {line}")
            legacy_pending: list = []
            invalid_tasks += legacy_task_states(root)[1]
            invalid_tasks.sort(key=lambda state: state.rel)
        else:
            legacy_pending, invalid_tasks = legacy_task_states(root) if desk_dir.exists() else ([], [])

        missing_desk_files: list[str] = []
        if inspection.classification == "absent":
            missing_desk_files.append("desk/")
        elif desk_dir.exists():
            if not (desk_dir / "tasks" / "Board.md").exists():
                missing_desk_files.append("desk/tasks/Board.md")
            if not (desk_dir / "drawer").exists():
                missing_desk_files.append("desk/drawer/")
            if not (desk_dir / "reviews").exists():
                missing_desk_files.append("desk/reviews/")
            if not (desk_dir / "rituals" / "phase.md").exists():
                missing_desk_files.append("desk/rituals/phase.md")
            if not (desk_dir / "runtimes" / "runtime-pi-deepseek-flash.md").exists():
                missing_desk_files.append("desk/runtimes/runtime-pi-deepseek-flash.md")

        # The lifecycle graph's documents are managed seeds: a desk's copy that differs from the
        # package's is rewritten. A missing one is written with the rest of the scaffold.
        scaffold_plan = seed_desk(root, apply=False, restore_managed=True) if desk_dir.exists() else None
        lifecycle_rewrites = (
            [path.relative_to(root).as_posix() for path in scaffold_plan.rewritten_paths] if scaffold_plan else []
        )
        lifecycle_missing = bool(scaffold_plan) and any(
            path.relative_to(root).as_posix().startswith("desk/lifecycle/") for path in scaffold_plan.created_paths
        )

        bootstrap = SLDBBootstrap()
        registered_entries: dict[str, Any] = {}
        if store_dir.exists():
            try:
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception:
                pass

        legacy_faq_pending = legacy_faq_model_pending(registered_entries)
        if legacy_faq_pending and apply:
            print(f"Migrating the deskops FAQ model from {LEGACY_FAQ_MODEL} to {FAQ_MODEL}...")
            try:
                for change in migrate_legacy_faq_model(root):
                    print(f"- {change}")
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception as exc:
                print(f"Error: {exc}")
                return 1
            legacy_faq_pending = False

        moved_contracts = (
            moved_model_contracts(root, registered_entries) if store_dir.exists() else []
        )
        if moved_contracts and apply:
            pythonpath = package_pythonpath()
            for model_name in moved_contracts:
                print(f"Updating the {model_name} contract...")
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "sldb",
                        "models",
                        "update",
                        model_name,
                        "--store",
                        str(store_dir),
                        "--pythonpath",
                        pythonpath,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode != 0:
                    detail = result.stderr.strip() or result.stdout.strip()
                    print(f"Error: could not update the {model_name} contract: {detail}")
                    return 1
                print(f"Updated {model_name} contract.")
            registered_entries = bootstrap._registered_model_entries(store_dir)
            moved_contracts = moved_model_contracts(root, registered_entries)

        unregistered_models: list[str] = []
        copied_models: list[str] = []
        # A non-editable install has no owner store to inherit from; its directly
        # registered models are the expected state, not copies to convert.
        owner_store = bootstrap._deskops_owner_store()
        if owner_store is not None and store_dir.exists() and store_dir.resolve() == owner_store.resolve():
            # The owner store registers the deskops models directly; that is what
            # the other stores link to, not a copy of it.
            owner_store = None
        for model_name, model_ref in MODEL_REFS.items():
            entry = registered_entries.get(model_name)
            if entry is None:
                unregistered_models.append(model_name)
            elif (
                owner_store is not None
                and not getattr(entry, "origin", None)
                and getattr(entry, "model_ref", None) == model_ref
            ):
                copied_models.append(model_name)

        invalid_docs: list[str] = []
        missing_docs: list[str] = []
        store_invalid_docs: list[tuple[str, str]] = []
        all_store_invalid_docs: list[tuple[str, str]] = []
        missing_store = not store_dir.exists()
        if not missing_store:
            result = subprocess.run(
                [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_dir), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            payload = None
            if result.stdout and result.stdout.strip():
                try:
                    payload = json.loads(result.stdout)
                except json.JSONDecodeError as exc:
                    raise DeskopsEnvironmentError(
                        f"Could not parse 'sldb stores check' output for {store_dir}: {exc}"
                    ) from exc
            if payload is None and result.returncode != 0:
                reason = f": {result.stderr.strip()}" if result.stderr and result.stderr.strip() else ""
                raise DeskopsEnvironmentError(
                    f"'sldb stores check' failed for {store_dir} with exit code {result.returncode}{reason}"
                )
            if payload is None:
                raise DeskopsEnvironmentError(
                    f"'sldb stores check' produced no JSON output for {store_dir}"
                )
            for model in (payload or {}).get("models", []):
                for doc in model.get("documents", []):
                    doc_path = doc.get("path")
                    if not doc_path:
                        continue
                    if doc.get("note") not in ("ok", "doc_invalid"):
                        invalid_docs.append(f"{doc_path} ({doc.get('note')})")
                        if doc.get("note") == "missing":
                            missing_docs.append(doc.get("name") or Path(doc_path).stem)
            # The documents sldb names as store/doc-invalid, except the invalid tasks the
            # frontmatter listing above already reports (g3).
            reported_tasks = {state.rel for state in [*legacy_pending, *invalid_tasks]}
            all_store_invalid_docs = invalid_document_findings(payload or {})
            store_invalid_docs = [(rel, what) for rel, what in all_store_invalid_docs if rel not in reported_tasks]

        # The desk documents the package's declared includes name and the store does not
        # track yet, each with its declared model (deskops/data/desk_declaration.yaml).
        untracked_docs = pending_desk_includes(root) if desk_dir.exists() else []

        # The store declares the namespaces of desk/atoms/tag-namespaces.yaml for sldb's tag
        # family; the file wins (deskops.atom_tags.sync_tag_declaration).
        tag_declaration_pending = (
            desk_dir.exists() and not missing_store and sync_tag_declaration(root, apply=False)
        )

        pending_local_types = pending_local_task_type_models(root)
        pending_migration = pending_task_type_migration(root)
        # A task whose lifecycle TaskDoc's validator rejects is not retyped (CC37); it is listed
        # below as a legacy state to migrate or as an invalid task document.
        pending_migration = [line for line in pending_migration if not line.startswith("inconsistent ")]

        if not lifecycle_rewrites and not legacy_faq_pending and not missing_store and not missing_desk_files and not unregistered_models and not copied_models and not untracked_docs and not invalid_docs and not store_invalid_docs and not moved_contracts and not pending_local_types and not pending_migration and not legacy_pending and not invalid_tasks and not tag_declaration_pending:
            print("Desk is up to date.")
            return 0

        print("Desk divergence report:")
        if missing_store:
            print("- Missing store: .sldb")
        if legacy_faq_pending:
            print(
                f"- Legacy FAQ model: {LEGACY_FAQ_MODEL} ({LEGACY_FAQ_MODEL_REF}) should be {FAQ_MODEL}."
            )
        if moved_contracts:
            print(f"- Moved model contracts: {', '.join(moved_contracts)}")
        if lifecycle_rewrites:
            print(f"- Lifecycle documents to rewrite: {', '.join(lifecycle_rewrites)}")
        if missing_desk_files:
            print(f"- Missing desk structure: {', '.join(missing_desk_files)}")
        if unregistered_models:
            print(f"- Unregistered models: {', '.join(unregistered_models)}")
        if copied_models:
            print(f"- Copied deskops models: {', '.join(copied_models)}")
        if untracked_docs:
            print(f"- Untracked desk documents: {', '.join(path for _model, path in untracked_docs)}")
        if tag_declaration_pending:
            print("- Tag namespace declaration: .sldb/store.yaml differs from desk/atoms/tag-namespaces.yaml")
        if pending_local_types:
            print(f"- Unregistered desk-local task types: {', '.join(pending_local_types)}")
        if pending_migration:
            print(f"- Pending task type migration: {len(pending_migration)} task(s)")
        if invalid_docs:
            print(f"- Stale document hashes: {', '.join(invalid_docs)}")
        if store_invalid_docs:
            print(f"- Invalid documents (not written): {len(store_invalid_docs)} document(s)")
            for rel, what in store_invalid_docs:
                print(f"  - {rel}: {what}")
        if legacy_pending:
            print(f"- Legacy task states to migrate: {len(legacy_pending)} task(s)")
            for state in legacy_pending:
                for line in state.migration_lines():
                    print(f"  - {line}")
        if invalid_tasks:
            print(f"- Invalid task documents (not written): {len(invalid_tasks)} task(s)")
            for state in invalid_tasks:
                print(f"  - {state.finding()}")
        if not apply:
            print("\nRun with --apply to repair these issues.")
            return 1

        print("\nApplying repairs...")

        if missing_desk_files or lifecycle_rewrites or lifecycle_missing:
            scaffold = seed_desk(root, restore_managed=True)
            if missing_desk_files:
                print("Scaffolded missing desk structure.")
            for change in lifecycle.seed_changes(root, scaffold):
                print(f"Lifecycle graph: {change}")

        failed = False
        if unregistered_models or copied_models:
            if bootstrap.init_local_store(root) == 0:
                print("Registered missing models and converted copied deskops models.")
            else:
                print("Error: could not register the missing models (sldb rejects a tracked document; see the report above).")
                failed = True

        try:
            for change in register_local_task_type_models(root):
                print(f"- {change}")
        except Exception as exc:
            print(f"Error: {exc}")
            return 1
        try:
            for change in migrate_task_types(root):
                if not change.startswith("inconsistent "):
                    print(f"- {change}")
        except Exception as exc:
            print(f"Error: could not migrate the task types: {exc}")
            failed = True

        # Always: a store this --apply just created has no declaration yet (idempotent).
        try:
            declared_tags = sync_tag_declaration(root)
        except Exception as exc:
            print(f"Error: could not declare the tag namespaces: {exc}")
            return 1
        if declared_tags:
            print("Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml.")

        # Recomputed: the scaffold may have written declared documents (the lifecycle graph).
        untracked_docs = pending_desk_includes(root) if desk_dir.exists() and store_dir.exists() else []
        if untracked_docs:
            declared_models = {path: model_name for model_name, path in untracked_docs}
            try:
                lifecycle.ensure_rule_model(root)
                tracked_paths = apply_desk_includes(root)
            except Exception as exc:
                # apply_includes tracks in order and stops at the first document sldb rejects, so
                # the first one still pending is the one the rule (named in ``exc``) refused.
                try:
                    refused = next(iter(pending_desk_includes(root)), None)
                except Exception:
                    refused = None
                where = f" ({refused[1]})" if refused else ""
                print(f"Error: could not track the declared desk documents{where}: {exc}")
                return 1
            for path in tracked_paths:
                model_name = declared_models.get(path, "its declared model")
                line = lifecycle.tracked_line(model_name, path)
                print(f"Lifecycle graph: {line}" if line else f"Tracked {path} as {model_name}.")

        if missing_docs:
            # A tracked document whose file is gone must be untracked, not
            # re-indexed: the store would keep describing something that is not there.
            pythonpath = package_pythonpath()
            for name in missing_docs:
                try:
                    untrack_document(root / ".sldb", name, pythonpath=pythonpath)
                    print(f"Untracked {name}: its file is gone.")
                except Exception as e:
                    print(f"Failed to untrack {name}: {e}")

        if invalid_docs or all_store_invalid_docs:
            pythonpath = package_pythonpath()
            update_store_indexes(root / ".sldb", pythonpath, wait=False)
            print("Updated store derived indexes.")

        # Exit 1 while a task or another document needs its owner's decision or a repair could not
        # run (the same as the dry-run, which exits 1 with any divergence).
        return 1 if invalid_tasks or store_invalid_docs or failed else 0

FILE:tests/fixtures/golden/scaffold/update.json
{
  "desk_name": "golden_desk",
  "files": {
    "desk/atoms/atom-golden-one.md": "83ca9a1565d606883dfd3e7fa539d4ba86bf96e9b8d5069ec821f361b59fd6d3",
    "desk/atoms/atom-golden-two.md": "0b0523ee366564d7156c7a5fca286235d50213a7417f9f92ca2486672461f0b3",
    "desk/atoms/tag-namespaces.yaml": "c42b81ba27b3feb0c50c3515dd94b68a26c3f99416a6dbcb2cb890d3c5976e5a",
    "desk/config.json": "6fe6bf8d22aff63d33b28de1a80a634b55028ff5765455352c52c0698dd93f1d",
    "desk/contexts/pill-golden-rule.md": "42fa182fcb4b2e48e39f4199bf46e2fea5eafe7dfefaa375b725124a128d491a",
    "desk/contexts/pills.md": "13eb253572c2230d308859e8c93c9f2b1082186c273455fc20a760ef155f0f91",
    "desk/drawer/README.md": "859d8fbe608b59290df99b30be87bb8ed0f3c64ffdb239c38bcee900882af77a",
    "desk/drawer/tasks/task-golden-drawer.md": "c00024944dfb048f27c62de57fd4c1f94d974e04971a926444a0e467d1a5d083",
    "desk/lifecycle/closeout-task_completes.md": "29579bdf3d30b8f5f21cbcd8af3d3760d183fdaa55bc07d8c1d47af9da7797dd",
    "desk/lifecycle/execution-task_activates.md": "335d1831e3de3d6a78a0b577815fc9fec1d9119d41ea8387ab15d26cabe7e4d9",
    "desk/lifecycle/rule-activation-task-aggregate.md": "96f2b5754fc820b142c9ec34810f69ca19b9e242eb969a038e7aad99584eba4b",
    "desk/lifecycle/rule-activation-task-code.md": "98b909ce90a1d7be43035d7a42332badca2a4b2baaee5d319a84aaeb565f09d6",
    "desk/lifecycle/rule-activation-task-debug.md": "9ef9824527e075491163874c0080efb04c67f64841bfc0d2eb7e958719280b53",
    "desk/lifecycle/rule-activation-task-decision.md": "450c0028d6dd3b3b5a115fac8125c1c26bd0aab24885b543c35a8a33d140555d",
    "desk/lifecycle/rule-activation-task-docs.md": "5091bbb884692532a950d0b910b4aa97bb5a632e41261062dc68adbd856d7cba",
    "desk/lifecycle/rule-activation-task-external.md": "41864d8366de65b23e0e078f4d12e5ab0a5cd454d6352ee7d55a620535e720d9",
    "desk/lifecycle/rule-activation-task-refactor.md": "5e544ad793bb5443f326931e4114079d4a12ed2b793e7fb3e6dea1fadca15aa3",
    "desk/lifecycle/rule-closeout-alert-implicit-code.md": "ef70e3a73b70df77017af2caf1214f95c2c6965d27570dc583034b1898cfeee0",
    "desk/lifecycle/rule-closeout-alert-pill-graduation.md": "1ff56c432a5b54ae33747191e1e20d128f183cb46fb141a38ebd22b99708c4aa",
    "desk/lifecycle/rule-closeout-task-aggregate.md": "73b4ae10c61941861c1445feea728ae182979ad87a9a18a96b7aefd73e1ae7e6",
    "desk/lifecycle/rule-closeout-task-code.md": "4cb425a18f58871230900ba27dd81de1ec496ff8b9ded20a32aa7297fd46e643",
    "desk/lifecycle/rule-closeout-task-debug.md": "68dda7c08e797b054f31410f5ab81fb23488b51e1607282a245344204f0de198",
    "desk/lifecycle/rule-closeout-task-decision.md": "04c34023b5bc62d6cbe7afd1b1498381faac81896276228b2b6d7984f560fb63",
    "desk/lifecycle/rule-closeout-task-docs.md": "e425a3b6b46e91682d0fe8bc490365855ee52ceb148e82b0ed4148fa6bb2f84e",
    "desk/lifecycle/rule-closeout-task-external.md": "e55304451cd14cd01ade7d996086321eeca150099b5acd46ccf1c172feb365be",
    "desk/lifecycle/rule-closeout-task-refactor.md": "44310c9d892138dc939c39b1ea55fbd1c0520aa0976e83334da82eccfd1c0b17",
    "desk/lifecycle/testing-task_hands_to_closeout.md": "e93064887b3745880b8307baf0d215696b1410eea6a7878333ef0077aa02bdb5",
    "desk/lifecycle/type-task_activates.md": "82694800f31844ed3b86b5913f2cbf02eaebf24f4143a8a4542a64374d9217b5",
    "desk/lifecycle/type-task_completes.md": "5b3f4ce0793df8b2ee535b6b37490b8d0abdd4c8bb8b43b330ddb6134ead7f0f",
    "desk/lifecycle/type-task_hands_to_closeout.md": "d16cc9c1d329c8d362e0d08c9ba3d6f23bbc7538429fd82cf20540c593f700bf",
    "desk/rituals/closeout.md": "ee499a2cf1d1188215544247068ece4fc8c30cc88abd289a8478feb08d2b2fba",
    "desk/rituals/execution.md": "03bf2e8139294480bcaa8911382f0b179237fc7c63c9c93cd842614cc91f5da7",
    "desk/rituals/phase.md": "20103739e5bf1c08c63304fa62fe56b8489c76d711f0831756a549b3da191fb9",
    "desk/rituals/testing.md": "6ea599f86a21b71c36c18f4d5c5ce4f9f6590f67bd1e27bcb2d7731f1d7d71fb",
    "desk/runtimes/runtime-pi-deepseek-flash.md": "d505ab97e1f3ed07fe01b72c1995abd4f450490ebc281fa4fa78ecc5347a6f54",
    "desk/tasks/Board.md": "83b1848d7186c7e8effe7ddb86c27a7972a10fe495b9f7a6c629da04dec44cf3",
    "desk/tasks/task-golden-alpha.md": "6abac2bba87e7a7b3db75ed744fb997bdc127d31ed00d0f2c52e6474be82ed87",
    "desk/tasks/task-golden-beta.md": "33fb4e4e48ae0d11b843db4b8a8e9221db199b92a60f087d8c51f9c1ab1686c8"
  },
  "report": [
    "- Missing desk structure: desk/tasks/Board.md, desk/reviews/, desk/rituals/phase.md, desk/runtimes/runtime-pi-deepseek-flash.md",
    "- Missing store: .sldb",
    "- Pending task type migration: 2 task(s)",
    "- Unregistered models: CrossroadDoc, AtomDoc, BoardDoc, DeskFAQDoc, InboxNoteDoc, MaterializationContractDoc, PillDoc, ProtoAtomDoc, RepositoryDoc, ReviewDoc, RitualDoc, RoleDoc, RunDoc, RuntimeProfileDoc, StepDoc, TaskAggregateDoc, TaskCodeDoc, TaskDebugDoc, TaskDecisionDoc, TaskDoc, TaskDocsDoc, TaskExternalDoc, TaskRefactorDoc",
    "- Untracked desk documents: desk/atoms/atom-golden-one.md, desk/atoms/atom-golden-two.md, desk/contexts/pill-golden-rule.md",
    "- migrated desk/tasks/task-golden-alpha.md: task_type 'implementation' -> 'task.code' (tracked as TaskCodeDoc)",
    "- migrated desk/tasks/task-golden-beta.md: task_type 'implementation' -> 'task.code' (tracked as TaskCodeDoc)",
    "Applying repairs...",
    "Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml.",
    "Desk divergence report:",
    "Inheriting AtomDoc in <root>/.sldb...",
    "Inheriting BoardDoc in <root>/.sldb...",
    "Inheriting CrossroadDoc in <root>/.sldb...",
    "Inheriting DeskFAQDoc in <root>/.sldb...",
    "Inheriting InboxNoteDoc in <root>/.sldb...",
    "Inheriting MaterializationContractDoc in <root>/.sldb...",
    "Inheriting PillDoc in <root>/.sldb...",
    "Inheriting ProtoAtomDoc in <root>/.sldb...",
    "Inheriting RepositoryDoc in <root>/.sldb...",
    "Inheriting ReviewDoc in <root>/.sldb...",
    "Inheriting RitualDoc in <root>/.sldb...",
    "Inheriting RoleDoc in <root>/.sldb...",
    "Inheriting RunDoc in <root>/.sldb...",
    "Inheriting RuntimeProfileDoc in <root>/.sldb...",
    "Inheriting StepDoc in <root>/.sldb...",
    "Inheriting TaskAggregateDoc in <root>/.sldb...",
    "Inheriting TaskCodeDoc in <root>/.sldb...",
    "Inheriting TaskDebugDoc in <root>/.sldb...",
    "Inheriting TaskDecisionDoc in <root>/.sldb...",
    "Inheriting TaskDoc in <root>/.sldb...",
    "Inheriting TaskDocsDoc in <root>/.sldb...",
    "Inheriting TaskExternalDoc in <root>/.sldb...",
    "Inheriting TaskRefactorDoc in <root>/.sldb...",
    "Initializing local store at <root>/.sldb...",
    "Lifecycle graph: tracked desk/lifecycle/closeout-task_completes.md",
    "Lifecycle graph: tracked desk/lifecycle/execution-task_activates.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-activation-task-aggregate.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-activation-task-code.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-activation-task-debug.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-activation-task-decision.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-activation-task-docs.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-activation-task-external.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-activation-task-refactor.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-alert-implicit-code.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-alert-pill-graduation.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-task-aggregate.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-task-code.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-task-debug.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-task-decision.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-task-docs.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-task-external.md",
    "Lifecycle graph: tracked desk/lifecycle/rule-closeout-task-refactor.md",
    "Lifecycle graph: tracked desk/lifecycle/testing-task_hands_to_closeout.md",
    "Lifecycle graph: tracked desk/lifecycle/type-task_activates.md",
    "Lifecycle graph: tracked desk/lifecycle/type-task_completes.md",
    "Lifecycle graph: tracked desk/lifecycle/type-task_hands_to_closeout.md",
    "Lifecycle graph: tracked desk/rituals/closeout.md as RitualDoc:ritual-closeout",
    "Lifecycle graph: tracked desk/rituals/execution.md as RitualDoc:ritual-execution",
    "Lifecycle graph: tracked desk/rituals/testing.md as RitualDoc:ritual-testing",
    "Lifecycle graph: wrote desk/lifecycle/closeout-task_completes.md",
    "Lifecycle graph: wrote desk/lifecycle/execution-task_activates.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-activation-task-aggregate.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-activation-task-code.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-activation-task-debug.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-activation-task-decision.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-activation-task-docs.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-activation-task-external.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-activation-task-refactor.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-alert-implicit-code.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-alert-pill-graduation.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-task-aggregate.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-task-code.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-task-debug.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-task-decision.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-task-docs.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-task-external.md",
    "Lifecycle graph: wrote desk/lifecycle/rule-closeout-task-refactor.md",
    "Lifecycle graph: wrote desk/lifecycle/testing-task_hands_to_closeout.md",
    "Lifecycle graph: wrote desk/lifecycle/type-task_activates.md",
    "Lifecycle graph: wrote desk/lifecycle/type-task_completes.md",
    "Lifecycle graph: wrote desk/lifecycle/type-task_hands_to_closeout.md",
    "Linked <owner-store> as deskops in <root>/.sldb.",
    "Registered missing models and converted copied deskops models.",
    "Scaffolded missing desk structure.",
    "Tracked desk/atoms/atom-golden-one.md as AtomDoc.",
    "Tracked desk/atoms/atom-golden-two.md as AtomDoc.",
    "Tracked desk/contexts/pill-golden-rule.md as PillDoc.",
    "Tracked desk/rituals/phase.md as RitualDoc.",
    "Tracked desk/tasks/Board.md as BoardDoc."
  ]
}

FILE:instruccion
Cold-bundle de la tarea task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

