---
sldb:
  by: agent
  at: '2026-11-23T19:12:55Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis@sha256:c52ce4ec99fb34200061b3db7e7573348c035eab8329a9144adfd17173ef6376
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261123-045344/context-review/task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis/preflight/2602a8731b5242f8717bd4de9288358b823971cf2129e64ff326195b5edab773/attempt-1
input_sha256: 2602a8731b5242f8717bd4de9288358b823971cf2129e64ff326195b5edab773
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 59bdf505bcbdfa30ed208be5162510b3d04f1ed3231a5f06610ab434fc00d652
output_sha256: 6667d1470f4ee694185e53e44efcbf8c31bc0ec849bd889c55626deb1bce9eee
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones de la preflight:

  1) Slug: re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", identidad): sin guion inicial ni
  final, sin guiones dobles, no vacio, sin limite de largo. Rechazo: "Error: ''<identidad>''
  no es un slug (minusculas, digitos y guiones simples)" en stdout, como el resto
  de errores de RepoCLI, rc 1, y el archivo no se toca.

  2) init --id: si desk/config.json no existia (lo crea este init) queda project_identity
  = <id>; si existia sin project_identity, se agrega; si ya tiene la misma, nada;
  si tiene otra, no se pisa y se avisa en stderr "desk/config.json ya dice project_identity
  <Y>; para cambiarla: deskops repo whoami --set <id> --root <path>", y init sigue
  y sale 0. Una ruta que no es desk la crea init como hoy. Sin --id todo queda como
  hoy (tests/test_scaffold_golden.py verde, sin regenerar el golden de scaffold).

  3) Edicion minima: funcion compartida set_project_identity(root, identidad) -> (vieja,
  nueva) en deskops/workspace.py, que usan whoami --set e init --id: igual que set_job_field
  (carga el JSON, cambia solo project_identity, valida con DeskConfig, reescribe con
  json.dumps(data, indent=2, ensure_ascii=False) + "\n"). Si falta la clave se agrega
  al final. JSON no tiene comentarios; claves duplicadas las colapsa json.loads (aceptado).
  Un desk/config.json ausente o JSON invalido es "Error: ..." rc 1. El test byte a
  byte compara el archivo de init con la linea de project_identity reemplazada.

  4) register: el aviso no cambia el exit code ni aborta el registro (solo stderr).
  Si <ruta>/desk/config.json falta, no se lee o no tiene project_identity, no avisa.

  5) Goldens: tests/fixtures/golden/help/deskops_init.txt (gana --id) y deskops_repo_whoami.txt
  (gana --set); regenerados con --update-golden (comando en la base comun). ("repo",
  "whoami") pasa a mutates=True en deskops/cli/registry.py porque --set escribe.

  Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas>
  (deskops/workspace.py deskops/cli/registry.py deskops/cli/commands/repo.py deskops/cli/commands/core.py
  tests/test_repo_identity.py y los dos goldens) y el trailer en el cuerpo:

  Task-Id: task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis


  Base comun: Hechos verificados (HEAD 40964f50): deskops init escribe desk/config.json
  como semilla de deskops/data/templates/config.json ("project_identity": "{desk_name}",
  sustituido por el nombre de la carpeta en _seed_text, deskops/workspace.py lineas
  173-226; seed_desk linea 239; InitCLI en deskops/cli/commands/core.py lo llama en
  la linea 41) y _write_or_patch_config (workspace.py linea 339, data.setdefault("project_identity",
  root.name) en la linea 366) lo parchea en migrate_desk. set_job_field (deskops/queue.py
  linea 284) carga el JSON, cambia una clave, valida con el modelo y reescribe con
  json.dumps(data, indent=2, ensure_ascii=False) + "\n" (linea 321); la clave conserva
  su posicion. RepoCLI (deskops/cli/commands/repo.py): register linea 33, whoami linea
  156; sus errores se imprimen como "Error: ..." en stdout y devuelven 1. Declaraciones
  en deskops/cli/registry.py: init (path ("init",), arg path), ("repo", "register")
  linea 1145 (ya tiene --id), ("repo", "whoami") linea 1166 (--root default ".", mutates=False).
  Goldens de ayuda: tests/fixtures/golden/help/deskops_init.txt, deskops_repo_whoami.txt,
  deskops_repo.txt; se regeneran con TMPDIR=/dev/shm ../.venv/bin/python -m pytest
  -q -p no:cacheprovider tests/test_output_goldens.py --update-golden (opcion declarada
  en tests/conftest.py linea 37).'
