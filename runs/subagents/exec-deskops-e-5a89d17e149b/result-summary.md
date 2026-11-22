# Result summary
run_id: exec-deskops-e-5a89d17e149b
session: n/a (not available to the executor)
session_sha256: n/a

Changed (committed in worktree branch deskops/deskops-e-5a89d17e149b): tests/fixtures/golden/help/deskops_drawer.txt (remove description now matches current help).

--update-golden also rewrote other goldens, reverted with git checkout (environment-dependent, out of scope):
help/deskops.txt, deskops_add.txt, deskops_edit.txt, deskops_list.txt, deskops_show.txt (usage line wrapping differs in this env), and deleted output/advance_lifecycle_seed_out_of_date.text, desk_update_legacy_migration.text, desk_update_nonterminal_migration.text, doctor_invalid_task.text, doctor_lifecycle_seed_out_of_date.text (update-golden removes goldens it considers unused/skipped here).
Validation: tests/test_output_goldens.py 7 passed without --update-golden; commit touches only deskops_drawer.txt.
