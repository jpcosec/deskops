# Result: deskops queue (add/run/list)

Changed: deskops/config.py (QueueJob, queue_jobs, queue_min_available_gb, queue_max_psi_avg60), deskops/queue.py (new; QueueCLI + logic, handler `deskops.queue:QueueCLI`), deskops/cli/registry.py (group `queue`), docs/operator-manual.md (section `Host queue`), tests/test_queue.py (new, 14 tests, cases a-j + help), goldens: tests/fixtures/golden/help/deskops.txt and new deskops_queue{,_add,_list,_run}.txt.

Decisions for review:
- Inbox note uses `MessageCLI()._deliver_note` (message.py untouched), with a temporary chdir to the root so the sender resolves, stdout suppressed; a note failure only warns on stderr.
- Handler lives in deskops/queue.py (no extra cli/commands file) to stay inside Scope.
- Job whose kind is no longer declared fails with exit_code 127. Timeout kills the process group; job gets `timeout: true` and no exit_code.
- Nothing left without reference; nothing deleted.
- Validation: see validation.log. No git add/commit done.
