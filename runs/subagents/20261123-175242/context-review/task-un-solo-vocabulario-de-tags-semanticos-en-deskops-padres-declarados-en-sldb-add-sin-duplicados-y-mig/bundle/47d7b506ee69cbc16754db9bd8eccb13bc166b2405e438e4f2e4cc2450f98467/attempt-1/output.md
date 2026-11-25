## REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: unificar el vocabulario de tags semánticos de deskops sobre el store de sldb, eliminando duplicados y tags planos. Resultado: tags de deskops declarados como semanticas de sldb con padres/equivalents, `add/edit` sin duplicados y documentos existentes migrados por CLI; demostrable con dos consultas resueltas por sldb (apartado y semántica hija). Repo: deskops (workspace desk). Límites: no tocar el lector de surface ni otros desks; deskops no reimplementa operaciones de sldb (si faltan, nota a sldb); el intento previo en `.worktrees/deskops-e-5f0471f4b90c` solo se consulta.

## AMBIGUEDADES

1. "board.tareas o equivalente" / "la que el informe fije como equivalente": no fija el nombre canónico del padre; obliga a inventar la semántica del apartado.
2. "siguiendo los tags de modelo con puntos como canonicos" frente a "tags libres con dos puntos en el frontmatter": no aclara si el tag final conserva puntos o se normaliza a dos puntos; obliga a inventar la dirección del mapeo.
3. "por ejemplo tareas de UI": no define qué tag existente identifica UI ni su padre; obliga a inventar la semántica hija.
4. "deskops edit o comando nuevo": no elige mecanismo de migración; obliga a decidir el comando.
5. "si a sldb le falta una operacion [...] queda nota a sldb y lo no resuelto se lista" frente a un Done When que exige las consultas: no aclara si la tarea cierra sin resolverlas; obliga a inventar el criterio de cierre.
6. "deskops doctor no suma errores": no da línea base; obliga a fijar el conteo inicial.

## DRY-RUN

Lecturas: TaskDoc, las dos notas de inbox, worktree previo, `.sldb_cache/semantic_dag.yaml`, modelos/templates de `add/edit`, tests. Cambios previstos: informe de mapeo en `result-summary.md`; declaraciones `sldb semantic parent/equivalent`; templates y validadores de tags; migración por CLI; tests. Dependencias: operaciones de sldb (consulta por tag con descendientes, migración en bloque) y CLI deskops. Validaciones futuras: pytest de tests tocados, `deskops doctor --root .`, conteo de tags sin padre antes/después, `sldb semantic show` y las dos consultas de aceptación. Sin ejecutar.

## FUTURO

JP/humano aprueba la tabla de mapeo y el nombre canónico del apartado; el equipo de sldb implementa operaciones faltantes si se envía nota; otro nodo u operador ejecuta la migración sobre el desk real y regenera el cache; el lector de surface queda para su propio encargo; la aceptación final la decide quien valide consultas e informe.
