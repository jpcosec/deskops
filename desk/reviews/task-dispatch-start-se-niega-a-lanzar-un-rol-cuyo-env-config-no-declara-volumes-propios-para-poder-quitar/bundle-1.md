---
sldb:
  by: agent
  at: '2026-11-23T19:19:42Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar@sha256:87486d14b16e29c22b3bddeff462f15750eb286f8cad6ec15d533d88af7153ec
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261123-045125/context-review/task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar/bundle/7a7098b0346ef27c144f4f9a617643de273bdc98d312936fb6b5a2d94790baa6/attempt-1
input_sha256: 7a7098b0346ef27c144f4f9a617643de273bdc98d312936fb6b5a2d94790baa6
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 494f2460be29055784c7b53aaeecd952bb230c23f7189c29231ed9b4751bf981
output_sha256: d139e5eff2aeb86e78b43c0b9d44dcf6b8b077744c72024ee662e70d91d80723
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del bundle. Decision de JP: retirar el montaje global
  de scion es de JP (lo ejecuta scion-coordination en ventana); esta tarea solo agrega
  el chequeo. depends_on se respeta: no se despacha antes de que cierre task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale.

  1) Esquema: volumes de primer nivel, lista de mapas {source, target} como en /mnt/ssd/proyectos/SLDB_1/.bootstrap/ir-scion-env.yaml;
  tambien cadena "source:target[:modo]" (target = segundo campo).

  2) Codigo nuevo EXIT_ENV_CONFIG = 7 en deskops/dispatch.py (3-6 y 8 ya existen,
  7 libre); los dispatch-* de la cola reintentan solo [3].

  3) "Contiene": el target normalizado (os.path.normpath, sin realpath) es igual a
  cfg.workspace o ancestro por componentes; target relativo no cuenta.

  4) doctor: alerta, no error, exit sin cambio; texto "dispatch <rol>: env_config
  <ruta> no declara un volume que contenga <workspace>", una por rol, metodo nuevo
  _check_dispatch_volumes en deskops/cli/commands/doctor.py, con la misma funcion
  de cobertura de deskops/dispatch.py.

  5) Seccion del manual: "### Launching the executor and tester through scion" (docs/operator-manual.md
  linea 723, bajo "## Host queue"); un parrafo: cada rol declara en su env_config
  un volume que cubre el workspace, start se niega con codigo 7 si no, y el montaje
  global de scion se retira por decision de JP cuando todos los desks despachados
  declaran los suyos.

  6) Test de doctor en tests/test_doctor_alerts.py.

  Ademas: env_config None tambien se niega ("(sin env_config)"); el chequeo va al
  principio de start, antes del gate de memoria, sin efectos laterales; el fixture
  env de tests/test_dispatch.py escribe tmp_path/env.yaml con un volume que cubre
  tmp_path y da env_config tambien al tester para que los tests existentes sigan verdes.

  Commit desde el worktree que dispatch le da al ejecutor, con git commit -- deskops/dispatch.py
  deskops/cli/commands/doctor.py docs/operator-manual.md tests/test_dispatch.py tests/test_doctor_alerts.py
  y el trailer en el cuerpo:

  Task-Id: task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar


  Base comun: Hechos verificados (HEAD 40964f50): DispatchRole.env_config (deskops/config.py
  linea 53) es la ruta que start pasa a scion start --config (deskops/dispatch.py
  lineas 514-515); DispatchConfig.workspace (linea 63) es ruta absoluta. start() esta
  en deskops/dispatch.py linea 381; codigos existentes: EXIT_BUSY=3, EXIT_ALIVE=4,
  EXIT_NO_ATTEMPTS=5, EXIT_SCION_ERROR=6, EXIT_WORKTREE=8 (lineas 22-26); 7 esta libre.
  Los queue_jobs dispatch-executor, dispatch-tester y dispatch-reap de desk/config.json
  tienen retry_exit_codes [3]. El desk real (desk/config.json de deskops) declara
  env_config absolutos: /mnt/ssd/proyectos/SLDB_1/.bootstrap/ir-scion-env.yaml (executor)
  y /mnt/ssd/proyectos/SLDB_1/.bootstrap/pi-scion-env.yaml (tester), y workspace /mnt/ssd/proyectos/SLDB_1;
  los dos YAML ya traen volumes: [{source: /mnt/ssd/proyectos/SLDB_1, target: /mnt/ssd/proyectos/SLDB_1},
  {source: /dev/shm, target: /dev/shm}]. doctor: DoctorCLI.run en deskops/cli/commands/doctor.py
  linea 54 encadena _check_*; Findings (deskops/doctor_findings.py linea 40) separa
  errors de alerts y las alertas solas salen con 0. Fixture env de tests/test_dispatch.py
  (linea 66): executor con env_config = tmp_path/env.yaml (el archivo no se escribe)
  y tester sin env_config; workspace = tmp_path. tests/test_doctor_alerts.py corre
  main(["doctor", ...]) en proceso (_doctor, linea 36). Manual: docs/operator-manual.md,
  seccion "### Launching the executor and tester through scion" (linea 723, dentro
  de "## Host queue").'
