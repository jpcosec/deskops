---
sldb:
  by: agent
  at: '2026-11-23T19:19:46Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
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
run_dir: runs/subagents/20261123-045102/context-review/task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar/preflight/75a7d5c88ff54871595b6f8a5591ce716e27db058d4914805bfb74eb4132acee/attempt-1
input_sha256: 75a7d5c88ff54871595b6f8a5591ce716e27db058d4914805bfb74eb4132acee
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: d343ac66082775288948b2db0f6c780aee4fc0177aaecb537ac707c1ba2f94bf
output_sha256: 5da1370178675ccc37e759543ea2513e44c292ca1b78578c6c07ca80edd982a0
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones de la preflight. Decision de JP: quitar el montaje
  global de scion (profiles.local.harness_overrides.claude en el settings.yaml) es
  decision de JP y lo ejecuta scion-coordination en ventana; esta tarea solo agrega
  el chequeo, la alerta de doctor y el parrafo del manual. Respeta depends_on: no
  se despacha hasta que cierre task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale.

  1) Esquema y contencion: env_config es YAML con volumes de primer nivel, lista de
  mapas {source, target} (formato de .bootstrap/ir-scion-env.yaml); se acepta tambien
  la forma cadena "source:target[:modo]" tomando el segundo campo como target. Un
  volume contiene el workspace si su target, normalizado con os.path.normpath (sin
  realpath), es igual a cfg.workspace o un ancestro por componentes (Path(target)
  == Path(ws) o Path(target) in Path(ws).parents). Target relativo no cuenta. YAML
  ilegible = no declara.

  2) Codigo: constante nueva EXIT_ENV_CONFIG = 7 en deskops/dispatch.py (7 esta libre).
  No es reintentable porque los dispatch-* de la cola solo reintentan [3]; el trabajo
  va a failed.

  3) doctor: alerta (findings.alerts), no error; no cambia el exit code (alertas solas
  = 0). Texto: "dispatch <rol>: env_config <ruta> no declara un volume que contenga
  <workspace>", una por rol (executor, tester) y solo si el desk tiene dispatch. Va
  en un metodo nuevo _check_dispatch_volumes de deskops/cli/commands/doctor.py llamado
  desde run(); la funcion que decide la cobertura vive en deskops/dispatch.py y la
  usan start y doctor.

  4) Test de doctor: tests/test_doctor_alerts.py (el que cita Validation), con un
  desk que declara dispatch y un env_config sin volumes.

  5) .bootstrap: no se resuelve nada especial; env_config absoluto se usa tal cual,
  relativo se resuelve contra la raiz de la tarea (como roles_root). Los dos YAML
  de .bootstrap ya traen volumes que cubren /mnt/ssd/proyectos/SLDB_1, asi que doctor
  --root . no debe dar el aviso.

  6) desk/config.json real = el del repo deskops (desk/config.json en la raiz del
  worktree que dispatch le da al ejecutor).

  Ademas: env_config sin declarar (None) tambien se niega, imprimiendo la ruta como
  "(sin env_config)". El chequeo va al principio de start, despues de leer role_cfg
  y antes del gate de memoria (linea ~396), sin efectos laterales. El fixture env
  de tests/test_dispatch.py pasa a escribir tmp_path/env.yaml con un volume que cubre
  tmp_path y a dar env_config tambien al tester, para que los tests existentes sigan
  lanzando.

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
created_at: '2026-11-23T04:51:13.243203+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:12:25.204393+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-045102/context-review/task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar/preflight/75a7d5c88ff54871595b6f8a5591ce716e27db058d4914805bfb74eb4132acee/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones de la preflight. Decision de JP: quitar el montaje global de scion (profiles.local.harness_overrides.claude en el settings.yaml) es decision de JP y lo ejecuta scion-coordination en ventana; esta tarea solo agrega el chequeo, la alerta de doctor y el parrafo del manual. Respeta depends_on: no se despacha hasta que cierre task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale.
1) Esquema y contencion: env_config es YAML con volumes de primer nivel, lista de mapas {source, target} (formato de .bootstrap/ir-scion-env.yaml); se acepta tambien la forma cadena "source:target[:modo]" tomando el segundo campo como target. Un volume contiene el workspace si su target, normalizado con os.path.normpath (sin realpath), es igual a cfg.workspace o un ancestro por componentes (Path(target) == Path(ws) o Path(target) in Path(ws).parents). Target relativo no cuenta. YAML ilegible = no declara.
2) Codigo: constante nueva EXIT_ENV_CONFIG = 7 en deskops/dispatch.py (7 esta libre). No es reintentable porque los dispatch-* de la cola solo reintentan [3]; el trabajo va a failed.
3) doctor: alerta (findings.alerts), no error; no cambia el exit code (alertas solas = 0). Texto: "dispatch <rol>: env_config <ruta> no declara un volume que contenga <workspace>", una por rol (executor, tester) y solo si el desk tiene dispatch. Va en un metodo nuevo _check_dispatch_volumes de deskops/cli/commands/doctor.py llamado desde run(); la funcion que decide la cobertura vive en deskops/dispatch.py y la usan start y doctor.
4) Test de doctor: tests/test_doctor_alerts.py (el que cita Validation), con un desk que declara dispatch y un env_config sin volumes.
5) .bootstrap: no se resuelve nada especial; env_config absoluto se usa tal cual, relativo se resuelve contra la raiz de la tarea (como roles_root). Los dos YAML de .bootstrap ya traen volumes que cubren /mnt/ssd/proyectos/SLDB_1, asi que doctor --root . no debe dar el aviso.
6) desk/config.json real = el del repo deskops (desk/config.json en la raiz del worktree que dispatch le da al ejecutor).
Ademas: env_config sin declarar (None) tambien se niega, imprimiendo la ruta como "(sin env_config)". El chequeo va al principio de start, despues de leer role_cfg y antes del gate de memoria (linea ~396), sin efectos laterales. El fixture env de tests/test_dispatch.py pasa a escribir tmp_path/env.yaml con un volume que cubre tmp_path y a dar env_config tambien al tester, para que los tests existentes sigan lanzando.
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- deskops/dispatch.py deskops/cli/commands/doctor.py docs/operator-manual.md tests/test_dispatch.py tests/test_doctor_alerts.py y el trailer en el cuerpo:
Task-Id: task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar

