## REFORMULACION
Nodo ejecutable, no agregado. **Propósito:** diagnosticar por qué `test_init_repairs_a_broken_deskops_link` falla tras el PR #3 de sldb y restaurar la suite de deskops. **Resultado:** decisión fundada entre (a) reescribir el test porque un enlace resoluble por nombre ya no está roto, o (b) hacer que `bootstrap.py` normalice también el path guardado; cambios en test, `bootstrap.py` solo si (b), `CHANGELOG`, y commit con `Task-Id`. **Repo:** deskops; rutas citadas: `tests/test_doctor_model_registration.py`, `deskops/bootstrap.py`. **Límites:** no tocar sldb —“el PR #3 es correcto”— ni el test intermitente de dispatch.

## AMBIGUEDADES
1. “Decidir con evidencia cuál de las dos cosas es cierta y hacerla”: no fija umbral de evidencia ni quién adjudica; obligaría a inventar el criterio de decisión.
2. “Preferir (a) salvo que algo de deskops lea el path guardado sin pasar por store_links (buscar con grep)”: no define patrones, alcance ni qué cuenta como lectura; obligaría a inventar la regla y el grep.
3. “anotarlo en el run dir”: el bundle no indica ruta del run dir; obligaría a inventar su ubicación.
4. “La suite de deskops vuelve a verde” frente a “la suite completa no tiene fallas de ese archivo”: no aclara si fallos ajenos bloquean; obligaría a inventar el criterio de cierre.

## DRY-RUN
Un ejecutor futuro leería el TaskDoc, el test, `bootstrap.py`, la implementación de `store_links` en `/mnt/ssd/herramientas/sldb`, `CHANGELOG` y el worktree/run dir que entregue dispatch. Reproduciría el fallo; inspeccionaría `_point_deskops_link_at` y `bootstrap.py` (~265); ejecutaría grep sobre `deskops/`; decidiría (a)/(b). Cambios previstos: reescritura del test y test nuevo del caso resoluble, o comparación/reescritura del path guardado. Dependencias: PR #3 de sldb, worktree de dispatch, `TMPDIR=/tmp`. Validaciones futuras: pytest del archivo, suite completa `-n 4`, `CHANGELOG` y commit con trailer. Sin ejecutar nada.

## FUTURO
Dispatch aporta worktree y run dir; un humano o el integrador acepta la decisión (a)/(b); la CI valida el commit; el integrate consume el resultado.
