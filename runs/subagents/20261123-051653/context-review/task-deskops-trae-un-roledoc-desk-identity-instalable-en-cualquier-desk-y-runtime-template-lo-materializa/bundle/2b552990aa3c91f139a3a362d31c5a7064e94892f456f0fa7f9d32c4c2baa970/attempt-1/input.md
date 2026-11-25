FILE:desk/tasks/task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa.md
---
sldb:
  by: agent
  at: '2026-11-23T05:15:42Z'
  authority: generated
  via: save_document_payload
id: task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-234447-suggestion-roledoc-de-identidad-de-desk-desk-identity-y-su-traduccion-a-agente-scion.md
depends_on:
- task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale
pills: []
files:
- deskops/data/roles/desk-identity.yaml
- pyproject.toml
- deskops/cli/commands/desk.py
- deskops/cli/commands/core.py
- deskops/runtime/scion.py
- deskops/cli/commands/runtime.py
- deskops/cli/registry.py
- tests/test_desk_sync.py
- tests/test_scion_runtime.py
- tests/fixtures/golden/help/deskops_runtime_template.txt
- tests/fixtures/golden/scaffold/init.json
- tests/fixtures/golden/scaffold/update.json
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops trae un RoleDoc desk-identity instalable en cualquier desk y runtime template lo materializa como agente scion persistente (--mode identity)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234447 (scion-coordination, workflow scion + deskops de JP): no hay RoleDoc para la identidad de un desk. deskops tiene deskops-executor, deskops-supervisor y deskops-tester en desk/roles; sldb no tiene desk/roles. El piloto wf-desks arma el prompt pegando reglas de /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh delante de desk/roles/deskops-supervisor.md, fuera de deskops. Texto base vigente, autorizado por Governance: /srv/wt/labchile_chatbots/.encargo-triaje-inbox.txt. Relacionadas, no se duplican: task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale (tools del RoleDoc a claude, dependencia) y task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale (image, resources y volumes en --config).

## Goal

_Describe the concrete result this task must produce._

(1) deskops empaqueta como dato (junto a las plantillas de deskops/data/templates) un RoleDoc desk-identity: name desk-identity, kind claude, tools read, grep, find, ls, bash, y un cuerpo con estas reglas: triar el inbox propio (ack con motivo, tarea + ack, o dejar abierto lo que pide decisión de JP y decirlo); reenviar lo ajeno por deskops message send --to <dueño>; registrar un acuerdo cerrado en un hilo como atom con la referencia del hilo, una sola vez; mandar lo sin dueño a su destino; no implementar código, no despachar, no tocar la cola, no hacer push; desk/ y .sldb/ solo con los CLI; todo comando con --root <raíz del desk>. (2) deskops desk update --apply (y el modo en seco lo lista) instala ese RoleDoc en desk/roles de un desk que no lo tiene, con deskops add role por debajo; no pisa uno existente. (3) deskops runtime template acepta --mode identity: escribe un agents.md de identidad persistente que nombra la raíz del desk y el proyecto scion, sin worktree por agente (workspace relativo en un proyecto de carpeta sin git, el único modo que admite reincarnate) y sin las instrucciones de ejecutor/tester/coordinador.

## Scope

_State what is in scope and what is out of scope._

Entra: el RoleDoc empaquetado como payload YAML en deskops/data/roles/desk-identity.yaml (carpeta hermana de deskops/data/templates; NO dentro de data/templates, porque lo que esta ahi lo siembra seed_desk como semilla gestionada y lo restauraria) y su entrada en [tool.setuptools.package-data] de pyproject.toml ("data/roles/*.yaml"); la instalacion en deskops/cli/commands/desk.py (desk update) y en deskops init (deskops/cli/commands/core.py, InitCLI, para que un desk recien creado siga "Desk is up to date"); --mode identity en deskops/runtime/scion.py y en la declaracion de runtime template de deskops/cli/registry.py (choices de --mode); goldens de ayuda (tests/fixtures/golden/help/deskops_runtime_template.txt) y de scaffold (tests/fixtures/golden/scaffold/init.json y update.json, que ganan desk/roles/role-desk-identity.md); tests/test_scion_runtime.py y tests/test_desk_sync.py. No entra: crear el agente en scion, el hook que lo despierta (tarea aparte), cambios en el repo scion, el mapa de propiedad, la traduccion de tools a claude (dependencia).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test en tests/test_desk_sync.py: test_desk_update_installs_desk_identity_role (en un desk sin el rol, desk update en seco lista "Missing role: desk-identity" y sale 1 como con cualquier divergencia; con --apply queda desk/roles/role-desk-identity.md, deskops show role desk-identity lo lee; una segunda corrida dice "Desk is up to date."; un desk/roles/role-desk-identity.md existente, aunque tenga otro cuerpo, no se pisa). p2: test en tests/test_scion_runtime.py: test_runtime_template_identity_mode (con el rol instalado en el desk temporal, el agents.md nombra la raiz del desk y el proyecto scion, no contiene "worktree" ni "deskops dispatch"; --mode foo sigue fallando: argparse lista las cinco opciones y el ValueError de scion.py, hoy "mode must be executor, coordinator, tester or specialist, got '<x>'" en deskops/runtime/scion.py linea 384, pasa a "mode must be executor, coordinator, tester, specialist or identity, got '<x>'"). p3: implementar. Instalacion: una funcion compartida (en deskops/cli/commands/desk.py) que, si ningun RoleDoc de desk/roles tiene name desk-identity, crea el rol con la misma ruta que deskops add role --from-yaml (parse_artifact_input + DeskopsOperations.create_artifact("artifact.role", payload)), que lo escribe en desk/roles/role-desk-identity.md con id role-desk-identity y lo trackea; desk update la llama en --apply y en seco solo la lista; InitCLI la llama despues de seed_desk. Payload: name desk-identity, kind claude, tools [read, grep, find, ls, bash], description de una linea, y body en espanol con estas secciones y comandos literales: Triaje del inbox propio (cada nota abierta termina en una salida: deskops message ack <id> --reason "<motivo>" --root <raiz del desk> si es informativa, duplicada, resuelta u obsoleta; deskops add task ... que cite la nota y despues el ack; o queda abierta si pide una decision de JP, y se dice en la respuesta con la pregunta concreta); Reenvio (lo que es de otro desk va con deskops message send --to <desk dueno> --root <raiz del desk> y despues el ack; el dueno sale del registro de repos del desk; lo que no tiene dueno claro va al destino de lo sin dueno que declare el desk y, si no declara ninguno, queda abierto y se dice); Acuerdos (un acuerdo cerrado en un hilo se registra una sola vez con deskops add atom --root <raiz del desk>, con la referencia del hilo en --provenance, mirando antes deskops list atoms --root <raiz del desk>); Limites (no implementar codigo, no despachar, no tocar la cola, no hacer push; desk/ y .sldb/ solo con los CLI deskops y sldb; todo comando con --root <raiz del desk>). Modo identity: rama nueva en la seleccion de agents.md de scion.py (hoy lineas 495-504) con una funcion _render_identity_agents_md que usa _example_roots (linea 508) para nombrar desk_root y project, dice que el agente es persistente, trabaja en su carpeta (workspace relativo de un proyecto de carpeta sin git, el unico modo que admite reincarnate) y no menciona worktree, deskops dispatch ni instrucciones de ejecutor, tester o coordinador. p4: goldens: TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py --update-golden y tests/test_scaffold_golden.py --update-golden, revisando que el diff solo agregue la opcion identity y el rol. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_desk_sync.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan; deskops init deja un desk con desk/roles/role-desk-identity.md y desk update dice Desk is up to date; y, en un desk temporal con el rol instalado, deskops runtime template desk-identity --mode identity --root <desk temporal> escribe el template sin error.

