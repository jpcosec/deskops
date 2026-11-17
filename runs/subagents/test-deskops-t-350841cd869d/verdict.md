# Veredicto — tester deskops-t-350841cd869d

Tarea: task-retirar-el-alias-deskops-inbox-docs-y-skills-pasan-a-deskops-message-y-se-borra-el-alias
Entrega: diff sin commitear + runs/subagents/exec-deskops-e-d5d217748798/. Evidencia propia: validation.log.

## Resultado: APROBADO

### done_when
- grep del contrato (`grep -rnw 'deskops inbox' docs .claude .opencode deskops/data README.md`) → vacío (rc=1).
- `python -m deskops inbox --list --root .` → `invalid choice: 'inbox'`, rc=2.
- Los 9 archivos de test pasan uno a uno (9+5+7+2+2+3+21+102+13), sin lock, PYTHONPATH al checkout.

### Diff contra el contrato
- `deskops/cli/registry.py`: borrado el Command `inbox` y las dos constantes que solo usaba (`ROOT_ARG_INBOX`, `PYTHONPATH_INBOX_ARG`); sin otros usos.
- Reemplazos de docs/skills: `deskops message send "<gap>" --kind unclear --root .`, `message list/read/ack`, `--to <repo>`, `--from`: todos los flags existen en `deskops message <sub> --help` (send: --title, --kind {unclear,suggestion}, --to, --from, --root; list/read/ack: --root, selector). Coincide con la precisión del preflight 1.
- docs/faq.md y deskops/data/faq.md siguen idénticos entre sí.
- Tests migrados conservan aserciones: test_cli.py (send --repo→--to, --ack→ack <sel>, misma verificación JSON/estado), test_inbox_promote_cli_gaps.py (mismo contrato --root y precedencia --desk-root, con `message list`), test_cli.py help (`message --help`, "read/ack selector").
- Cobertura borrada con equivalente: `test_legacy_inbox_repo_tracks_only_in_target_store` es la misma prueba que `test_send_to_registered_repo_tracks_only_in_target_store` (tests/test_message_delivery.py:180) con `message send --to`; aserciones idénticas. Los dos tests del alias en test_message_cli.py se sustituyen por `test_retired_inbox_alias_is_an_unknown_command`. La captura golden `inbox` de test_output_goldens.py duplicaba `message_send` (sigue en tests/test_output_goldens.py:593).
- `git status tests/fixtures`: solo `M help/deskops.txt` y `D help/deskops_inbox.txt`, `D output/inbox.{json,text,yaml}`. No quedó golden reescrito de más.

### Coincidencias restantes de `deskops inbox` (todas fuera de alcance o históricas, listadas por el ejecutor)
- deskops/cli/commands/message.py:39 — docstring de `_run_legacy` (código ahora muerto; limpieza fuera de `files`).
- tests/test_repo_identity.py:97 — docstring histórico.
- tests/e2e_agent/scenarios/inbox-to-task.yaml:16 — `deskops inbox list ... || deskops list inbox-notes`: no queda roto; la 1ª rama da rc=2 y cae al `||`. (Antes la 1ª rama era peor: `inbox list` habría enviado una nota con cuerpo "list".) Conviene cambiarla a `deskops message list --root .` en otra tarea.

## Riesgos / para el coordinador
1. `files:` del TaskDoc no cubre lo entregado (README.md, deskops/data/faq.md, tests/test_cli.py, test_cli_grammar.py, test_command_registry.py, test_inbox_promote_cli_gaps.py, test_output_goldens.py, goldens). Ampliar `files` antes de `closeout verify/commit`.
2. Suite completa (`pytest -n 4 -q tests`) no corrida (excluida por el encargo); queda para el integrador.
3. `_run_legacy` en message.py queda como código muerto: rutear su retirada.
VEREDICTO: APROBADO
