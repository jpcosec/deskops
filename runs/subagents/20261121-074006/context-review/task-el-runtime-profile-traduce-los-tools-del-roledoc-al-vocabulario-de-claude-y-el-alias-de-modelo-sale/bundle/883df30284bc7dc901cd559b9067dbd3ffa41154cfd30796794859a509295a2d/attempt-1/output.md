## REFORMULACION
Propósito: cerrar dos brechas del piloto scion fase 1: los tools del RoleDoc, en vocabulario pi, pasan sin traducir a `--allowedTools` de claude; y el template fija `medium` aunque el RoleDoc pida opus.

Resultado: en `build_agent_spec_args` (`runtime_profiles.py`), cuando el perfil es kind claude, traducir read→Read, grep→Grep, find→Glob, ls→Glob, bash→Bash, edit→Edit, write→Write, en orden de primera aparición y sin duplicados; un tool desconocido lanza `ValueError("tool '<nombre>' has no translation for harness claude")`; otros kinds no cambian. En `scion.py`, derivar el alias de `RoleDoc.model` (opus→large, sonnet→medium, haiku→small; subcadena sin mayúsculas), con `DEFAULT_MODEL_ALIAS` (medium) y comentario si no hay mapeo; un alias explícito gana. Actualizar/añadir tests en `test_runtime_profiles.py` y `test_scion_runtime.py`.

Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no tocar RoleDocs del desk, harness pi ni repo scion; superficie: los cuatro archivos listados.

## AMBIGUEDADES
1. **Join de tools.** «da --allowedTools Read,Grep,Glob,Bash» y «se actualiza para esperar [Read, Grep, Glob, Bash]» frente a `CLAUDE_PROFILE` con `"tools_join": "repeat"` y `test_build_agent_spec_args_repeat_joins_tools`. Obliga a inventar si el join sigue siendo repeat (flags repetidos) o pasa a comma, y la forma exacta del test.
2. **Alias explícito vs. default.** «Si no se pasa un alias explicito» y «Un alias explicito siempre gana» frente a `model_alias: str = DEFAULT_MODEL_ALIAS` en `scion.py`. Obliga a inventar cómo distinguir el default de un explícito (p. ej. `None`) y si la firma cambia.
3. **Texto del comentario.** «'# model alias medium: no mapping for RoleDoc.model <valor>'». Obliga a inventar formato exacto, comillas del valor y ubicación en el YAML.
4. **Goldens.** La validación incluye `tests/test_output_goldens.py`, pero el Scope solo nombra cuatro archivos. Obliga a decidir si se actualizan goldens o solo se verifican.

## DRY-RUN
Lecturas: los cuatro archivos del Scope y los tests nombrados. Cambios previstos: tabla `TOOL_NAMES_BY_HARNESS` y su aplicación; `model_alias_for`; derivación por defecto y comentario; actualización de `test_build_agent_spec_args_repeat_joins_tools`; tests nuevos de tools claude, tool desconocido, opus y modelo sin mapeo. Dependencias: `RuntimeProfileDoc.kind`, `MODEL_SIZE_ALIASES`, `DEFAULT_MODEL_ALIAS`, `build_agent_spec_args`, pytest, `.venv` y `TMPDIR=/dev/shm`. Validaciones futuras: los tres pytest de módulos, suite completa con `-n 4`, y comparación de fallas en worktree limpio de `origin/main`. Sin ejecutar nada.

## FUTURO
Otro nodo ejecutor implementa y corre las validaciones; un humano decide las ambigüedades 1–3 (join, centinela, comentario) y 4 (goldens). Luego un nodo de closeout verifica y registra el commit descriptivo; merge/push queda fuera.
