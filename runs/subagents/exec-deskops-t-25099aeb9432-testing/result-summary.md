PASA

# Verificación

Tarea: `task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale`

Commit del ejecutor: `89777a0e0618be2cbfc5596d5ce2ad215d5389bf` — "runtime profile traduce tools del RoleDoc y alias de modelo"
(`git log -1 --grep "Task-Id: ..."` devuelve exactamente ese commit).

Archivos del commit:
- `deskops/materializers/runtime_profiles.py`
- `deskops/runtime/scion.py`
- `deskops/cli/commands/runtime.py`
- `deskops/cli/registry.py`
- `tests/test_runtime_profiles.py`
- `tests/test_scion_runtime.py`

# Resultado contra el Goal

1. Traducción de tools para harness `claude`:
   - `TOOL_NAMES_BY_HARNESS` cubre `read->Read`, `grep->Grep`, `find->Glob`, `ls->Glob`, `bash->Bash`, `edit->Edit`, `write->Write`.
   - `build_agent_spec_args` traduce solo cuando el profile es `claude`; preserva orden de primera aparición y elimina duplicados (`find`+`ls` -> un solo `Glob`).
   - Un tool desconocido levanta `ValueError("tool '<nombre>' has no translation for harness claude")`.
   - Para `pi` (u otro kind sin tabla) devuelve los tools sin cambios.
   - Verificación manual adicional con `[write, read, ls, bash, find, grep, edit, ls]` -> `[Write, Read, Glob, Bash, Grep, Edit]`.

2. Alias de modelo derivado del RoleDoc:
   - `model_alias_for` mapea subcadena sin mayúsculas: `opus -> large`, `sonnet -> medium`, `haiku -> small`; sin coincidencia -> `None`.
   - `scion_template_files` usa el derivado cuando no se pasa alias explícito; sin coincidencia cae a `DEFAULT_MODEL_ALIAS` (`medium`) y escribe en `scion-agent.yaml`:
     `# model alias medium: no mapping for RoleDoc.model <valor>`.
   - Un alias explícito gana sobre el derivado (`model_alias="small"` con modelo opus produce `small`).
   - El default del CLI y de `materialize_scion_template` pasó a `None` para habilitar la derivación.

# Tests

Los comandos de validación se corrieron con un venv funcional equivalente (`/dev/shm/t311`) porque
`../.venv/bin/python` de este contenedor no tiene pytest (symlink roto a python3.12 inexistente);
el venv usado tiene instalado el repo en modo editable y pytest 9.2.0.

- `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_runtime_profiles.py` -> **12 passed**
- `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_scion_runtime.py` -> **46 passed**
- `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_output_goldens.py` -> **7 passed** (479 s)
- Smoke adicional de módulos tocados: `tests/test_role_runtime_artifacts.py` -> 3 passed;
  `tests/test_cli_help_examples.py tests/test_cli_contract.py` -> 21 passed.

Los tests nuevos cubren: tools de claude sin duplicados, tool desconocido con mensaje exacto,
derivación de alias por modelo (mayúsculas incluidas), fallback con comentario y prioridad del
alias explícito. No se observaron regresiones en los archivos de validación.

# Veredicto

**PASA**: se cumplen los casos del Goal y el Done When; los tests de `pi` siguen verdes sin cambios.
