# Result
run_id: exec-deskops-e-d9b25ac30dc8
session: (child session path not available to the executor)
session_sha256: n/a

Added optional `retry_exit_codes` (list[int], default []) to QueueJob. `queue run`: a job whose exit code is in it returns to pending (no unclear note), prints "en espera: <id> ocupado" and stops with exit 0; other non-zero codes still fail.
Files: deskops/config.py, deskops/queue.py, tests/test_queue.py, docs/operator-manual.md, CHANGELOG.md
Validation: tests/test_queue.py 16 passed (2 new).
For supervisor: the integrator must add retry_exit_codes [3] to dispatch-executor/dispatch-tester in the config.json of deskops, sldb and IR (not done here, per the task).
