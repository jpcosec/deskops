# result-summary — exec-deskops-e-44a082df5dbe (attempt 1)

run_id: exec-deskops-e-44a082df5dbe
session: Claude Code session 5e6f6805-1853-4cfa-ae11-a4865855ce6f (no pi child session; session_sha256: n/a)
task: task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li

## Changes (all inside files: of the TaskDoc)

- `deskops/cli/commands/message.py`: deleted `_run_legacy` along with the class docstring that described it. `run()` now calls `_run_message_command` directly. The parser already declares the `message` subcommand with `add_subparsers(required=True)` (deskops/cli/parser.py:46), so `deskops message` with no subcommand exits with rc 2 from argparse. The usage line in stderr lists `{send,list,read,ack}`; it prints the usage error, not the full help (coordinator precision 1). No change to the registry was needed.
- `tests/e2e_agent/scenarios/inbox-to-task.yaml`: the line `deskops inbox list --root . || deskops list inbox-notes --root .` becomes just `deskops message list --root .` (precision 3).
- `tests/test_repo_identity.py` (docstring, around line 97): `deskops inbox --ack` -> `deskops message ack` (precision 2).
- `tests/test_inbox_promote_cli_gaps.py` (header docstring, lines 1-4): the reference to the note no longer presents `inbox --root` as a command; it names `deskops message list --root` (precision 2).
- `tests/test_message_cli.py`: new test `test_message_without_subcommand_is_a_usage_error_naming_the_verbs`. It checks rc 2, that stderr names send/list/read/ack, and that the full help (`Examples:`) is not printed. `test_retired_inbox_alias_is_an_unknown_command` is unchanged (precision 4).

No file outside `files:` was touched. The pre-existing dirty files `.sldb/*` and `runs/subagents/*` belong to other sessions and I did not touch them.

## Validation (details in validation.log)

- tests/test_message_cli.py: 17 passed, rc 0
- tests/test_command_registry.py: 3 passed, rc 0
- tests/test_cli.py: 102 passed, rc 0
- `grep -rn _run_legacy deskops/`: no output (rc 1)
- `grep 'deskops inbox'` in the e2e scenario: no output (rc 1)
- `python -m deskops message`: rc 2, "the following arguments are required: message_command" plus a usage line with {send,list,read,ack}

Full suite: not run (per the integrator's order); it is for the integrator.

## Risks

- The e2e scenario is not run here (it is an agent scenario); the only change is its setup command, and `deskops message list --root .` exists and is covered by test_message_cli.
- Anyone who called `MessageCLI().run(args)` directly with `message_command=None` now gets a "Unknown message command: None" error instead of the legacy path. The CLI can no longer produce that state.
