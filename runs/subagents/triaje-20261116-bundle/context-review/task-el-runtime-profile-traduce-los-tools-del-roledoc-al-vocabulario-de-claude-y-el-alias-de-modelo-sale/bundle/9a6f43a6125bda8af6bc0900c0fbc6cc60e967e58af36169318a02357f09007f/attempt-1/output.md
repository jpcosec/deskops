## REFORMULACION

Propósito: al materializar el template Scion para harness claude, traducir los `tools` del RoleDoc (vocabulario pi) y derivar el alias de modelo de `RoleDoc.model`. Resultado: tabla de traducción aplicada en `deskops/materializers/runtime_profiles.py`, `model_alias_for(...)` en `deskops/runtime/scion.py` con su comentario en `scion-agent.yaml`, y tests en `tests/test_runtime_profiles.py` y `tests/test_scion_runtime.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no tocar RoleDocs del desk, ni el comportamiento del harness pi, ni el repo scion. Es tarea ejecutable (`task.code`), no agregado.

## AMBIGUEDADES

1. "anthropic/claude-opus-* -> opus" choca con el código: `scion_template_files` rechaza alias fuera de `MODEL_SIZE_ALIASES` ("small","medium","large","extra-large"). Obligaría a inventar si opus/sonnet/haiku sustituyen esa lista, se añaden, o solo aparecen en el comentario.
2. "para el harness pi no cambia nada" frente al test existente `test_build_agent_spec_args_repeat_joins_tools`, que con `CLAUDE_PROFILE` espera `["read","grep","find","ls","bash"]`. Obligaría a decidir si ese test se actualiza o si `build_agent_spec_args` no traduce.
3. "levanta ValueError(\"tool '<nombre>' has no translation for harness claude\") al materializar el profile", pero `build_agent_spec_args` recibe `profile`, no harness. Obligaría a inventar el criterio de detección (`profile["kind"]` u otro).
4. Validation exige `tests/test_output_goldens.py` mientras Scope solo nombra dos tests. Obligaría a decidir si los goldens se regeneran y entran en el commit.
5. No se declara precedencia entre un `--model-alias` explícito y `RoleDoc.model`.

## DRY-RUN

Lecturas: los cuatro archivos listados, `desk/runtimes/runtime-claude.md` y RoleDocs vía `load_runtime_profiles`/`find_role_doc`. Cambios previstos: `TOOL_NAMES_BY_HARNESS` y su aplicación solo cuando el profile es claude (orden de primera aparición, dedupe find/ls→Glob); `model_alias_for` y su uso en `scion_template_files`; comentario de fallback; tests nuevos y ajuste del test repeat. Dependencias: `profile["kind"]`, `MODEL_SIZE_ALIASES`, `_command_args`. Validaciones futuras: los cuatro pytest indicados; fallas comparadas en worktree limpio de `origin/main`. Nada ejecutado.

## FUTURO

Decisión humana/arquitecto: resolver alias opus/sonnet/haiku frente a `MODEL_SIZE_ALIASES` y el alcance de goldens. El coordinador hace dispatch y `closeout commit` (sin `git add -A`); un tester independiente valida el contrato.
