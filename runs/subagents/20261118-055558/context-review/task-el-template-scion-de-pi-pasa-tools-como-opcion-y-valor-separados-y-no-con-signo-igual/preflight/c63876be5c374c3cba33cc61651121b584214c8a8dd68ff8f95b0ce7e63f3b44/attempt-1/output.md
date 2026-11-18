## REFORMULACION
Nodo ejecutable de código (no agregado). Propósito: corregir el template scion para que el harness pi reciba `--tools` y su valor como argumentos separados. Resultado: en `deskops/runtime/scion.py`, `_command_args` emite para pi `"--tools", "read,grep,find,ls,bash"`; los demás harness conservan `opcion=valor`; la decisión se basa en el `kind` de `RuntimeProfileDoc`, no en el nombre del rol. Repo: el actual, con rutas `deskops/runtime/scion.py` y `tests/test_scion_runtime.py`. Límites: incluye esos archivos y, condicionalmente, `docs/operator-manual.md`; excluye cambios en scion, imagen de pi y otros flags; checkout principal, sin worktree ni rama, sin `git add` ni `git commit`. Validación: `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py`.

## AMBIGUEDADES
1. Contradicción sobre commit: el Scope dice “sin git add ni git commit”, pero el átomo se llama `atom-code-changes-close-with-tests-and-commit`. Obliga a inventar si el cierre exige commit o lo prohíbe.
2. “La decision se toma por el kind del RuntimeProfileDoc” no explicita el literal del `kind` que identifica pi; solo se menciona `--harness pi`. Obliga a asumir el valor concreto o el mapeo interno.
3. “la mencion en `docs/operator-manual.md` si el manual describe la forma de command_args” no define qué cuenta como describirla ni si la actualización es obligatoria. Obliga a inventar el criterio de edición.

## DRY-RUN
Lecturas: TaskDoc, `deskops/runtime/scion.py`, `tests/test_scion_runtime.py` y, condicionalmente, `docs/operator-manual.md`. Cambios previstos: localizar `_command_args`; añadir rama por `kind` para pi con dos elementos; conservar la forma actual para los demás; añadir o ajustar tests para pi separado y claude sin cambios; tocar el manual solo si describe `command_args`. Dependencias: valores de `RuntimeProfileDoc.kind` y generación de templates. Validaciones futuras: ejecutar el pytest indicado e inspeccionar templates generados con `--harness pi` y `--harness claude`. Sin ejecutar nada.

## FUTURO
Revisión humana del diff; decisión humana sobre la contradicción del commit; eventual CI o suite completa ejecutada por otro nodo; integración del cambio según el flujo del repo.
