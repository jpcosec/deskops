from __future__ import annotations

import os
import sys
from pathlib import Path
import re
from typing import Any

from sldb.cli.model_utils import registered_model
from sldb.cli.store_context import get_store_context
from sldb.api import transaction
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import extract_model_data, render_model_markdown, validate_model_input_roundtrip
from sldb.store.layout import project_root

from deskops import doc_access
from deskops.models import RepositoryDoc
from deskops.identity import load_repository_registry, EcosystemIdentity
from deskops.identity import find_local_store
from deskops.identity import resolve_registered_root


class RepoCLI:
    """Handle repository registration and discovery."""

    def run(self, args: Any) -> int:
        if args.repo_command == "register":
            return self.register(args)
        if args.repo_command == "whoami":
            return self.whoami(args)
        if args.repo_command == "remove":
            return self.remove(args)
        return 1

    def register(self, args: Any) -> int:
        name = args.name
        path = args.path_option or args.path
        if not path:
            print("Error: repository path is required. Use 'deskops repo register <name> --path <abs>' or provide the positional path.")
            return 1
        repo_id = args.id or self._slug(name)
        description = args.description or f"Repository for {name}."
        tags = [t.strip() for p in (args.tags or "").split(",") if (t := p.strip())]
        owns_paths = [t for p in (getattr(args, "owns_paths", None) or "").split(",") if (t := p.strip())]
        owns_topics = [t for p in (getattr(args, "owns_topics", None) or "").split(",") if (t := p.strip())]

        # Preflight: resolve store context and model before any mutation
        try:
            store_path, root = self._store_context(args)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        desk_root = self._desk_root(args)
        registry_dir = desk_root / "registry"
        resolved_repo_root = self._resolve_registered_root(root, path)
        payload = {
            "name": name,
            "id": repo_id,
            # Stored relative to the root of the repo that holds the registry directory
            # (desk/registry -> the desk's repo, ~/setup/desk/registry -> ~/setup), so the
            # entry resolves on any machine that checks the ecosystem out side by side.
            "path": self._registry_relative_path(registry_dir, resolved_repo_root),
            "status": "active",
            "description": description,
            "tags": tags,
            "owns_paths": owns_paths,
            "owns_topics": owns_topics,
        }

        try:
            model_type, entry, idx = registered_model(
                store_path, "RepositoryDoc", args.pythonpath
            )
        except SLDBStoreError:
            print("Error: RepositoryDoc model is not registered in the store.")
            print("Register it first with: python -m sldb models add deskops.models:RepositoryDoc --store <path>")
            return 1
        except (FileNotFoundError, OSError) as e:
            print(f"Error: cannot read store at {store_path}: {e}")
            return 1

        filename = f"repo-{repo_id}.md"
        output_path = registry_dir / filename

        if output_path.exists():
            print(f"Error: Repository file already exists at {output_path}")
            return 1

        try:
            existing_entries = load_repository_registry(desk_root, root)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        for existing_entry in existing_entries:
            if existing_entry.id == repo_id:
                print(
                    f"Error: Repository id '{repo_id}' is already registered by {existing_entry.source_path}."
                )
                return 1
            if existing_entry.repo_root is not None and resolved_repo_root == existing_entry.repo_root:
                print(
                    "Error: Repository root "
                    f"'{resolved_repo_root}' is already registered as '{existing_entry.id}' by {existing_entry.source_path}."
                )
                return 1

        from sldb.store.io import load_models_index, load_documents_index
        models_idx = load_models_index(root / entry.models_index)
        docs_idx = load_documents_index(root / models_idx.documents_index)
        if any(d.name == f"repo-{repo_id}" for d in docs_idx.documents):
            print(f"Error: Repository repo-{repo_id} is already registered in the store.")
            return 1

        rendered = render_model_markdown(model_type, payload)
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            print("Error: Repository registration failed validation.")
            for issue in details:
                print(f"  - {issue}")
            return 1

        # All prerequisites verified: the file and its tracking in one transaction.
        with transaction(store_path, args.pythonpath) as tx:
            tx.write_file(output_path, (rendered + "\n").encode("utf-8"))
            print(f"Wrote {output_path}")
            tx.track(output_path, "RepositoryDoc", f"repo-{repo_id}")
        print(f"Tracked 'repo-{repo_id}'")

        from deskops.workspace import read_project_identity

        desk_identity = read_project_identity(resolved_repo_root)
        if desk_identity is not None and desk_identity != repo_id:
            print(
                f"el desk de {path} dice project_identity {desk_identity}; "
                f"alinéalo con deskops repo whoami --set {repo_id} --root {path}",
                file=sys.stderr,
            )

        return 0

    def remove(self, args: Any) -> int:
        root = Path(args.root).resolve()
        desk_root = root / "desk"
        try:
            entries = load_repository_registry(desk_root, root)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        selector = args.selector
        matches = [
            entry
            for entry in entries
            if selector in {entry.id, entry.source_path.stem, f"repo-{entry.id}"}
        ]
        if not matches:
            known = ", ".join(sorted(entry.id for entry in entries)) or "(none)"
            print(f"Error: Repository '{selector}' is not registered. Registered ids: {known}")
            return 1
        if len(matches) > 1:
            paths = ", ".join(str(entry.source_path) for entry in matches)
            print(f"Error: Repository selector '{selector}' is ambiguous: {paths}")
            return 1

        entry = matches[0]
        doc_access.delete_doc(root, entry.source_path)
        print(entry.source_path)
        return 0

    def whoami(self, args: Any) -> int:
        if getattr(args, "set_identity", None) is not None:
            from deskops.errors import UsageError
            from deskops.workspace import set_project_identity

            try:
                previous = set_project_identity(Path(args.root).resolve(), args.set_identity)
            except UsageError as e:
                print(f"Error: {e}")
                return 1
            print(f"project_identity: {previous} -> {args.set_identity}")
            return 0
        try:
            project_id = EcosystemIdentity(args.store).what_repository_am_i_in(Path(args.root), require_registry_match=True)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1
        print(project_id)
        return 0

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "repo"

    def _desk_root(self, args: Any) -> Path:
        if args.store:
            return (project_root(Path(args.store).resolve()) / "desk").resolve()
        local_store = find_local_store()
        if local_store is not None:
            return (project_root(local_store) / "desk").resolve()
        return (Path.cwd() / "desk").resolve()

    def _store_context(self, args: Any) -> tuple[Path, Path]:
        if args.store:
            try:
                return get_store_context(args.store)
            except (SLDBStoreError, FileNotFoundError, OSError) as e:
                raise SLDBStoreError(str(e))
        local_store = find_local_store()
        if local_store is None:
            raise SLDBStoreError("No store found to anchor the registry.")
        return local_store, project_root(local_store)

    def _resolve_registered_root(self, ecosystem_root: Path, repo_path: str) -> Path:
        return resolve_registered_root(ecosystem_root, repo_path)

    def _registry_relative_path(self, registry_dir: Path, repo_root: Path) -> str:
        """``repo_root`` relative to the repo containing ``registry_dir`` (its grandparent)."""
        registry_repo_root = registry_dir.resolve().parent.parent
        return Path(os.path.relpath(repo_root, registry_repo_root)).as_posix()


