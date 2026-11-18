# Result: task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook

run_id: run-deskops-e-9fc95085d5a3
session: scion://agent/deskops-e-9fc95085d5a3
session_sha256: (none recorded)

## Changes (uncommitted)
- desk/roles/role-sldb-store-specialist.md (+ .sldb RoleDoc): created with `deskops add role --name sldb-store-specialist --kind pi --tools read grep find ls bash`, model copied from deskops-tester; body transcribes Goal a-f.
- deskops/runtime/scion.py: mode `specialist` (explicit + resolved by `-specialist` suffix on name/id), new `_render_specialist_agents_md`, `scion_child_identity` accepts `specialist` -> `deskops-s-<12hex>`.
- deskops/cli/registry.py: `--mode` choices include specialist.
- tests/test_scion_runtime.py: 3 new tests (a-e of Validation).
- docs/operator-manual.md: hook example `encola-especialista-de-store` + mode description.
- Dead code/tests: none left unreferenced (grep), nothing deleted.

## Validation (see validation.log)
- pytest tests/test_scion_runtime.py: 39 passed (run with the deskops tool python + sldb venv site-packages; no pytest in the tool env).
- runtime template sldb-store-specialist --out /dev/shm/...: exit 0, dir removed.
- `deskops graph missing --root .`: exit 1, 47 missing declared targets, identical to the snapshot taken before my changes (graph.txt); none mention this task. PRE-EXISTING, supervisor must review.
- sldb stores check: many pre-existing doc_lost alerts from other tasks; the new RoleDoc is not reported unregistered. Only doc_changed alerts for this task's own preflight reviews (anchors to the task, which was edited by the lifecycle).

## Notes
- Manual says the coordinator's scion start recipe is the one in the coordinator agents.md (the manual itself has no scion start recipe).
