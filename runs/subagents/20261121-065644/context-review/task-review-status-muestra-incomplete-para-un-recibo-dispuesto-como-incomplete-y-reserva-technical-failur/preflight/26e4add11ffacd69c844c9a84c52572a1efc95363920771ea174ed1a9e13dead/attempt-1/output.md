## REFORMULACION

Encargo ejecutable (`task.code`) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: corregir el cálculo de estado de `deskops review status` para que un recibo vigente con `verdict: incomplete` y `reason` no técnica se muestre como `incomplete`, reservando `technical_failure` solo para `verdict: incomplete` con `reason: technical`. Resultado: cambio en `deskops/services/review.py` (~880-912), ajuste de la lista de estados en la ayuda de `review status` (`deskops/cli/registry.py`) si existe y de su golden, más un test nuevo. Límites: no se modifica cómo se escriben los recibos; `accepted`, `rejected`, `reviewed`, `stale` y `missing` no cambian.

## AMBIGUEDADES

1. "Distinguir incomplete humano de incomplete technical por el campo reason" / "cuya reason no es technical": no se especifica si la comparación es igualdad exacta con `technical`, prefijo, sensibilidad a mayúsculas, ni qué hacer si `reason` falta o está vacío. Obliga a inventar la regla de detección.
2. "un recibo vigente": no define vigencia (último recibo del bundle, no superseded, por fecha). Obliga a inventar el criterio de selección.
3. "la lista de estados en la ayuda de review status si la hay ... y su golden de ayuda si cambia": no nombra el fichero golden ni confirma que la ayuda enumere estados. Obliga a inventar ubicación y necesidad del cambio.
4. "accepted, rejected, reviewed, stale y missing no cambian": no explica de dónde surgen `reviewed`, `stale` y `missing` ni su relación con el bloque ~880-912. Obliga a inventar su semántica.
5. "la corrida que fallo por transporte o cuota": no vincula explícitamente ese origen a un valor concreto de `reason` distinto de `technical`. Obliga a asumir que el escritor (~641-647) siempre emite exactamente `technical`.
6. Los 16 recibos ya dispuestos: no aclara si basta recalcular al leer o si requieren backfill (excluido del scope). Obliga a decidir el tratamiento de datos existentes.

## DRY-RUN

Lecturas: `deskops/services/review.py` (640-670 y 880-912), `deskops/cli/registry.py` (ayuda de `review status`), golden de ayuda correspondiente, tests existentes de review, recibo de inbox referenciado. Cambios previstos: rama de cálculo que devuelve `incomplete` cuando `verdict == incomplete` y `reason` no técnica; test nuevo con dos fixtures (reason `re-fundar` → `incomplete`; reason `technical` → `technical_failure`); actualización de ayuda/golden si enumera estados. Dependencias: estructura real del recibo y del bloque de estado. Validaciones futuras: `pytest -q tests -k review`; suite completa `-n 4` comparando fallas en worktree limpio de `origin/main`. Sin ejecutar nada.

## FUTURO

Un humano decide si las fallas preexistentes detectadas en la suite se aceptan como baseline y aprueba la entrega/merge; otro nodo podría encargarse del backfill de los 16 recibos históricos, aquí fuera de alcance.
