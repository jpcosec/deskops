---
sldb:
  by: agent
  at: '2026-11-23T19:34:13Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt@sha256:ed506d28e42006a39986e4ffc9ca2929ba1a8c44302ce6caef9ee0fa39dd8edb
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261123-045315/context-review/task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt/bundle/49b9f64b37124fd84eb38c1def72835c93e088b63206fe2473b0564469d7e685/attempt-1
input_sha256: 49b9f64b37124fd84eb38c1def72835c93e088b63206fe2473b0564469d7e685
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 95524fe1d1210cf0ce9d1ebcf24a3701c37a7eae3cb2c73b596e38dd50eb61a5
output_sha256: d664dcd58213b48dd42e1134d4a46950b0c83aebfe30584ea69edcd32e5319bf
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del bundle:

  1) Condicion exacta: al final de reap, despues del bucle, siempre (haya borrado
  o no, con conflicto, busy o error de scion en algun agente); se llama de nuevo _list_agents(cfg)
  y si ningun agente del proyecto tiene phase == "running" se limpia. No requiere
  rc 0 y no cambia el codigo de salida. Si scion list falla, no se limpia.

  2) Ruta inexistente: no se hace nada y no se imprime. Si existe: shutil.rmtree(ruta,
  ignore_errors=True) y print(f"limpieza: {ruta}") a stdout. La ruta sale de DESKOPS_SCION_PYTEST_TMP
  o, sin esa variable, /dev/shm/pytest-of-scion (leida al llamar); es lo que la hace
  parcheable con el CLI en subproceso (Env.cli de tests/test_dispatch.py, linea 45).
  Env.__init__ fija DESKOPS_SCION_PYTEST_TMP = tmp_path / "pytest-of-scion" para todos
  los tests.

  3) Se reemplaza: export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<name>".

  4) Solo en el prompt: seccion "## Temporales de pytest" agregada por _role_instructions
  para role executor y tester; no se tocan validaciones ni otros comandos.

  5) Punto de inyeccion: dinamico por agente; _role_instructions gana agent_name y
  start le pasa name (deskops/dispatch.py linea 422) en la llamada de la linea 492.

  Commit desde el worktree que dispatch le da al ejecutor, con git commit -- deskops/dispatch.py
  tests/test_dispatch.py y el trailer en el cuerpo:

  Task-Id: task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt


  Base comun: Hechos verificados (HEAD 40964f50) en deskops/dispatch.py: _list_agents(cfg)
  linea 67 (scion list --project cfg.project --format json; lista de dicts con name,
  phase, activity, labels; UsageError si scion falla); _role_instructions(role, task_id,
  quick_gates, worktree, root) linea 330 arma _base_instructions (linea 341, textos
  de executor y tester) + _quick_gates_text + _worktree_text; start() escribe prompt.md
  en las lineas 483-494 y ya tiene name = identity["name"] (linea 422, el nombre real
  del agente scion); reap() linea 533 recorre los agentes de la tarea, imprime una
  linea por agente y devuelve EXIT_ALIVE=4 / EXIT_WORKTREE=8 / EXIT_BUSY=3 / EXIT_SCION_ERROR=6
  / 0. En tests/test_dispatch.py el CLI corre en subproceso (Env.cli, linea 45) con
  un scion falso cuyo list lee FAKE_SCION_LIST (estatico: despues de borrar sigue
  listando lo mismo) y Env.__init__ quita del entorno toda variable DESKOPS_*; test_reap
  y test_reap_scion_error_continues_and_fails asertan stdout linea por linea.'
# ISO 8601 timestamp
created_at: '2026-11-23T04:53:31.368138+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:33:06.654647+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-045315/context-review/task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt/bundle/49b9f64b37124fd84eb38c1def72835c93e088b63206fe2473b0564469d7e685/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del bundle:
1) Condicion exacta: al final de reap, despues del bucle, siempre (haya borrado o no, con conflicto, busy o error de scion en algun agente); se llama de nuevo _list_agents(cfg) y si ningun agente del proyecto tiene phase == "running" se limpia. No requiere rc 0 y no cambia el codigo de salida. Si scion list falla, no se limpia.
2) Ruta inexistente: no se hace nada y no se imprime. Si existe: shutil.rmtree(ruta, ignore_errors=True) y print(f"limpieza: {ruta}") a stdout. La ruta sale de DESKOPS_SCION_PYTEST_TMP o, sin esa variable, /dev/shm/pytest-of-scion (leida al llamar); es lo que la hace parcheable con el CLI en subproceso (Env.cli de tests/test_dispatch.py, linea 45). Env.__init__ fija DESKOPS_SCION_PYTEST_TMP = tmp_path / "pytest-of-scion" para todos los tests.
3) Se reemplaza: export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<name>".
4) Solo en el prompt: seccion "## Temporales de pytest" agregada por _role_instructions para role executor y tester; no se tocan validaciones ni otros comandos.
5) Punto de inyeccion: dinamico por agente; _role_instructions gana agent_name y start le pasa name (deskops/dispatch.py linea 422) en la llamada de la linea 492.
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- deskops/dispatch.py tests/test_dispatch.py y el trailer en el cuerpo:
Task-Id: task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt

Base comun: Hechos verificados (HEAD 40964f50) en deskops/dispatch.py: _list_agents(cfg) linea 67 (scion list --project cfg.project --format json; lista de dicts con name, phase, activity, labels; UsageError si scion falla); _role_instructions(role, task_id, quick_gates, worktree, root) linea 330 arma _base_instructions (linea 341, textos de executor y tester) + _quick_gates_text + _worktree_text; start() escribe prompt.md en las lineas 483-494 y ya tiene name = identity["name"] (linea 422, el nombre real del agente scion); reap() linea 533 recorre los agentes de la tarea, imprime una linea por agente y devuelve EXIT_ALIVE=4 / EXIT_WORKTREE=8 / EXIT_BUSY=3 / EXIT_SCION_ERROR=6 / 0. En tests/test_dispatch.py el CLI corre en subproceso (Env.cli, linea 45) con un scion falso cuyo list lee FAKE_SCION_LIST (estatico: despues de borrar sigue listando lo mismo) y Env.__init__ quita del entorno toda variable DESKOPS_*; test_reap y test_reap_scion_error_continues_and_fails asertan stdout linea por linea.
