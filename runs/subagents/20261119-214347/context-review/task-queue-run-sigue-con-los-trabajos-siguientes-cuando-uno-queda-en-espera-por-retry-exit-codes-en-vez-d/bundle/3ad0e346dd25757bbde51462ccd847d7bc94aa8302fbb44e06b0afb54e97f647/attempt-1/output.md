## REFORMULACION

Encargo ejecutable (`task.code`, no agregado): modificar `run_queue` en `deskops/queue.py` para que, con `--all`, un trabajo que vuelve a `pending` por `retry_exit_codes` se saltee en esa corrida y la cola siga con los siguientes pendientes; sin `--all` se mantiene un solo trabajo; un fallo real sigue deteniendo la cola. Resultado: código, tests en `tests/test_queue.py`, `docs/operator-manual.md` (Host queue) y `CHANGELOG`. Repo: `deskops` (`/mnt/ssd/proyectos/SLDB_1/deskops`). Límites: no cambian el JSON ni `retry_exit_codes`; no debe haber bucle; un trabajo ya esperado no se reintenta hasta la próxima corrida.

## AMBIGUEDADES

1. «retorna 0 e imprime 'en espera: <A> ocupado (exit 3)'»: no queda claro si el retorno 0 se mantiene aunque A quede pendiente, ni el formato exacto del mensaje. Obligaría a inventar el contrato de salida y el texto.
2. «con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra»: el input no incluye esos artefactos ni el contenido de `queue.py`, `tests/test_queue.py`, docs o CHANGELOG. Obligaría a inventar su estado y APIs.
3. «B y C salen con 0»: no especifica si son ejecuciones simuladas del fixture o trabajos reales de la cola. Obligaría a decidir el diseño del test.

## DRY-RUN

Lecturas previstas: TaskDoc, `deskops/queue.py` (`run_queue`), `tests/test_queue.py`, `docs/operator-manual.md` (Host queue), `CHANGELOG` y artefactos enlazados si se aportan. Cambios previstos: conjunto de ids salteados por corrida; al detectar `retry_exit_codes`, dejar `pending`, incrementar `attempts`, emitir mensaje y continuar con `--all`; conservar el comportamiento sin `--all`; detener ante fallo. Tests: A sale con 3 y `retry_exit_codes [3]`, B y C con 0; verificar A `pending` con `attempts 1`, B/C `done`, retorno 0 y mensaje; segundo test con todos en espera sin bucle. Dependencias: semántica actual de `run_queue`, hook `dispatch-reap`, formato de salida. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py`; suite completa por `integrate`; commit con rutas nombradas y `Task-Id`. No se ejecuta nada.

## FUTURO

Otro nodo implementará p2–p4 y aportará los archivos enlazados; un humano o el Board decidirá el contrato exacto de retorno/mensaje si no se aclara; `integrate` validará la suite completa y el commit.
