REFORMULACION
Nodo ejecutable de código, no agregado. Propósito: corregir dos brechas del piloto scion fase 1: traducir los tools del RoleDoc al vocabulario de claude en `build_agent_spec_args` y derivar el alias de modelo del RoleDoc. Resultado: en `deskops/materializers/runtime_profiles.py`, tabla y traducción solo para `kind: claude`; en `deskops/runtime/scion.py`, `model_alias_for` y comentario de no mapeo; tests actualizados y nuevos. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no cambiar RoleDocs del desk, harness pi ni repo scion; cambios acotados a los cuatro archivos listados.

AMBIGUEDADES
1. “da --allowedTools Read,Grep,Glob,Bash” frente a `CLAUDE_PROFILE` con `"tools_join": "repeat"` y el test `repeat_joins_tools`, que espera pares repetidos. Obliga a inventar si el argv final es un valor comma-joined o pares `--allowedTools=Read`; afecta test y `_command_args`.
2. “Si no se pasa un alias explicito” frente a `scion_template_files(... model_alias: str = DEFAULT_MODEL_ALIAS)` y `materialize_scion_template` ídem: omitido y `"medium"` explícito son indistinguibles. Obliga a decidir si el default pasa a `None` y cómo conserva compatibilidad la CLI.
3. “contiene 'opus' -> large, 'sonnet' -> medium, 'haiku' -> small (subcadena, sin distinguir mayusculas)” no fija precedencia si el modelo contiene varias subcadenas. Obliga a inventar orden o error.
4. “sin coincidencia -> DEFAULT_MODEL_ALIAS (medium) y el scion-agent.yaml generado lleva el comentario '# model alias medium: no mapping for RoleDoc.model <valor>'” no dice si `model` vacío/ausente cuenta como sin coincidencia. Obliga a inventar si se emite comentario con valor vacío.
5. “en el orden de primera aparicion y sin duplicados” no aclara si deduplica nombres originales o traducidos; `find` y `ls` ambos van a `Glob`. El ejemplo sugiere traducidos, pero no se declara.

DRY-RUN
Lecturas: TaskDoc, átomos, `runtime_profiles.py`, `scion.py`, tests. Cambios previstos: `TOOL_NAMES_BY_HARNESS` y aplicación claude en `build_agent_spec_args`; `model_alias_for` y comentario; firmas/CLI para alias omitido; tests. Dependencias: modelos SLDB, perfiles existentes, `_command_args`. Validaciones futuras: los pytest listados, suite completa y baseline en worktree si hay fallas.

FUTURO
Otro nodo ejecutor implementa y entrega commit; tester independiente y closeout verifican; un humano decide las ambigüedades 1-2 si no se resuelven en el plan.
