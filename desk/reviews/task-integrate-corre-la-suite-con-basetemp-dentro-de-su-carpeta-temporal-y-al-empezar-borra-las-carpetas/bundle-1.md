---
sldb:
  by: agent
  at: '2026-11-24T18:06:33Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas@sha256:405d06862240cfa1110fd232b161f017102676154df583a5a34d5685600d8ebe
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261123-044846/context-review/task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas/bundle/08ebd42818beace515dbe76db428d559eb6542b92cddeef491de5bd38badcc21/attempt-1
input_sha256: 08ebd42818beace515dbe76db428d559eb6542b92cddeef491de5bd38badcc21
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 73e5aa684b7d8dd65387aafee886be8dc3e190e8c9a7aa7557e868c0ece58ddd
output_sha256: ceafe0f31afef6a6a08af1a2664d322b876446dfc74305a0b09746f0127cd28d
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del bundle (hechos del repo; ver base comun al final):

  1) Ubicacion de la limpieza: _run_suite pasa a _run_suite(cfg, copy, log_path, work)
  (hoy linea 195, no recibe work); la llamada de la linea 319 en _steps pasa work.
  Dentro del with _suite_lock(cfg.tests_lock) (linea 199) y antes del Popen se llama
  la funcion nueva _clean_stale_work_dirs(work, cfg.suite_timeout) -> list[Path],
  definida en deskops/integrate.py.

  2) owner.pid: texto decimal con salto de linea, f"{os.getpid()}\n", escrito por
  _steps justo despues de mkdtemp (lineas 303-304); tambien en --dry-run porque work
  se crea igual.

  3) owner.pid vacio, ilegible o no numerico = sin owner.pid (aplica la regla de mtime
  > cfg.suite_timeout). PermissionError de os.kill cuenta como vivo; solo ProcessLookupError
  es muerto.

  4) Orden en PYTEST_ADDOPTS: lo previo primero y --basetemp al final: env["PYTEST_ADDOPTS"]
  = (previo + " " if previo else "") + f"--basetemp={work / ''pytest''}". Asi --basetemp
  gana si el previo ya traia otro.

  5) La limpieza solo corre cuando corre la suite (rango que toca codigo, lineas 318-319);
  en rangos solo-desk no hay suite ni limpieza; si falla antes de la suite tampoco.
  Es lo que dice el Goal ("Al empezar la suite").

  6) API para el test: test_stale_integrate_dirs_are_removed_under_the_lock llama
  directo a _clean_stale_work_dirs(own, max_age) con monkeypatch.setattr(tempfile,
  "tempdir", str(tmp_path)) y crea las carpetas a/b/c y la propia en tmp_path; el
  "under the lock" lo garantiza el sitio de la llamada (dentro de _suite_lock). Pid
  muerto: el de un subprocess.run(["true"]) ya terminado. test_suite_gets_basetemp_inside_work
  va por el CLI: _configure(root, suite=["sh", "-c", f''echo "$PYTEST_ADDOPTS" > {probe}''])
  con probe = tmp_path / "addopts.txt", y _integrate_env(root, {"PYTEST_ADDOPTS":
  "-p no:cacheprovider"}).

  Commit desde el worktree que dispatch le da al ejecutor, con git commit -- deskops/integrate.py
  tests/test_integrate.py y el trailer en el cuerpo:

  Task-Id: task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas


  Base comun: Hechos verificados en deskops/integrate.py (HEAD 40964f50): _suite_lock
  linea 181, _run_suite(cfg, copy, log_path) linea 195 (toma el lock en la linea 199
  y lanza cfg.suite con Popen), integrate() linea 258 con el finally que borra temps
  en la linea 283, _steps linea 292 con work = Path(tempfile.mkdtemp(prefix="deskops-integrate-"))
  en la linea 303 y temps.append(work) en la 304; _run_suite se llama en la linea
  319 solo si el rango toca codigo. IntegrateConfig (deskops/config.py): suite_timeout
  int, default 5400; tests_lock str|None. Los tests de tests/test_integrate.py corren
  el CLI en subproceso con _cli (linea 28), _configure (linea 43), _integrate (linea
  130, TMPDIR=root.parent/tmpdir) e _integrate_env (linea 518, acepta env extra).
  Modelo a seguir: test_suite_runs_under_the_declared_lock_with_pythonpath_of_the_copy
  (linea 231).'
