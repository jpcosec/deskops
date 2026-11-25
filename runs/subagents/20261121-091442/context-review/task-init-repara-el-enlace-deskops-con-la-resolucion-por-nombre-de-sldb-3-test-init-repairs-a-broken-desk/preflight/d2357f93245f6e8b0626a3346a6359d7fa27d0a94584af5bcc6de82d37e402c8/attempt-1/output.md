REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: devolver el verde a `tests/test_doctor_model_registration.py::test_init_repairs_a_broken_deskops_link` en deskops contra el sldb de `/mnt/ssd/herramientas/sldb`, tras el PR #3 que resuelve enlaces por nombre de store. Resultado: decidir con evidencia entre (a) reescribir el test para casos realmente rotos y añadir uno para el caso resoluble por nombre, o (b) normalizar el path guardado en `bootstrap.py`; más CHANGELOG y commit con trailer `Task-Id`. Repo: deskops, en el worktree que dé dispatch; sldb solo como dependencia. Límites: tocar `tests/test_doctor_model_registration.py`, `bootstrap.py` solo si (b), y CHANGELOG; no tocar sldb ni el test intermitente de dispatch.

AMBIGUEDADES

1. «el worktree que dispatch te da»: el input no trae ruta; obligaría a inventar el worktree o asumir que otro nodo lo entrega.
2. «store_links sobre el store del test»: no se nombra fixture ni ruta; obligaría a inventar cuál es ese store.
3. «un enlace 'deskops' cuyo nombre resuelve a otro store o a ninguno, o cuyo status no es ok»: no fija número de casos ni aserciones; obligaría a inventar escenarios concretos.
4. «Decidir con evidencia»: no define umbral; obligaría a inventar el criterio de aceptación de (a) frente a (b).
5. «bootstrap.py (línea ~265, target == owner)»: línea aproximada y condición sin contexto de código; obligaría a inventar la ubicación exacta.

DRY-RUN

Lecturas: TaskDoc, `tests/test_doctor_model_registration.py` (incl. `_point_deskops_link_at`, línea 153), `deskops/bootstrap.py` (~265), fuente de `store_links` en `/mnt/ssd/herramientas/sldb`, CHANGELOG. Cambios previstos: p1 reproducir con `store_links` el estado tras `_point_deskops_link_at` y anotarlo en el run dir; p2 `grep -rn 'store_index\|"path"' deskops/` y elegir (a)/(b); p3 reescribir test (a) o comparar path en bootstrap (b); p4 pytest del archivo y suite `-n 4`; p5 CHANGELOG y `git commit -- <rutas>` con trailer. Dependencias: sldb PR #3 instalado, pytest, worktree de dispatch. Validaciones futuras: comando pytest indicado, suite sin fallas de ese archivo, trailer presente.

FUTURO

Dispatch entrega el worktree; un humano o el merge valida contra `origin/main`; el test intermitente de `test_dispatch.py` queda para otra tarea; se asume decidido que el PR #3 de sldb es correcto.
