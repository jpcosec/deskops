# Result summary

run_id: exec-deskops-e-31759c7475bf
session: (not available to the executor)
session_sha256: (not available to the executor)

Commit (branch deskops/deskops-e-31759c7475bf): 1d6ffdee875966e98f3b5fff8bab5d74d0e1e0e5, trailer Task-Id present.

## Changes
- deskops/graph/checks.py: a missing_declared_target whose source is a task:* node and whose target is source_file:/test_file:/doc: becomes kind=planned_target (record=True, same reason) unless the TaskDoc frontmatter status is closed/superseded/cancelled/retired (absent/unknown = open).
- deskops/cli/commands/graph.py: summary is now "N missing, M informational (P planned_target)".
- tests/test_graph_checks.py: 4 new tests (open task -> planned_target; no status -> planned; closed -> missing; non-task issue -> missing).
- tests/test_graph_declared_edges.py: 2 summary assertions updated to the new format.

## Validation (see validation.log)
- Focused graph tests: 39 passed.
- Full suite -n 4 in the worktree: 1333 passed, 3 skipped, 1 xfailed, 0 failures (6376s). No baseline comparison needed.
- deskops graph missing on the real desk with worktree code: 38 missing -> 25 missing + 13 planned_target.

## For the reviewer
- The installed deskops points at the main checkout, so the real-desk check was run with the worktree on sys.path.
- The 25 remaining missing are unprefixed paths (desk/drawer/... .md/.yaml) the extractor gives no source_file/test_file/doc kind; out of scope (extractor not to change).
- A misspelled path in an open task also shows as planned_target (accepted per task).
- Run dir also holds board/task/next/graph/git-status snapshots taken before the commit.
