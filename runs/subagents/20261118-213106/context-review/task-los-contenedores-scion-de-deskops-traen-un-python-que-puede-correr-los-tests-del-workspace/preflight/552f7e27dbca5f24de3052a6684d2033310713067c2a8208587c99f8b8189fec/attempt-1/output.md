## REFORMULACION

El encargo es resolver que los contenedores scion de deskops no pueden usar el `.venv` del workspace y que los ejecutores improvisan entornos. Debe medirse la viabilidad de dos vías, elegir una, implementarla y documentarla. Resultado observable: un ejecutor despachado corre los tests del workspace dentro del contenedor sin improvisar entorno; la decisión y medición quedan en un atom y en el manual. Repo: deskops (`/mnt/ssd/proyectos/SLDB_1/deskops`), principalmente `deskops/runtime/scion.py`, sus tests y el manual; opcionalmente el build de imagen si se elige (b). Límites: no cambiar código de scion; trabajar en el checkout principal; commits con rutas nombradas y Task-Id; build de imagen solo si (b). Secuencia: medir ambas vías en contenedor con el `--config` de dispatch; preferir (a) si arranca en menos de 3 minutos; implementar con test; documentar y registrar atom; informe con tiempos.

## AMBIGUEDADES

1. “lanzado con el mismo --config que usa dispatch (/mnt/ssd/proyectos/SLDB_1/.bootstrap/ir-scion-env.yaml)”: no da comando, imagen/tag, montajes ni forma de entrar al contenedor; obliga a inventar la invocación.
2. “uv pip install -e <repo>[dev] del repo de la tarea”: no identifica repo ni extras; obliga a inventar si es SLDB_1 o deskops y qué dependencias instalar.
3. “un paso de arranque del template (hook pre-start del harness o comando de inicio)”: no indica cuál soporta la versión instalada ni su API; obliga a inventar el mecanismo.
4. “documentar en el manual (sección de dispatch)”: no da ruta ni nombre del manual; obliga a inventar el archivo.
5. “registrar la decisión y la medición en un atom (deskops add atom)”: no da id, título ni campos; obliga a inventar metadatos.
6. “el archivo de build de imagen”: no da Dockerfile, ruta ni imagen base; obliga a inventar el artefacto si se elige (b).

## DRY-RUN

Nodo ejecutable (`task.code`), no agregado. Lecturas: TaskDoc, `scion.py`, `tests/test_scion_runtime.py`, manual, `pyvenv.cfg`, `pyproject.toml`, `ir-scion-env.yaml` y build de imagen si aplica. Cambios previstos: mediciones en contenedor (p1), decisión (p2), edición de `scion.py` y test (p3), manual y atom (p4), informe (p5). Dependencias: imagen scion-claude, CLI/config de scion, docker/podman, uv/red para descargar 3.12, workspace montado. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py`; en contenedor despachado, `python -m pytest -q tests/test_dispatch.py`; revisión de diff, commit, atom y manual. Nada se ejecuta aquí.

## FUTURO

La ejecución y las mediciones las produce el nodo ejecutor; no hay nodos hijos. Un humano o revisor decide la aceptación y, si se elige (b), autoriza el build de imagen; dispatch/infraestructura provee imagen y configuración.
