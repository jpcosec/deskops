## REFORMULACION
Encargo ejecutable (no agregado): en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, producir `docs/config-vs-code.md` con (1) líneas Python por directorio de primer nivel en la base `827f3db7` y en el HEAD medido —anotando su hash—, (2) inventario de configuración (modelos, RelationDoc, RuleDoc, ViewDoc, semillas, configuración de grafo) con ubicación, y (3) lista única de archivos de `deskops/` categorizados como configuración declarada, código justificado con razón o deuda con tarea/nota. Añadir entrada en `CHANGELOG.md` y test `tests/test_config_vs_code_doc.py`. Límites: solo esos archivos; no cambiar código para reducir líneas; si el total supera N, reportarlo y abrir deuda.

## AMBIGUEDADES
1. «Total del HEAD medido < N (N lo fija JP en la tarea de decision)»: falta el valor de N; obligaría a inventar el umbral.
2. «cada archivo de deskops/ aparece una vez en una lista» frente a «Lista por archivo con `git ls-files 'deskops/*.py'`»: no aclara si la lista cubre todos los archivos o solo `.py`; obligaría a inventar el alcance.
3. «su categoria: 'configuracion declarada en Python' [...] 'codigo justificado' [...] o 'deuda'»: no hay mapa completo; archivos no ejemplificados obligarían a inventar categoría o razón.
4. «configuracion de grafo»: no indica ubicación ni artefactos; obligaría a inventar qué incluir.
5. «CHANGELOG con la entrada»: sin formato ni versión; obligaría a inventar estilo.
6. «por directorio de primer nivel»: el comando citado no agrupa; obligaría a inventar el método de agrupación/presentación.

## DRY-RUN
Lecturas: TaskDoc, `desk/drawer/plans/deskops-como-config/dag.yaml`, `decisiones.md`, `CHANGELOG.md`, tests existentes y metadatos git. Cambios previstos: crear el doc y el test; editar `CHANGELOG.md`. Medición: worktree temporal en `827f3db7`, ejecutar `find ... | xargs wc -l`, retirarlo; medir HEAD y registrar hash; obtener archivos con `git ls-files`; categorizar. Dependencias: N de la tarea JP; hechos de CC33/CC34. Validaciones futuras: `pytest -q tests/test_config_vs_code_doc.py` y total `< N`.

## FUTURO
La tarea dependiente/JD aporta N; el ejecutor mide y redacta; el revisor humano resuelve o acepta las ambigüedades; el test valida cobertura; si supera N, otro nodo abre tareas de deuda.