class OwnerCLI:
    """`deskops owner <path|topic>`: which registered repo owns it."""

    def run(self, args: Any) -> int:
        import fnmatch

        from deskops.identity import ecosystem_registry_dir, load_ecosystem_registry

        root = Path(args.root).resolve()
        try:
            entries = {e.id: e for e in load_ecosystem_registry()}
            for e in load_repository_registry(root / "desk", root):
                entries[e.id] = e
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1
        eco_root = ecosystem_registry_dir().parent.parent
        target = args.target
        owners: dict[str, dict[str, Any]] = {}
        for entry in entries.values():
            payload = extract_model_data(RepositoryDoc, entry.source_path.read_text(encoding="utf-8"))
            owners[entry.id] = payload

        matches: list[str] = []
        looks_like_path = "/" in target or target.startswith((".", "~")) or Path(target).exists()
        rel = self._relative(target, eco_root)
        best = -1
        for repo_id, payload in owners.items():
            for glob in payload.get("owns_paths") or []:
                if rel is not None and self._glob_covers(glob, rel, fnmatch) and len(glob) > best:
                    best, matches = len(glob), [repo_id]
                elif rel is not None and self._glob_covers(glob, rel, fnmatch) and len(glob) == best and repo_id not in matches:
                    matches.append(repo_id)
        if not matches and looks_like_path:
            absolute = Path(target).expanduser()
            absolute = absolute if absolute.is_absolute() else eco_root / absolute
            absolute = absolute.resolve()
            deepest = -1
            for entry in entries.values():
                if entry.repo_root is None:
                    continue
                if absolute == entry.repo_root or entry.repo_root in absolute.parents:
                    depth = len(entry.repo_root.parts)
                    if depth > deepest:
                        deepest, matches = depth, [entry.id]
                    elif depth == deepest and entry.id not in matches:
                        matches.append(entry.id)
        if not matches:
            matches = [rid for rid, p in owners.items() if target in (p.get("owns_topics") or [])]
        if not matches:
            print("sin dueno")
            return 1
        if len(matches) > 1:
            for repo_id in sorted(matches):
                print(repo_id)
            return 2
        print(matches[0])
        return 0

    @staticmethod
    def _relative(target: str, eco_root: Path) -> str | None:
        path = Path(target).expanduser()
        if path.is_absolute():
            try:
                return path.resolve().relative_to(eco_root).as_posix()
            except ValueError:
                return None
        return Path(os.path.normpath(target)).as_posix()

    @staticmethod
    def _glob_covers(glob: str, rel: str, fnmatch: Any) -> bool:
        glob = glob.rstrip("/")
        if fnmatch.fnmatchcase(rel, glob):
            return True
        # A glob also covers everything under a directory it matches.
        parts = rel.split("/")
        return any(fnmatch.fnmatchcase("/".join(parts[:i]), glob) for i in range(1, len(parts)))
