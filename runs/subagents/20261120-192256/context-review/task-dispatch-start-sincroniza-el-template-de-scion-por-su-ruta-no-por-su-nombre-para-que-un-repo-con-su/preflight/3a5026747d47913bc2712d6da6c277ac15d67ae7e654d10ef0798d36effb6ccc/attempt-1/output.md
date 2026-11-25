REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: que `dispatch start` sincronice el template de scion por la ruta absoluta del directorio recién escrito, no por el nombre del rol, para que funcione en un desk con `.scion` propio (IR). Resultado: cambio en `deskops/dispatch.py` (start), test nuevo en `tests/test_dispatch.py` que simula un desk con `.scion/settings.yaml` propio, entrada en CHANGELOG y commit con trailer Task-Id. Repo: deskops (cwd). Límites: no borrar ni modificar `IR/.scion`; el resto queda fuera de alcance.

AMBIGUEDADES

1. «cerca de la línea 297» — no fija el punto exacto; obliga a localizar `target` por inspección.
2. «se corrige igual o se corre con un cwd sin grove local, y se informa» — no da criterio de elección ni destino del informe; obliga a decidir e inventar dónde reportar.
3. «verificar con 'scion start --help' si acepta ruta o si hace falta cwd» — depende de una CLI externa cuyo comportamiento no está en el input; obliga a asumirlo.
4. «con _scion simulado» — no define el mecanismo de simulación; obliga a inventar el fixture.
5. «trailer Task-Id» — no indica formato ni valor; obliga a deducirlo.

DRY-RUN

Lecturas: TaskDoc, `deskops/dispatch.py` (bloque start, `target`, `scion_start_argv`), `tests/test_dispatch.py`, CHANGELOG y salidas de `scion templates sync --help` y `scion start --help`. Cambios previstos: añadir test que falla (sync recibe ruta absoluta con `.scion` local), cambiar el argv de sync, ajustar `scion_start_argv`/cwd si procede, CHANGELOG y commit `git commit -- <rutas>` con Task-Id. Dependencias: scion CLI, pytest, git. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`. Sin ejecutar.

FUTURO

El integrador relanza el dispatch de la tarea de IR y confirma que el sync no falla; un humano decide la alternativa (ruta frente a cwd) si `scion start` no acepta ruta y valida que `IR/.scion` queda intacto.
