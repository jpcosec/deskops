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
        from deskops.tag_migration import summarize

        root = Path(args.root).resolve()
        changes = plan_tag_migration(root)
        if not changes:
            print("No document carries a duplicate, class-name or model-restating tag.")
            return 0
        print(f"{len(changes)} document(s) carry tags the model or the list already says:")
        for tag, count in sorted(summarize(changes).items(), key=lambda item: (-item[1], item[0])):
            print(f"  {count:5d}  {tag}")
        if not args.apply:
            print("Dry run; pass --apply to rewrite them.")
            return 0
        print(f"Rewrote {apply_tag_migration(root, changes)} document(s).")
        return 0
