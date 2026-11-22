# Result summary
run_id: run-deskops-e-4ba4e5b27cdb
session: scion://agent/deskops-e-4ba4e5b27cdb
session_sha256: n/a (no session file available)

Commit f736c7ba on branch deskops/deskops-e-4ba4e5b27cdb (worktree .worktrees/deskops-e-4ba4e5b27cdb).

## Changed files
deskops/models/run.py, deskops/runtime/scion.py, deskops/services/closure.py, deskops/dispatch.py,
tests/test_scion_runtime.py, tests/test_closeout.py, tests/fixtures/model_contract_hashes.json
(deskops/dispatch.py is outside the listed files: it passes attempt=identity["attempt"] and calls confirm_scion_dispatch after `scion start`.)

## What
- Scion API: Agent.RunID/PreviousRunIDs are `json:"-"`, not exposed -> only internal identity; documented in run.py docstring.
- RunDoc: new intent_at, dispatch_confirmed_at, external_ref (None reads as "" so old RunDocs still read). Docstring rewritten (writers, fields, id format).
- record_scion_run(attempt=1|2): id run-<slug> / run-<slug>-a2, sets intent_at, external_ref scion://agent/<slug>. confirm_scion_dispatch(root, run_dir) sets dispatch_confirmed_at once.
- closure.close_with_run: updates the RunDoc whose run_dir matches (outcome=success, ended_at) inside the closing commit; restored if the close fails; commit_sha is written AFTER the commit (hash cannot be in its own commit), so it stays as an uncommitted working-tree change in run.md/.sldb. resolved-by / --no-run untouched.
- Snapshot hash for RunDoc edited by hand in the fixture.
- Tests: two attempts -> two RunDocs; closeout of attempt 2 updates only it; old RunDoc without new fields reads; --no-run leaves RunDocs.

## Review
- Outcome is always "success" on closeout --run-dir (no failure signal exists there).
- commit_sha left uncommitted after closeout (see above).
- Full-suite failure list: see validation.log (PYTHONPATH artifact, passes on origin/main and with PYTHONPATH unset).
