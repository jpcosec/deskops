# result-summary
run_id: exec-deskops-e-85084b2b474c  (session path/sha256: not available to this executor)

Changes (committed on branch deskops/deskops-e-85084b2b474c):
- deskops/runtime/scion.py: env keys (image/resources/volumes/kubernetes/telemetry, those present) go to scion-env.yaml, not scion-agent.yaml; overwritten each run, removed if empty; scion_start_argv(env_config=) adds --config; coordinator agents.md uses --config and executor_role/tester_role (--type = id without 'role-'); ids without 'role-' raise ValueError.
- deskops/cli/commands/runtime.py, deskops/cli/registry.py: --executor-role / --tester-role (defaults role-deskops-executor / role-deskops-tester).
- tests/test_scion_runtime.py: 3 tests adapted, 5 new. tests/fixtures/golden/help/deskops_runtime_template.txt updated.
Note: deskops/dispatch.py untouched (out of scope); it still passes --config via role_cfg.env_config.
Validation: see validation.log. Only failure: test_command_registry::test_mutating_commands_are_declared_explicitly, pre-existing at branch base (repo whoami).
Review: --update-golden rewrote unrelated goldens (terminal width); I reverted them.
