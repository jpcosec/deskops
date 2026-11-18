# Result summary

run_id: run-deskops-e-cd2f053c032d
session: scion://agent/deskops-e-cd2f053c032d
session_sha256: (not available)

## Done (uncommitted)
- deskops/dispatch.py (new): `deskops dispatch start <executor|tester> --task` and `dispatch reap --task`; every scion call goes through `_scion` (subprocess.run). Exit codes 0/2/3/4/5 as specified; `falta el campo dispatch en desk/config.json` -> 2.
- deskops/config.py: `dispatch` field (DispatchConfig/DispatchRoles/DispatchRole).
- deskops/cli/registry.py: group dispatch (+start, reap) after queue.
- tests/test_dispatch.py (new, 10 tests, fake `scion` executable first in PATH, no mocks).
- tests/test_cli.py, test_cli_grammar.py, test_command_registry.py: group declared.
- Goldens: tests/fixtures/golden/help/deskops.txt (modified) + deskops_dispatch{,_start,_reap}.txt (new); unrelated regenerated goldens reverted.
- docs/operator-manual.md: dispatch config + queue_jobs example.

## Review notes
- `scion list` JSON is assumed to be a list of agents (a dict with `agents` also accepted); fields name/phase/activity/labels.
- Role name for the template folder/sync/--type comes from find_role_doc; RunDoc written via record_scion_run in `start` (materialize_scion_template itself does not write it).
- A failing `templates sync` returns its exit code before start.
- The pre-existing unrelated dirty files were not touched. No git add/commit. Real scion never run.
