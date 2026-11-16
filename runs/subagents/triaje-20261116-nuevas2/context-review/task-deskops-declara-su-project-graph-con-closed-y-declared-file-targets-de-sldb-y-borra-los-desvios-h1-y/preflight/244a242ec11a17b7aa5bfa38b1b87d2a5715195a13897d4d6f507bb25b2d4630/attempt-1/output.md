## REFORMULACION

Encargo ejecutable (tarea `task.code`, con dos átomos; no es paquete agregado). Propósito: que deskops deje de emular dos capacidades que sldb ya ofrece desde GD21. Resultado: `deskops/graph/desk_graph.py` configura `project_graph` usando el predicado `closed:` del lenguaje de reglas de sldb (equivalente a `_closed_issue`) y declara `declared_file_targets` para archivos existentes no-documento; desaparecen `_closed_issue` y `declared_target_is_a_file` de `deskops/graph/checks.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops` (no se modifica sldb). Límites: tocar solo `desk_graph.py`, `checks.py` y sus tests; no editar `.sldb/store.yaml` a mano; antes de cambiar guardar `deskops graph missing --root .` en `runs/subagents/project-graph-<AAAAMMDD>/graph-missing-antes.txt`; comparar por conjunto de líneas; destinos no declarables (p. ej. `dag.yaml`, `tests/fixtures/model_contract_hashes.json`) conservan tratamiento y se avisan a sldb.

## AMBIGUEDADES

1. "se manda deskops message send --to sldb con el caso": no se define cuerpo, formato ni criterio de cierre del mensaje; obligaría a inventar el contenido y cómo acreditar que se envió.
2. "misma lista de faltantes" (Goal) frente a "La comparacion de graph missing es por conjunto de lineas (orden indistinto)" (Scope): obligaría a decidir si el orden importa; la segunda precisión lo resuelve, pero el contraste queda.
3. "declara declared_file_targets para los archivos existentes que no son documento" y luego "al menos desk/materializations con field target_identity": no enumera todas las carpetas/campos; obligaría a inventar el inventario completo de `DeclaredFileTargets`.
4. "la misma condicion que hoy evalua _closed_issue": exige leer el código; no es ambigüedad de texto pero obliga a fijar la sintaxis `closed:` exacta desde docs/tests de sldb.

## DRY-RUN

Lecturas: `desk_graph.py:180-215`, `checks.py:55-90`; en sldb `document_surface.py`, `project_texts.py`, `project_graph_config_mapping.py`, `project_graph_config.py`, `declared_file_targets.py`, `declared_target_nodes.py`, docs y `tests/api/test_project_graph.py`. Cambios previstos: guardar salida `graph missing`; traducir `_closed_issue` a `closed:`; construir `declared_file_targets`; borrar código viejo; ajustar ambos tests. Dependencias: venv `../.venv`, acceso a repo sldb y `origin/main` para worktree. Validaciones futuras: los cinco comandos de Validation, incluida suite completa y comparación de fallas en worktree limpio.

## FUTURO

El envío/aceptación de la nota a sldb y la decisión sobre destinos no declarables corresponden a ese equipo; la aceptación final y el commit, al átomo `atom-code-changes-close-with-tests-and-commit` y al revisor humano.
