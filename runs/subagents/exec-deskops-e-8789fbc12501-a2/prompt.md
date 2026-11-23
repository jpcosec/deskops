Task: task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis
Title: deskops init --id fija project_identity, deskops repo whoami --set la cambia por CLI y repo register avisa si --id no coincide con la identidad del desk
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-23T08:22:32Z'
  authority: generated
  via: save_document_payload
id: task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261122-234848-suggestion-deskops-init-fija-project-identity-con-el-nombre-de-la-carpeta-y-no-hay-comando-para-cambiarlo.md
- desk/inbox/20261122-222005-unclear-de-labchile-chatbots-no-hay-verbo-para-cambiar-project-identity-editar-la-portada-de-pills-ni-fusionar-dos-desks.md
depends_on: []
pills: []
files:
- deskops/workspace.py
- deskops/cli/registry.py
- deskops/cli/commands/repo.py
- tests/test_repo_identity.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops init --id fija project_identity, deskops repo whoami --set la cambia por CLI y repo register avisa si --id no coincide con la identidad del desk

## Rationale

_Explain why this task exists or the business driver behind it._

Dos notas con el mismo hueco. Nota 20261122-234848 (desk de workflow, scion-coordination, 2026-11-23): deskops init /mnt/ssd/proyectos/wf-desks dejó project_identity wf-desks en desk/config.json; después deskops repo register workflow <ruta> --id workflow registró el repo como workflow, y deskops repo whoami en ese desk responde wf-desks. Nota 20261122-222005 (labchile_chatbots, punto 2): al fusionar dos desks no hubo verbo para cambiar project_identity y se editó desk/config.json a mano. Hoy deskops/workspace.py (alrededor de la línea 366) hace data.setdefault("project_identity", root.name) y no hay otra forma. Relacionada, no se duplica: task-init-en-un-worktree-usa-el-nombre-del-repo-y-doctor-lee-el-pythonpath-del-store (cómo se deriva la identidad por defecto en un worktree); esta tarea agrega la forma explícita.

## Goal

_Describe the concrete result this task must produce._

(1) deskops init [path] --id <identidad>: escribe project_identity = <identidad> en desk/config.json (sin --id, igual que hoy); si el desk ya existe con otra identidad, no la pisa y avisa que se use repo whoami --set. (2) deskops repo whoami --set <identidad> --root <desk>: valida que <identidad> sea un slug (minúsculas, dígitos, guiones), reescribe solo project_identity en desk/config.json (como set_job_field de deskops/queue.py, sin tocar el resto del archivo) e imprime "project_identity: <vieja> -> <nueva>". (3) deskops repo register <nombre> <ruta> --id X avisa en stderr cuando el desk de <ruta> tiene project_identity distinto de X: "el desk de <ruta> dice project_identity <Y>; alinéalo con deskops repo whoami --set X --root <ruta>".

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/workspace.py, deskops/cli/registry.py (argumentos de init), deskops/cli/commands/repo.py, goldens de ayuda y tests/test_repo_identity.py. No entra: los puntos 1 y 3 de la nota 20261122-222005 (editar la portada de pills y fusionar desks), que esperan decisión de JP; renombrar referencias a la identidad vieja en otros desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_repo_identity.py: test_init_with_id_sets_project_identity, test_whoami_set_rewrites_only_project_identity (el resto de desk/config.json queda byte a byte), test_whoami_set_rejects_non_slug, test_register_warns_when_id_differs_from_desk_identity. p2: implementar. p3: goldens de ayuda. p4: suite con -n 4. p5: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_repo_identity.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_scaffold_golden.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro tests nuevos pasan y deskops init sin --id deja el mismo desk/config.json que hoy (test existente de scaffold verde).

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-8789fbc12501-a2`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-8789fbc12501-a2

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
