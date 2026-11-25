## REFORMULACION
El nodo es ejecutable (`task.code`), no un agregado. Debe unificar el vocabulario de tags semánticos de deskops: inventariar tags actuales, definir una tabla de mapeo vieja→nueva, declarar padres/equivalencias mediante `sldb semantic parent/equivalent`, impedir que `deskops add/edit` escriban duplicados o nombres de clase como tags, migrar por CLI los documentos del desk de deskops y regenerar `.sldb_cache/semantic_dag.yaml`. El resultado incluye informe, tests y conteo antes/después de tags planos sin padre. Límites: no editar `.sldb` a mano; si falta operación, avisar a sldb con `deskops message send --to sldb`; fuera de alcance otros desks y el lector de surface. Repo: deskops.

## AMBIGUEDADES
1. “cada tag libre que sobrevive tiene padre declarado […] o es equivalente declarado”: no define qué tags sobreviven ni el criterio para justificar excepciones; obligaría a inventar la taxonomía final.
2. “siguiendo los tags de modelo con puntos como canonicos”: no da el mapeo concreto para `workspace:desk`, `artifact:task`, `topic:*`, nombres de clase o sueltos como `ci/cd`; obligaría a inventar la tabla.
3. “comando o paso de migracion por CLI”: no decide entre usar `deskops edit`, un comando nuevo o un script; obligaría a inventar el diseño de migración.
4. “los documentos existentes del desk de deskops”: no fija ruta, selección ni tratamiento de documentos dudosos; obligaría a inventar el alcance físico.
5. “se migra lo que el CLI permita”: no define si una migración parcial cumple aceptación; obligaría a inventar el criterio de cierre.
6. “el informe” / `result-summary.md`: no fija ruta ni formato; obligaría a inventar su ubicación y esquema.
7. El bundle menciona rituales, pills y átomos, pero el input muestra `pills: []`, `atoms: []`, `files: []`; obligaría a inventar instrucciones rituales no presentes.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, sugerencia referenciada, store de deskops, `sldb semantic`, templates/validadores de tags de add/edit, tests y `semantic_dag.yaml`. Cambios previstos: inventario y conteo por tag; tabla de mapeo en `result-summary.md`; declaración de padres/equivalentes vía CLI; ajuste de templates/validadores; migración CLI del desk y regeneración de cache; tests. Dependencias: operaciones `sldb semantic parent/equivalent` y migración en bloque; CLI de deskops; instrucciones rituales del Board. Validaciones futuras: `TMPDIR=/tmp pytest -q` de tests tocados, `deskops doctor --root .` y conteo antes/después de tags sin padre.

## FUTURO
Un humano o nodo revisor deberá aprobar la tabla de mapeo y las excepciones justificadas. Si falta operación en sldb, otro nodo atenderá el mensaje. La migración de otros desks queda para ejecuciones posteriores. El lector de surface no se modifica aquí.
