REFORMULACION
Propósito: que `deskops closeout commit` deje de stagear con `git add -A -- .sldb` y de responder "Nothing staged" mudo. Resultado: commit con solo TaskDoc, `desk/tasks/Board.md` y los archivos `.sldb` escritos por la transacción de cierre, más `--paths`; sin `--paths` funciona, y si no hay nada, el error lista rutas y sugiere `--paths`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `deskops/services/closure.py` y `tests/test_closeout.py` (y resolved-by/retire/supersede si comparten helper); fuera: reglas de activación, gramática CLI, `.gitignore`. El nodo es un encargo de código, no ejecutable por sí solo.

AMBIGUEDADES
1. "archivos de .sldb/core y .sldb/store.yaml creados o modificados por la transaccion del cierre": no define cómo distinguir autoría de la transacción de cambios previos; obligaría a inventar un manifiesto de escrituras o aceptar el snapshot git como proxy.
2. "el error lista las rutas modificadas": no dice contra qué (HEAD, índice o working tree previo); obligaría a inventar la fuente.
3. "Si resolved-by, retire o supersede usan el mismo helper de staging, el cambio les aplica y se prueba igual.": no afirma si hoy lo usan ni cuántos tests añadir; obligaría a inventar cobertura.
4. "sin fallas nuevas respecto de main": no fija qué main (local/remoto) ni método de comparación; obligaría a inventar el baseline.

DRY-RUN
Lecturas: `closure.py` 600-720 (staging ~695-697, rama manual 113-140, mensaje 645-657) y fixtures de `test_closeout.py`. Cambios previstos: foto `git status --porcelain -z --untracked-files=all -- .sldb` antes del cierre; después `git add -u -- .sldb` más solo nuevos ausentes en la foto; sin `--paths` stagear TaskDoc/Board/.sldb; error con rutas y sugerencia. Tests: dos casos sandbox (yaml ajeno sigue untracked; sin `--paths` commitea TaskDoc y Board). Dependencias: git, pytest y fixtures sandbox. Validaciones futuras: los cuatro comandos pytest indicados, incluida la suite completa.

FUTURO
Un humano fija el baseline de main y decide si resolved-by/retire/supersede requieren tests; CI ejecuta la suite; la tarea de reglas de activación queda fuera de este nodo.
