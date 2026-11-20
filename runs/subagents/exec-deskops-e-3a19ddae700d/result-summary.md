# Result
run_id: exec-deskops-e-3a19ddae700d
session: (not recorded: Claude Code interactive session)
session_sha256: n/a

Added `SLDBBootstrap.ensure_merge_driver` (deskops/bootstrap.py), called from `init_local_store` and from `desk update --apply` (deskops/cli/commands/desk.py). It skips on ImportError, does nothing outside a git work tree and warns on stderr if git fails.
tests/conftest.py: `lifecycle_desk` installs the driver after its git init, as `deskops init` in a git repo now does. That is what keeps the golden unchanged with the sldb that has the alert (9007f78a).

Files: deskops/bootstrap.py, deskops/cli/commands/desk.py, tests/test_desk_merge_driver.py, tests/conftest.py, docs/operator-manual.md, CHANGELOG.md
Validation: test_desk_merge_driver + test_desk_sync pass; test_lifecycle_seed_drift 8 passed with sldb 9007f78a. Golden untouched. Full suite left to integrate.
Review: I did not run the pre-alert sldb (fd3c024b); it hits the ImportError skip path.