# ISO 8601 timestamp
created_at: '2026-11-23T04:49:10.447374+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:02:46.512479+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-044846/context-review/task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas/bundle/08ebd42818beace515dbe76db428d559eb6542b92cddeef491de5bd38badcc21/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del bundle (hechos del repo; ver base comun al final):
1) Ubicacion de la limpieza: _run_suite pasa a _run_suite(cfg, copy, log_path, work) (hoy linea 195, no recibe work); la llamada de la linea 319 en _steps pasa work. Dentro del with _suite_lock(cfg.tests_lock) (linea 199) y antes del Popen se llama la funcion nueva _clean_stale_work_dirs(work, cfg.suite_timeout) -> list[Path], definida en deskops/integrate.py.
2) owner.pid: texto decimal con salto de linea, f"{os.getpid()}\n", escrito por _steps justo despues de mkdtemp (lineas 303-304); tambien en --dry-run porque work se crea igual.
3) owner.pid vacio, ilegible o no numerico = sin owner.pid (aplica la regla de mtime > cfg.suite_timeout). PermissionError de os.kill cuenta como vivo; solo ProcessLookupError es muerto.
4) Orden en PYTEST_ADDOPTS: lo previo primero y --basetemp al final: env["PYTEST_ADDOPTS"] = (previo + " " if previo else "") + f"--basetemp={work / 'pytest'}". Asi --basetemp gana si el previo ya traia otro.
5) La limpieza solo corre cuando corre la suite (rango que toca codigo, lineas 318-319); en rangos solo-desk no hay suite ni limpieza; si falla antes de la suite tampoco. Es lo que dice el Goal ("Al empezar la suite").
6) API para el test: test_stale_integrate_dirs_are_removed_under_the_lock llama directo a _clean_stale_work_dirs(own, max_age) con monkeypatch.setattr(tempfile, "tempdir", str(tmp_path)) y crea las carpetas a/b/c y la propia en tmp_path; el "under the lock" lo garantiza el sitio de la llamada (dentro de _suite_lock). Pid muerto: el de un subprocess.run(["true"]) ya terminado. test_suite_gets_basetemp_inside_work va por el CLI: _configure(root, suite=["sh", "-c", f'echo "$PYTEST_ADDOPTS" > {probe}']) con probe = tmp_path / "addopts.txt", y _integrate_env(root, {"PYTEST_ADDOPTS": "-p no:cacheprovider"}).
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- deskops/integrate.py tests/test_integrate.py y el trailer en el cuerpo:
Task-Id: task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas

Base comun: Hechos verificados en deskops/integrate.py (HEAD 40964f50): _suite_lock linea 181, _run_suite(cfg, copy, log_path) linea 195 (toma el lock en la linea 199 y lanza cfg.suite con Popen), integrate() linea 258 con el finally que borra temps en la linea 283, _steps linea 292 con work = Path(tempfile.mkdtemp(prefix="deskops-integrate-")) en la linea 303 y temps.append(work) en la 304; _run_suite se llama en la linea 319 solo si el rango toca codigo. IntegrateConfig (deskops/config.py): suite_timeout int, default 5400; tests_lock str|None. Los tests de tests/test_integrate.py corren el CLI en subproceso con _cli (linea 28), _configure (linea 43), _integrate (linea 130, TMPDIR=root.parent/tmpdir) e _integrate_env (linea 518, acepta env extra). Modelo a seguir: test_suite_runs_under_the_declared_lock_with_pythonpath_of_the_copy (linea 231).
