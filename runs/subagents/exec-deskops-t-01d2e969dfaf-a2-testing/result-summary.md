# Test result: deskops queue (host queue)

Verdict: **FAIL**

The four TaskDoc Validation points and the literal Done When conditions pass, and
the feature works in a throwaway desk. But the new CLI surface leaves three
existing guard tests red, so the change is not acceptable as-is.

## Validation / Done When

| Check | Verdict |
|---|---|
| `TMPDIR=/dev/shm pytest -q tests/test_queue.py` | PASS (14 passed) |
| `TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py` | PASS (20 passed) |
| `queue --help` and each subcommand help exit 0 | PASS |
| `deskops graph missing --root .` adds no reference to this task | PASS (47 preexisting, none ours) |
| Manual has `Host queue` section | PASS |
| `git status --short` shows no task files outside the expected set | PASS (expected code/tests/goldens; unrelated checkout changes ignored) |
| New tests use real commands, not mocks | PASS (real subprocesses/`sh -c`) |

## Independent manual run

Created `/dev/shm/queue-manual-desk` with `deskops init`, configured real
`queue_jobs` entries (`[sh, -c, ...]`), and verified:

- add declared/undeclared (rc 2 with declared kinds) and missing task (rc 2);
- run success -> `done`, `exit_code: 0`, log with stdout and all five env vars;
- run failure -> rc 1, `failed`, `exit_code: 7`, log with stderr, inbox note
  `queue: <id>` naming the log;
- list text/json with the four states and exit codes;
- two simultaneous `queue run` -> one executes, the other prints
  `ocupado: otro queue run en curso`, command runs once;
- `queue run --all` stops with rc 1 on the first failure;
- timeout -> `failed` with `timeout: true`, no `exit_code`, rc 1;
- orphan `running` -> `failed` with `interrupted: true`, `exit_code: null`, and
  a note without code/log;
- `queue_min_available_gb=1e9` -> `en espera: ...`, rc 0, job stays pending.

The desk was deleted afterwards.

## Blocking regressions (task-caused, pre-existing tests)

These passed before this change and fail now; each was run isolated with a clean
`/dev/shm`:

1. `tests/test_cli.py::test_cli_help_uses_deskops_name` — expects the old exact
   top-level command list; `queue` is missing from that assertion.
2. `tests/test_cli_grammar.py::test_top_level_nouns_are_classified_exactly_once` —
   `TOP_LEVEL_GRAMMAR` does not classify `queue`.
3. `tests/test_command_registry.py::test_mutating_commands_are_declared_explicitly` —
   `MUTATING_COMMANDS` lacks `("queue",)`, `("queue", "add")`, `("queue", "run")`,
   while the registry marks them `mutates=True` (`queue list` correctly does not).

`test_help_goldens` and `test_registry_paths_match_help_goldens` pass.

## Environment note

The path `/mnt/ssd/proyectos/SLDB_1/.venv` does not exist in this container. Tests
were run with the uv Python 3.13 (`/home/scion/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13`)
and `PYTHONPATH=/workspace/deskops:/workspace/sldb/src:/workspace/sldb/.venv/lib/python3.13/site-packages`.
`test_concurrent_runs_execute_once` overwrites `PYTHONPATH` for its subprocess, so a
temporary `.pth` was used to make `sldb` importable there; it was removed after the run.
`/dev/shm` is 64 MB, so pytest temp dirs were cleaned between files.

No implementation or test changes were made; no commit was created.
