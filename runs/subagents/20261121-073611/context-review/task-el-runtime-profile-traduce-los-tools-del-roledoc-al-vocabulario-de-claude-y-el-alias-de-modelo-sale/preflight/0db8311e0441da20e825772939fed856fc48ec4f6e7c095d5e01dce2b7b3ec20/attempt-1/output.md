REFORMULACION
Encargo ejecutable (task.code, no agregado/paquete): en `/mnt/ssd/proyectos/SLDB_1/deskops`, hacer que `RuntimeProfileDoc` con kind claude traduzca los tools del RoleDoc en `build_agent_spec_args`: read→Read, grep→Grep, find→Glob, ls→Glob, bash→Bash, edit→Edit, write→Write, en orden de primera aparición y sin duplicados; tool desconocido: `ValueError("tool '<nombre>' has no translation for harness claude")`. Otros kind no cambian. Si no hay alias explícito, derivar de `RoleDoc.model`: opus→large, sonnet→medium, haiku→small (subcadena, sin distinguir mayúsculas); sin coincidencia→`DEFAULT_MODEL_ALIAS` medium y comentario exacto en `scion-agent.yaml`; el explícito gana. Actualizar `test_build_agent_spec_args_repeat_joins_tools` y añadir casos. Límites: solo `runtime_profiles.py` (~78-80), `scion.py` (~51-55, ~421-427) y los dos tests indicados; no tocar RoleDocs, harness pi ni repo scion. Validación: pytest de esos tests, goldens y suite completa, comparando fallas en worktree limpio de `origin/main`.

AMBIGUEDADES
1. “Si no se pasa un alias explicito”: no define dónde/cómo se pasa ni su validación. Obliga a inventar firma y precedencia.
2. “el scion-agent.yaml generado lleva el comentario '# model alias medium: no mapping for RoleDoc.model <valor>'”: no fija posición ni qué imprimir si falta `model`. Obliga a inventar renderizado.
3. “contiene 'opus' -> large, 'sonnet' -> medium, 'haiku' -> small”: no fija precedencia si el valor contiene varias subcadenas. Obliga a inventar orden.
4. “tests/test_output_goldens.py” aparece en Validation pero no en files/Scope; si el comentario cambia el YAML, no se sabe si actualizar goldens. Obliga a inventar alcance.
5. “tool '<nombre>'”: no aclara si `<nombre>` es placeholder ni el formato exacto final. Obliga a inventar el mensaje.

DRY-RUN
Hipotético, sin ejecutar: leer `runtime_profiles.py`, `scion.py`, ambos tests y goldens relevantes; localizar `build_agent_spec_args`, la tabla de tools, el template y `DEFAULT_MODEL_ALIAS`. Cambios previstos: tabla de traducción aplicada solo a claude; `model_alias_for` y comentario; actualizar/añadir tests. Dependencias: `RuntimeProfileDoc`, renderer de scion y fixtures. Validaciones futuras: los pytest indicados y suite completa; fallas se comparan en worktree de `origin/main` y se reportan.

FUTURO
Un humano decide las ambigüedades 1-4 antes de implementar; el ejecutor produce diff, tests y reporte de fallas baseline; otro nodo o revisor valida goldens y aceptación.
