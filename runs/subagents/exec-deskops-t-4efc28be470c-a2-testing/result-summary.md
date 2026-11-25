PASA

# Verificación

Commit del ejecutor (último, intento 2): `2b5f68da` — "docs: faq y deskops-ui advierten que promote no es el camino para notas que son trabajo"
Commit previo del mismo task (intento 1): `812f6115` — skill, ritual, help de promote, golden y operator-manual.

Archivos del commit 2b5f68da:
- `docs/faq.md`
- `docs/deskops-ui.md`

# Tests

Los tres tests de la validación pasan. Nota de entorno: `../.venv/bin/python` no tiene pytest
(el symlink apunta a `/usr/bin/python3` y el shebang de `../.venv/bin/pytest` apunta a una ruta
inexistente), así que usé el venv funcional `/dev/shm/t311`.

- `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_skill_cli_drift.py` → 2 passed
- `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_output_goldens.py` → 7 passed
- `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_operator_manual.py` → 1 passed

Los dos últimos tardan ~6-7 min cada uno porque el golden de ayuda lanza ~293 invocaciones del CLI
y el manual ejecuta todos sus bloques; no hubo cuelgues ni fallos.

# Done When

1. `grep -rn 'inbox-to-drawer' .claude docs desk/rituals`: todas las menciones son advertencias
   (SKILL.md, vocabulary.md, deskops-cli.md, operator-manual.md, faq.md, deskops-ui.md) o
   ejemplos runnable permitidos de la mecánica del comando (operator-manual.md:448,468 y
   faq.md:121, precedidos por la advertencia). Las dos que fallaban en el intento 1
   (`docs/faq.md:53` y `docs/deskops-ui.md:237`) ya advierten que promote borra la nota y no es
   el camino para notas que son trabajo.
2. El ritual `desk/rituals/ritual-drawer-triage.md` tiene el paso 1 nuevo:
   "Capture repo-local deferred work directly in desk/drawer/tasks/. Inbox notes that are work
   become tasks with references to the note and then message ack; they do not go to the drawer."
3. El help real de `deskops promote inbox-to-drawer-task` coincide con
   `tests/fixtures/golden/help/deskops_promote_inbox-to-drawer-task.txt` y advierte que borra la
   nota de origen y que no es el camino para notas que son trabajo.
4. Los tres tests pasan.

Sin hallazgos bloqueantes.
