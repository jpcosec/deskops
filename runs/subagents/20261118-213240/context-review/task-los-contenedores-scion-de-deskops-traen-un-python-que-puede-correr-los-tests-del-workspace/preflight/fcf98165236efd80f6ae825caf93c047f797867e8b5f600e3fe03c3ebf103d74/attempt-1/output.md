## REFORMULACION

Nodo ejecutable (`task.code`) del repo **deskops**. Propósito: evitar que ejecutores y testers despachados por scion improvisen entornos Python porque el `.venv` del workspace apunta a Python 3.12 y las imágenes solo traen 3.13. Resultado: una de dos vías implementada y documentada en el manual del operador: (a) paso de arranque en el template scion que crea un venv propio desde el `pyproject` del workspace y lo pone primero en `PATH`, o (b) imágenes con Python 3.12 en la ruta que espera el entorno. Debe medirse viabilidad, registrarse la decisión en un atom y dejar informe. Límites: no modificar código de scion; no construir la imagen (solo dejar el comando); trabajar en el checkout principal.

## AMBIGUEDADES

1. Cita: “solo si a falla o tarda más de 3 min”. No define qué se cronometra exactamente (creación del venv, instalación editable, pytest o el conjunto), ni qué significa “falla”; obliga a inventar el criterio.
2. Cita: “- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py”. No indica qué intérprete usar (host, `.venv` del workspace o venv del contenedor); obliga a inventarlo.
3. Cita: “El repo a instalar es la raíz de la tarea (--root) con su extra dev, más /mnt/ssd/herramientas/sldb cuando la tarea no es de sldb”. No define cómo obtener `--root` ni cómo decidir si la tarea “es de sldb”; obliga a asumir.
4. Cita: “commitea su código con rutas nombradas y Task-Id, como dice su RoleDoc”. El RoleDoc no está en el input; obliga a inventar formato de commit.
5. Cita: “medir cual es viable con la version de scion instalada”. No indica cómo medir la versión instalada ni la viabilidad de (b); p1 solo describe la medición de (a).

## DRY-RUN

Lecturas: `deskops/runtime/scion.py`, `tests/test_scion_runtime.py`, `tests/test_dispatch.py`, `docs/operator-manual.md`, `pyproject.toml`, `.bootstrap/ir-scion-env.yaml` y código/documentación de scion sobre template y hooks. Cambios previstos: paso de arranque en `scion.py` o bloque en `prompt.md`; test; manual; atom; `result-summary.md`; `Dockerfile` solo si se elige (b). Dependencias: `uv`, descarga de Python 3.12, scion instalado, red y build externo de Docker. Validaciones futuras: medición cronometrada, pytest de `test_scion_runtime.py` y ejecución de `test_dispatch.py` en contenedor despachado.

## FUTURO

El integrador construye la imagen si se elige (b). El operador aplica el manual. Otro nodo o humano valida el atom y la decisión.
