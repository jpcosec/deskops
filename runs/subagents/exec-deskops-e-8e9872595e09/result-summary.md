# Result summary
run_id: exec-deskops-e-8e9872595e09
session: (claude scion agent; no session file path available)
session_sha256: n/a

Reproduced: in a desk with store (`deskops init <path>`), `edit task <id> goal` left the Board line with the old goal. Without a store the Board is never rendered (unrelated).
Fix: `deskops/doc_access.py` `edit_artifact_field` now, for subject task and field title/status/goal, saves the Board again (`refresh_board`) in the same desk transaction, so sldb re-renders `task_summaries`.
`advance` leaves status unchanged on the checked path; not modified (out of the edit verb's scope).
Files: deskops/doc_access.py, tests/test_edit_task_refreshes_board.py (new), CHANGELOG.md.
Validation: see validation.log. Failing test before the fix confirmed.
