# Result
run_id: exec-deskops-e-a3513307b96e
session: n/a (no child session path available)
session_sha256: n/a

Fix: `_git` in deskops/dispatch.py now runs git with LC_ALL=C and LANGUAGE= so the "would be overwritten" message that reap parses is never localized; same message, same rc 8.
Added test test_reap_names_the_files_under_a_spanish_locale (reruns the scenario with es_ES env).
Files committed (worktree branch deskops/deskops-e-a3513307b96e): deskops/dispatch.py, tests/test_dispatch.py, CHANGELOG.md.
Validation: see validation.log (both locales pass, 36 tests).
Review note: I did not run the new test against the unfixed code to show it failing first (p1).
