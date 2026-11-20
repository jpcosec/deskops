---
sldb:
  by: agent
  at: '2026-11-20T08:45:12Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk@sha256:164cb0d7692d98f941881d4d36316e3b87efc599fc4cfd4555af3ca41848a302
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-084356/context-review/task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk/preflight/b30b576b56a53c21e3bc43bb08bc59e16fe5cc4bec4580d8d2df65be095a5f67/attempt-1
input_sha256: b30b576b56a53c21e3bc43bb08bc59e16fe5cc4bec4580d8d2df65be095a5f67
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 1186a4729cd7942c9163a27c719dfade01cef3e14dd499bb1353256f706a212b
output_sha256: 5abca81db600c2b56416b610c008e88ef53788c4d19a07cfc77b6df6ca338926
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. 1), 4) bundle y punto de inserción:
  una función nueva ensure_sldb_merge_driver(root: Path) -> None en deskops/bootstrap.py.
  La llaman (a) BootstrapService.init_local_store, después de que el store existe
  o se inicializó y antes de _register_models, y (b) DeskCLI.update en deskops/cli/commands/desk.py,
  al final de la rama con --apply, justo antes del return de éxito. Solo con --apply;
  sin --apply no escribe nada. 2) Firma, en sldb: install_merge_driver(store_path:
  Path) -> dict[str, list[str]], en sldb.api.stores.merge_driver_install. Se llama
  con root / ''.sldb''. Devuelve las líneas agregadas a .gitattributes y las claves
  de config cambiadas; si alguna no está vacía, se imprime ''merge driver de sldb
  instalado'' por stdout. 3) y bundle 3) ''Repo git'' significa que ''git -C <root>
  rev-parse --show-toplevel'' sale con 0; si no, o si no hay git, la función no hace
  nada (worktrees incluidos, porque rev-parse lo resuelve). 4) y bundle 2) Si install_merge_driver
  lanza CalledProcessError u OSError, se imprime por stderr ''aviso: merge driver
  de sldb no instalado: <motivo>'' y el comando sigue con su código de salida normal.
  ImportError (sldb sin el módulo): se omite en silencio. 5) y bundle 1) Las líneas
  son las que escribe install_merge_driver: ''.sldb/core/store_index.yaml merge=sldb'',
  ''.sldb/core/models/*.yaml merge=sldb'' y ''.sldb/store.yaml merge=sldb'', y las
  claves merge.sldb.name y merge.sldb.driver. Los tests las comparan importando nada
  de sldb, solo leyendo .gitattributes y git config. 6) Test nuevo en tests/test_merge_driver_install.py.
  7) Obligatorio si existe /workspace/sldb y tiene el commit 9007f78a (''git -C /workspace/sldb
  cat-file -e 9007f78a''): correr tests/test_lifecycle_seed_drift.py con PYTHONPATH
  a un worktree de ese commit. Si no existe, se informa y lo corre el integrador en
  el host. 8) Fuera de git, el store se inicializa igual y solo el driver se omite.
  Bundle 5) Commit con trailer ''Task-Id: <id de esta tarea>'' y rutas nombradas.'
# ISO 8601 timestamp
created_at: '2026-11-20T08:44:07.640338+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T08:45:06.495749+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-084356/context-review/task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk/preflight/b30b576b56a53c21e3bc43bb08bc59e16fe5cc4bec4580d8d2df65be095a5f67/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. 1), 4) bundle y punto de inserción: una función nueva ensure_sldb_merge_driver(root: Path) -> None en deskops/bootstrap.py. La llaman (a) BootstrapService.init_local_store, después de que el store existe o se inicializó y antes de _register_models, y (b) DeskCLI.update en deskops/cli/commands/desk.py, al final de la rama con --apply, justo antes del return de éxito. Solo con --apply; sin --apply no escribe nada. 2) Firma, en sldb: install_merge_driver(store_path: Path) -> dict[str, list[str]], en sldb.api.stores.merge_driver_install. Se llama con root / '.sldb'. Devuelve las líneas agregadas a .gitattributes y las claves de config cambiadas; si alguna no está vacía, se imprime 'merge driver de sldb instalado' por stdout. 3) y bundle 3) 'Repo git' significa que 'git -C <root> rev-parse --show-toplevel' sale con 0; si no, o si no hay git, la función no hace nada (worktrees incluidos, porque rev-parse lo resuelve). 4) y bundle 2) Si install_merge_driver lanza CalledProcessError u OSError, se imprime por stderr 'aviso: merge driver de sldb no instalado: <motivo>' y el comando sigue con su código de salida normal. ImportError (sldb sin el módulo): se omite en silencio. 5) y bundle 1) Las líneas son las que escribe install_merge_driver: '.sldb/core/store_index.yaml merge=sldb', '.sldb/core/models/*.yaml merge=sldb' y '.sldb/store.yaml merge=sldb', y las claves merge.sldb.name y merge.sldb.driver. Los tests las comparan importando nada de sldb, solo leyendo .gitattributes y git config. 6) Test nuevo en tests/test_merge_driver_install.py. 7) Obligatorio si existe /workspace/sldb y tiene el commit 9007f78a ('git -C /workspace/sldb cat-file -e 9007f78a'): correr tests/test_lifecycle_seed_drift.py con PYTHONPATH a un worktree de ese commit. Si no existe, se informa y lo corre el integrador en el host. 8) Fuera de git, el store se inicializa igual y solo el driver se omite. Bundle 5) Commit con trailer 'Task-Id: <id de esta tarea>' y rutas nombradas.
