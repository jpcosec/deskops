## REFORMULACION

GC07 (kind `code`, `delivery`, repo **deskops**, hijo de PC02) encarga dejar de resolver `inherits_from` en Python: `_resolve_task_payload` obtendrá de sldb la clausura `inherits_from+` (sin duplicados, origen excluido, ciclos tolerados y documentados) y calculará los `effective_*` sobre esa lista; el gate de cierre leerá `effective_references` y `effective_atoms`. Límites: no modifica sldb; sin GO04 el payload ancestral sigue leyéndose por `doc_io`; `output_scope` se limita a `operations.py`, `closeout_gates.py`, `tests/` y `CHANGELOG.md`; depende de GC01 y requiere `G_SLDB_LANG` (pending).

## AMBIGUEDADES

1. **Orden de la cadena.** Cita: «los effective_* se calculan sobre esa lista en el orden que sldb devuelve (hipótesis: el orden de un conjunto alcanzado por camino lo fija GO05; si no, deskops ordena por id y lo documenta)» frente a «effective_pills = pills de A ∪ B ∪ C en ese orden». Un conjunto no tiene orden; ordenar por id puede no coincidir con A→B→C; el ejecutor tendría que inventar cuál rige en el test.
2. **Dónde se documenta el ciclo.** Cita: «un ciclo deja de ser error y se documenta», mientras `output_scope` no incluye `docs/`. Obliga a inventar destino y forma de esa documentación, y si `CHANGELOG.md` basta.

## DRY-RUN

Lecturas hipotéticas: `operations.py` (`_resolve_task_payload`, `_closeout_reference_evidence`), `closeout_gates.py:129` y `:146`, tests de herencia y contrato de GO02(b)/GO05 con la versión pinneada. Cambios previstos: sustituir el recorrido recursivo por una consulta de clausura a sldb; calcular los `effective_*` sobre la lista devuelta; leer `effective_*` en el gate; eliminar el error de ciclo; adaptar tests existentes y añadir A→B→C y ciclo; actualizar `CHANGELOG.md`. Dependencias: GC01 cerrado y `G_SLDB_LANG` satisfecho (GO05 en main de sldb y pin en `pyproject.toml`). Validaciones futuras: `pytest tests` verde, grep sin «Task inheritance cycle», y los escenarios de `acceptance` (pills heredadas, ciclo sin `ValueError`, `closeout verify` con commit heredado).

## FUTURO

sldb cierra GO05 y deskops pinnea esa versión; hasta entonces GC07 no se promueve. El TaskDoc fijará nombres exactos de tests y archivos al promover. Quien opera el desk escribe la disposición de la revisión. GC08 actualizará rituales/manual si nombran la herencia, y PC02 validará el conjunto con GC04–GC08 y `G_CONSUMER`.
