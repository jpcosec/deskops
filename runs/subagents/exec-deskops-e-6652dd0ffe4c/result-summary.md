# Result
- deskops/dispatch.py: new _scion_pytest_tmp() reads DESKOPS_SCION_PYTEST_TMP (default SCION_PYTEST_TMP); used for cleanup and the "limpieza:" message.
- tests/test_dispatch.py: Env fixture sets DESKOPS_SCION_PYTEST_TMP=tmp_path/pytest-of-scion; in-process reap helper uses setenv instead of patching the constant.
- Validation: see validation.log (49 passed). Caveat: in the full run the real /dev/shm/pytest-of-scion vanished, but a targeted rerun of reap tests left it intact, so the cause is external (another reap).
- Code commit on branch deskops/deskops-e-6652dd0ffe4c, Task-Id trailer.
- advance BLOCKED: rule-activation-task-debug needs accepted preflight and reproduction receipts (none exist). Code is committed and validated; the coordinator must supply the receipts.
