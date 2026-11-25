## REFORMULACION
El nodo es una tarea de código, no un agregado ni paquete. Propósito: corregir `deskops review status` para que un recibo con verdict `incomplete` humano se muestre como `incomplete`, reservando `technical_failure` para fallas técnicas. Resultado: cambio en el cálculo de estado, ayuda/documentación de estados y test nuevo; `accepted`, `rejected`, `reviewed`, `stale` y `missing` no cambian. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no cambiar cómo se escriben los recibos; alcance en `deskops/services/review.py` (~880-912), lista de estados en ayuda (`deskops/cli/registry.py`) y golden si cambia, más un test.

## AMBIGUEDADES
1. El cold-bundle pide considerar “los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra”, pero el TaskDoc declara `pills: []`, `atoms: []`, `files: []` y no lista rituales. Obligaría a inventar artefactos o rutas.
2. “verdict incomplete cuya reason no es technical” no define la comparación exacta; el texto solo dice “Distinguir incomplete humano de incomplete technical por el campo reason”. Obligaría a inventar regla para mayúsculas, subcadenas, `reason` vacío o valores compuestos.
3. “recibo vigente” no está definido. Obligaría a inventar el criterio de vigencia.

## DRY-RUN
Lecturas futuras: TaskDoc; referencia `desk/inbox/20261116-013120-...`; `review.py` líneas 640-670 y 880-912; ayuda en `registry.py`; golden asociado; tests de review. Cambios previstos: condicionar `technical_failure` a verdict `incomplete` con `reason` técnica; devolver `incomplete` para `incomplete` no técnico; añadir `incomplete` a la enumeración de estados/ayuda y actualizar golden si corresponde; crear test con dos casos: dispuesto `incomplete` con reason `"re-fundar"` y falla técnica. Dependencias: forma real del recibo, campo `reason` y helpers de estado existentes. Validaciones futuras: `pytest -q tests -k review`; suite completa con `-n 4`; repetir cada falla en worktree limpio de `origin/main` y listarla si falla igual. Sin ejecutar nada.

## FUTURO
El ejecutor futuro inspeccionará el código y fijará la regla exacta de `reason`; producirá diff, test y eventual actualización de ayuda/golden. Un humano o validador decidirá si acepta fallas preexistentes y si la documentación basta. Si el Board debía aportar rituales, pills o átomos, otro nodo deberá entregarlos.
