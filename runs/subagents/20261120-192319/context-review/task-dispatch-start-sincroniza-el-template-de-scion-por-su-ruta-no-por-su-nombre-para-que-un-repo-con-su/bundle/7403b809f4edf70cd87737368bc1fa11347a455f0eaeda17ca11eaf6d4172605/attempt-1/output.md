## REFORMULACION

El encargo es corregir `dispatch start` en el repo `deskops` para que sincronice el template de scion mediante la ruta absoluta del directorio recién escrito —la variable `target` de `deskops/dispatch.py`, cerca de la línea 297— y no por el nombre del rol, de modo que funcione tanto en desks con `.scion` propio, como IR, como sin él. El resultado esperado incluye un test en `tests/test_dispatch.py` que verifique que `sync` recibe la ruta, la revisión de `scion_start_argv` por si también resuelve por nombre, y `CHANGELOG`. Límites: no borrar ni modificar `IR/.scion`; el alcance son `deskops/dispatch.py`, `tests/test_dispatch.py` y `CHANGELOG`.

## AMBIGUEDADES

1. «Si scion start también resuelve el template por nombre en el grove local, se corrige igual o se corre con un cwd sin grove local, y se informa.» Obliga a inventar qué alternativa elegir, qué significa «se informa» y dónde.
2. «con un desk que tiene .scion/settings.yaml propio, con _scion simulado» no define `_scion`; obliga a inventar el fixture y cómo simula el CLI.
3. «cerca de la línea 297» obliga a asumir la ubicación exacta de `target` y que no hay otras llamadas relevantes.
4. «scion acepta según 'scion templates sync --help'» no incluye la salida ni la versión; obliga a inventar el contrato CLI si no se relee.

## DRY-RUN

Lecturas previstas: TaskDoc, `deskops/dispatch.py` en `start` y `scion_start_argv`, `tests/test_dispatch.py`, `CHANGELOG`, y ayuda de `scion templates sync`/`scion start`. Cambios previstos: añadir test que falle primero con `.scion/settings.yaml` local y verifique que `sync` recibe la ruta absoluta; cambiar el argv de `sync`; ajustar `scion_start_argv` o su cwd si procede; actualizar `CHANGELOG`; commit con trailer `Task-Id`. Dependencias: pytest, git, fixtures existentes y semántica real de scion. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py` y relanzamiento del dispatch de IR. No se ejecuta nada.

## FUTURO

El integrador relanza el dispatch de la tarea de IR y confirma que `sync` no falla. Un humano decide la alternativa para `scion start` si ambas son viables y valida el cierre.
