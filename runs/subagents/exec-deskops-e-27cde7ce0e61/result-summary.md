# Result summary
run_id: exec-deskops-e-27cde7ce0e61
session: (not recorded by the executor)
session_sha256: (not available)

## What changed (worktree branch deskops/deskops-e-27cde7ce0e61)
- deskops/doctor_findings.py: `read_store_check` no longer reports sldb `anchors/doc_lost` alerts of a ReviewDoc
  `subject` when the task has a closeout commit in git (trailer Task-Id plus Closeout-Mode or Run-Id; new `closed_task_ids`).
  This covers receipts already lost (backfill) with no manual step. Remaining lost receipts go to `Findings.lost`
  and print under their own section saying `desk update --apply` does not repair them (restore the task or close it).
- deskops/cli/commands/doctor.py: wires `findings.lost` into the report and the alert count.
- tests/test_doctor_lost_receipts.py: closed task (run-dir and resolved-by trailers) -> no alert; task gone with only a code commit -> alert, no `desk update` hint.

## Decisions for review
- The closeout does not re-anchor or archive receipts (sldb owns anchors); doctor reads closure from git instead.
  Closure recorded only in the store (no git trailer) is not recognised.
- "Closed" = any commit with Task-Id plus Closeout-Mode/Run-Id trailer.
