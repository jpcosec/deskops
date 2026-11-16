# Result summary — exec-deskops-e-a6a9943b2333

- run_id: run-deskops-e-a6a9943b2333
- task: task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit
- session: scion://agent/deskops-e-a6a9943b2333 (agente claude; session_sha256 no disponible desde dentro de la sesión)

## Qué cambié

- `deskops/services/closure.py`: helper `ClosureService.missing_run_evidence(run_dir) -> list[str]` (classmethod sobre `REQUIRED_EVIDENCE`), `missing_run_evidence_message(run_dir, missing)` con el texto exacto `Missing required evidence in <run_dir>: <a, b>`, y `_resolve_run_dir` (resolución relativa a root que ya hacía commit). `close_with_run` (commit) los usa sin cambio de comportamiento. `verify_task_closeout` acepta `run_dir=None`; con run_dir, si faltan archivos agrega el hallazgo `{"code": "missing_run_evidence", "message": <mismo texto>}` a `findings` y pone `ok: false`. Sin run_dir, nada cambia (el resto del reporte JSON intacto; `declared`/`found`/`gates` no se tocan).
- `deskops/cli/commands/closeout.py`: `_verify` pasa `args.run_dir` a `verify_task_closeout`.
- `deskops/cli/registry.py` (**fuera de `files`**): el parser de `closeout verify` vive aquí, no en closeout.py (el scope lo ubicaba "en closeout.py alrededor de 83-86", que es el handler). Agregué el argumento opcional `--run-dir` y un párrafo en el epílogo. Sin esto el goal no es implementable.
- `tests/fixtures/golden/help/deskops_closeout_verify.txt`: regenerado solo ese golden (con `COLUMNS=80 PYTHONPATH=$PWD python -m deskops closeout verify --help`, igual que lo genera el test). No corrí `--update-golden`; ningún otro golden cambió.
- `tests/test_closeout_declared_evidence.py`: 4 tests nuevos (desk sandbox tmp_path vía fixture `repo`):
  - run-dir sin task.txt → verify rc=1, ok:false, hallazgo `missing_run_evidence` nombrando task.txt; `closeout commit --run-dir` con ese mismo dir falla con el mismo texto exacto y no commitea.
  - run-dir completo → ok:true, findings vacíos.
  - sin --run-dir (con un run-dir vacío presente) → ok:true, sin hallazgo `missing_run_evidence`.
  - el helper devuelve los faltantes en orden y commit y verify lo llaman ambos.

## Validación (ver validation.log)

- tests/test_closeout_declared_evidence.py: 23 passed, rc=0
- tests/test_closeout.py: 59 passed, rc=0
- tests/test_output_goldens.py: 7 passed, rc=0
- tests/test_cli_help_examples.py: 13 passed, rc=0
- Suite completa (`pytest -n 4 -q tests` + comparación con origin/main): **para el integrador** (no corrida, por orden del brief).

## Riesgo de entorno (importante para el integrador)

El venv `../.venv` tiene `deskops` instalado en modo editable desde **/mnt/ssd/herramientas/deskops** (otro checkout de opsys). Los tests que lanzan `python -m deskops` por subprocess con `cwd=<tmp_path>` (p.ej. test_closeout_declared_evidence.py) importan ese checkout, no este árbol, salvo que haya `PYTHONPATH`. Por eso corrí la validación con `PYTHONPATH=$PWD`; sin ella, los 2 tests nuevos de CLI fallan con `unrecognized arguments: --run-dir` (lo vi en el primer intento). test_output_goldens.py ya inyecta PYTHONPATH por sí mismo. El integrador debe correr con PYTHONPATH apuntando al árbol (o reinstalar) para que la validación pruebe este código.

## Otros riesgos

- `closeout commit` no pasa run_dir a verify: sigue chequeando su evidencia en `close_with_run` como antes (sin cambio de comportamiento, como pide el scope).
- Los archivos `.sldb/` y `runs/subagents/*` sucios en git status no son míos (estaban al iniciar).
- `desk/tasks/Board.md`, la tarea nueva `task-deskops-atoms-citations-queda-declarado-...` y los `.sldb/` de BoardDoc/TaskCodeDoc aparecieron durante la sesión por otras sesiones; no los toqué. Mis archivos: los 6 listados en "Qué cambié".
