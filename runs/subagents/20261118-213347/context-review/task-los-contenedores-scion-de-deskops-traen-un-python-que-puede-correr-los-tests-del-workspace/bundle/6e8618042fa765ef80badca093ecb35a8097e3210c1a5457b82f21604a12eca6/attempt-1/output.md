## REFORMULACION

**Propósito:** que un ejecutor despachado por scion pueda correr los tests del workspace sin improvisar `PYTHONPATH`, porque las imágenes scion-claude/scion-pi traen python 3.13 y el `.venv` apunta a 3.12. **Resultado:** una vía elegida e implementada —(a) paso de arranque en el template de `scion.py` que crea un venv desde el pyproject y lo pone primero en PATH, o (b) imágenes con python 3.12 en `/usr/bin/python3.12`—, con medición, test, manual, atom e informe. **Repo:** deskops; `deskops/runtime/scion.py`, `tests/test_scion_runtime.py`, `docs/operator-manual.md` y, solo para (b), un Dockerfile derivado. **Límites:** no se toca el código de scion; (b) solo si (a) falla o tarda más de 3 min; la imagen no se construye, el comando `docker build` queda para el integrador.

## AMBIGUEDADES

1. «las imágenes traen python 3.12 en la misma ruta…» frente a «un Dockerfile… FROM ghcr.io/jpruizantonia/scion-claude:latest». Obliga a inventar si (b) modifica las imágenes existentes o publica una derivada, su nombre/registro y si incluye scion-pi.
2. «más /mnt/ssd/herramientas/sldb cuando la tarea no es de sldb». Obliga a inventar cómo se detecta que la tarea no es de sldb y si las dos instalaciones `-e` se solapan.
3. «Si el template… admite un comando o hook de inicio… usar eso». Obliga a inventar qué hook ofrece la versión instalada de scion y en qué campo de `scion-agent.yaml` se declara.
4. «tarda más de 3 min». Obliga a inventar qué se cronometra (¿todo p1 o solo el arranque?) y qué hacer cerca del umbral.
5. «commitea su código con rutas nombradas y Task-Id, como dice su RoleDoc». Obliga a inventar el formato del mensaje, porque el RoleDoc no está en el input.

## DRY-RUN

**Lecturas:** TaskDoc y átomo; `scion.py`; tests; manual; `pyproject.toml` y `pyvenv.cfg`; `scion-agent.yaml` generado; versión de scion y hooks. **Cambios previstos:** medir en el contenedor (`uv venv /tmp/ws-venv --python 3.12`; `uv pip install -e …`; `pytest test_dispatch.py`) y anotar tiempos; según resultado, añadir el paso de arranque en `scion.py` o crear el Dockerfile; test nuevo; sección del manual; atom; `result-summary.md`. **Dependencias:** scion, uv, red, workspace y sldb montados, TMPDIR escribible. **Validaciones futuras:** `pytest test_scion_runtime.py`; en contenedor nuevo, `pytest tests/test_dispatch.py`; closeout con rutas y Task-Id.

## FUTURO

El integrador construye y decide publicar la imagen si se elige (b); el tester verifica la evidencia; el coordinador cierra; el owner decide la política de imágenes si la medición no concluye. El contenedor nuevo produce la salida de `test_dispatch`. Actualizar el `.venv` del host queda fuera.
