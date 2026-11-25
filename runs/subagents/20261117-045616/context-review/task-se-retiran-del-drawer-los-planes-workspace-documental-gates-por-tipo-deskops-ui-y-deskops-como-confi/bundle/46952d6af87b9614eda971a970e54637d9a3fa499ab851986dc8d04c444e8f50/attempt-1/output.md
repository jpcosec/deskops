REFORMULACION
Propósito: retirar del drawer los planes `workspace-documental`, `gates-por-tipo`, `deskops-ui` y `deskops-como-config`, y la carpeta `desk/drawer/tasks/workspace-documental`, dejando los tests de review node sobre un fixture propio y sin citas vivas en help ni docs. Resultado: árbol sin esos planes, fixture bajo `tests/fixtures/plans/`, ejemplos y docs ajustados y los tests de la validación verdes. Repo: deskops. Límites: no toca los recibos ya escritos en `desk/reviews/`, ni la tarea GC08, ni `tests/test_graph_missing_existing_files.py`.

AMBIGUEDADES
1. «por ejemplo ROOT, GC01, GC02 y GC03» frente al test que exige «review-deskops-gates-por-tipo-pc01-node-1»: obliga a inventar si PC01 entra en el fixture.
2. «solo lo que los tests de review node leen (dag.yaml recortado…)», pero el test hace `brief = plan_dir / "brief.md"` y lo reescribe: obliga a inventar si el fixture incluye `brief.md` y con qué contenido.
3. «PLAN_SRC y las rutas de tests/test_review_command.py y tests/test_review_doc.py»: en `test_review_doc.py` son literales de validación («desk/drawer/plans/gates-por-tipo/dag.yaml#node:GC02»); obliga a inventar si se reescriben o se dejan.
4. «queda como texto historico sin ruta viva»: obliga a inventar la forma concreta en `docs/deskops-ui.md` (borrar la ruta o marcarla).
5. «pasan a una ruta de ejemplo generica de plan»: obliga a inventar cuál es esa ruta en `registry.py`.
6. «sin entradas nuevas por los planes borrados»: obliga a inventar la línea base de `graph missing` contra la que se compara.

DRY-RUN
Lecturas: los cuatro planes y la carpeta de fichas; los dos tests de review; `deskops/cli/registry.py` (ejemplos y goldens); `docs/operator-manual.md` y `docs/deskops-ui.md`; tests de goldens. Cambios previstos: crear `tests/fixtures/plans/gates-por-tipo/` (dag.yaml y brief.md mínimos), apuntar `PLAN_SRC`, `git rm` de los cuatro planes y de la carpeta, sustituir la ruta de ejemplo en registry.py, regenerar goldens de ayuda, editar las dos docs. Dependencias: `task-deskops-review-node-…` (depends_on), deskops y su venv, git. Validaciones futuras: los cuatro pytest y `graph missing`.

FUTURO
El cierre (commit y evidencia atom/materialization) lo produce closeout; un humano confirma el retiro y el contenido mínimo del fixture; sldb GO07 sigue como xfail ajeno y los recibos históricos quedan para otros nodos.
