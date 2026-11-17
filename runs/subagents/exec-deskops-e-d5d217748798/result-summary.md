# result-summary — exec-deskops-e-d5d217748798

- run_id: run-deskops-e-d5d217748798
- task: task-retirar-el-alias-deskops-inbox-docs-y-skills-pasan-a-deskops-message-y-se-borra-el-alias
- session: scion://agent/deskops-e-d5d217748798 (agente claude); session_sha256: no disponible desde dentro de la sesión
- Sin commits (los hace `deskops closeout commit`).

## Qué cambié

En `files` del TaskDoc:
- `deskops/cli/registry.py`: borrado el `Command(path=("inbox",), deprecated_for=("message",))` y las constantes que solo usaba él (`ROOT_ARG_INBOX`, `PYTHONPATH_INBOX_ARG`). `deskops inbox` ahora da `invalid choice: 'inbox'`, rc=2.
- `docs/operator-manual.md`: quitado el párrafo del alias y su bloque `bash runnable` `deskops inbox --list`; quitada la nota de que `--sender` es la forma de `inbox`.
- `docs/faq.md`: quitadas las dos menciones del alias (líneas 52 y 230).
- `.claude/skills/deskops-workflow/SKILL.md`: `deskops inbox "<gap>" --kind unclear --root .` → `deskops message send "<gap>" --kind unclear --root .`.
- `.claude/skills/deskops-workflow/references/deskops-cli.md`: los ejemplos de inbox pasan a `deskops message send/list/read/ack` (con `--to <repo>` para otro desk).
- `.claude/skills/deskops-workflow/references/vocabulary.md`: `(deskops inbox)` → `(deskops message)`.
- `tests/test_message_cli.py`: borrados los dos casos del alias (aviso de deprecado y equivalencia con `message list`); nuevo `test_retired_inbox_alias_is_an_unknown_command` (main devuelve 2). Docstring actualizado.
- `tests/test_message_delivery.py`: borrado `test_legacy_inbox_repo_tracks_only_in_target_store` (el caso equivalente con `message send --to` ya existe justo antes).

Nombrados en el Scope (precisiones del preflight) pero no en `files`:
- `deskops/data/faq.md`: copia empaquetada de docs/faq.md; mismas dos líneas.
- `README.md:227`: quitado "(`deskops inbox` is a deprecated alias)".
- Goldens: borrado `tests/fixtures/golden/help/deskops_inbox.txt`; regenerado `help/deskops.txt` (sale `inbox` de la lista). `.opencode/` no tenía usos.

Fuera de `files` y del Scope, tocados porque la eliminación del comando los rompía (lo pedido en las notas del coordinador):
- `tests/test_command_registry.py`: quitado `("inbox",)` de `MUTATING_COMMANDS`.
- `tests/test_cli_grammar.py`: quitado `"inbox"` del grupo `operational`.
- `tests/test_output_goldens.py`: quitada la captura de salida `inbox` (envío legado); borrados `tests/fixtures/golden/output/inbox.{json,text,yaml}`.
- `tests/test_cli.py`: el test de ayuda usa `message --help`; la lista de comandos del help top-level sin `inbox`; tres tests de envío/ack migrados a `message send --to` / `message ack <sel>` (mismas aserciones).
- `tests/test_inbox_promote_cli_gaps.py`: dos tests de `inbox --list --root/--desk-root` migrados a `message list` (mismo contrato de `--root` y precedencia de `--desk-root`).

Goldens revertidos: `--update-golden` también reescribió `help/deskops_{add,edit,list,show}.txt` (solo cambio de ajuste de línea por versión de Python) y borró como "stale" `output/{advance_lifecycle_seed_out_of_date,desk_update_legacy_migration,desk_update_nonterminal_migration,doctor_invalid_task,doctor_lifecycle_seed_out_of_date}.text` (los usan otros tests). Los restauré con `git checkout`; no están en el diff.

## Validación (validation.log)

- `! grep -rnw 'deskops inbox' docs .claude .opencode deskops/data README.md` → rc=0 (vacío).
- test_message_cli.py → 9 passed (la 1ª corrida falló por mi test nuevo, que esperaba SystemExit; `main` devuelve 2. Corregido y re-corrido).
- test_message_delivery.py → 5 passed.
- test_output_goldens.py → 7 passed.
- test_skill_cli_drift.py → 2 passed.
- test_cli_grammar.py → 2 passed.
- test_command_registry.py → 3 passed.
- test_inbox_promote_cli_gaps.py → 21 passed.
- test_cli.py → 102 passed.
- `python -m deskops inbox --list --root .` → rc=2, `invalid choice: 'inbox'` (done_when).
- Suite completa (`pytest -n 4 -q tests`) y comparación con origin/main: **no corrida, para el integrador** (orden del integrador wA:p1).

## Usos restantes de "deskops inbox" fuera de alcance (sin tocar; para que el coordinador los rutee)

- `deskops/cli/commands/message.py:39` docstring y `_run_legacy`: ahora es código muerto en la práctica (solo lo alcanza `deskops message` sin subcomando, que da "Provide a message or use send/list/read/ack."). Borrar `_run_legacy` y su docstring es limpieza de compatibilidad fuera de `files`.
- `tests/test_repo_identity.py:97`: docstring histórico que menciona `deskops inbox --ack`.
- `tests/test_inbox_promote_cli_gaps.py:4`: docstring que cita una nota de inbox antigua ("CLI gaps: inbox --root"); es histórico.
- `tests/e2e_agent/scenarios/inbox-to-task.yaml:16`: `deskops inbox list --root . || deskops list inbox-notes --root .` — la primera rama ahora falla y cae al `||`; conviene cambiarla a `deskops message list --root .`.
- `desk/` (atoms/tasks/drawer/inbox) no revisado ni tocado (prohibido por el encargo).

## Riesgos

- `message send` tiene `--kind` por defecto `suggestion` (el alias tenía `unclear`); la skill nombra el kind explícitamente, así que no cambia el comportamiento documentado.
- Archivos tocados fuera de `files` (listados arriba): el `files:` del TaskDoc debería ampliarse antes del closeout para que el diff coincida con lo declarado.
- `.sldb/*` y `runs/subagents/*` sucios en git status eran previos o de otras sesiones; no los toqué.
