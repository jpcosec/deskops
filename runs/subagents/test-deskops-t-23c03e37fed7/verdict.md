# Veredicto del tester deskops-t-23c03e37fed7

Tarea: task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit
Entrega: exec-deskops-e-a6a9943b2333 (sin commitear). Evidencia completa en validation.log.

## Contrato contra diff

- Goal: `closeout verify --run-dir` reporta cada archivo de REQUIRED_EVIDENCE que falta, con `ok:false` y el mismo texto que commit. Cumple: `deskops/services/closure.py` en `verify_task_closeout` (bloque `if run_dir is not None`) agrega el hallazgo `{"code": "missing_run_evidence", "message": ...}` armado por `missing_run_evidence_message`, el mismo helper que usa `close_with_run`.
- Sin --run-dir nada cambia: `run_dir=None` por defecto y el bloque nuevo no corre. Cumple.
- Commit sigue igual: `close_with_run` solo pasa a usar `_resolve_run_dir`, `missing_run_evidence` y `missing_run_evidence_message`, con la misma lógica y el mismo texto. Cumple.
- Implementation path (helper `missing_run_evidence(run_dir) -> list[str]` compartido): cumple, es un classmethod en ClosureService.
- Done when: verify con run-dir incompleto da ok:false y nombra task.txt (el test lo comprueba y además que commit falla con ese mismo texto exacto); commit y verify usan el mismo helper; los tests listados pasan.
- `deskops/cli/registry.py` (fuera de `files`): el cambio era necesario. El parser de `closeout verify` se declara ahí (`A("--task", ...)` en la entrada de closeout verify); `closeout.py:83-86` es solo el handler. Sin tocar registry.py, `--run-dir` no se puede agregar. El cambio se limita a un argumento opcional y a un párrafo del epílogo. Hay que declararlo en el informe de cierre o en los paths del commit.
- Golden: solo cambió `tests/fixtures/golden/help/deskops_closeout_verify.txt` (`git status`/`git diff --stat` sobre tests/fixtures muestra 1 archivo), y coincide con el registro nuevo (test_output_goldens pasa).

## Validación (PYTHONPATH=$PWD, TMPDIR=/dev/shm, de a un archivo)

- test_closeout_declared_evidence.py: 23 passed
- test_closeout.py: 59 passed
- test_output_goldens.py: 7 passed
- test_cli_help_examples.py: en la primera corrida fallaron 2 tests (`add pill` y `add repository`, por un `ScannerError` de YAML en la línea 475 de algún documento que lee el CLI), sin relación con closeout. Corriendo `-k "pill or repository"` pasan en el checkout y en la copia de HEAD, y al repetir el archivo completo da 13 passed. Fue un fallo transitorio, probablemente por un archivo editado al mismo tiempo por otra sesión. No es de esta entrega.
- test_command_registry.py: 3 passed (closeout verify no es un comando nuevo).

## Reproducción contra HEAD

Copia en /dev/shm hecha con `git archive HEAD`, más el test nuevo, con PYTHONPATH apuntando a esa copia: 3 de los 4 tests nuevos fallan (`unrecognized arguments: --run-dir`; `ClosureService has no attribute 'missing_run_evidence'`). El cuarto (`test_verify_without_run_dir_ignores_run_evidence`) pasa en HEAD, como corresponde: es el test de no regresión. La copia está borrada.

## Riesgos y observaciones (no bloquean)

- `closure.py`, bloque nuevo de `verify_task_closeout`: con `--run-dir` inexistente o fuera de runs/subagents/, verify informa los 4 archivos como faltantes, mientras que commit rechaza antes con "Run dir not found" o "Run dir must live under runs/subagents/". El ok:false igual anticipa el rechazo de commit, aunque con otro texto. El scope no lo pedía.
- `test_commit_and_verify_share_the_run_evidence_helper` cuenta las apariciones literales de `self.missing_run_evidence(resolved_run_dir)` en el código fuente, así que es frágil ante un renombrado. Es aceptable como prueba del "mismo helper".
- El venv tiene deskops editable desde /mnt/ssd/herramientas/deskops. Sin PYTHONPATH, los tests de subproceso prueban ese otro checkout. El integrador debe correrlos con PYTHONPATH.
- La suite completa no la corrí (lo prohíbe el brief). Queda para el integrador.

VEREDICTO: APROBADO
