# Result summary

run_id: run-deskops-e-e54423baf717
session: scion://agent/deskops-e-e54423baf717
session_sha256: (not recorded; scion session)

## What changed (uncommitted)
- `deskops/data/lifecycle/testing-task_returns_to_execution.md`, `type-task_returns_to_execution.md`: new seeds (same frontmatter shape as the hands_to_closeout pair; empty condition; sets.status active, terminal false, manual true). Both added to `deskops/data/desk_declaration.yaml` (managed files + RelationDoc include paths), so `deskops init` seeds them and `desk update --apply` delivers them.
- `deskops/lifecycle.py`: `Transition.manual`; `transitions_from(..., manual=False)` hides manual edges from the normal advance, gates and diagram (so normal `advance` is unchanged); `advance(..., back_reason=)` takes only manual edges, history entry `task_returns_to_execution: <reason>`, no manual edge -> blocked `no hay transicion de vuelta desde <nodo>`.
- `deskops/models/task_lifecycle.py`: the validator reads the relation type before `": "` of the last history item so the reason entry is coherent.
- `deskops/services/tasks.py`, `deskops/operations.py`: pass `back_reason`; post-hooks run as in any advance.
- `deskops/cli/registry.py`, `deskops/cli/commands/operations.py`: `--back`, `--reason`; exit 2 for `--back` without/empty `--reason` and `--reason` without `--back`; blocked -> exit 1 (same shape as a gate block).
- `deskops/runtime/scion.py`: executor agents.md gains the rule: blocked/no changes -> do NOT run `deskops advance task`, write the blocker, `sciontool status blocked "<reason>"`.
- `docs/operator-manual.md`: new subsection "Going back from testing" under "Inspect, edit, and advance a task".
- Tests: new in `tests/test_lifecycle_graph.py` (seed + normal advance untouched, back with reason in history, 3 exit-2 cases + blocked case, post-hook on back edge); `tests/test_scion_runtime.py` (agents.md has `sciontool status blocked`); updated the lists in `tests/test_desk_sync.py`, `tests/test_task_lifecycle_validator.py`.
- Goldens: `tests/fixtures/golden/help/deskops_advance_task.txt`, `scaffold/init.json`, `scaffold/update.json` (only the new seeds). Other help goldens that `--update-golden` rewrote (atoms, closeout, review record, runtime) were pre-existing drift unrelated to this task; reverted with git checkout.

## Validation
See validation.log. No xdist in this env, so `-n 4` was not used (run serially).
`deskops doctor` on a fresh `deskops init` desk: "Desk is healthy", exit 0; the two new seeds are present.

## Review notes
- Manual edges are hidden from `deskops next/show` gates and the mermaid diagram (design choice to avoid churn); say if the diagram should show them.
- Unrelated pre-existing drift in help goldens (atoms/closeout/review/runtime) remains in the checkout for someone else.
