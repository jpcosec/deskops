---
sldb:
  by: agent
  at: '2026-11-20T17:48:31Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise@sha256:3ba87c9d4ee39cd9f298e23b099a28ae31c9682799daffbdb0c0f5bb1116add7
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-174709/context-review/task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise/preflight/b1f3045e336de57f474772ef3026c6d66ada857411233d60b80f1849ae172b83/attempt-1
input_sha256: b1f3045e336de57f474772ef3026c6d66ada857411233d60b80f1849ae172b83
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 7584f55999191623d4cae7bace7a369d6153ba6b11cc914b1a84ff3d745130e5
output_sha256: 1955c5bd5f7b2ababb3d072b731c9d50cadeddaa5080fabe3040bf25bf5339c4
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador (diseño fijado). 1) y bundle 4) Rama
  ''deskops/<name>'', donde <name> es el nombre del agente scion de scion_child_identity
  (deskops-e-<hash12> o con -a2): es único por tarea, rol e intento, así que no hay
  colisiones. Vale para cualquier repo de desk, no solo deskops. 2) Base: la rama
  local cfg.branch del bloque integrate de desk/config.json (main); si no hay bloque
  integrate, main. Si el checkout principal no está en esa rama, start falla con un
  mensaje claro y no lanza. 3) y bundle 3) Ruta: <root>/.worktrees/<name>, con <root>
  la raíz del desk de la tarea (la del --root). Se ignora con una línea ''.worktrees/''
  en .git/info/exclude (local, no versionado), que start agrega si falta. 4) y bundle
  2) Superficie: solo el prompt.md que escribe dispatch.py (línea 200). Dice al ejecutor
  que trabaje y commitee en <root>/.worktrees/<name>, que dentro del contenedor está
  en la misma ruta porque el workspace está montado. El template de scion no cambia.
  5) El diseño va en el result-summary.md del ejecutor, sección ''## Diseño''. 6)
  y bundle 1) y 5) Integración y limpieza en reap (deskops/dispatch.py:231), que ya
  corre al terminar el ejecutor (lo encola el hook execution-task_activates). Para
  un ejecutor terminado, reap hace cherry-pick sobre la rama local cfg.branch de los
  commits de deskops/<name> que no están en ella, en orden. Si el cherry-pick tiene
  conflictos, hace ''cherry-pick --abort'', deja el worktree y la rama, imprime el
  conflicto y sale con código distinto de 0, y la cola deja la nota de fallo. Si sale
  bien, borra el worktree (''git worktree remove'') y la rama. El tester sigue probando
  la rama principal como hoy, porque reap corre antes que él. integrate no cambia.
  Para los testers no se crea worktree, porque no escriben. 7) Commit con trailer
  ''Task-Id: <id de esta tarea>'' y rutas nombradas con ''git commit -- <rutas>''.
  Bundle 6) La retención de un ejecutor por repo es la regla del coordinador mientras
  esto no entre; no es requisito de la tarea y se retira cuando entre.'
# ISO 8601 timestamp
created_at: '2026-11-20T17:47:24.341976+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T17:48:25.500733+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-174709/context-review/task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise/preflight/b1f3045e336de57f474772ef3026c6d66ada857411233d60b80f1849ae172b83/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador (diseño fijado). 1) y bundle 4) Rama 'deskops/<name>', donde <name> es el nombre del agente scion de scion_child_identity (deskops-e-<hash12> o con -a2): es único por tarea, rol e intento, así que no hay colisiones. Vale para cualquier repo de desk, no solo deskops. 2) Base: la rama local cfg.branch del bloque integrate de desk/config.json (main); si no hay bloque integrate, main. Si el checkout principal no está en esa rama, start falla con un mensaje claro y no lanza. 3) y bundle 3) Ruta: <root>/.worktrees/<name>, con <root> la raíz del desk de la tarea (la del --root). Se ignora con una línea '.worktrees/' en .git/info/exclude (local, no versionado), que start agrega si falta. 4) y bundle 2) Superficie: solo el prompt.md que escribe dispatch.py (línea 200). Dice al ejecutor que trabaje y commitee en <root>/.worktrees/<name>, que dentro del contenedor está en la misma ruta porque el workspace está montado. El template de scion no cambia. 5) El diseño va en el result-summary.md del ejecutor, sección '## Diseño'. 6) y bundle 1) y 5) Integración y limpieza en reap (deskops/dispatch.py:231), que ya corre al terminar el ejecutor (lo encola el hook execution-task_activates). Para un ejecutor terminado, reap hace cherry-pick sobre la rama local cfg.branch de los commits de deskops/<name> que no están en ella, en orden. Si el cherry-pick tiene conflictos, hace 'cherry-pick --abort', deja el worktree y la rama, imprime el conflicto y sale con código distinto de 0, y la cola deja la nota de fallo. Si sale bien, borra el worktree ('git worktree remove') y la rama. El tester sigue probando la rama principal como hoy, porque reap corre antes que él. integrate no cambia. Para los testers no se crea worktree, porque no escriben. 7) Commit con trailer 'Task-Id: <id de esta tarea>' y rutas nombradas con 'git commit -- <rutas>'. Bundle 6) La retención de un ejecutor por repo es la regla del coordinador mientras esto no entre; no es requisito de la tarea y se retira cuando entre.
