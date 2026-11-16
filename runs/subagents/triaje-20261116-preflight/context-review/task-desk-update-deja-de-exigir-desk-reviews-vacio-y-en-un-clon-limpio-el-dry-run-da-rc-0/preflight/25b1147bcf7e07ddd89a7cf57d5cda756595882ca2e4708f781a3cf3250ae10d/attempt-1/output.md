## REFORMULACION

El nodo debe modificar el repo `/mnt/ssd/proyectos/SLDB_1/deskops` para que `desk update` deje de considerar `desk/reviews/` como estructura faltante. El resultado esperado es que, tras `deskops init .`, commit y clon limpio, `deskops desk update --root <clon>` en dry-run devuelva rc 0, y que `desk/reviews/` se cree al escribir el primer recibo. Límites: tocar `deskops/cli/commands/desk.py`, el golden `tests/fixtures/golden/scaffold/update.json` si cambia y `tests/test_cli.py`; no agregar `.gitkeep`.

## AMBIGUEDADES

1. “Sigue hoy en deskops/cli/commands/desk.py:231-232.” No se cita el código exacto; obliga a inventar qué líneas o condición eliminar si la numeración cambió.
2. “el golden tests/fixtures/golden/scaffold/update.json si cambia” es condicional; obliga a inventar si el output cambia y cuál sería el golden correcto.
3. “Test en tests/test_cli.py con git init, init, commit, clone y desk update dry-run rc 0” no fija rama, rutas temporales, invocación exacta ni limpieza; obliga a inventar el arnés del test.
4. “sin fallas nuevas respecto de main” no define “main” (rama local, remota o commit base); obliga a inventar la referencia de comparación.

## DRY-RUN

Lecturas previstas: `deskops/cli/commands/desk.py`, `deskops/services/review.py`, `deskops/cli/commands/doctor.py`, `tests/test_cli.py`, `tests/test_output_goldens.py`, `tests/test_review_command.py` y el golden `update.json`. Cambios previstos: quitar el chequeo que reporta `desk/reviews/` como faltante; ajustar el golden solo si el output cambia; añadir un test que inicialice repo, haga commit, clone y verifique rc 0 en dry-run, y compruebe que el primer recibo crea la carpeta. Dependencias: Python del venv, pytest, git y directorios temporales. Validaciones futuras: ejecutar los cuatro comandos de `Validation`, incluida la suite completa, sin ejecutarlos ahora.

## FUTURO

Un nodo ejecutor aplicará los cambios y correrá las validaciones; el validador o CI confirmará rc 0 y ausencia de fallas nuevas. Un humano revisará el diff, el golden y el commit final.
