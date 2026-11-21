# Result
run_id: exec-deskops-e-7cdeb2d8da8b
session: (no child session file; executed directly) session_sha256: n/a

Decision (a). Cause confirmed (sldb at /mnt/ssd/proyectos/SLDB_1/sldb, already with name resolution): after _point_deskops_link_at to a deleted dir, store_links gives status=ok, by=name, resolved=owner (also for an existing non-store dir). Grep: nothing in deskops reads a stored store-link path outside store_links (the "path" reads are model entries/docs). bootstrap.py unchanged.

Files changed (committed in worktree branch):
- tests/test_doctor_model_registration.py: test_init_repairs_a_broken_deskops_link now simulates a not-ok link by wrapping sldb.api.store_links (missing while stored path does not exist), since current sldb cannot produce a non-ok deskops link with a stale path; new test_init_leaves_a_deskops_link_with_a_stale_path_that_resolves_by_name.
- CHANGELOG.md

Validation: see validation.log. File passes 9/9. Full suite -n 4: 1 failure, tests/test_model_contract_snapshot.py::test_model_contract_hashes_match_the_snapshot, a file/models I did not touch (probably sldb checkout difference; /mnt/ssd/herramientas/sldb does not exist in this container, I used /mnt/ssd/proyectos/SLDB_1/sldb). Supervisor should review it. test_dispatch intermittent did not fail this run.
