## REFORMULACION

Encargo ejecutable `task.code` en el repo `deskops` (cwd `/mnt/ssd/proyectos/SLDB_1/deskops`): ampliar `CloseoutGates.reference_points_to_test` en `deskops/services/closeout_gates.py` para que el gate de tests del closeout acepte como evidencia archivos TypeScript existentes con sufijos `.test.ts`, `.test.tsx`, `.spec.ts` o `.spec.tsx`, situados en un directorio de tests o declarados en `files`, excluyendo `node_modules` y directorios ocultos. El mensaje de rechazo debe nombrar los sufijos aceptados. Límites: solo `closeout_gates.py` y sus tests; no ejecutar tests JS desde `deskops`. Resultado observable: los tests nuevos pasan y los del closeout siguen verdes.

No es un agregado ni paquete no ejecutable.

## AMBIGUEDADES

1. «en un directorio de tests»: no define qué directorios cuentan para TS (¿`tests/`, `__tests__/`, `src/`?). Obligaría a inventar la lista.
2. «Actualizar el mensaje de Unresolvable --test»: no cita el texto ni la función exacta. Obligaría a inventar redacción y ubicación.
3. «closeout verify de una tarea cuyo commit trae tests de vitest pasa el gate»: no indica fixture ni comando de comprobación. Obligaría a inventar una prueba de integración.
4. «un archivo surface/src/x.test.ts declarado en files cuenta como evidencia»: no aclara si basta `files` o también debe estar bajo directorio de tests. Obligaría a inventar la precedencia.

## DRY-RUN

Lecturas hipotéticas: `deskops/services/closeout_gates.py` (especialmente línea 166), `tests/test_closeout_test_paths.py`, `tests/test_closeout_gates.py` y el formato de `files` en TaskDocs. Cambios previstos: helper de sufijos TS, comprobación de existencia, exclusión de `node_modules`/ocultos, criterio directorio-de-tests-o-`files`, mensaje de rechazo y tests de aceptación/rechazo. Dependencias: resolución de rutas y estructura de `files`. Validaciones futuras: `TMPDIR=/tmp pytest -q tests/test_closeout_test_paths.py tests/test_closeout_gates.py`, casos TS aceptados y `node_modules` rechazado. Sin ejecutar nada.

## FUTURO

Un nodo de ejecución implementará y correrá los pytest; otro aportará el commit/fixture de vitest si hace falta. Un humano decidirá la lista exacta de directorios de tests TS y el texto final del mensaje.
