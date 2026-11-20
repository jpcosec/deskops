# Result
- deskops/dispatch.py: `scion templates sync` now receives `str(target.resolve())` (the template dir just written) instead of the role name.
- tests/test_dispatch.py: new test with a desk having .scion/settings.yaml asserting sync gets the absolute path; two existing assertions updated to the path.
- CHANGELOG.md: Fixed entry.
- scion_start_argv unchanged: `scion start --type <name>` resolves the template on the hub (already synced); `--type` has no documented path form. Not verifiable against the real IR desk here; integrator should relaunch the IR dispatch.
- Committed in worktree branch deskops/deskops-e-1ae7acd5a6d9 with Task-Id trailer.
- Validation: see validation.log.
