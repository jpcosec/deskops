# Result
run_id: exec-deskops-e-f585f0ef0e37
session: n/a (sesion del ejecutor claude en scion)
session_sha256: n/a

Cambio: run_queue con --all salta el trabajo que vuelve a pending por retry_exit_codes (conjunto `waiting` por corrida) y sigue con los siguientes; sin --all corre uno solo; un fallo sigue deteniendo la cola; si todo queda en espera termina sin bucle.

Archivos: deskops/queue.py, tests/test_queue.py, docs/operator-manual.md, CHANGELOG.md
Tests nuevos: test_retry_job_is_skipped_and_queue_continues, test_all_waiting_jobs_end_run_without_loop.
Validacion: tests/test_queue.py 18 passed (validation.log). No corri el test fallando antes del cambio. Suite completa: la corre integrate.
