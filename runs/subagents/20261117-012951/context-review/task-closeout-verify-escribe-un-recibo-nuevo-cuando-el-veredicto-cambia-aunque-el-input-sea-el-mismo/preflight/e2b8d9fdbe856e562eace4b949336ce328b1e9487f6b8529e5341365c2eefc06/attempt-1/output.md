## REFORMULACION
Propósito: corregir la deduplicación de `_write_evidence_receipts` para que `closeout verify` no omita un recibo de evidencia cuando cambia el veredicto aunque `input_sha256` sea el mismo. Resultado: escribir un recibo nuevo si existe uno intacto del mismo `fact` e `input_sha256` con `verdict` distinto; mantener el salto si coinciden input y verdict. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar solo `deskops/services/closure.py` y `tests/test_closeout_declared_evidence.py`; quedan fuera el cálculo de `input_sha256`, los nombres de recibos y la regla de closeout. Es una tarea ejecutable, no un agregado.

## AMBIGUEDADES
1. “el unico recibo intacto con el mismo fact e input_sha256 tiene otro verdict”: no define “intacto” ni qué hacer si hay varios recibos coincidentes; obliga a inventar el criterio de selección y el comportamiento ante multiplicidad.
2. “se arregla la causa sin cambiar el input de ese fact”: no indica cómo lograrlo en el test; obliga a inventar la fixture o condición externa que cambia el veredicto sin alterar el input.
3. “filtrar same_input por payload verdict igual al verdict nuevo”: no detalla la estructura del payload; obliga a asumir la ubicación y forma exacta de `verdict`.
4. “desbloquea el cierre” / “closeout commit pasa la regla”, pero la regla está fuera de alcance: no aclara si el test debe ejecutar un commit real o simularlo; obliga a inventar el nivel de integración.

## DRY-RUN
Lecturas: `closure.py` (`_write_evidence_receipts`), `tests/test_closeout_declared_evidence.py`, la nota de inbox referenciada y `tests/test_closeout.py`. Cambios previstos: añadir el `verdict` a la comparación de `same_input`; agregar tests para rejected→accepted con mismo input y accepted→accepted sin duplicado. Dependencias: helpers de sandbox, fixtures de gates, pytest y el entorno `PYTHONPATH`/`TMPDIR` indicado. Validaciones futuras: los dos comandos pytest de Validation; comprobar que no cambian `input_sha256` ni nombres de recibos. Sin ejecutar nada.

## FUTURO
Otro nodo ejecutor producirá el diff y la salida de pytest. Un humano decidirá la aceptación o el merge. El cierre verificará el resultado con la regla existente; este preflight no decide la implementación.
