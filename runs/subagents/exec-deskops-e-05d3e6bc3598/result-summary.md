# Resultado

run_id: exec-deskops-e-05d3e6bc3598
session: no disponible (agente scion claude)
session_sha256: no disponible

## Hecho
- deskops/dispatch.py: reap calcula la etiqueta con _scion_task_label(task_id) (sin leer el TaskDoc); si stop o delete fallan imprime "<nombre> <rol> error:<codigo>", sigue y devuelve rc 6 (4 si queda alguno vivo). Nuevo _role_instructions: prompt.md del executor (commit con rutas nombradas, Task-Id, sin push, luego advance) y del tester (git log --grep / git show --name-only, tests tocados de a uno con TMPDIR=/tmp, PASA/FALLA, suite completa en integrate).
- tests/test_dispatch.py: 4 tests nuevos (reap con tarea borrada, error de scion, prompts executor y tester) y el fake scion admite FAKE_SCION_FAIL_STOP.
- docs/operator-manual.md y CHANGELOG.md.

## Archivos para commitear
deskops/dispatch.py, tests/test_dispatch.py, docs/operator-manual.md, CHANGELOG.md

## Validacion
tests/test_dispatch.py: 18 passed (ver validation.log). Suite completa: la corre integrate.

## Revisar
- Elegí rc 6 para error de scion en reap (la tarea solo pedia "distinto de 0").
- No commiteé: el arbol tiene trabajo ajeno sin commitear.
