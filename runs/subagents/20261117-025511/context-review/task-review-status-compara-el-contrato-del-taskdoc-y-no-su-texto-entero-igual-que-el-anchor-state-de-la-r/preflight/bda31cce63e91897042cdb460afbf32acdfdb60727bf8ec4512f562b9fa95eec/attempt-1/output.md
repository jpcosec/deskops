## REFORMULACION

**Propósito:** corregir el falso "stale" de `deskops review status` cuando cambia texto del TaskDoc que no pertenece a su contrato (cabecera `sldb.at`, `tags`, `status`, `current_node`, `history`, `references`).

**Resultado:** `review status` marca stale solo si cambia el contrato del TaskDoc (`title, goal, scope, implementation_path, files, validation, done_when`) o alguna otra fuente del input de la revisión (para bundle: pills, átomos, rituales y archivos enlazados). El estado por clave debe coincidir con el `anchor_state` del recibo de activación. Se añade `contract_sha256` a `ReviewDoc`; recibos viejos sin campo mantienen la comparación actual por `input_sha256` completo.

**Repo/archivos:** `/mnt/ssd/proyectos/SLDB_1/deskops`; `deskops/services/review.py`, `deskops/models/review.py`, `tests/test_review_command.py`.

**Límites:** no cambiar `input.md` ni el `input_sha256` registrado, ni las reglas de activación.

## AMBIGUEDADES

1. "el mismo digest que usa deskops para el contrato, si existe" — el condicional no define qué hacer si no existe; obligaría a inventar el algoritmo de digest.
2. "se ubica con grep -rn contract_sha256 deskops ../sldb/src" — no aclara si deskops debe importar de `sldb` o duplicar el cálculo; obligaría a inventar una dependencia entre paquetes.
3. "para bundle: pills, atomos, rituales y archivos de files" frente a `files` ya presente en `__contract__` — no aclara si los archivos se cuentan dos veces o se excluyen del hash bundle; obligaría a inventar precedencia.
4. La validación exige `tests/test_review_doc.py`, pero `files` y el scope solo listan `tests/test_review_command.py` — obligaría a inventar si ese test es editable.
5. "Recibos viejos sin el campo: se comparan como hoy" — no define cómo se detecta "sin campo" (`None` vs ausente) ni si se reescriben retroactivamente.

## DRY-RUN

**Lecturas:** `review.py` ~440-520 y ~740-800; `models/review.py`; `tests/test_review_command.py`; búsqueda de `__contract__` y `contract_sha256`.
**Cambios previstos:** campo `contract_sha256` en `ReviewDoc`; función de digest contractual; rama en `_state_for_key` que compara digest (fallback a `input_sha256` en recibos viejos); dos tests (tags/status → accepted; goal → stale).
**Dependencias:** implementación real del digest en `sldb`/deskops; formato persistido de `ReviewDoc`.
**Validaciones futuras:** los tres comandos pytest indicados y baseline en worktree limpio de `origin/main` para fallas preexistentes.

## FUTURO

Implementación y commit por el ejecutor; decisión humana sobre importar `sldb` vs cálculo local; revisión del informe con fallas baseline.
