## REFORMULACION

Añadir a deskops una cola de trabajos pesados ejecutada en el host: `DeskConfig` gana `queue_jobs`, `queue_min_available_gb` y `queue_max_psi_avg60`; un módulo nuevo `queue.py` y el grupo `deskops queue` (`add`, `run`, `list`) operan sobre `runs/queue/{pending,running,done,failed,logs}`, con cerrojo `flock`, gates de memoria/PSI, timeout, log por trabajo y nota `unclear` al inbox si falla; el manual gana `Host queue`. Repo: checkout principal de deskops. Límites: sin servicio ni timer, sin lanzar agentes/suites/push, sin declarar hooks en desks reales, sin tocar los archivos ya modificados listados, sin `git add`/`git commit`, sin registrar `runs/queue` en el store.

## AMBIGUEDADES

1. Cierre: el Scope dice «sin `git add` ni `git commit`», pero el átomo ligado exige que «el cambio completado se registra en un commit descriptivo de git». Obliga a inventar si la tarea se cierra sin commit o si el átomo se exceptúa.
2. Raíz: «se lee de `desk/config.json`» y «Vive en la carpeta `runs/queue` del repo», con comandos `deskops queue add ... --root .`. Obliga a inventar si `--root` es la raíz del repositorio o la carpeta `desk/`.
3. Interrumpidos: «se mueve a `failed` con `exit_code: null` y `interrupted: true` antes del paso (b), con su nota», mientras la nota del paso (f) lleva «el tipo, la tarea, el codigo de salida y la ruta del log». Un interrumpido no tiene código ni log. Obliga a inventar el cuerpo de esa nota.

## DRY-RUN

Lecturas: `deskops/config.py`, `deskops/cli/registry.py` y grupos vecinos, `deskops/cli/commands/message.py` (función de envío), tests vecinos de CLI y `tests/test_lifecycle_graph.py`, `docs/operator-manual.md`. Cambios previstos: tres campos en `DeskConfig`; `deskops/queue.py` con encolar, correr y listar; registro del grupo; `tests/test_queue.py`; sección `Host queue`. Dependencias: `fcntl`, `/proc/meminfo`, `/proc/pressure/memory`, `subprocess.run`, pydantic y la función de nota del inbox. Validaciones futuras: los diez casos (a)–(j), `test_lifecycle_graph.py`, las tres ayudas y `graph missing`.

## FUTURO

Quién invoca `queue run` (host, timer externo) y qué tarea consumirá la cola para suites y push; la decisión sobre el commit de cierre; y la declaración real de `queue_jobs`/hooks en desks reales.
