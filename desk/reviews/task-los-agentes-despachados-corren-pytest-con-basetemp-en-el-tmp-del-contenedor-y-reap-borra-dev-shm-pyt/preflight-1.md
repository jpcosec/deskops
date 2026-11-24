---
sldb:
  by: agent
  at: '2026-11-23T19:34:31Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
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
run_dir: runs/subagents/20261123-045248/context-review/task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt/preflight/defd9794260243f302c392d61255257ff91aac4ab6bd482178dcaa4da9ff8c0d/attempt-1
input_sha256: defd9794260243f302c392d61255257ff91aac4ab6bd482178dcaa4da9ff8c0d
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 1079a8754e9d7916d81888e30a8708b2f3e6ae80839b90c58f3ff76745464f96
output_sha256: 736fc75ba9084f1d3a0438bb08c603e2eb63301a0d46e1b646b7acf69c855279
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones de la preflight:

  1) Nombre real del agente: el name de scion_child_identity que start ya tiene en
  la variable name (deskops/dispatch.py linea 422), por ejemplo deskops-e-<hash>;
  _role_instructions gana un parametro agent_name y start le pasa name. Los nombres
  de scion ya son slugs (minusculas, digitos, guiones): no se sanea.

  2) Proyecto y esquema: el segundo _list_agents(cfg) es del proyecto cfg.project
  (el mismo que usa reap), sin filtrar por la etiqueta deskops.task_id; cuenta como
  vivo todo agente con phase == "running" (campo phase de cada dict, como en reap).

  3) Secuencia: una sola comprobacion al final de reap, despues del bucle (aunque
  no se haya borrado ninguno) y antes de calcular el codigo de salida. Si scion list
  falla (UsageError) no se limpia y el codigo de salida no cambia.

  4) Canal: print(f"limpieza: {ruta}") a stdout, como el resto de lineas de reap,
  y solo si el directorio existia y se borro (shutil.rmtree(..., ignore_errors=True)).
  Si no existe, no imprime nada; la limpieza nunca cambia el codigo de salida.

  5) PYTEST_ADDOPTS se reemplaza (no se concatena): la seccion "## Temporales de pytest"
  dice export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<name>" con el nombre ya sustituido,
  antes de cualquier pytest. Va solo en el prompt (para executor y tester), no en
  las lineas de validacion de las tareas.

  Parcheable en tests: como el CLI corre en subproceso, monkeypatch no llega; SCION_PYTEST_TMP
  = Path(os.environ.get("DESKOPS_SCION_PYTEST_TMP", "/dev/shm/pytest-of-scion")) se
  lee al llamar (no al importar) y Env.__init__ de tests/test_dispatch.py fija DESKOPS_SCION_PYTEST_TMP
  = tmp_path / "pytest-of-scion" para todos los tests, asi ningun test toca el /dev/shm
  real y los stdout existentes no cambian (el directorio de prueba no existe salvo
  en los dos tests nuevos).

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
created_at: '2026-11-23T04:53:02.818273+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:32:50.897548+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-045248/context-review/task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt/preflight/defd9794260243f302c392d61255257ff91aac4ab6bd482178dcaa4da9ff8c0d/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones de la preflight:
1) Nombre real del agente: el name de scion_child_identity que start ya tiene en la variable name (deskops/dispatch.py linea 422), por ejemplo deskops-e-<hash>; _role_instructions gana un parametro agent_name y start le pasa name. Los nombres de scion ya son slugs (minusculas, digitos, guiones): no se sanea.
2) Proyecto y esquema: el segundo _list_agents(cfg) es del proyecto cfg.project (el mismo que usa reap), sin filtrar por la etiqueta deskops.task_id; cuenta como vivo todo agente con phase == "running" (campo phase de cada dict, como en reap).
3) Secuencia: una sola comprobacion al final de reap, despues del bucle (aunque no se haya borrado ninguno) y antes de calcular el codigo de salida. Si scion list falla (UsageError) no se limpia y el codigo de salida no cambia.
4) Canal: print(f"limpieza: {ruta}") a stdout, como el resto de lineas de reap, y solo si el directorio existia y se borro (shutil.rmtree(..., ignore_errors=True)). Si no existe, no imprime nada; la limpieza nunca cambia el codigo de salida.
5) PYTEST_ADDOPTS se reemplaza (no se concatena): la seccion "## Temporales de pytest" dice export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<name>" con el nombre ya sustituido, antes de cualquier pytest. Va solo en el prompt (para executor y tester), no en las lineas de validacion de las tareas.
Parcheable en tests: como el CLI corre en subproceso, monkeypatch no llega; SCION_PYTEST_TMP = Path(os.environ.get("DESKOPS_SCION_PYTEST_TMP", "/dev/shm/pytest-of-scion")) se lee al llamar (no al importar) y Env.__init__ de tests/test_dispatch.py fija DESKOPS_SCION_PYTEST_TMP = tmp_path / "pytest-of-scion" para todos los tests, asi ningun test toca el /dev/shm real y los stdout existentes no cambian (el directorio de prueba no existe salvo en los dos tests nuevos).
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- deskops/dispatch.py tests/test_dispatch.py y el trailer en el cuerpo:
Task-Id: task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt

Base comun: Hechos verificados (HEAD 40964f50) en deskops/dispatch.py: _list_agents(cfg) linea 67 (scion list --project cfg.project --format json; lista de dicts con name, phase, activity, labels; UsageError si scion falla); _role_instructions(role, task_id, quick_gates, worktree, root) linea 330 arma _base_instructions (linea 341, textos de executor y tester) + _quick_gates_text + _worktree_text; start() escribe prompt.md en las lineas 483-494 y ya tiene name = identity["name"] (linea 422, el nombre real del agente scion); reap() linea 533 recorre los agentes de la tarea, imprime una linea por agente y devuelve EXIT_ALIVE=4 / EXIT_WORKTREE=8 / EXIT_BUSY=3 / EXIT_SCION_ERROR=6 / 0. En tests/test_dispatch.py el CLI corre en subproceso (Env.cli, linea 45) con un scion falso cuyo list lee FAKE_SCION_LIST (estatico: despues de borrar sigue listando lo mismo) y Env.__init__ quita del entorno toda variable DESKOPS_*; test_reap y test_reap_scion_error_continues_and_fails asertan stdout linea por linea.
