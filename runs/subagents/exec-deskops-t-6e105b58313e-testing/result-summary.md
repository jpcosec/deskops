FALLA

# Resultado del tester

Tarea: `task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis`
Run: `run-deskops-t-6e105b58313e`
Commit evaluado: `b57253694217931af6a97cd572f3658804dd880c` — "deskops init --id, repo whoami --set y aviso en repo register".
Trailer verificado: `Task-Id: task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis`.
Archivos del commit:

- `deskops/cli/commands/core.py`
- `deskops/cli/commands/repo.py`
- `deskops/cli/registry.py`
- `deskops/workspace.py`
- `tests/fixtures/golden/help/deskops_init.txt`
- `tests/fixtures/golden/help/deskops_repo_whoami.txt`
- `tests/test_repo_identity.py`

## Veredicto

El comportamiento pedido en el Goal funciona y los tests nuevos pasan, pero el commit deja una
regresión en un test del módulo tocado: al marcar `repo whoami` con `mutates=True` en
`deskops/cli/registry.py`, no se actualizó `MUTATING_COMMANDS` en `tests/test_command_registry.py`.
`test_mutating_commands_are_declared_explicitly` falla porque el conjunto declarado contiene
`('repo', 'whoami')` de más. Por eso el veredicto es FALLA.

## Tests ejecutados (de a uno, `TMPDIR=/tmp`, sin suite completa)

El `.venv` versionado en `/mnt/ssd/proyectos/SLDB_1/.venv` está roto en este contenedor: sus
binarios apuntan a `/home/robocop/...` y a un Python 3.12 ausente, y `python` del sistema no tiene
pytest. Usé el venv temporal `/dev/shm/t311` (Python 3.11.2, pytest 9.2.0, pydantic 2.14.3) que
importa el `deskops` del árbol y el `sldb` local (`/mnt/ssd/proyectos/SLDB_1/sldb/src`).

```text
TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_repo_identity.py
  -> 12 passed (57.78 s)
TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_scaffold_golden.py
  -> 3 passed (63.63 s)
TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
  -> 7 passed (494.08 s)
TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_cli.py
  -> 103 passed (800.58 s)
TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_registry_robustness.py
  -> 8 passed (59.56 s)
TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider \
    tests/test_command_registry.py tests/test_cli_grammar.py tests/test_cli_contract.py tests/test_cli_help_examples.py
  -> 25 passed, 1 FAILED (102.95 s)
TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider \
    tests/test_skill_cli_drift.py tests/test_cli_escape_hatches.py tests/test_view.py
  -> 29 passed (243.85 s)
```

No existe `tests/test_workspace.py`; para `cli/registry.py` el test de módulo es
`tests/test_command_registry.py`, que es justamente el que falla.

## Fallo concreto

```text
tests/test_command_registry.py::test_mutating_commands_are_declared_explicitly
E   AssertionError: assert {('add',), ('...zation'), ...} == {('add',), ('...zation'), ...}
E     Extra items in the left set:
E     ('repo', 'whoami')
1 failed, 1 warning
```

Causa: `deskops/cli/registry.py` cambia `repo whoami` de `mutates=False` a `mutates=True` (por
`--set`), pero `tests/test_command_registry.py` no agrega `("repo", "whoami")` a
`MUTATING_COMMANDS`. El repo ya tiene precedente para este ajuste: el commit `b5516606` hizo lo
mismo al declarar `deskops atoms citations`.

## Lo que sí cumple el Goal

- `deskops init <path> --id workflow`: escribe `project_identity: workflow`; sin `--id` conserva la
  identidad derivada del nombre de la carpeta (lo cubre también el scaffold golden).
- `deskops init <path> --id other` sobre un desk ya existente con otra identidad no la pisa e
  imprime el aviso con `deskops repo whoami --set other --root <path>`.
- `deskops repo whoami --set new-id --root <desk>` valida slug, reescribe solo el valor de
  `project_identity` e imprime `project_identity: old -> new-id`; un slug inválido devuelve 1 y deja
  el archivo intacto.
- `deskops repo register workflow <ruta> --id workflow` avisa por stderr cuando el desk de `<ruta>`
  tiene otra `project_identity`, con el texto y el comando `repo whoami --set` pedidos.
- Los goldens de ayuda de `init` y `repo whoami` están actualizados y `test_output_goldens.py` pasa.

## Observaciones menores (no bloquean por sí solas)

- `set_project_identity` re-serializa el JSON completo con `json.dumps(indent=2)`, igual que el
  precedente `set_job_field` de `deskops/queue.py`. El test nuevo solo prueba un
  `desk/config.json` con formato canónico; un archivo editado a mano con otro formato se
  reformatearía aunque los valores se conserven.
- `repo whoami --set X` sobre un config sin `project_identity` imprime `project_identity: None -> X`;
  el Goal no define ese caso.

## Acción sugerida para el ejecutor

Agregar `("repo", "whoami")` a `MUTATING_COMMANDS` en `tests/test_command_registry.py` (o, si se
prefiere no declararlo mutante, justificar y ajustar la convención; pero `--set` escribe
`desk/config.json`), y repetir `tests/test_command_registry.py` junto con los tests de
`test_repo_identity.py`. No modifiqué el repositorio durante la verificación; solo escribí este
result-summary.
