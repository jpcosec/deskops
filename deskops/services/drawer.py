"""Drawer lookup and inbox-to-drawer promotion.

The drawer holds disorganized material (features, issues, questions, loose task
candidates). This service resolves a drawer file by selector, records a task's
drawer origin, and promotes an inbox note into a loose drawer task candidate.
It never promotes drawer material into an active task.
"""

from __future__ import annotations

from deskops.slugs import ascii_slug

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
import re
from typing import Any
from typing import Callable

import yaml
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops import doc_access
from deskops.models import TaskDoc
from deskops.services.references import alert_dangling
from deskops.services.references import dangling_referrers


@dataclass
class DrawerPromotion:
    """Outcome of one inbox-to-drawer promotion, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


@dataclass
class DrawerRemoval:
    """Outcome of removing one drawer entry, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


class DrawerService:
    DRAWER_INDEX_FILES = {"README.md", "Board.md"}

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"

    def resolve_drawer_source(self, selector: str) -> Path:
        """The desk/drawer/ file a task is being authored from.

        Accepts a path (relative to the repo root, or absolute) or a stem /
        unique slug fragment searched across every drawer subfolder, since the
        drawer holds features, issues and questions, not only task candidates.
        The file must live under desk/drawer/.
        """
        drawer_root = (self.desk_root / "drawer").resolve()
        candidate = Path(selector)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            resolved = candidate.resolve()
            if drawer_root not in resolved.parents:
                raise ValueError(f"--from-drawer must point inside desk/drawer/: {selector}")
            return resolved
        if not drawer_root.exists():
            raise FileNotFoundError(f"No drawer found at {drawer_root}")
        files = self._drawer_files(drawer_root)
        exact = [path for path in files if selector in {path.name, path.stem}]
        matches = exact or [path for path in files if selector.lower() in path.stem.lower()]
        if not matches:
            raise FileNotFoundError(f"No drawer file matches '{selector}'")
        if len(matches) > 1:
            listing = ", ".join(str(path.relative_to(drawer_root)) for path in matches)
            raise ValueError(f"Ambiguous drawer selector '{selector}': {listing}")
        return matches[0].resolve()

    def _drawer_files(self, drawer_root: Path) -> list[Path]:
        """Every selectable drawer entry: .md files plus .yml/.yaml entries (plan dags are not entries)."""
        plans_root = drawer_root / "plans"
        found: list[Path] = []
        for path in drawer_root.rglob("*"):
            if not path.is_file() or path.name in self.DRAWER_INDEX_FILES:
                continue
            if path.suffix == ".md":
                found.append(path)
            elif path.suffix in {".yml", ".yaml"} and plans_root not in path.parents:
                found.append(path)
        return sorted(found)

    def resolve_plan_dir(self, selector: str, *, by_name: bool = True) -> Path | None:
        """The desk/drawer/plans/<plan>/ directory named by a path or a plan name (exact or unique fragment)."""
        plans_root = (self.desk_root / "drawer" / "plans").resolve()
        if not plans_root.is_dir():
            return None
        candidate = Path(selector)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_dir():
            resolved = candidate.resolve()
            if resolved.parent == plans_root:
                return resolved
            return None
        if not by_name:
            return None
        plans = sorted(path for path in plans_root.iterdir() if path.is_dir())
        exact = [path for path in plans if path.name == selector]
        matches = exact or [path for path in plans if selector.lower() in path.name.lower()]
        if len(matches) > 1:
            listing = ", ".join(path.name for path in matches)
            raise ValueError(f"Ambiguous drawer plan selector '{selector}': {listing}")
        return matches[0].resolve() if matches else None

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        """Record where an authored task came from, without copying or deleting it.

        Stored in the task's own from_drawer field, not in references:
        `deskops edit task <id> references ...` replaces that whole list (the
        closeout step does exactly that), which would silently drop the origin.
        One field, one fact -- no parallel tag that could drift from it.
        Cleanup of the drawer file is left to a human."""
        relative = drawer_file.resolve().relative_to(self.root.resolve()).as_posix()
        return {**payload, "from_drawer": relative}

    def promote_inbox_to_drawer_task(
        self,
        selector: str,
        title_override: str | None = None,
        *,
        parse_sections: Callable[[str], dict[str, Any]],
    ) -> DrawerPromotion:
        """Promote one inbox note into a loose drawer task candidate."""
        source = self._resolve_unique(self.desk_root / "inbox", selector)
        if source is None:
            return DrawerPromotion(1, [f"No inbox note found for {selector}"])
        if isinstance(source, list):
            listing = ", ".join(path.stem for path in source)
            return DrawerPromotion(1, [f"Ambiguous inbox note selector {selector}: {listing}"])

        note = self._read_markdown(source)
        title = (title_override or note["title"] or source.stem).strip()
        task_id = f"task-{self._slug(title)}"
        target = self.desk_root / "drawer" / "tasks" / f"{task_id}.md"
        if target.exists():
            return DrawerPromotion(1, [f"Drawer task already exists: {target}"])

        parsed = parse_sections(note["body"])
        messages = [f"Created drawer task candidate {task_id}"]
        with doc_access.desk_transaction(self.root) as transaction:
            if transaction is not None:
                transaction.record(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                self._render_drawer_task(
                    title=title,
                    task_id=task_id,
                    source_path=source.relative_to(self.root),
                    body=note["body"],
                    parsed_sections=parsed,
                ),
                encoding="utf-8",
            )
            # Untrack before deleting: the note is a tracked InboxNoteDoc, so
            # unlinking the file alone leaves an orphan entry in the store and
            # `deskops status` reports it as an invalid missing document.
            # Untrack first so a store failure cannot destroy the source file.
            untrack_message = self._untrack_note(source)
            if transaction is not None:
                transaction.record(source)
            source.unlink(missing_ok=True)
        if untrack_message:
            messages.append(untrack_message)
        messages.append(f"Deleted source file {source}")
        messages.append(f"Path: {target}")
        return DrawerPromotion(0, messages)

    def remove_entry(
        self,
        selector: str,
        *,
        force: bool = False,
        reason: str | None = None,
        refs: list[str] | None = None,
    ) -> DrawerRemoval:
        """Remove one drawer file, its tracking, and its bullets on the drawer board.

        Every other reference to it (``sldb.api.referrers`` over the desk graph) is left as it
        is and reported on stderr as ``alert: <entry> still referenced by <referrer>``.

        A task in desk/tasks/ that records the entry in from_drawer blocks the
        removal unless force is set, so deleting the source cannot silently
        leave active work pointing at a file someone still expects to exist.
        """
        try:
            plan = self.resolve_plan_dir(selector, by_name=False)
            if plan is not None:
                return self._remove_plan(plan, reason=reason, refs=refs)
            try:
                source = self.resolve_drawer_source(selector)
            except FileNotFoundError:
                plan = self.resolve_plan_dir(selector)
                if plan is None:
                    raise
                return self._remove_plan(plan, reason=reason, refs=refs)
        except (FileNotFoundError, ValueError) as exc:
            return DrawerRemoval(1, [f"Error: {exc}"])

        relative = source.relative_to(self.root).as_posix()
        if not force:
            owners = self._tasks_recording(relative)
            if owners:
                listing = ", ".join(owners)
                return DrawerRemoval(
                    1,
                    [
                        f"Error: refusing to remove {relative}: "
                        f"task records it in from_drawer ({listing}). Use --force to remove it anyway."
                    ],
                )

        board = self.desk_root / "drawer" / "tasks" / "Board.md"
        board_changed = False
        with doc_access.desk_transaction(self.root) as transaction:
            if board.exists():
                original = board.read_text(encoding="utf-8")
                updated = self._without_entry_bullets(original, source.stem)
                if updated != original:
                    if transaction is not None:
                        transaction.record(board)
                    board.write_text(updated, encoding="utf-8")
                    board_changed = True
            # Read after the Board lost its bullets: what is left still names the entry once it is gone.
            dangling = dangling_referrers(self.root, source)
            doc_access.delete_doc(self.root, source)
            assets = self._issue_assets_dir(source)
            removed_assets = None
            if assets is not None and not self._assets_referenced(assets, source):
                removed_assets = self._delete_tree(assets, transaction)
        alert_dangling(relative, dangling)

        messages = [f"Removed drawer entry {relative}"]
        if board_changed:
            messages.append(f"Removed its bullets from {board.relative_to(self.root).as_posix()}")
        if removed_assets:
            messages.append(f"Removed its assets {removed_assets}")
        messages.extend(self._registration(reason, refs))
        return DrawerRemoval(0, messages)

    @staticmethod
    def _registration(reason: str | None, refs: list[str] | None) -> list[str]:
        lines: list[str] = []
        clean_reason = " ".join((reason or "").split())
        if clean_reason:
            lines.append(f"Reason: {clean_reason}")
        clean_refs = [ref.strip() for ref in refs or [] if ref.strip()]
        if clean_refs:
            lines.append(f"Refs: {', '.join(clean_refs)}")
        return lines

    def _remove_plan(self, plan: Path, *, reason: str | None, refs: list[str] | None) -> DrawerRemoval:
        """Remove a whole plan directory: its files, their tracking and the drawer Board bullets naming the plan."""
        relative = plan.relative_to(self.root).as_posix()
        board = self.desk_root / "drawer" / "tasks" / "Board.md"
        board_changed = False
        with doc_access.desk_transaction(self.root) as transaction:
            if board.exists():
                original = board.read_text(encoding="utf-8")
                updated = self._without_entry_bullets(original, plan.name)
                if updated != original:
                    if transaction is not None:
                        transaction.record(board)
                    board.write_text(updated, encoding="utf-8")
                    board_changed = True
            self._delete_tree(plan, transaction)
        messages = [f"Removed drawer plan {relative}"]
        if board_changed:
            messages.append(f"Removed its bullets from {board.relative_to(self.root).as_posix()}")
        messages.extend(self._registration(reason, refs))
        return DrawerRemoval(0, messages)

    def _delete_tree(self, directory: Path, transaction: Any) -> str:
        """Delete every file under directory (tracked ones through the store), then the empty folders."""
        for path in sorted(p for p in directory.rglob("*") if p.is_file()):
            doc_access.delete_doc(self.root, path)
        for folder in sorted((p for p in directory.rglob("*") if p.is_dir()), reverse=True):
            folder.rmdir()
        directory.rmdir()
        return directory.relative_to(self.root).as_posix()

    def _issue_assets_dir(self, source: Path) -> Path | None:
        """desk/drawer/issues/assets/<stem>/ for a drawer issue, when it exists."""
        issues_root = self.desk_root / "drawer" / "issues"
        if source.parent != issues_root.resolve():
            return None
        assets = issues_root / "assets" / source.stem
        return assets.resolve() if assets.is_dir() else None

    def _assets_referenced(self, assets: Path, issue: Path) -> bool:
        """True when a desk document other than the removed issue and the drawer Board mentions the assets folder."""
        needle = f"assets/{assets.name}/"
        skip = {issue.resolve(), (self.desk_root / "drawer" / "tasks" / "Board.md").resolve()}
        for path in self.desk_root.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".yml", ".yaml"}:
                continue
            resolved = path.resolve()
            if resolved in skip or assets in resolved.parents:
                continue
            try:
                if needle in path.read_text(encoding="utf-8"):
                    return True
            except (OSError, UnicodeDecodeError):
                continue
        return False

    def _tasks_recording(self, relative: str) -> list[str]:
        """Active task ids in desk/tasks/ whose from_drawer points at relative."""
        tasks_dir = self.desk_root / "tasks"
        if not tasks_dir.exists():
            return []
        owners: list[str] = []
        for path in sorted(tasks_dir.glob("task-*.md")):
            try:
                payload = extract_model_data(TaskDoc, path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001 - one unreadable task must not block the check
                continue
            if payload.get("from_drawer") == relative:
                owners.append(str(payload.get("id") or path.stem))
        return owners

    def _without_entry_bullets(self, text: str, stem: str) -> str:
        """Drop every line that starts with ``- `<stem>` ``."""
        prefix = f"- `{stem}` "
        return "".join(
            line for line in text.splitlines(keepends=True) if not line.startswith(prefix)
        )

    def _untrack_note(self, source: Path) -> str | None:
        """Drop the promoted note from the sldb store, best effort.

        Returns a human-readable line describing what happened, or None when
        there is nothing to say. Never raises: a promotion must not be left
        half-done because the store was unavailable."""
        store_path = self.root / ".sldb"
        if not store_path.exists():
            return None
        try:
            doc_access.untrack_doc(self.root, source)
            return None
        except Exception as exc:  # noqa: BLE001 - store problems must not abort the promotion
            return f"Warning: could not untrack '{source.stem}' from the store: {exc}"

    def _resolve_unique(self, directory: Path, selector: str) -> Path | list[Path] | None:
        if not directory.exists():
            return None
        candidates = sorted(directory.glob("*.md"))
        exact = [path for path in candidates if selector in {path.name, path.stem}]
        if exact:
            return exact[0] if len(exact) == 1 else exact
        lowered = selector.lower()
        matches = [path for path in candidates if lowered in path.stem.lower()]
        if not matches:
            return None
        return matches[0] if len(matches) == 1 else matches

    def _read_markdown(self, path: Path) -> dict[str, str]:
        text = path.read_text(encoding="utf-8")
        frontmatter: dict[str, Any] = {}
        body = text
        if text.startswith("---\n"):
            _, rest = text.split("---\n", 1)
            fm_block, body = rest.split("\n---\n", 1)
            frontmatter = yaml.safe_load(fm_block) or {}
        lines = body.strip().splitlines()
        title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else str(frontmatter.get("title") or path.stem)
        content = "\n".join(lines[1:]).strip() if lines and lines[0].startswith("# ") else body.strip()
        return {"title": title, "body": content}

    def _render_drawer_task(
        self,
        *,
        title: str,
        task_id: str,
        source_path: Path,
        body: str,
        parsed_sections: dict[str, Any],
    ) -> str:
        # A drawer task is a TaskDoc like any other task, so `add task --from-drawer`,
        # the store and the readers that extract TaskDoc can all read it.
        fields = parsed_sections["fields"]
        validation = fields.get("validation") or []
        if isinstance(validation, str):
            validation = [line.lstrip("- ").strip() for line in validation.splitlines() if line.strip()]
        payload = {
            "id": task_id,
            "title": title,
            "status": "deferred",
            "why": fields.get("why") or f"Promoted from the inbox note `{source_path}`.",
            "goal": fields.get("goal") or f"Triage and resolve the inbox message promoted from `{source_path}`.",
            "scope": fields.get("scope") or body.strip() or "No additional detail provided.",
            "implementation_path": fields.get("implementation_path") or "To be defined when the task is promoted.",
            "validation": validation,
            "done_when": fields.get("done_when") or "The message is resolved, answered, or promoted into active work.",
            # The source note is deleted below, so it is named in `why`, not referenced.
            "tags": ["source:inbox"],
        }
        return render_model_markdown(TaskDoc, payload) + "\n"

    def _slug(self, text: str) -> str:
        return ascii_slug(text) or "task"
