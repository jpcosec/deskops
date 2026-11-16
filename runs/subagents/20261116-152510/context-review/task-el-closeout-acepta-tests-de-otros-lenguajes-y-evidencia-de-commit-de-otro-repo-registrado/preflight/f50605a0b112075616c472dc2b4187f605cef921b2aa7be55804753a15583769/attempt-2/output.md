## REFORMULACION

**Propósito:** ampliar el closeout para que acepte tests de otros lenguajes y evidencia de commits de otros repos registrados, desbloqueando tres tareas de scion ya verificadas.

**Resultado:** (1) `reference_points_to_test` acepta una lista cerrada de sufijos (`*_test.go`, `*.test.sh`, `*.bats`, `*.test.ts`, `*.test.tsx`) además de `test_*.py`; (2) un log bajo `runs/` con primera línea `$ ...` y última línea no vacía `rc=0` vale como evidencia; (3) `RepositoryReferences` resuelve `<repo-id>:<sha>` también contra el registro del ecosistema vía `find_registered_desk`; (4) `closeout resolved-by` acepta esos sufijos en `--test` y `<repo-id>:<sha>` en `--ref`.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** no cerrar las tres tareas de scion; no cambiar qué evidencia exige cada tipo; `tests/test_closeout_test_paths.py` solo se ejecuta salvo rotura legítima justificada; sufijos cerrados; `runs/` relativo a la raíz de `--root`.

## AMBIGUEDADES

1. “el archivo debe estar en files o references de la tarea” frente a “files sigue sirviendo solo para ampliar ubicaciones, como hoy”: no queda claro si basta citar el test solo en `files`. Obligaría a inventar la precedencia entre ambas frases.
2. “debe buscar tambien en el registro del ecosistema”: no se indica ruta, variable ni formato de ese registro. Obligaría a inventar dónde vive y cómo se localiza.
3. “con la misma resolucion que usa deskops message send --to (find_registered_desk…)”: no aclara si hay que reutilizar la función o replicar su semántica ante IDs ambiguos/ausentes. Obligaría a inventar el criterio de errores.
4. “*.test.ts” dentro de una lista que también contiene “*.test.tsx”: no fija si el emparejamiento es por sufijo literal (donde `.ts` no captura `.tsx`) ni sensibilidad a mayúsculas. Obligaría a inventar el orden y la normalización.

## DRY-RUN

**Lecturas:** `deskops/services/closeout_gates.py` (140–300), `deskops/services/closure.py` (rama resolved-by), `deskops/identity.py` (`find_registered_desk`), `docs/workflow-policy-reference.md`, tests existentes.

**Cambios previstos:** tabla de sufijos; validador de log en `runs/`; consulta al registro del ecosistema en `RepositoryReferences`; extensión de `--test`/`--ref`; tests nuevos.

**Dependencias:** helpers y fixtures actuales, registro del ecosistema, worktree limpio de `origin/main`.

**Validaciones futuras:** los tres pytest indicados y suite completa con `-n 4`, comparando fallas contra worktree limpio.

## FUTURO

El coordinador de scion cierra sus tres tareas tras recibir la nota con el hash; marcado-ui recibe su nota; un humano o nodo revisor evalúa el informe y las fallas preexistentes; el commit de cierre produce el hash referenciado.
