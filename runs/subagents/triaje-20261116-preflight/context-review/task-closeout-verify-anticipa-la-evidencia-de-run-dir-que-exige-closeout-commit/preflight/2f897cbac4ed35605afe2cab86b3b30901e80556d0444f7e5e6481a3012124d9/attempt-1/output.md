## REFORMULACION

Encargo ejecutable (`task.code`): en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, hacer que `deskops closeout verify --task <id> --run-dir <dir>` acepte `--run-dir` opcional y, cuando se pase, devuelva `ok:false` por cada archivo de `REQUIRED_EVIDENCE` ausente en ese run-dir, con el mismo texto que usa `closeout commit`. Sin `--run-dir`, verify debe comportarse igual que hoy. Resultado observable: verify detecta run-dir incompleto, commit y verify comparten helper, y pasan los tests listados. Límites: no cambiar qué evidencia exige commit ni el formato del JSON fuera del nuevo hallazgo.

## AMBIGUEDADES

1. «tests/fixtures/golden (el golden de ayuda de closeout verify)»: no identifica ruta ni nombre de archivo; obligaría a inventar cuál golden actualizar.
2. «con el mismo texto que usa commit»: no transcribe la cadena exacta (¿basename, ruta completa, prefijo?). Aunque el código la contiene, el input no la fija.
3. «alrededor de las lineas 83-86», «alrededor de la linea 104», «539-543», «843»: referencias aproximadas; obligarían a asumir que la numeración actual coincide.
4. «sin fallas nuevas respecto de main»: no define cómo obtener/verificar la baseline de main; obligaría a inventar el criterio de comparación.
5. Átomo `atom-cli-mutation-testing-uses-sandbox-desk-roots` sin validación asociada: no queda claro si exige pruebas de mutación con sandbox.

## DRY-RUN

Lecturas previstas: `deskops/cli/commands/closeout.py` (parser de verify), `deskops/services/closure.py` (`REQUIRED_EVIDENCE`, chequeo de commit, `verify_task_closeout`), `tests/test_output_goldens.py`, golden de ayuda, `tests/test_closeout_declared_evidence.py`. Cambios: extraer `missing_run_evidence(run_dir)`; reutilizar en commit sin cambio; en verify si llega `run_dir`; añadir `--run-dir` al parser; actualizar golden; añadir tres casos de test. Dependencias: `../.venv`, `TMPDIR=/dev/shm`, fixtures de run-dir. Validaciones futuras: los cinco pytest indicados, incluida suite completa con `-n 4`. Sin ejecución.

## FUTURO

Otro nodo implementa y ejecuta los tests; un humano aprueba el cambio de contrato CLI/golden. El cierre formal (`closeout commit --run-dir`) corresponde a un nodo posterior, no a esta revisión.
