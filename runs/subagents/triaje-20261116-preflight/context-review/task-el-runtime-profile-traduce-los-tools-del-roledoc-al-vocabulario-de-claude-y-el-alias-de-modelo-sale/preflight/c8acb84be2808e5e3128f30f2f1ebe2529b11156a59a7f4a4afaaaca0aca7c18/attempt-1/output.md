## REFORMULACION

Encargo ejecutable (`task.code`, no agregado): en el repo `deskops`, al materializar un runtime profile o argv para el harness claude, traducir los tools del RoleDoc al vocabulario de Claude (`read→Read`, `grep→Grep`, `find/ls→Glob`, `bash→Bash`, `edit→Edit`, `write→Write`) y derivar el alias de modelo desde `RoleDoc.model` (`opus`, `sonnet`, `haiku`), con fallback a `DEFAULT_MODEL_ALIAS`. Resultado: cambios en `runtime_profiles.py`, `scion.py` y tests asociados. Límites: no cambiar RoleDocs del desk, harness pi ni repo scion. Cierre: pasan los casos indicados y pi sigue verde.

## AMBIGUEDADES

1. “un nombre sin traduccion da error claro”: no define tipo de excepción, texto exacto ni dónde falla (materialización o construcción de argv). Obliga a inventar contrato de error.
2. “el template lo dice en un comentario”: no identifica qué template ni dónde va el comentario; los archivos listados no incluyen template. Obliga a inventar archivo y formato.
3. “sin duplicados”: no fija orden ni criterio de deduplicación cuando `find` y `ls` colapsan a `Glob`. Obliga a inventar orden canónico de `--allowedTools`.

## DRY-RUN

Lecturas hipotéticas: `deskops/materializers/runtime_profiles.py` (zona 78-80), `deskops/runtime/scion.py` (`DEFAULT_MODEL_ALIAS` 53-55 y comentario 421-427), `tests/test_runtime_profiles.py`, `tests/test_scion_runtime.py` y la nota referenciada. Cambios previstos: tabla `TOOL_NAMES_BY_HARNESS`, aplicación solo para claude, error ante tool desconocido; función `model_alias_for(role_model)` con mapeo y fallback; tests de traducción, deduplicación, tool desconocido, modelo opus y fallback. Dependencias: estructuras actuales de RoleDoc, `DEFAULT_MODEL_ALIAS`, entorno pytest con `TMPDIR=/dev/shm`. Validaciones futuras: los cuatro comandos de `Validation`, incluida suite completa con `-n 4` y comparación contra main. Sin ejecutar nada.

## FUTURO

Otro nodo ejecutor producirá el diff y correrá las validaciones; el átomo de cierre hará commit tras tests verdes. Un humano o nodo de aceptación decidirá si el mensaje de error y el comentario del template son suficientes.