# ISO 8601 timestamp
created_at: '2026-11-23T04:53:59.819420+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:33:22.252708+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-045344/context-review/task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis/preflight/2602a8731b5242f8717bd4de9288358b823971cf2129e64ff326195b5edab773/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones de la preflight:
1) Slug: re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", identidad): sin guion inicial ni final, sin guiones dobles, no vacio, sin limite de largo. Rechazo: "Error: '<identidad>' no es un slug (minusculas, digitos y guiones simples)" en stdout, como el resto de errores de RepoCLI, rc 1, y el archivo no se toca.
2) init --id: si desk/config.json no existia (lo crea este init) queda project_identity = <id>; si existia sin project_identity, se agrega; si ya tiene la misma, nada; si tiene otra, no se pisa y se avisa en stderr "desk/config.json ya dice project_identity <Y>; para cambiarla: deskops repo whoami --set <id> --root <path>", y init sigue y sale 0. Una ruta que no es desk la crea init como hoy. Sin --id todo queda como hoy (tests/test_scaffold_golden.py verde, sin regenerar el golden de scaffold).
3) Edicion minima: funcion compartida set_project_identity(root, identidad) -> (vieja, nueva) en deskops/workspace.py, que usan whoami --set e init --id: igual que set_job_field (carga el JSON, cambia solo project_identity, valida con DeskConfig, reescribe con json.dumps(data, indent=2, ensure_ascii=False) + "\n"). Si falta la clave se agrega al final. JSON no tiene comentarios; claves duplicadas las colapsa json.loads (aceptado). Un desk/config.json ausente o JSON invalido es "Error: ..." rc 1. El test byte a byte compara el archivo de init con la linea de project_identity reemplazada.
4) register: el aviso no cambia el exit code ni aborta el registro (solo stderr). Si <ruta>/desk/config.json falta, no se lee o no tiene project_identity, no avisa.
5) Goldens: tests/fixtures/golden/help/deskops_init.txt (gana --id) y deskops_repo_whoami.txt (gana --set); regenerados con --update-golden (comando en la base comun). ("repo", "whoami") pasa a mutates=True en deskops/cli/registry.py porque --set escribe.
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas> (deskops/workspace.py deskops/cli/registry.py deskops/cli/commands/repo.py deskops/cli/commands/core.py tests/test_repo_identity.py y los dos goldens) y el trailer en el cuerpo:
Task-Id: task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis

Base comun: Hechos verificados (HEAD 40964f50): deskops init escribe desk/config.json como semilla de deskops/data/templates/config.json ("project_identity": "{desk_name}", sustituido por el nombre de la carpeta en _seed_text, deskops/workspace.py lineas 173-226; seed_desk linea 239; InitCLI en deskops/cli/commands/core.py lo llama en la linea 41) y _write_or_patch_config (workspace.py linea 339, data.setdefault("project_identity", root.name) en la linea 366) lo parchea en migrate_desk. set_job_field (deskops/queue.py linea 284) carga el JSON, cambia una clave, valida con el modelo y reescribe con json.dumps(data, indent=2, ensure_ascii=False) + "\n" (linea 321); la clave conserva su posicion. RepoCLI (deskops/cli/commands/repo.py): register linea 33, whoami linea 156; sus errores se imprimen como "Error: ..." en stdout y devuelven 1. Declaraciones en deskops/cli/registry.py: init (path ("init",), arg path), ("repo", "register") linea 1145 (ya tiene --id), ("repo", "whoami") linea 1166 (--root default ".", mutates=False). Goldens de ayuda: tests/fixtures/golden/help/deskops_init.txt, deskops_repo_whoami.txt, deskops_repo.txt; se regeneran con TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py --update-golden (opcion declarada en tests/conftest.py linea 37).
