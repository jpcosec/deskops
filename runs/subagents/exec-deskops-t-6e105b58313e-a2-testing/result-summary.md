PASA

# Testing — task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis

## Commit revisado

- `b57253694217931af6a97cd572f3658804dd880c` — `deskops init --id, repo whoami --set y aviso en repo register` (`Task-Id` correcto)
- `9162620670c432e13f5dc02e5dee9f27e9d3a889` — `test_command_registry: declarar repo whoami como mutante` (mismo `Task-Id`)

Archivos del cambio: `deskops/cli/commands/core.py`, `deskops/cli/commands/repo.py`, `deskops/cli/registry.py`, `deskops/workspace.py`, `tests/fixtures/golden/help/deskops_init.txt`, `tests/fixtures/golden/help/deskops_repo_whoami.txt`, `tests/test_repo_identity.py`, `tests/test_command_registry.py`.

## Verificación funcional

Cumple los tres puntos del Goal:

1. `deskops init <path> --id <identidad>` escribe `project_identity`; sin `--id` mantiene el comportamiento previo. En un desk existente con otra identidad no la pisa y remite a `deskops repo whoami --set ...`.
2. `deskops repo whoami --set <identidad> --root <desk>` valida slug, reescribe solo `project_identity` conservando el resto del JSON byte a byte en el formato del config sembrado, e imprime `project_identity: <vieja> -> <nueva>`. Slug inválido retorna 1 y deja el archivo intacto.
3. `deskops repo register ... --id X` avisa por stderr cuando la identidad del desk difiere de X, con el texto y comando de alineación pedidos.

También comprobé manualmente: init con id válido, repetición con el mismo id, intento con id distinto (sin sobrescritura), id inválido, `whoami --set` válido e inválido.

## Comandos de test y resultados

Entorno: el `.venv` del proyecto apunta a rutas inexistentes y su Python 3.12 ya no está disponible en el host. Usé el Python 3.13 de `SLDB_1/sldb/.venv` con el checkout de `deskops` en el working tree, que importa correctamente `deskops` y `sldb`.

- `tests/test_repo_identity.py` → **12 passed**
- `tests/test_command_registry.py` → **3 passed**
- `tests/test_scaffold_golden.py` → **3 passed**
- `tests/test_output_goldens.py` → **7 passed** (incluye goldens de ayuda de `init` y `repo whoami`)
- `tests/test_cli.py` → **103 passed**
- `tests/test_cli_grammar.py tests/test_cli_contract.py tests/test_registry_robustness.py` → **18 passed**
- `tests/test_config.py` → **6 passed**
- `tests/test_desk_paths.py` → **16 passed**

Todos con `TMPDIR=/tmp`, `-q -p no:cacheprovider`. No corrí la suite completa, según la instrucción del encargo.

## Observaciones

- `set_project_identity` reserializa el JSON con `indent=2`, igual que `set_job_field` de `deskops/queue.py`; conserva orden de claves y contenido, y el test nuevo verifica que el resto del archivo quede idéntico para el formato del config real.
- La validación de slug en `init` ocurre después de crear el store local; no afecta el resultado funcional ni los tests, y el exit code es 1 sin tocar la identidad.
- Sin fallos detectados en el alcance de la tarea.
