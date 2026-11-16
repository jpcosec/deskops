## REFORMULACION
**Propósito:** corregir dos brechas del piloto scion fase 1 al materializar el harness claude. **Resultado:** (1) los tools del RoleDoc (vocabulario pi) se traducen al vocabulario claude antes de pasar a `--allowedTools`: read→Read, grep→Grep, find→Glob, ls→Glob, bash→Bash, edit→Edit, write→Write; sin traducción, `ValueError("tool '<nombre>' has no translation for harness claude")`. Orden = primera aparición en `RoleDoc.tools`, sin duplicados. (2) el alias de modelo sale de `RoleDoc.model` (anthropic/claude-opus-*→opus, *sonnet*→sonnet, *haiku*→haiku); sin mapeo, `DEFAULT_MODEL_ALIAS` con comentario en el `scion-agent.yaml` generado. pi no cambia. **Repo:** deskops. **Límites:** entran `deskops/materializers/runtime_profiles.py` (~78-80), `deskops/runtime/scion.py` (~53-55, ~421-427), `tests/test_runtime_profiles.py`, `tests/test_scion_runtime.py`; excluye RoleDocs del desk, harness pi y repo scion.

## AMBIGUEDADES
1. "tests/test_output_goldens.py" aparece en Validation pero no en Scope: obliga a inventar si se permite tocarlo/actualizarlo si un golden refleja el comentario de modelo.
2. "un modelo sin mapeo da el alias por defecto y el comentario": no dice el texto exacto del comentario ni qué valor concreto imprime; obligaría a inventar formato.
3. "preflight 1" se cita como fuente de precisiones pero no se adjunta; obliga a asumir que el input las transcribe completas.
4. "anthropic/claude-opus-*" no define si el match es prefijo, subcadena o regex case-insensitive; obliga a elegir.
5. "cada test que falle se corre... worktree limpio": no aclara si `origin/main` debe actualizarse (fetch) antes; obliga a suponer.

## DRY-RUN (hipotético, sin ejecutar)
Lecturas: los cuatro ficheros listados y `tests/test_output_goldens.py` (solo lectura). Cambios: tabla `TOOL_NAMES_BY_HARNESS` + aplicación en claude en runtime_profiles; `model_alias_for(role_model)` y comentario en scion.py; tests nuevos en ambos ficheros. Dependencias: pytest, `.venv`, TMPDIR=/dev/shm, git worktree. Validaciones futuras: los cuatro comandos de Validation, worktree base para fallas nuevas, informe con lista de fallas preexistentes.

## FUTURO
Un ejecutor implementa y corre la suite; un humano decide si actualiza goldens y aprueba el commit; el nodo de cierre consume el informe de fallas preexistentes.
