REFORMULACION

Propósito: que `queue run --all` no se detenga cuando un trabajo vuelve a `pending` por `retry_exit_codes`; debe saltearlo en esa corrida y seguir con los siguientes pendientes en orden, para que un `dispatch-reap` o `integrate` posterior corra aunque un ejecutor espere cupo. Resultado: `run_queue` modificado en `deskops/queue.py`, tests nuevos en `tests/test_queue.py`, `docs/operator-manual.md` (Host queue) y CHANGELOG actualizados, más commit con rutas y Task-Id. Repo: deskops (cwd `/mnt/ssd/proyectos/SLDB_1/deskops`). Límites: no cambian el JSON ni `retry_exit_codes`; sin `--all` se corre un solo trabajo; un fallo sigue deteniendo la cola; un trabajo ya en espera no se reintenta en la misma corrida, sin bucle.

AMBIGUEDADES

1. «Sin --all se corre un solo trabajo como hoy»: «como hoy» remite a la implementación actual, no descrita; obligaría a inventar el comportamiento vigente.
2. «imprime 'en espera: <A> ocupado (exit 3)'»: no fija stream ni formato exacto (¿stdout/stderr?, ¿nombre o id?); obligaría a inventar una salida verificable.
3. «el hook encola al final»: no identifica qué hook ni si su orden es requisito; obligaría a inventar el mecanismo.
4. «commit con rutas nombradas y Task-Id»: no define el valor del Task-Id ni el formato; obligaría a inventar la convención.

DRY-RUN

Lecturas: `deskops/queue.py` (`run_queue`), `tests/test_queue.py`, `docs/operator-manual.md` (Host queue), CHANGELOG. Cambios previstos: conjunto de ids salteados por corrida en `run_queue`; con `--all`, saltar el trabajo que vuelve a pending por `retry_exit_codes` y continuar con el siguiente; mensaje de espera; sin `--all`, un solo trabajo; fallo detiene. Tests: primero el que falla (A exit 3 con retry [3], B y C exit 0 → A pending attempts 1, B/C done, retorno 0, mensaje); segundo, todos en espera termina sin bucle. Docs y CHANGELOG. Dependencias: semántica existente de `retry_exit_codes` y JSON sin cambios. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py`; suite completa por integrate.

FUTURO

El nodo `integrate` ejecuta la suite completa; un humano decide la aprobación o merge del commit.