# ISO 8601 timestamp
created_at: '2026-11-23T04:51:40.918043+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:12:40.899773+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-045125/context-review/task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar/bundle/7a7098b0346ef27c144f4f9a617643de273bdc98d312936fb6b5a2d94790baa6/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del bundle. Decision de JP: retirar el montaje global de scion es de JP (lo ejecuta scion-coordination en ventana); esta tarea solo agrega el chequeo. depends_on se respeta: no se despacha antes de que cierre task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale.
1) Esquema: volumes de primer nivel, lista de mapas {source, target} como en /mnt/ssd/proyectos/SLDB_1/.bootstrap/ir-scion-env.yaml; tambien cadena "source:target[:modo]" (target = segundo campo).
2) Codigo nuevo EXIT_ENV_CONFIG = 7 en deskops/dispatch.py (3-6 y 8 ya existen, 7 libre); los dispatch-* de la cola reintentan solo [3].
3) "Contiene": el target normalizado (os.path.normpath, sin realpath) es igual a cfg.workspace o ancestro por componentes; target relativo no cuenta.
4) doctor: alerta, no error, exit sin cambio; texto "dispatch <rol>: env_config <ruta> no declara un volume que contenga <workspace>", una por rol, metodo nuevo _check_dispatch_volumes en deskops/cli/commands/doctor.py, con la misma funcion de cobertura de deskops/dispatch.py.
5) Seccion del manual: "### Launching the executor and tester through scion" (docs/operator-manual.md linea 723, bajo "## Host queue"); un parrafo: cada rol declara en su env_config un volume que cubre el workspace, start se niega con codigo 7 si no, y el montaje global de scion se retira por decision de JP cuando todos los desks despachados declaran los suyos.
6) Test de doctor en tests/test_doctor_alerts.py.
Ademas: env_config None tambien se niega ("(sin env_config)"); el chequeo va al principio de start, antes del gate de memoria, sin efectos laterales; el fixture env de tests/test_dispatch.py escribe tmp_path/env.yaml con un volume que cubre tmp_path y da env_config tambien al tester para que los tests existentes sigan verdes.
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- deskops/dispatch.py deskops/cli/commands/doctor.py docs/operator-manual.md tests/test_dispatch.py tests/test_doctor_alerts.py y el trailer en el cuerpo:
Task-Id: task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar

Base comun: Hechos verificados (HEAD 40964f50): DispatchRole.env_config (deskops/config.py linea 53) es la ruta que start pasa a scion start --config (deskops/dispatch.py lineas 514-515); DispatchConfig.workspace (linea 63) es ruta absoluta. start() esta en deskops/dispatch.py linea 381; codigos existentes: EXIT_BUSY=3, EXIT_ALIVE=4, EXIT_NO_ATTEMPTS=5, EXIT_SCION_ERROR=6, EXIT_WORKTREE=8 (lineas 22-26); 7 esta libre. Los queue_jobs dispatch-executor, dispatch-tester y dispatch-reap de desk/config.json tienen retry_exit_codes [3]. El desk real (desk/config.json de deskops) declara env_config absolutos: /mnt/ssd/proyectos/SLDB_1/.bootstrap/ir-scion-env.yaml (executor) y /mnt/ssd/proyectos/SLDB_1/.bootstrap/pi-scion-env.yaml (tester), y workspace /mnt/ssd/proyectos/SLDB_1; los dos YAML ya traen volumes: [{source: /mnt/ssd/proyectos/SLDB_1, target: /mnt/ssd/proyectos/SLDB_1}, {source: /dev/shm, target: /dev/shm}]. doctor: DoctorCLI.run en deskops/cli/commands/doctor.py linea 54 encadena _check_*; Findings (deskops/doctor_findings.py linea 40) separa errors de alerts y las alertas solas salen con 0. Fixture env de tests/test_dispatch.py (linea 66): executor con env_config = tmp_path/env.yaml (el archivo no se escribe) y tester sin env_config; workspace = tmp_path. tests/test_doctor_alerts.py corre main(["doctor", ...]) en proceso (_doctor, linea 36). Manual: docs/operator-manual.md, seccion "### Launching the executor and tester through scion" (linea 723, dentro de "## Host queue").
