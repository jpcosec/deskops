REFORMULACION

Propósito: corregir `deskops closeout commit` para que stagee solo lo escrito por el cierre, más `--paths`. Resultado: commit con TaskDoc, Board y rutas de `.sldb/core`/`.sldb/store.yaml` creadas o modificadas por la transacción; nunca archivos de `.sldb` ya sin trackear antes; sin `--paths` debe funcionar y, si no hay nada, error con rutas modificadas y sugerencia `--paths`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: `deskops/services/closure.py` (rama manual ~113-140, “Nothing staged” ~645-657, `git add -A -- .sldb` ~695-697) y `tests/test_closeout.py`; mismo helper para resolved-by/retire/supersede si aplica. Fuera: derrama de reglas de activación, gramática CLI y `.gitignore`. Es tarea ejecutable `task.code`, no agregado.

AMBIGUEDADES

1. “Los dos tests nuevos pasan” frente a tres casos “(a)… (b)… (c)”: obliga a inventar si son dos o tres y cuál no cuenta.
2. El Goal limita a “archivos de .sldb/core y .sldb/store.yaml”, pero el paso 2 stagea “solo las rutas que estan en B y no estan en A, o que estan en ambas con distinto codigo de estado”, sin filtro: obliga a decidir si se stagea cualquier ruta de `.sldb` o solo core/store.yaml.
3. “si el indice queda vacio” no cubre cambios ya staged ajenos: obliga a inventar si se commitean, se rechazan o se preservan.
4. “stagear el TaskDoc, el Board” no fija rutas exactas ni su fuente: obliga a inventar si salen de la transacción, de convenciones o de argumentos.

DRY-RUN

Lecturas: `closure.py` 600-720, `tests/test_closeout.py`, helper de staging y llamadas de resolved-by/retire/supersede por grep. Cambios previstos: foto A/B con `git status --porcelain -z --untracked-files=all -- .sldb`; calcular rutas nuevas o con estado cambiado; `git add -- <rutas>` más TaskDoc, Board y `--paths`; error con lista de B y sugerencia. Tests (a), (b), (c). Dependencias: git, sandbox desk y pytest. Validaciones futuras: los pytest listados y suite completa comparada en worktree de `origin/main`. No se ejecuta nada.

FUTURO

Un nodo ejecutor produce el diff, los tests y el informe de fallas; un humano decide las ambigüedades 1-4 y aprueba el criterio de staging; el gate de preflight valida el TaskDoc.
