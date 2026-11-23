# Result
- deskops/integrate.py: _run_suite adds --basetemp=<work>/pytest to PYTEST_ADDOPTS (keeps prior value); new _clean_stale_integrate_dirs run under the suite lock (dead owner.pid, or no owner.pid and mtime older than suite_timeout; never own dir/live pid; prints "limpieza: <ruta>"); _steps writes work/owner.pid.
- tests/test_integrate.py: test_suite_gets_basetemp_inside_work, test_stale_integrate_dirs_are_removed_under_the_lock.
- Validation: see validation.log. Full suite fails at setup with FileNotFoundError store_index.yaml in this sandbox; reproduced on main for test_view.py; supervisor should compare in a proper env.
- Committed in worktree branch deskops/deskops-e-63752d14bbc2 with Task-Id trailer.
