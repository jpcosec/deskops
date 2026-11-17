# Result summary

run_id: run-deskops-e-95ee81688bed
session: scion://agent/deskops-e-95ee81688bed
session_sha256: (not available; no session file)

## Done (uncommitted)
- deskops/lifecycle.py: Hook, parse_hooks, HookDefinitionError, Transition.raw_hooks/hooks, hooks_from_text/with_hooks/provenance_from_text, TransitionResult.transition; malformed hooks fail in `advance` before the payload changes.
- deskops/lifecycle_hooks.py (new): runs hooks in order (cwd=desk root, DESKOPS_* env, timeout default 300 s), log runs/hooks/<task>/<relation>-AAAAMMDDTHHMMSSZ.log.
- deskops/services/tasks.py: advance_task runs hooks after write_doc; on failure restores the original payload and returns blocked with the finding `error: [lifecycle/hook-failed] <relation>: hook '<n>' fallo: codigo de salida N | timeout tras N s; log: <path>`; next/show gates list hooks.
- deskops/cli/commands/operations.py: catches HookDefinitionError; prints Post-hooks in next, post-hook lines in show task.
- deskops/workspace.py (_keep_desk_hooks) + deskops/doctor_findings.py + cli/commands/doctor.py: desk update --apply keeps the whole hooks list (and sldb provenance of that copy); doctor ignores hooks.
- deskops/runtime/scion.py: executor runs `deskops advance task` before task_completed (blocked + finding on failure); coordinator verifies via `deskops show task`.
- atom-automatic-routines-vs-llm-tasks (edited by hand, as the task lists it) and docs/operator-manual.md (post-hooks section).
- Tests: 11 new in tests/test_lifecycle_graph.py (real sh/sleep hooks), 1 in tests/test_scion_runtime.py.

## For the supervisor
- Task restore compared by status/current_node/history, not bytes (sldb provenance timestamp changes).
- Atom edited by hand: check `sldb stores check`/index for it.
- Installed pytest into the deskops uv tool env (outside repo).
- Did not touch message.py / message & inbox tests / other runs.
- Full suite and closeout: coordinator.
