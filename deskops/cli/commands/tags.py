from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.errors import UsageError


class TagsCLI:
    """Bring the desk's documents to one tag vocabulary."""

    def run(self, args: Any) -> int:
        if args.tags_command != "migrate":
            raise UsageError(f"Unknown tags command: {args.tags_command}")
        from deskops.tag_migration import apply_tag_migration
        from deskops.tag_migration import plan_tag_migration
        from deskops.tag_migration import reindex_stale_documents
        from deskops.tag_migration import stale_semantic_documents
        from deskops.tag_migration import summarize

        root = Path(args.root).resolve()
        changes = plan_tag_migration(root)
        stale = stale_semantic_documents(root)
        if not changes and not stale:
            print("No document carries a duplicate, class-name or model-restating tag.")
            return 0
        if changes:
            print(f"{len(changes)} document(s) carry tags the model or the list already says:")
            for tag, count in sorted(summarize(changes).items(), key=lambda item: (-item[1], item[0])):
                print(f"  {count:5d}  {tag}")
        if stale:
            print(f"{sum(len(docs) for docs in stale.values())} document(s) have a semantic index older than their model's semantics:")
            for model, docs in stale.items():
                print(f"  {len(docs):5d}  {model}")
        if not args.apply:
            print("Dry run; pass --apply to rewrite and reindex them.")
            return 0
        if changes:
            print(f"Rewrote {apply_tag_migration(root, changes)} document(s).")
        # Rewriting already indexed those documents; reindex what is still behind its model.
        stale = stale_semantic_documents(root)
        if stale:
            print(f"Reindexed {reindex_stale_documents(root, stale)} document(s) through sldb.")
        return 0
