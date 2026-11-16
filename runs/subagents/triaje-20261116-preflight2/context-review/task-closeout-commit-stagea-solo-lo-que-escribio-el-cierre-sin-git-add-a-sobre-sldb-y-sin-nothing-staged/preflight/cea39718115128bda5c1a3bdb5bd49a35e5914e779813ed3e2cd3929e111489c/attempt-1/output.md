## REFORMULACION

Encargo ejecutable (`task.code`): en el repo `/mnt/ssd/proyectos/SLDB_1/deskops` (cwd), modificar `deskops/services/closure.py` y `tests/test_closeout.py` para que `deskops closeout commit` stagee únicamente las rutas escritas por el cierre (TaskDoc, `desk/tasks/Board.md`, `.sldb/core` y `.sldb/store.yaml` tocados por la transacción), más `--paths`; nunca un `.sldb` que ya estaba sin trackear. Sin `--paths` debe funcionar; si el índice queda vacío, error con rutas modificadas y sugerencia `--paths`. Resultado observable: dos tests nuevos pasan, el archivo ajeno no aparece en `git show --stat HEAD`, y la suite completa no suma fallas. Límites: no tocar la gramática del CLI ni `.gitignore`, no abordar la tarea de derrame de reglas.

## AMBIGUEDADES

1. «stagear con `git add -u -- .sldb` mas solo los archivos nuevos que no estaban en la foto previa»: `-u` también stagea modificaciones *tracked* previas al cierre, contradiciendo «exactamente las rutas que el cierre escribió». Obliga a inventar un filtro sobre el diff antes/después.
2. «'Rutas modificadas' del error = la salida de git status --porcelain del working tree respecto de HEAD»: no dice formato, si incluye untracked ni si son rutas relativas; obliga a inventar presentación.
3. «deskops/services/closure.py» frente a cwd `.../deskops` y `desk/tasks/Board.md`: no aclara si «deskops» y «desk» son subdirectorios del repo o del workspace padre; obliga a inventar la raíz efectiva.
4. «archivos de .sldb/core y .sldb/store.yaml creados o modificados por la transacción»: no define qué escrituras cuentan (¿temporales, locks?); obliga a inventar inclusión/exclusión.
5. «si resolved-by, retire o supersede usan el mismo helper de staging»: no fija el patrón de grep; obliga a inventar el criterio de detección.

## DRY-RUN

Lecturas: `closure.py` líneas ~600–720 (y 113–140, 645–657, 695–697), `tests/test_closeout.py` y fixtures sandbox, llamadas a staging en resolved-by/retire/supersede, notas del inbox referenciadas. Cambios: foto `git status --porcelain -z --untracked-files=all -- .sldb` antes; staging selectivo después; rama sin `--paths`; mensaje de error enriquecido; dos tests (a) y (b). Dependencias: fixtures de desk sandbox existentes, git disponible, `origin/main` accesible para worktree base. Validaciones futuras: los tres pytest indicados, suite completa con `-n 4`, comparación de fallas en worktree limpio, e inspección de `git show --stat HEAD`.

## FUTURO

El ejecutor produce el diff, los tests y el informe con fallas base; un nodo de closeout/commit lo entrega; un humano decide si las fallas preexistentes listadas son aceptables y si el criterio de foto git (preflight 1) sigue vigente.
