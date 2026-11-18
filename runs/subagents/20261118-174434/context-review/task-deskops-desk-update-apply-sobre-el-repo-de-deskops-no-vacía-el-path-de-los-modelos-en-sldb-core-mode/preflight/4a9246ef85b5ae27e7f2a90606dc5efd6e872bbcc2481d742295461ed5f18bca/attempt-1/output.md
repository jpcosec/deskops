## REFORMULACION

Encargo ejecutable (`task.debug`, no agregado): en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, corregir que `deskops desk update --apply` vacía `path` en `.sldb/core/models/*.yaml` y escribe relation types no declarados. El resultado debe ser: paths preservados según `models:` de `.sldb/store.yaml`; relation types limitados a los declarados por el paquete; test regresivo en `tests/test_desk_sync.py`; informe en `result-summary.md`; CHANGELOG. Límites: no cambiar el layout de `.sldb`; el ejecutor solo corre `tests/test_desk_sync.py` y tests de archivos tocados; la suite completa la corre integrate.

## AMBIGUEDADES

1. “`git -C /tmp/repro checkout --detach <HEAD>`” y “HEAD local de deskops al momento del despacho”: no se fija el SHA. Obliga a inventar o resolver externamente el commit exacto.
2. “con el mismo helper que usan los tests existentes de ese archivo”: no se nombra el helper. Obliga a inventar cuál es.
3. “El informe va en result-summary.md del run dir que fija el despacho”: no se da la ruta del run dir. Obliga a inventar la ubicación.
4. “si reltype-links_to y el cambio de has_model.md están declarados”: no se indica dónde ni con qué criterio verificarlo. Obliga a inventar la fuente de declaración.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, repo deskops, `.sldb/store.yaml`, `.sldb/core/models/*.yaml`, código de `desk update`, `tests/test_desk_sync.py`, relation types y CHANGELOG. Cambios previstos: clonar en `/tmp/repro`, reproducir con `deskops desk update --apply --root /tmp/repro`, guardar `git diff --stat` y diff acotado; localizar el writer del path vacío; añadir test que falle antes; aplicar el fix; actualizar CHANGELOG e informe. Dependencias: HEAD local, helper de tests, `store.yaml` como fuente de verdad y entorno Python/pytest. Validaciones futuras: ejecutar `TMPDIR=/tmp python -m pytest -q tests/test_desk_sync.py` y tests tocados; verificar que la reproducción ya no modifica modelos ni relation types no declarados.

## FUTURO

Integrate ejecuta la suite completa y valida el cierre. Un humano decide commit/merge y aceptación final. El despacho debe aportar el run dir y el SHA si no se resuelven desde el repo.
