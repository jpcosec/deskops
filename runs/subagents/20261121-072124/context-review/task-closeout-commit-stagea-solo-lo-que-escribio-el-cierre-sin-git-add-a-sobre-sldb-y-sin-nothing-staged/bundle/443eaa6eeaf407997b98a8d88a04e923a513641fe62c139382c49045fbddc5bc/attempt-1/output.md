## REFORMULACION

Propósito: corregir `deskops closeout commit` para que stagee solo las rutas escritas por el cierre más `--paths`, sin `git add -A` sobre `.sldb` ni un “Nothing staged” mudo. Resultado: staging por diferencia de snapshots de git antes/después del cierre, error con rutas modificadas y sugerencia `--paths`, y tests de regresión. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: `deskops/services/closure.py` y `tests/test_closeout.py`; pruebas equivalentes si `resolved-by`, `retire` o `supersede` comparten helper. Fuera: gramática del CLI, `.gitignore` y derrame de reglas. Es un nodo ejecutable de código, no un agregado.

## AMBIGUEDADES

1. “Los dos tests nuevos pasan” frente a Implementation Path, que enumera “(a)… (b)… (c)”. Obliga a inventar si son dos o tres tests y si (b) cuenta como nuevo.
2. “Si resolved-by, retire o supersede usan el mismo helper de staging” no nombra helper ni rutas; obliga a inventar el criterio de identificación más allá del grep indicado.
3. “archivos de .sldb/core y .sldb/store.yaml” no precisa si el cierre puede escribir otras rutas `.sldb`; obliga a inventar si todo archivo nuevo de `.sldb` entra o solo esas rutas.
4. “si aun asi no hay nada que stagear, el error lista las rutas modificadas” no define el mensaje si el snapshot B está vacío; obliga a inventar esa salida.

## DRY-RUN

Leer `closure.py` 600-720 y `tests/test_closeout.py`; buscar por grep si `resolved-by`, `retire` y `supersede` usan el helper. Tomar snapshot A y B con `git status --porcelain -z --untracked-files=all -- .sldb`; stagear novedades o cambios de estado mediante `git add -- <rutas>`, añadir TaskDoc, Board y `--paths`; si el índice queda vacío, error con lista y sugerencia. Añadir tests sandbox (a), (b), (c) y equivalentes. Dependencias: git, venv, pytest y `origin/main`. Validar con los cuatro comandos del TaskDoc y comparar fallas en worktree limpio.

## FUTURO

El ejecutor implementa, ejecuta las validaciones y deja informe con fallas comparadas contra `origin/main`; un humano revisa y acepta el cierre.
