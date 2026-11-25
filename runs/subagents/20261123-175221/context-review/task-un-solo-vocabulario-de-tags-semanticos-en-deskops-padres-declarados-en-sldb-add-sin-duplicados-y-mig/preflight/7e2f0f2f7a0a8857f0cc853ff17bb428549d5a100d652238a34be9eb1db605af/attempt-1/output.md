## REFORMULACION

**Propósito:** unificar el vocabulario de tags de deskops en el store semántico de sldb, eliminando duplicados y tags planos con dos puntos, para que el lector de surface resuelva apartados y filtros mediante semánticas de sldb.

**Resultado:** tags de deskops declarados como semánticas de sldb con padres/equivalentes, `add`/`edit` sin duplicados, documentos existentes migrados por CLI, tests y evidencia de consultas (apartado y subfiltro) sobre el desk real.

**Repo:** deskops, con dependencia de la CLI de sldb; el desk real de deskops como caso de validación.

**Límites:** no editar `.sldb` a mano ni reimplementar operaciones de sldb; si falta una operación, nota a sldb. Fuera: lector de surface y otros desks. El intento previo en worktree solo se consulta.

## AMBIGUEDADES

1. «board.tareas o la que el informe fije como equivalente»: no fija el nombre ni el criterio de equivalencia; obligaría a inventar el árbol semántico final.
2. «tareas de UI»: no define qué tag o condición identifica una tarea de UI; obligaría a inventar el criterio de filtrado.
3. «sldb semantic parent/equivalent»: no consta la sintaxis ni la operación CLI exacta; obligaría a inventar comandos.
4. «migración ... por CLI (deskops edit o comando nuevo)»: no elige mecanismo; obligaría a inventar la vía de migración.
5. «se puede consultar pero no se da por bueno»: no concreta qué reutilizar del worktree; obligaría a inventar el grado de aprovechamiento.
6. «Fuera: el lector de surface» frente a «desde el lector de surface»: contradicción sobre el alcance de validación; obligaría a inventar si se modifica o solo se usa.
7. «tags sin padre»: no define "sin padre"; obligaría a inventar la métrica de conteo.

## DRY-RUN

**Lecturas:** TaskDoc, notas de inbox referenciadas, inventario de tags con `sldb semantic`, store de deskops, templates/validadores de `add`/`edit`, worktree previo solo como consulta.

**Cambios previstos:** tabla de mapeo en `result-summary.md`; declaración de padres/equivalentes; ajuste de templates y validadores; tests; migración por CLI; regeneración de `.sldb_cache/semantic_dag.yaml`.

**Dependencias:** operaciones de sldb (consulta por tag con descendientes, migración en bloque) y `deskops message send --to sldb` si faltan.

**Validaciones futuras:** `pytest` de tests tocados, `deskops doctor --root .`, conteos antes/después de tags sin padre, consultas de apartado y subfiltro con salidas, `sldb semantic show`.

## FUTURO

Otro nodo ejecuta inventario, mapeo, migración y mediciones. Un humano aprueba la tabla de mapeo y decide si las carencias de sldb se elevan como nota.
