# Result
run_id: run-deskops-e-e5f89cdffe35
session: scion://agent/deskops-e-e5f89cdffe35
session_sha256: n/a

Changed (committed on branch deskops/deskops-e-e5f89cdffe35): deskops/dispatch.py, tests/test_dispatch.py, CHANGELOG.md.
- start commits with pathspec only the RunDoc store files (store.yaml, store_index.yaml, models/RunDoc.yaml, shard), message `run: <agent>` + `[skip ci]`.
- reap does the same before the cherry-pick/ff; if a local change still blocks the pick, the error names the conflicting files and suggests committing them.
- Tests: new `commits_the_rundoc...` and `names_the_files...`.
Review: full test file passed once (34) before the hint fix; after it only the 2 new tests were re-run (full run takes ~8 min).
Note: store_index.yaml is committed whole, so other uncommitted edits in that file ride along.
