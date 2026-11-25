## REFORMULACION

**Propósito:** evitar que `closeout commit` reescriba con `--amend` el commit que la propia tarea cita como evidencia, dejando el recibo apuntando a un sha inalcanzable (caso `task-puente-de-pytest`, 2026-11-16).

**Resultado:** en la rama `_close` de `deskops/services/closure.py` que arma `argv`, decidir commit nuevo cuando `rev-parse HEAD` coincida con un commit citado por la tarea; conservar el amend en el resto de casos.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** dentro, la decisión amend/commit nuevo en `closure.py` y tests en `tests/test_closeout.py`. Fuera, el amend de `runs/subagents/index.jsonl`, el contenido de trailers y otros modos (`supersede`, `resolved-by`, `manual`).

## AMBIGUEDADES

1. "es el value de un recibo evidence-commit aceptado de la tarea": no define formato, ubicación ni qué hace "aceptado" a un recibo; obligaría a inventar esquema y ruta.
2. "su sha, completo o abreviado": no fija longitud mínima ni criterio de comparación de prefijos; obligaría a inventar la regla.
3. "los dos archivos de la Validation pasan" cita `tests/test_closeout_declared_evidence.py`, ausente en `files` y en el bundle; obligaría a inventar su contenido o asumir que ya existe.
4. "cualquier otro modo de cierre (supersede, resolved-by, manual)": `resolved-by` no aparece en los tests mostrados; obligaría a inventar un modo inexistente.
5. "verify cito 9f7d4f13 y el closeout lo amendo": no aclara si el sha se busca solo en `references` o también en `history`/cuerpo; obligaría a inventar el alcance.

## DRY-RUN

**Lecturas:** rama `_close` y lectura de `references`/recibos en `closure.py`; helpers `_git`, `_write_task`, `_write_atom` en `tests/test_closeout.py`.

**Cambios previstos:** comprobar `rev-parse HEAD` contra los shas citados antes de elegir `--amend`; añadir dos tests (citado → commit nuevo, ancestro intacto con mismo sha; no citado → amend como hoy).

**Dependencias:** git, pytest, sandbox en `tmp_path`.

**Validaciones futuras (sin ejecutar):** los dos comandos `pytest -q` de la sección Validation.

## FUTURO

Decisión humana sobre el formato/ubicación de los recibos `evidence-commit` y sobre crear `tests/test_closeout_declared_evidence.py`; otro nodo ejecutará los tests y el commit de cierre.