FILE:pyproject.toml
[project]
name = "deskops"
version = "0.2.0"
description = "Workflow-domain layer for the hum-ecosystem"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.0",
    "PyYAML>=6.0",
    "structuredLanguageDB>=0.1.13",
]

[project.scripts]
deskops = "deskops.cli.main:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-xdist>=3.5",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["deskops*"]

[tool.setuptools.package-data]
deskops = ["spec/**/*.yaml", "data/faq.md", "data/templates/**/*", "data/lifecycle/**/*", "data/rules/**/*", "data/views/**/*", "data/desk_declaration.yaml"]

[tool.pytest.ini_options]
pythonpath = ["."]
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]

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
from deskops.workspace import legacy_frontmatter_keys
from deskops.workspace import migrate_legacy_frontmatter_keys
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

        if apply and store_dir.exists():
            for change in SLDBBootstrap().ensure_merge_driver(store_dir):
                print(f"Installed sldb merge driver: {change}")

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
            # Frontmatter keys TaskDoc does not declare (checklists, routine): every model write
            # refuses to erase them, so --apply removes them and prints each previous value.
            removed_lines, unremoved = migrate_legacy_frontmatter_keys(root)
            if removed_lines:
                print("Removing legacy task frontmatter keys...")
                for line in removed_lines:
                    print(f"- {line}")
            invalid_tasks += unremoved
            invalid_tasks.sort(key=lambda state: state.rel)
            legacy_keys_pending: list = []
        else:
            legacy_pending, invalid_tasks = legacy_task_states(root) if desk_dir.exists() else ([], [])
            legacy_keys_pending = legacy_frontmatter_keys(root) if desk_dir.exists() else []

        missing_desk_files: list[str] = []
        if inspection.classification == "absent":
            missing_desk_files.append("desk/")
        elif desk_dir.exists():
            if not (desk_dir / "tasks" / "Board.md").exists():
                missing_desk_files.append("desk/tasks/Board.md")
            if not (desk_dir / "drawer").exists():
                missing_desk_files.append("desk/drawer/")
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
                and not bootstrap.is_local_model_entry(entry, store_dir)
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

        if not lifecycle_rewrites and not legacy_faq_pending and not missing_store and not missing_desk_files and not unregistered_models and not copied_models and not untracked_docs and not invalid_docs and not store_invalid_docs and not moved_contracts and not pending_local_types and not pending_migration and not legacy_pending and not legacy_keys_pending and not invalid_tasks and not tag_declaration_pending:
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
        if legacy_keys_pending:
            print(f"- Legacy task frontmatter keys to remove: {len(legacy_keys_pending)} key(s)")
            for item in legacy_keys_pending:
                print(f"  - {item.pending_line()}")
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

FILE:deskops/cli/commands/core.py
from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.bootstrap import SLDBBootstrap
from deskops.workspace import ensure_target_directory
from deskops.workspace import seed_desk


class AboutCLI:
    def run(self, args: Any) -> int:
        # Resolved through the CLI module so a patched entrypoint stays visible.
        from deskops.cli import main as main_module

        return main_module.print_about()


class BootstrapCLI:
    def run(self, args: Any) -> int:
        return SLDBBootstrap().ensure_machine_ready()


