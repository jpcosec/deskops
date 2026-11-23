PASA

# Veredicto: PASA

Commit del ejecutor: `05ac75a9952b657734dd767351b0c0e7feef4d49`
(`RepositoryDoc owns_paths/owns_topics, deskops owner, message send --to unowned`)
Trailer verificado: `Task-Id: task-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-deskops-owner-responde-el-dueno-de-un`.

## Tests del commit (de a uno, TMPDIR=/tmp)

- `tests/test_message_ecosystem_registry.py`: 12 passed (incluye los 6 nuevos de owner/unowned)
  - test_owner_resolves_path_by_longest_glob
  - test_owner_resolves_topic
  - test_owner_without_owner_exits_1
  - test_owner_tie_exits_2
  - test_send_to_unowned_uses_unowned_target
  - test_send_to_unowned_without_config_fails
- `tests/test_config.py`: 7 passed (incluye test_unowned_target_comes_from_config_local_json)
- `tests/test_cli.py`: 103 passed
- `tests/test_cli_grammar.py`: 2 passed

Los 7 tests nuevos se corrieron además de forma explícita con `-k 'owner or unowned'` y `-k unowned`: 6 passed + 1 passed.

## Tests de los módulos tocados y goldens/contrato

- `tests/test_message_cli.py`: 18 passed
- `tests/test_command_registry.py`: 3 passed
- `tests/test_repo_identity.py`: 12 passed
- `tests/test_model_validators.py tests/test_model_templates.py`: 28 passed
- `tests/test_registry_robustness.py`: 8 passed
- `tests/test_model_contract_snapshot.py`: 2 passed
- `tests/test_output_goldens.py`: 7 passed

## Comprobaciones adicionales

- Las fichas existentes de `desk/registry/` (7 repos) cargan con el modelo nuevo y `owns_paths`/`owns_topics` vacíos por defecto.
- No hay cambios sin commitear en `deskops/` ni `tests/`.
- No se corrió la suite completa, según la indicación del rol.

## Nota de entorno

`../.venv/bin/python` no tiene pytest usable (entorno roto: interpreter 3.11 frente a pyvenv 3.12), por lo que los tests se ejecutaron con `/dev/shm/tester-venv/bin/python` (Python 3.12.16, pytest 9.2.0, deskops y sldb del checkout actual).
