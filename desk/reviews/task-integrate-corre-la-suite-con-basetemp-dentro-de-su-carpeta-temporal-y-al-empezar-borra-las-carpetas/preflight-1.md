---
sldb:
  by: agent
  at: '2026-11-23T05:02:36Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
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
run_dir: runs/subagents/20261123-044550/context-review/task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas/preflight/5c53eb6ec977833e7dc44eea50ede80d40de25cba99cf6574e99a24867a63ae9/attempt-1
input_sha256: 5c53eb6ec977833e7dc44eea50ede80d40de25cba99cf6574e99a24867a63ae9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 3e75f1263ae3a58e4a22ef4ed0e77cd3103d10e383bfc3d4b26f3b61467f97ef
output_sha256: f66931580ccd626000cf7bb6825b30b75c6741ccc0bc9b572101316dd96e5b7b
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones de la preflight (todas con hechos del repo; ver base
  comun al final):

  1) owner.pid: lo escribe _steps justo despues de mkdtemp (linea 303-304), antes
  del clone: (work / "owner.pid").write_text(f"{os.getpid()}\n"). Se escribe siempre
  que exista work, tambien en --dry-run. Como la limpieza corre despues (dentro de
  _run_suite), la propia ya tiene owner.pid y ademas se excluye por ruta.

  2) PermissionError de os.kill(pid, 0) cuenta como vivo (no se borra). Solo ProcessLookupError
  cuenta como muerto. owner.pid vacio, ilegible o no numerico se trata como "sin owner.pid"
  (aplica la regla de mtime).

  3) La carpeta propia se identifica por ruta: se omite toda carpeta cuyo Path.resolve()
  sea igual a work.resolve().

  4) Funcion nueva en deskops/integrate.py: _clean_stale_work_dirs(own: Path, max_age:
  int) -> list[Path]. Recorre Path(tempfile.gettempdir()).glob("deskops-integrate-*")
  (solo directorios), borra con shutil.rmtree(..., ignore_errors=True) y devuelve
  las borradas. _run_suite pasa a _run_suite(cfg, copy, log_path, work) y, dentro
  del with _suite_lock(cfg.tests_lock) y antes del Popen, llama _clean_stale_work_dirs(work,
  cfg.suite_timeout). La llamada de la linea 319 pasa work.

  5) Canal y formato: print(f"limpieza: {ruta}") a stdout (como el resto de mensajes
  de integrate), una linea por carpeta, ruta absoluta tal como la da glob sobre gettempdir().

  6) <archivo> del test: probe = tmp_path / "addopts.txt"; la suite falsa es ["sh",
  "-c", f''echo "$PYTEST_ADDOPTS" > {probe}''] configurada con _configure(root, suite=...),
  y se corre con _integrate_env(root, {"PYTEST_ADDOPTS": "-p no:cacheprovider"}).
  Se asierta rc 0 y que el contenido es "-p no:cacheprovider --basetemp=<tmpdir>/deskops-integrate-XXXX/pytest"
  (lo previo primero, un espacio, luego --basetemp; el prefijo es root.parent / "tmpdir").
  El test de limpieza es unitario sobre _clean_stale_work_dirs: monkeypatch.setattr(tempfile,
  "tempdir", str(tmp_path)); pid muerto = pid de un subprocess.run(["true"]) ya terminado;
  mtime viejo con os.utime a time.time() - max_age - 60; deskops-integrate-c con owner.pid
  = os.getpid() y la carpeta propia (pasada como own) quedan.

  Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas>
  (deskops/integrate.py tests/test_integrate.py) y el trailer en el cuerpo:

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
created_at: '2026-11-23T04:47:18.051303+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:02:34.861585+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-044550/context-review/task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas/preflight/5c53eb6ec977833e7dc44eea50ede80d40de25cba99cf6574e99a24867a63ae9/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones de la preflight (todas con hechos del repo; ver base comun al final):
1) owner.pid: lo escribe _steps justo despues de mkdtemp (linea 303-304), antes del clone: (work / "owner.pid").write_text(f"{os.getpid()}\n"). Se escribe siempre que exista work, tambien en --dry-run. Como la limpieza corre despues (dentro de _run_suite), la propia ya tiene owner.pid y ademas se excluye por ruta.
2) PermissionError de os.kill(pid, 0) cuenta como vivo (no se borra). Solo ProcessLookupError cuenta como muerto. owner.pid vacio, ilegible o no numerico se trata como "sin owner.pid" (aplica la regla de mtime).
3) La carpeta propia se identifica por ruta: se omite toda carpeta cuyo Path.resolve() sea igual a work.resolve().
4) Funcion nueva en deskops/integrate.py: _clean_stale_work_dirs(own: Path, max_age: int) -> list[Path]. Recorre Path(tempfile.gettempdir()).glob("deskops-integrate-*") (solo directorios), borra con shutil.rmtree(..., ignore_errors=True) y devuelve las borradas. _run_suite pasa a _run_suite(cfg, copy, log_path, work) y, dentro del with _suite_lock(cfg.tests_lock) y antes del Popen, llama _clean_stale_work_dirs(work, cfg.suite_timeout). La llamada de la linea 319 pasa work.
5) Canal y formato: print(f"limpieza: {ruta}") a stdout (como el resto de mensajes de integrate), una linea por carpeta, ruta absoluta tal como la da glob sobre gettempdir().
6) <archivo> del test: probe = tmp_path / "addopts.txt"; la suite falsa es ["sh", "-c", f'echo "$PYTEST_ADDOPTS" > {probe}'] configurada con _configure(root, suite=...), y se corre con _integrate_env(root, {"PYTEST_ADDOPTS": "-p no:cacheprovider"}). Se asierta rc 0 y que el contenido es "-p no:cacheprovider --basetemp=<tmpdir>/deskops-integrate-XXXX/pytest" (lo previo primero, un espacio, luego --basetemp; el prefijo es root.parent / "tmpdir"). El test de limpieza es unitario sobre _clean_stale_work_dirs: monkeypatch.setattr(tempfile, "tempdir", str(tmp_path)); pid muerto = pid de un subprocess.run(["true"]) ya terminado; mtime viejo con os.utime a time.time() - max_age - 60; deskops-integrate-c con owner.pid = os.getpid() y la carpeta propia (pasada como own) quedan.
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas> (deskops/integrate.py tests/test_integrate.py) y el trailer en el cuerpo:
Task-Id: task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas

Base comun: Hechos verificados en deskops/integrate.py (HEAD 40964f50): _suite_lock linea 181, _run_suite(cfg, copy, log_path) linea 195 (toma el lock en la linea 199 y lanza cfg.suite con Popen), integrate() linea 258 con el finally que borra temps en la linea 283, _steps linea 292 con work = Path(tempfile.mkdtemp(prefix="deskops-integrate-")) en la linea 303 y temps.append(work) en la 304; _run_suite se llama en la linea 319 solo si el rango toca codigo. IntegrateConfig (deskops/config.py): suite_timeout int, default 5400; tests_lock str|None. Los tests de tests/test_integrate.py corren el CLI en subproceso con _cli (linea 28), _configure (linea 43), _integrate (linea 130, TMPDIR=root.parent/tmpdir) e _integrate_env (linea 518, acepta env extra). Modelo a seguir: test_suite_runs_under_the_declared_lock_with_pythonpath_of_the_copy (linea 231).