class InitCLI:
    def run(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        bootstrap = SLDBBootstrap()
        ready = bootstrap.ensure_machine_ready()
        if ready != 0:
            return ready

        local_store = bootstrap.init_local_store(target_path)
        if local_store != 0:
            return local_store

        result = seed_desk(target_path)
        if result.wrote_anything:
            print(f"Scaffolded desk at {target_path / 'desk'}.")
            for path in result.created_paths:
                print(f"Wrote {path}")
            for path in result.rewritten_paths:
                print(f"Rewrote {path}")
        else:
            print(f"Desk already exists at {target_path / 'desk'}.")
        from deskops.lifecycle import write_lifecycle_graph

        for change in write_lifecycle_graph(target_path):
            print(f"Lifecycle graph: {change}")
        # The store declares the namespaces of the seeded desk/atoms/tag-namespaces.yaml for
        # sldb's tag family (CC35d resto); a declaration already equal is left alone.
        from deskops.atom_tags import sync_tag_declaration

        if sync_tag_declaration(target_path):
            print("Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml.")
        print("Initialization complete.")
        return 0

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


def _command_args(role_doc: dict[str, Any], profile: dict[str, Any], harness: str = "") -> list[str]:
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
    if harness == "pi":
        # pi rejects ``--tools=a,b`` (Unknown option) and takes option and value as two args.
        return list(args)
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

    command_args = _command_args(role_doc, profile, harness)
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
        + _render_python_env_section(desk_root, context)
        +
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


def _render_python_env_section(desk_root: str, context: dict[str, str] | None) -> str:
    """Startup step: the container builds its own Python 3.12 venv (the workspace .venv does not run there)."""
    sldb_pkg = (
        str(Path(context["sldb_root"]).parent) if context is not None else "<sldb checkout>"
    )
    return (
        "## Python environment (run first)\n"
        "\n"
        "The workspace `.venv` links to the host's `/usr/bin/python3.12`, which this image lacks. Build your own\n"
        "venv from the task repo's `pyproject.toml` before any test (about 30 s) and put it first on `PATH`:\n"
        "\n"
        "```bash\n"
        "export PATH=\"$HOME/.local/bin:$PATH\" TMPDIR=/tmp; unset PYTHONPATH\n"
        "uv venv /tmp/ws-venv --python 3.12\n"
        f"VIRTUAL_ENV=/tmp/ws-venv uv pip install -e \"{desk_root}[dev]\" -e {sldb_pkg}\n"
        "export VIRTUAL_ENV=/tmp/ws-venv PATH=\"/tmp/ws-venv/bin:$PATH\"\n"
        "python -c 'import xdist'  # pytest-xdist comes with the [dev] extra\n"
        "python -m pytest -q -p no:cacheprovider <tests>\n"
        "python -m pytest -q -p no:cacheprovider -n 4  # full suite, always with -n 4\n"
        "```\n"
        "\n"
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
        + _render_python_env_section(desk_root, context)
        +
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
        "- If you end blocked or without changes, do NOT run `deskops advance task`: write the blocker in\n"
        "  `result-summary.md` and finish with `sciontool status blocked \"<reason>\"`.\n"
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
    attempt: int = 1,
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
    if isinstance(attempt, bool) or attempt not in (1, 2):
        raise ValueError(f"attempt must be 1 or 2, got {attempt!r}")
    slug = _slug(agent_slug)
    if attempt == 2 and not slug.endswith("-a2"):
        slug += "-a2"
    # attempt 1 is the bare slug; a child name already carries its -a2 suffix.
    run_id = f"run-{slug}"
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
        "session_path": f"scion://agent/{slug}",
        "intent_at": now,
        "dispatch_confirmed_at": "",
        "external_ref": f"scion://agent/{slug}",
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


def confirm_scion_dispatch(root: Path, run_dir: str) -> bool:
    """Set ``dispatch_confirmed_at`` on the RunDoc of ``run_dir`` once the agent was observed in Scion.

    Returns False when there is no RunDoc there or it is already confirmed.
    """
    path = root / Path(run_dir) / "run.md"
    if not path.is_file():
        return False
    payload = doc_access.read_doc(path, RunDoc)
    if payload.get("dispatch_confirmed_at"):
        return False
    payload["dispatch_confirmed_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    doc_access.write_doc(root, path, RunDoc, payload)
    return True

FILE:deskops/cli/commands/runtime.py
from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.config import DeskConfig
from deskops.runtime.grouping import group_agents_by_workspace
from deskops.runtime.herdr import HerdrClient, HerdrProvider
from deskops.runtime.initializer import ensure_herdr_server, initialize_desk
from deskops.runtime.supervise import SuperviseOutcome, run_supervise_loop


class RuntimeCLI:
    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        executable = getattr(args, "herdr", "herdr")
        try:
            if args.runtime_command == "template":
                return self._template(args, root)
            if args.runtime_command == "supervise":
                return self._supervise(args, executable)
            if args.runtime_command == "workers":
                return self._workers(args, executable)
            if args.runtime_command == "init":
                ensure_herdr_server(executable)
                info, handle = initialize_desk(root, agents=args.agents, executable=executable)
                if handle is None:
                    print(f"Herdr Space already exists: {info.identity}")
                else:
                    print(f"DeskOps identity: {info.identity}; tasks discovered: {info.task_count}")
                    print(f"Created Herdr Space: {handle.workspace_id} ({info.identity})")
                    print(f"Panes: {handle.panes}")
                    if handle.agents:
                        print(f"Agents: {handle.agents}")
                return 0

            client = HerdrClient(executable)
            identity = DeskConfig.load(root / "desk").project_identity
            workspaces = client.call("workspace", "list").get("result", {}).get("workspaces", [])
            matches = [item for item in workspaces if isinstance(item, dict) and item.get("label") == identity]
            if args.runtime_command == "status":
                for workspace in matches:
                    print(f"{workspace.get('workspace_id')} | {workspace.get('label')} | panes={workspace.get('pane_count')}")
                if not matches:
                    print(f"No Herdr Space found for {identity}")
                return 0
            if not matches:
                print(f"No Herdr Space found for {identity}")
                return 1
            workspace_id = matches[0]["workspace_id"]
            if args.runtime_command == "attach":
                client.call("workspace", "focus", workspace_id)
                print(f"Focused Herdr Space: {workspace_id} ({identity})")
                return 0
            if args.runtime_command == "stop":
                client.call("workspace", "close", workspace_id)
                print(f"Closed Herdr Space: {workspace_id} ({identity})")
                return 0
        except (ValueError, RuntimeError) as exc:
            return render_error(
                str(exc),
                getattr(args, "format", "text"),
                type_name=type(exc).__name__,
                text=f"Error: {exc}",
            )
        return 1

    def _template(self, args: Any, root: Path) -> int:
        """Write a Scion template for one role; optionally record the dispatch as a RunDoc.

        Never calls ``scion``: launching (``scion start <agent> "<task>"
        --type <template>``) stays a deliberate gesture of the supervisor.
        """
        from deskops.runtime.scion import load_scion_context, materialize_scion_template, record_scion_run

        out_dir = Path(args.out).expanduser().resolve() if getattr(args, "out", None) else None
        task_id = getattr(args, "task", None)
        agent = getattr(args, "agent", None)
        if bool(task_id) != bool(agent):
            raise ValueError("--task and --agent go together: the RunDoc needs both the task and the Scion agent slug")
        context_file = getattr(args, "context_file", None)
        context = load_scion_context(Path(context_file).expanduser()) if context_file else None
        target = materialize_scion_template(
            root,
            args.role_id,
            harness=getattr(args, "harness", None),
            out_dir=out_dir,
            model_alias=getattr(args, "model_alias", "medium"),
            task_repo=getattr(args, "task_repo", None),
            mode=getattr(args, "mode", None),
            context=context,
            harness_auth=getattr(args, "harness_auth", None),
        )
        print(f"Scion template: {target}")
        for name in ("scion-agent.yaml", "system-prompt.md", "agents.md"):
            print(f"  {name}")
        if task_id and agent:
            harness = getattr(args, "harness", None) or ""
            # Roles live in the deskops desk; the task may live in another repo's
            # desk. The RunDoc belongs next to the task.
            task_root = Path(args.task_root).expanduser().resolve() if getattr(args, "task_root", None) else root
            run_path = record_scion_run(
                task_root,
                task_id=task_id,
                role_id=args.role_id,
                kind=harness or "scion",
                agent_slug=agent,
                run_dir=getattr(args, "run_dir", None),
            )
            print(f"RunDoc: {run_path.relative_to(task_root)} (in {task_root})")
        print(f"Next: scion start {agent or '<agent>'} \"<task>\" --type {target.name}")
        return 0

    def _supervise(self, args: Any, executable: str) -> int:
        """Block on one agent, reporting blocked/done settles as they happen.

        Never answers a blocked agent's prompt (only notifies and reports —
        a human decides) and never advances desk state on done (only
        captures and reports). Both are the explicit anti-patterns this
        command exists to avoid; see
        desk/roles/deskops-supervisor.md and
        desk/drawer/features/feature-herdr-supervised-execution-runtime.md.
        """
        provider = HerdrProvider(HerdrClient(executable))
        agent_id = args.agent
        max_iterations = getattr(args, "max_iterations", None)
        read_lines = getattr(args, "read_lines", 200)

        def on_blocked(outcome: SuperviseOutcome) -> None:
            excerpt_tail = "\n".join(outcome.excerpt.strip().splitlines()[-20:])
            print(f"[blocked] {outcome.agent_id} is waiting on input. Recent output:\n{excerpt_tail}")
            try:
                provider.notify(
                    f"{outcome.agent_id} blocked",
                    body="Waiting on input; not answering automatically.",
                )
            except Exception as exc:  # noqa: BLE001 - notification failure must not crash supervision
                print(f"(notification failed: {exc})")

        def on_done(outcome: SuperviseOutcome) -> None:
            excerpt_tail = "\n".join(outcome.excerpt.strip().splitlines()[-20:])
            print(f"[done] {outcome.agent_id} settled. Recent output:\n{excerpt_tail}")
            print(f"[done] {outcome.agent_id} did not advance any task; review and run `deskops advance` yourself.")

        outcomes = run_supervise_loop(
            provider,
            agent_id,
            max_iterations=max_iterations,
            read_lines=read_lines,
            timeout_ms=getattr(args, "timeout_ms", None),
            on_blocked=on_blocked,
            on_done=on_done,
        )
        if outcomes and outcomes[-1].status in {"timeout", "unknown"}:
            print(f"[{outcomes[-1].status}] stopped supervising {agent_id}.")
            return 1
        return 0

    def _workers(self, args: Any, executable: str) -> int:
        """List live Herdr agents machine-wide, grouped by workspace.

        Joins ``herdr agent list`` with ``herdr workspace list`` so each
        space shows its readable label and Herdr's own ordering by workspace
        number. Agents whose workspace is unknown to Herdr are kept in a
        trailing group rather than dropped.
        """
        provider = HerdrProvider(HerdrClient(executable))
        agents = provider.list_agents()
        spaces = group_agents_by_workspace(agents, provider.list_workspaces())
        payload = {
            "workers": [self._project_agent(agent) for agent in agents],
            "spaces": [
                {
                    "workspace": space["workspace"],
                    "label": space["label"],
                    "number": space["number"],
                    "status": space["status"],
                    "workers": [self._project_agent(agent) for agent in space["workers"]],
                }
                for space in spaces
            ],
        }
        return render(payload, getattr(args, "format", "text"), lambda _data: self._format_workers(agents, spaces))

    @staticmethod
    def _format_workers(agents: list[dict[str, Any]], spaces: list[dict[str, Any]]) -> str:
        if not agents:
            return "No live Herdr agents."
        lines: list[str] = []
        for space in spaces:
            lines.append(
                f"{space['workspace'] or '-'}  {space['label'] or '-'}  ({len(space['workers'])} workers)"
            )
            for agent in space["workers"]:
                lines.append(
                    f"  {agent.get('pane_id', '')} | {agent.get('agent', '')} | {agent.get('name') or '-'} | {agent.get('agent_status', '')} | {agent.get('cwd') or ''}"
                )
        return "\n".join(lines)

    @staticmethod
    def _project_agent(agent: dict[str, Any]) -> dict[str, Any]:
        """Project one raw Herdr agent onto the stable public worker shape."""
        return {
            "pane": agent.get("pane_id"),
            "kind": agent.get("agent"),
            "name": agent.get("name"),
            "status": agent.get("agent_status"),
            "cwd": agent.get("cwd"),
            "title": agent.get("terminal_title_stripped"),
            "workspace": agent.get("workspace_id"),
            "seq": agent.get("state_change_seq"),
            "focused": agent.get("focused"),
        }

FILE:tests/test_desk_sync.py
import json
import pytest
from pathlib import Path
from sldb.api.stores.init_store import init_store
from sldb.cli.commands.model import ModelCLI
from deskops.cli.main import CLI
from deskops.workspace import seed_desk
from sldb.api.documents.track_document_file import track_document_file
import yaml
from types import SimpleNamespace
from deskops.bootstrap import SLDBBootstrap

def test_desk_update_command(tmp_path: Path):
    # Setup desk
    cli = CLI()
    assert cli.run(["init", str(tmp_path)]) == 0

    desk_dir = tmp_path / "desk"
    store_dir = tmp_path / ".sldb"

    # Create untracked file
    untracked_path = desk_dir / "tasks" / "task-untracked.md"
    untracked_path.write_text("---\nid: task-untracked\nstatus: draft\ntags: []\n---\n# Untracked\n\n## Rationale\n\n## Goal\n")

    # Create tracked file then modify it to make hash stale
    tracked_path = desk_dir / "tasks" / "task-stale.md"
    tracked_path.write_text("---\nid: task-stale\nstatus: draft\ntags: []\n---\n# Stale\n\n## Rationale\n\n## Goal\n")
    track_document_file(
        store_dir, "TaskDoc", tracked_path, name="task-stale",
        pythonpath=str(Path(__file__).resolve().parents[1]), force=True
    )
    tracked_path.write_text("---\nid: task-stale\nstatus: draft\ntags: []\n---\n# Stale modified\n\n## Rationale\n\n## Goal\n")

    # Unregister a model
    store_idx = store_dir / "core" / "store_index.yaml"
    if not store_idx.exists():
        # Maybe it's json? No, sldb uses yaml for store_index now. 
        # But if not, we can just use bootstrap logic.
        store_idx = store_dir / "index.json"
    if store_idx.exists():
        if store_idx.suffix == ".yaml":
            with open(store_idx) as f: data = yaml.safe_load(f)
            data["models"] = [m for m in data["models"] if m["name"] != "DeskFAQDoc"]
            with open(store_idx, "w") as f: yaml.safe_dump(data, f)
        else:
            with open(store_idx) as f: data = json.load(f)
            data["models"] = [m for m in data["models"] if m["name"] != "DeskFAQDoc"]
            with open(store_idx, "w") as f: json.dump(data, f)

    # Test update (dry run)
    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 1

    # Test update apply
    assert cli.run(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0

    # Ensure it's clean now
    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 0



def test_desk_update_untracks_a_document_whose_file_is_gone(tmp_path: Path) -> None:
    """A deleted file must be untracked, not re-indexed.

    `git rm` on a tracked document leaves the store describing something that is
    not there, and neither 'stores update' nor an index rebuild clears it.
    """
    from deskops.cli.main import main
    from sldb.store.diagnostics import diagnose_store
    from sldb.api.model_registry.model_reference import resolve_model_ref

    assert main(["init", str(tmp_path)]) == 0
    assert main(
        ["add", "atom", "--root", str(tmp_path), "--title", "Gone soon",
         "--five-wh-one-plus", "what", "--answer", "Answered."]
    ) == 0

    atom = tmp_path / "desk" / "atoms" / "atom-gone-soon.md"
    assert atom.exists()
    atom.unlink()

    assert main(["desk", "update", "--root", str(tmp_path)]) != 0
    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0

    diagnosis = diagnose_store(
        tmp_path / ".sldb", resolve_model_ref, project_root=tmp_path, pythonpath=str(tmp_path)
    )
    notes = [doc.note.value for model in diagnosis.models for doc in model.documents]
    assert "missing" not in notes


def test_desk_update_apply_on_a_fresh_repo_writes_the_lifecycle_graph(tmp_path: Path, capsys) -> None:
    """One --apply on a fresh repo must leave a desk that the next update calls up to date."""
    cli = CLI()

    assert cli.run(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 0
    assert "Desk is up to date." in capsys.readouterr().out


def _make_faq_model_legacy(root: Path) -> None:
    """Rewrite the store as it looked when the deskops FAQ model was still `FAQDoc`."""
    store = root / ".sldb"
    index_path = store / "core" / "store_index.yaml"
    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    entry = next(model for model in index["models"] if model["name"] == "DeskFAQDoc")
    entry["name"] = "FAQDoc"
    entry["model_ref"] = "deskops.models:FAQDoc"
    entry["models_index"] = ".sldb/core/models/FAQDoc.yaml"
    index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")

    models_dir = store / "core" / "models"
    (models_dir / "DeskFAQDoc.yaml").rename(models_dir / "FAQDoc.yaml")
    model_index_path = models_dir / "FAQDoc.yaml"
    model_index = yaml.safe_load(model_index_path.read_text(encoding="utf-8"))
    model_index["name"] = "FAQDoc"
    model_index["model_ref"] = "deskops.models:FAQDoc"
    model_index["documents_index"] = ".sldb/core/documents/FAQDoc.yaml"
    model_index["sections_index"] = ".sldb/runtime/sections/FAQDoc.yaml"
    model_index_path.write_text(yaml.safe_dump(model_index, sort_keys=False), encoding="utf-8")

    documents_dir = store / "core" / "documents"
    (documents_dir / "DeskFAQDoc").rename(documents_dir / "FAQDoc")


def test_desk_update_apply_migrates_the_legacy_faq_model(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main
    from sldb.api import describe_model

    assert main(["init", str(tmp_path)]) == 0
    assert main(
        [
            "add",
            "faq-doc",
            "--root",
            str(tmp_path),
            "--title",
            "Legacy FAQ",
            "--body",
            "Question?\n\nAnswer.",
        ]
    ) == 0
    faq_path = tmp_path / "desk" / "faq" / "faq-legacy-faq.md"
    original = faq_path.read_bytes()
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()
    _make_faq_model_legacy(tmp_path)

    assert main(["desk", "update", "--root", str(tmp_path)]) == 1
    assert "Legacy FAQ model" in capsys.readouterr().out

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    names = {
        model["name"]
        for model in yaml.safe_load(
            (tmp_path / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8")
        )["models"]
    }
    assert "DeskFAQDoc" in names
    assert "FAQDoc" not in names

    documents = describe_model(
        tmp_path / ".sldb",
        "DeskFAQDoc",
        pythonpath=str(Path(__file__).resolve().parents[1]),
    ).documents
    assert [document.name for document in documents] == ["faq-legacy-faq"]
    assert faq_path.read_bytes() == original

    assert main(["desk", "update", "--root", str(tmp_path)]) == 0


def test_desk_update_does_not_call_the_owner_store_models_copies(tmp_path: Path, monkeypatch, capsys) -> None:
    from deskops.bootstrap import SLDBBootstrap
    from deskops.cli.main import main

    # Without an owner store, init registers the models directly, which is the
    # shape of the deskops owner store itself.
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    assert main(["init", str(tmp_path)]) == 0
    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    other = tmp_path.parent / f"{tmp_path.name}-owner" / ".sldb"
    other.mkdir(parents=True)
    capsys.readouterr()

    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: other)
    main(["desk", "update", "--root", str(tmp_path)])
    assert "Copied deskops models" in capsys.readouterr().out, "another store's direct models are copies"

    owner = tmp_path / ".sldb"
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: owner)
    main(["desk", "update", "--root", str(tmp_path)])
    assert "Copied deskops models" not in capsys.readouterr().out
def test_desk_update_apply_resigns_a_moved_model_contract(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main
    from sldb.store.hashing import hash_model_contract
    from deskops.models import RitualDoc

    assert main(["init", str(tmp_path)]) == 0
    model_path = tmp_path / ".sldb" / "core" / "models" / "RitualDoc.yaml"
    model_index = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    model_index["contract_hash"] = "0" * 64
    model_path.write_text(yaml.safe_dump(model_index, sort_keys=False), encoding="utf-8")
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(tmp_path)]) == 1
    assert "Moved model contracts: RitualDoc" in capsys.readouterr().out

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    resigned = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    assert resigned["contract_hash"] == hash_model_contract(RitualDoc)
    assert main(["desk", "update", "--root", str(tmp_path)]) == 0


def test_declared_includes_treat_extra_boards_in_tasks_as_boards(tmp_path: Path) -> None:
    """`deskops add board` writes `board-<slug>.md` next to Board.md (ARTIFACT_PATHS puts boards in
    tasks/); tracking it as a TaskDoc fails validation (no `status`) and breaks `desk update --apply`.
    The declared includes (deskops/data/desk_declaration.yaml) name it a BoardDoc, track the seeded
    Board by its path (CC35b d1) and leave the tasks to the paths that track them."""
    from deskops.workspace import pending_desk_includes
    from deskops.workspace import seed_desk

    seed_desk(tmp_path)
    tasks = tmp_path / "desk" / "tasks"
    (tasks / "board-compromisos-26-10.md").write_text("# Board\n", encoding="utf-8")
    (tasks / "task-doc-7.md").write_text("# Task\n", encoding="utf-8")

    pending = pending_desk_includes(tmp_path)
    assert ("BoardDoc", "desk/tasks/board-compromisos-26-10.md") in pending
    assert not any(path.startswith("desk/tasks/task-") for _model, path in pending), "tasks are tracked by their own paths"
    # Without a store, the lifecycle graph (CC31), the activation rules (CC32) and the seeded
    # Board (CC35b d1) the scaffold wrote are pending too.
    assert [row for row in pending if row[0] not in ("RelationTypeDoc", "RelationDoc", "RitualDoc", "RuleDoc")] == [
        ("BoardDoc", "desk/tasks/Board.md"),
        ("BoardDoc", "desk/tasks/board-compromisos-26-10.md"),
    ]


def test_declared_includes_cover_what_desk_update_used_to_guess(tmp_path: Path) -> None:
    """One `{model, glob}` per desk folder `desk update --apply` tracked by path, under the model's
    own id pattern; the scaffold's own files (pills.md) match no glob. The lifecycle graph is tracked
    by its declared paths (CC31): the RelationDocs by name, the lifecycle rituals by their ids; the
    activation rules (CC32) and the closeout rules (CC33b) by their globs, the seeded Board and phase ritual by theirs (CC35b d1)."""
    from deskops.workspace import desk_declaration

    include = desk_declaration("x").include
    rules: dict[str, list[str]] = {}
    for rule in include:
        if "glob" in rule:
            rules.setdefault(rule["model"], []).append(rule["glob"])
    listed = {rule["model"]: rule["paths"] for rule in include if "paths" in rule}
    assert listed == {
        "RelationDoc": [
            "desk/lifecycle/execution-task_activates.md",
            "desk/lifecycle/testing-task_hands_to_closeout.md",
            "desk/lifecycle/testing-task_returns_to_execution.md",
            "desk/lifecycle/closeout-task_completes.md",
        ],
        "BoardDoc": ["desk/tasks/Board.md"],
        "RitualDoc": [
            {"path": "desk/rituals/phase.md", "name": "ritual-phase"},
            {"path": "desk/rituals/execution.md", "name": "ritual-execution"},
            {"path": "desk/rituals/testing.md", "name": "ritual-testing"},
            {"path": "desk/rituals/closeout.md", "name": "ritual-closeout"},
        ],
    }
    assert rules == {
        "RelationTypeDoc": ["desk/lifecycle/type-*.md"],
        "RuleDoc": ["desk/lifecycle/rule-activation-*.md", "desk/lifecycle/rule-closeout-*.md"],
        "BoardDoc": ["desk/tasks/board-*.md"],
        "PillDoc": ["desk/contexts/pill-*.md"],
        "RitualDoc": ["desk/rituals/ritual-*.md"],
        "AtomDoc": ["desk/atoms/atom-*.md"],
        "ProtoAtomDoc": ["desk/atoms/proto-*.md"],
        "RoleDoc": ["desk/roles/*.md"],
        "RepositoryDoc": ["desk/registry/*.md"],
        "StepDoc": ["desk/steps/*.md"],
        "DeskFAQDoc": ["desk/faq/*.md"],
    }


def test_desk_update_apply_keeps_the_local_path_of_a_declared_model(tmp_path: Path, monkeypatch, capsys) -> None:
    """A store that declares a deskops model with a local source path keeps that path."""
    from deskops.cli.main import main

    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    assert main(["init", str(tmp_path)]) == 0
    source = tmp_path / "deskops" / "models" / "role.py"
    source.parent.mkdir(parents=True)
    source.write_text("# local model source\n", encoding="utf-8")
    store_yaml = tmp_path / ".sldb" / "store.yaml"
    store = yaml.safe_load(store_yaml.read_text(encoding="utf-8"))
    for entry in store["models"]:
        if entry["name"] == "RoleDoc":
            entry["path"] = "deskops/models/role.py"
    store_yaml.write_text(yaml.safe_dump(store, sort_keys=False), encoding="utf-8")
    store_index_path = tmp_path / ".sldb" / "core" / "store_index.yaml"
    store_index = yaml.safe_load(store_index_path.read_text(encoding="utf-8"))
    for entry in store_index["models"]:
        if entry["name"] == "RoleDoc":
            entry["path"] = "deskops/models/role.py"
    store_index_path.write_text(yaml.safe_dump(store_index, sort_keys=False), encoding="utf-8")
    model_path = tmp_path / ".sldb" / "core" / "models" / "RoleDoc.yaml"
    index = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    index["path"] = "deskops/models/role.py"
    model_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")

    # Another deskops checkout owns the models; this store only declares local copies.
    owner_root = tmp_path.parent / f"{tmp_path.name}-owner"
    owner_root.mkdir()
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    assert main(["init", str(owner_root)]) == 0
    owner = owner_root / ".sldb"
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: owner)
    capsys.readouterr()

    main(["desk", "update", "--root", str(tmp_path), "--apply"])
    capsys.readouterr()

    after = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    assert after["path"] == "deskops/models/role.py"
    store_after = yaml.safe_load(store_yaml.read_text(encoding="utf-8"))
    role = next(entry for entry in store_after["models"] if entry["name"] == "RoleDoc")
    assert role.get("path") == "deskops/models/role.py"
    assert not role.get("origin")

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
    # an executor that ends blocked or without changes does not advance the task
    assert "sciontool status blocked" in worker["agents.md"]
    assert "do NOT run `deskops advance task`" in worker["agents.md"]

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


def test_pi_tools_are_option_and_value_as_separate_args(profiles: dict[str, dict]) -> None:
    role = {"id": "role-x", "name": "x", "description": "d", "kind": "pi", "model": "", "tools": ["read", "grep", "bash"], "body": "# x"}
    agent = yaml.safe_load(scion_template_files(role, profiles["pi"], harness="pi")["scion-agent.yaml"])
    assert agent["command_args"] == ["--tools", "read,grep,bash"]


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


@pytest.mark.parametrize("mode", ["executor", "tester"])
def test_executor_and_tester_agents_md_build_their_own_py312_venv(
    executor: dict, profiles: dict[str, dict], mode: str, tmp_path: Path
) -> None:
    for d in ("desk/desk", "desk/deskops", "sldb/src/sldb"):
        (tmp_path / d).mkdir(parents=True)
    ws = str(tmp_path)
    ctx = {
        "desk_root": f"{ws}/desk",
        "source_root": f"{ws}/desk",
        "sldb_root": f"{ws}/sldb/src",
        "workspace_root": ws,
        "project": "p",
    }
    files = scion_template_files(executor, profiles["claude"], harness="claude", mode=mode, context=ctx)
    text = files["agents.md"]
    assert "uv venv /tmp/ws-venv --python 3.12" in text
    assert "import xdist" in text and "-n 4" in text
    assert f'uv pip install -e "{ws}/desk[dev]" -e {ws}/sldb' in text
    assert 'PATH="/tmp/ws-venv/bin:$PATH"' in text and "unset PYTHONPATH" in text
    assert text.index("Python environment") < text.index("Recover state first")


def test_two_attempts_get_two_rundocs_with_intent_and_external_ref(tmp_path: Path) -> None:
    first = record_scion_run(
        tmp_path, task_id="task-a", role_id="role-deskops-executor", kind="claude",
        agent_slug="deskops-e-abc123abc123", run_dir="runs/subagents/exec-1", attempt=1,
    )
    second = record_scion_run(
        tmp_path, task_id="task-a", role_id="role-deskops-executor", kind="claude",
        agent_slug="deskops-e-abc123abc123", run_dir="runs/subagents/exec-2", attempt=2,
    )
    one = extract_model_data(RunDoc, first.read_text(encoding="utf-8"))
    two = extract_model_data(RunDoc, second.read_text(encoding="utf-8"))
    assert one["id"] == "run-deskops-e-abc123abc123"
    assert two["id"] == "run-deskops-e-abc123abc123-a2"
    assert two["external_ref"] == "scion://agent/deskops-e-abc123abc123-a2"
    assert one["intent_at"] and one["dispatch_confirmed_at"] == ""
    assert one["outcome"] == "in_progress"


def test_confirm_scion_dispatch_sets_the_confirmation_once(tmp_path: Path) -> None:
    from deskops.runtime.scion import confirm_scion_dispatch

    run_dir = "runs/subagents/exec-1"
    path = record_scion_run(
        tmp_path, task_id="task-a", role_id="role-deskops-executor", kind="claude",
        agent_slug="deskops-e-abc123abc123", run_dir=run_dir,
    )
    assert confirm_scion_dispatch(tmp_path, run_dir) is True
    assert confirm_scion_dispatch(tmp_path, run_dir) is False
    data = extract_model_data(RunDoc, path.read_text(encoding="utf-8"))
    assert data["dispatch_confirmed_at"] and data["intent_at"]


def test_a_rundoc_without_the_new_fields_still_reads() -> None:
    old = """---
id: run-old
task_id: task-a
role_id: role-x
kind: claude
run_dir: runs/subagents/old
herdr_pane_id: ''
session_path: ''
session_sha256: ''
started_at: '2026-10-01T00:00:00+00:00'
ended_at: ''
outcome: in_progress
commit_sha: ''
tags: []
---

# Old

## Summary

old
"""
    data = extract_model_data(RunDoc, old)
    assert data["id"] == "run-old"

FILE:tests/fixtures/golden/help/deskops_runtime_template.txt
usage: deskops runtime template [-h] [--root ROOT] [--harness HARNESS]
                                [--out OUT]
                                [--model-alias {small,medium,large,extra-large}]
                                [--harness-auth {api-key,oauth-token,auth-file,vertex-ai}]
                                [--task-repo TASK_REPO]
                                [--mode {executor,coordinator,tester,specialist}]
                                [--context-file CONTEXT_FILE] [--task TASK]
                                [--agent AGENT] [--task-root TASK_ROOT]
                                [--run-dir RUN_DIR]
                                role_id

Materialize a RoleDoc + RuntimeProfileDoc as a Scion agent template (scion-
agent.yaml, system-prompt.md, agents.md).

positional arguments:
  role_id               RoleDoc id or name, e.g. role-deskops-executor or
                        deskops-executor.

options:
  -h, --help            show this help message and exit
  --root ROOT           Target repository root.
  --harness HARNESS     Scion harness-config / runtime kind to target (claude,
                        codex, antigravity, pi); defaults to the role's kind.
  --out OUT             Template directory; defaults to
                        <root>/.scion/templates/<role-name>/.
  --model-alias {small,medium,large,extra-large}
                        Portable Scion model size alias written to the
                        template (the harness-config resolves it).
  --harness-auth {api-key,oauth-token,auth-file,vertex-ai}
                        auth_selectedType written to the template (claude:
                        auth-file uses the CLAUDE_AUTH credentials secret,
                        oauth-token uses CLAUDE_CODE_OAUTH_TOKEN). Default:
                        claude -> oauth-token, other harnesses -> none.
  --task-repo TASK_REPO
                        Repository under /workspace the agent may write to;
                        named in agents.md.
  --mode {executor,coordinator,tester,specialist}
                        Which agents.md to write: executor (one bounded task),
                        tester (independent verification), specialist (leaves
                        the sldb store clean) or coordinator (owns a desk).
                        Default: by the selected role's name/id; an explicit
                        mode wins.
  --context-file CONTEXT_FILE
                        JSON with project, workspace_root, desk_root,
                        source_root and sldb_root; emits DESKOPS_*
                        environment, PYTHONPATH and a workspace volume.
                        Omitted: no context keys, previous behavior.
  --task TASK           Task id being dispatched; with --agent, also records a
                        RunDoc under runs/subagents/.
  --agent AGENT         Scion agent slug for the RunDoc (what you pass to
                        `scion start`).
  --task-root TASK_ROOT
                        Repository root whose desk owns --task; the RunDoc is
                        written there (defaults to --root).
  --run-dir RUN_DIR     Existing evidence directory (relative to the task
                        root) the RunDoc points at; defaults to a new
                        runs/subagents/<ts>-<task> path.

FILE:tests/fixtures/golden/scaffold/init.json
{
  "desk_name": "golden-desk",
  "files": {
    "desk/atoms/tag-namespaces.yaml": "e0ce95fd0a0c8faf71f9455540a49ea1237f8e2c45756d11e03e0e01c64ea490",
    "desk/config.json": "f14803cf45789d2c46a629df0ebbf5d76ce48b62b4b9e9b45b8ff5edf2ff843b",
    "desk/contexts/pills.md": "f9d6c0a6d7627bd9725d45f73c889059dea5bc43aa4a9c0f2f3598bbca31b2b5",
    "desk/drawer/README.md": "bedd04b7bf954932f544a44742246a36f73bcf94af25998608ac4dfa65a5b6f8",
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
    "desk/lifecycle/testing-task_returns_to_execution.md": "6028e8c2f0b4daea76bad68e92cf4ac8edb17b8975aca237df2c1d3169371193",
    "desk/lifecycle/type-task_activates.md": "82694800f31844ed3b86b5913f2cbf02eaebf24f4143a8a4542a64374d9217b5",
    "desk/lifecycle/type-task_completes.md": "5b3f4ce0793df8b2ee535b6b37490b8d0abdd4c8bb8b43b330ddb6134ead7f0f",
    "desk/lifecycle/type-task_hands_to_closeout.md": "d16cc9c1d329c8d362e0d08c9ba3d6f23bbc7538429fd82cf20540c593f700bf",
    "desk/lifecycle/type-task_returns_to_execution.md": "4046d511fd0a115b08243b37914deb9f7dfd3b9a623b0dcadac51ab4a1ec259f",
    "desk/rituals/closeout.md": "b2afbd1d1d3a1d292c1509add5877e5537fd450b1336346401e40b42f64b0c17",
    "desk/rituals/execution.md": "dc201702b3e015634c18724b162e71cfd542103029667990d2fa140bf19c4174",
    "desk/rituals/phase.md": "885d511461bb712f8c542d187d931f51ff18c9831622b7965300e3ce7aa7e48e",
    "desk/rituals/testing.md": "c1949f8d04c94205d46e143a9f53fb6959f94abd03bc8df32d627d7e05082fc8",
    "desk/runtimes/runtime-pi-deepseek-flash.md": "d505ab97e1f3ed07fe01b72c1995abd4f450490ebc281fa4fa78ecc5347a6f54",
    "desk/tasks/Board.md": "b3a1b3c5559c33320e688aa8bc47d18dc945a144f017ec6eefd57dc2ac351d80"
  }
}

FILE:tests/fixtures/golden/scaffold/update.json
{
  "desk_name": "golden_desk",
  "files": {
    "desk/atoms/atom-golden-one.md": "83ca9a1565d606883dfd3e7fa539d4ba86bf96e9b8d5069ec821f361b59fd6d3",
    "desk/atoms/atom-golden-two.md": "0b0523ee366564d7156c7a5fca286235d50213a7417f9f92ca2486672461f0b3",
    "desk/atoms/tag-namespaces.yaml": "e0ce95fd0a0c8faf71f9455540a49ea1237f8e2c45756d11e03e0e01c64ea490",
    "desk/config.json": "c722f11b39a34ac0ebb54809ed17f6d535a5d8e16960717930792cf441085d1b",
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
    "desk/lifecycle/testing-task_returns_to_execution.md": "6028e8c2f0b4daea76bad68e92cf4ac8edb17b8975aca237df2c1d3169371193",
    "desk/lifecycle/type-task_activates.md": "82694800f31844ed3b86b5913f2cbf02eaebf24f4143a8a4542a64374d9217b5",
    "desk/lifecycle/type-task_completes.md": "5b3f4ce0793df8b2ee535b6b37490b8d0abdd4c8bb8b43b330ddb6134ead7f0f",
    "desk/lifecycle/type-task_hands_to_closeout.md": "d16cc9c1d329c8d362e0d08c9ba3d6f23bbc7538429fd82cf20540c593f700bf",
    "desk/lifecycle/type-task_returns_to_execution.md": "4046d511fd0a115b08243b37914deb9f7dfd3b9a623b0dcadac51ab4a1ec259f",
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
    "- Missing desk structure: desk/tasks/Board.md, desk/rituals/phase.md, desk/runtimes/runtime-pi-deepseek-flash.md",
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
    "Lifecycle graph: tracked desk/lifecycle/testing-task_returns_to_execution.md",
    "Lifecycle graph: tracked desk/lifecycle/type-task_activates.md",
    "Lifecycle graph: tracked desk/lifecycle/type-task_completes.md",
    "Lifecycle graph: tracked desk/lifecycle/type-task_hands_to_closeout.md",
    "Lifecycle graph: tracked desk/lifecycle/type-task_returns_to_execution.md",
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
    "Lifecycle graph: wrote desk/lifecycle/testing-task_returns_to_execution.md",
    "Lifecycle graph: wrote desk/lifecycle/type-task_activates.md",
    "Lifecycle graph: wrote desk/lifecycle/type-task_completes.md",
    "Lifecycle graph: wrote desk/lifecycle/type-task_hands_to_closeout.md",
    "Lifecycle graph: wrote desk/lifecycle/type-task_returns_to_execution.md",
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
Cold-bundle de la tarea task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_desk_sync.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

