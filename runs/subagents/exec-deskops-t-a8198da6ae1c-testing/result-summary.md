PASA

# Tester — task-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal-sin-wor

## Commit revisado

- Ejecutor: `16a95ba0cd7f3621355cfef0b219b8d0636d1015` ("Document desk-only changes rule in use-deskops skill and operator manual")
- Archivos del commit:
  - `.opencode/skills/use-deskops/SKILL.md`
  - `docs/operator-manual.md`
- Solo se añadieron 8 líneas (4 + 4), sin cambios de código.

## Verificación del contenido

`grep -n 'Desk-only changes go straight on the main checkout' .opencode/skills/use-deskops/SKILL.md docs/operator-manual.md` devuelve una línea por archivo:

- `.opencode/skills/use-deskops/SKILL.md:197`
- `docs/operator-manual.md:266`

El párrafo es idéntico en ambos archivos y coincide literalmente con el texto pedido en el Goal. En el manual queda como subsección `### Desk-only changes` al final de `## Desk scaffold, migration, and repair`, justo antes de `## Artifact commands`.

## Tests ejecutados

Se corrieron de a uno, con `TMPDIR=/tmp`:

- `tests/test_skill_cli_drift.py` → `2 passed`
- `tests/test_operator_manual.py` → `1 passed` (411.96 s)

## Nota de entorno (no imputable al ejecutor)

Los comandos de validación con `../.venv/bin/python -m pytest` no pueden ejecutarse en este host porque el venv compartido está roto: sus shebangs apuntan a `/home/robocop/...` (workspace reubicado) y su `python3` apunta a `/usr/bin/python3` (3.11.2), mientras los paquetes son de Python 3.12 (`No module named pytest`).

Para verificar los tests se creó un venv temporal con `uv` (Python 3.13.18) e instalación editable de este checkout y del `sldb` hermano:

- `/tmp/deskops-test-venv`

Con ese intérprete ambos tests pasan. El problema del venv es preexistente y ajeno al commit evaluado.

## Veredicto

PASA: la regla aparece en ambos archivos y los dos tests de validación pasan.