Base comun: Hechos verificados (HEAD 40964f50): DispatchRole.env_config (deskops/config.py linea 53) es la ruta que start pasa a scion start --config (deskops/dispatch.py lineas 514-515); DispatchConfig.workspace (linea 63) es ruta absoluta. start() esta en deskops/dispatch.py linea 381; codigos existentes: EXIT_BUSY=3, EXIT_ALIVE=4, EXIT_NO_ATTEMPTS=5, EXIT_SCION_ERROR=6, EXIT_WORKTREE=8 (lineas 22-26); 7 esta libre. Los queue_jobs dispatch-executor, dispatch-tester y dispatch-reap de desk/config.json tienen retry_exit_codes [3]. El desk real (desk/config.json de deskops) declara env_config absolutos: /mnt/ssd/proyectos/SLDB_1/.bootstrap/ir-scion-env.yaml (executor) y /mnt/ssd/proyectos/SLDB_1/.bootstrap/pi-scion-env.yaml (tester), y workspace /mnt/ssd/proyectos/SLDB_1; los dos YAML ya traen volumes: [{source: /mnt/ssd/proyectos/SLDB_1, target: /mnt/ssd/proyectos/SLDB_1}, {source: /dev/shm, target: /dev/shm}]. doctor: DoctorCLI.run en deskops/cli/commands/doctor.py linea 54 encadena _check_*; Findings (deskops/doctor_findings.py linea 40) separa errors de alerts y las alertas solas salen con 0. Fixture env de tests/test_dispatch.py (linea 66): executor con env_config = tmp_path/env.yaml (el archivo no se escribe) y tester sin env_config; workspace = tmp_path. tests/test_doctor_alerts.py corre main(["doctor", ...]) en proceso (_doctor, linea 36). Manual: docs/operator-manual.md, seccion "### Launching the executor and tester through scion" (linea 723, dentro de "## Host queue").
