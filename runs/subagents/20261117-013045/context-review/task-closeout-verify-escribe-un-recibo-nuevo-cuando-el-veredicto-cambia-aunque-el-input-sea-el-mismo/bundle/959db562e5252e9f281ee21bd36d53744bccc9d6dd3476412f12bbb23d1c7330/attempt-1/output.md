## REFORMULACION
Propósito: corregir la deduplicación de recibos de evidencia de `closeout verify` para que un cambio de veredicto genere un recibo nuevo aunque `input_sha256` no cambie. Resultado: `_write_evidence_receipts` solo omitirá el recibo si ya existe uno intacto con el mismo fact, `input_sha256` y verdict; además, tests que cubran rejected→accepted y la no duplicación verde→verde. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `deskops/services/closure.py` y `tests/test_closeout_declared_evidence.py`; fuera de alcance el cálculo de `input_sha256`, nombres de recibos y regla de closeout.

## AMBIGUEDADES
1. “si ya existe uno intacto con el mismo input_sha256”: no se define “intacto”. Obligaría a inventar el criterio de integridad si no se reutiliza el existente.
2. “se arregla la causa sin cambiar el input de ese fact”: no se especifica cómo provocar rojo→verde manteniendo el input. Obligaría a inventar el mecanismo de test.
3. “cuando el veredicto cambia”: el Goal concreta “otro verdict”, pero no aclara si aplica simétricamente accepted→rejected y rejected→accepted. Obligaría a decidir el alcance.

## DRY-RUN
Lecturas: `closure.py` (`_write_evidence_receipts`, estructura de payload/recibos), `tests/test_closeout_declared_evidence.py`, fixtures de `test_closeout.py` y helpers de sandbox. Cambios previstos: filtrar `same_input` exigiendo también igual verdict al nuevo; añadir test rejected→accepted con mismo input que escriba recibo accepted y permita `closeout commit`; añadir test de dos verify verdes sin duplicar. Dependencias: que el payload conserve `verdict`, que exista el filtro `same_input` y que los tests usen raíz desk desechable conforme al átomo de sandbox. Validaciones futuras, sin ejecutar: los dos comandos pytest del TaskDoc; comprobar recibo nuevo y desbloqueo; comprobar no duplicación.

## FUTURO
Un nodo implementador aplicaría el cambio y ejecutaría las validaciones; otro nodo o un humano revisaría el diff, el commit descriptivo y el cierre conforme al átomo de tests y commit.
