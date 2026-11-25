## REFORMULACION
**Propósito:** retirar del drawer los planes `workspace-documental`, `gates-por-tipo`, `deskops-ui` y `deskops-como-config`, y la carpeta `desk/drawer/tasks/workspace-documental`; desacoplar los tests de review node del plan real mediante un fixture propio; limpiar citas en ayuda y documentación.

**Resultado:** árbol sin esos cuatro planes ni la carpeta de fichas; `tests/fixtures/plans/` con una copia mínima de `gates-por-tipo`; `PLAN_SRC` y rutas de `tests/test_review_command.py` y `tests/test_review_doc.py` apuntando al fixture; ejemplos de `deskops/cli/registry.py` con ruta genérica y goldens actualizados; `docs/operator-manual.md` y `docs/deskops-ui.md` sin rutas vivas; tests de Validation pasando y `graph missing` sin crecer.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`, según los comandos de Validation.

**Límites:** no tocar los recibos de `desk/reviews/`, la tarea de GC08 ni `tests/test_graph_missing_existing_files.py`; solo los `git rm` y ajustes enumerados.

## AMBIGUEDADES
1. «dag.yaml recortado a los nodos que usan, por ejemplo ROOT, GC01, GC02 y GC03»: «por ejemplo» no fija el conjunto exacto; obligaría a inspeccionar los tests o inventar qué nodos incluir.
2. «pasan a una ruta de ejemplo generica de plan»: no se especifica la ruta concreta; obligaría a inventarla.
3. «sus goldens de ayuda»: no se nombran los archivos golden afectados; obligaría a localizarlos o suponerlos.
4. «queda como texto historico sin ruta viva»: no define la redacción exacta ni qué parte de la cita conservar; obligaría a inventar el texto final.
5. «solo lo que los tests de review node leen»: no enumera archivos ni campos del fixture; obligaría a inspeccionar los tests o inventar el contenido mínimo.

## DRY-RUN
**Lecturas previstas:** task doc; `tests/test_review_command.py`; `tests/test_review_doc.py`; `deskops/cli/registry.py`; `docs/operator-manual.md`; `docs/deskops-ui.md`; `desk/drawer/plans/gates-por-tipo/dag.yaml`; goldens de ayuda.

**Cambios previstos:** crear `tests/fixtures/plans/gates-por-tipo/dag.yaml` recortado; actualizar `PLAN_SRC` y rutas de tests; `git rm` de los cuatro planes y `desk/drawer/tasks/workspace-documental`; sustituir ejemplos por ruta genérica; regenerar goldens; ajustar las dos docs.

**Dependencias:** los tests deben revelar los nodos y campos realmente usados; debe existir herramienta de regeneración de goldens; el plan real debe seguir presente hasta comprobar el fixture.

**Validaciones futuras:** ejecutar los cuatro pytest de Validation y `deskops graph missing --root .`, comparando que no aparezcan entradas nuevas.

## FUTURO
El nodo ejecutor producirá el fixture, los borrados, los ajustes de ayuda/docs y la evidencia de tests. Un humano decidirá si el recorte del fixture y el texto histórico de las docs son aceptables.
