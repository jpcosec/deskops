# Resultado: task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible

- run_id: run-deskops-e-2ea9647a5250
- session: scion://agent/deskops-e-2ea9647a5250 (session_sha256: no disponible desde dentro de la sesión)
- Ejecutor: claude (Opus 5.5), robocop2, sin commit.

## Cambios (todos dentro de `files`)

### deskops/services/review.py
- `_command(engine, input_path, input_data)` nuevo: elige la rama según el perfil (`kind: claude` o binario `claude` → claude; si no, pi) y devuelve el argv, el stdin y los datos del manifest.
- La rama pi (`_argv`) no cambia: `pi <extra_args> [system_prompt_flag prompt] @<input.md>`, sin stdin.
- `_claude_argv` nuevo: `claude -p <extra_args sin -p/--print> --system-prompt <prompt del perfil o SYSTEM> <aislamiento>`. El input va por **stdin** (`subprocess.run(input=...)`), nunca como `@<ruta>`.
  - Modelo: RuntimeProfileDoc no tiene un campo `model`, así que el perfil lo trae en `extra_args` (`--model haiku`), igual que el perfil de pi. Un perfil de claude sin `--model <m>` se **rechaza** con DomainError, para no revisar en silencio con el modelo por defecto de claude.
  - Se usa `--system-prompt` (reemplaza el prompt), no el `--append-system-prompt` del perfil, para que el revisor quede aislado.
  - `CLAUDE_ISOLATION`, con los flags sacados de `claude --help` (claude 2.1.326 en robocop2): `--tools ""`, `--no-session-persistence`, `--strict-mcp-config`, `--disable-slash-commands`, `--setting-sources ""`, `--settings '{"autoMemoryEnabled":false}'`. Lo probé a mano antes de fijarlos: sin `--setting-sources ""` el modelo ve el CLAUDE.md del usuario y el AGENTS.md; sin `autoMemoryEnabled:false` ve el MEMORY.md; con los dos flags no ve ninguno. No usé `--bare` porque exige ANTHROPIC_API_KEY, y en robocop2 la autenticación es OAuth.
- manifest.json ahora registra `binary`, `model`, `input_delivery` (file|stdin), `isolation_flags` y un `selection_reason` según la rama. Con pi, `model` sigue siendo la constante MODEL y `isolation_flags` son los `--no-*`/`--offline` de `extra_args`.
- El default sigue siendo `runtime-pi-deepseek-flash`.

### tests/test_review_command.py (4 tests nuevos, usan un `claude` falso en PATH; no llaman al modelo)
- `test_claude_profile_argv_is_isolated_print_mode_without_input_path`: el argv tiene -p, `--model haiku`, `--system-prompt SYSTEM`, `--tools ""` y los flags de aislamiento; no tiene `@<ruta>` ni la ruta del input; el stdin lleva el input.
- `test_claude_profile_without_model_is_refused`.
- `test_pi_profile_argv_is_unchanged`.
- `test_preflight_with_claude_engine_sends_input_on_stdin_and_records_it`: de punta a punta en un desk tmp_path. Crea el perfil con `deskops add runtime-profile --from-yaml` y comprueba: manifest (binary/model/profile/input_delivery/isolation_flags), receipt technical_ok, input recibido por stdin y ReviewDoc con engine.

## Validación
- `pytest -q tests/test_review_command.py`: 25 passed, rc=0.
- `pytest -q tests/test_review_doc.py` (solo se corre, sin modificarlo): 19 passed, 1 xfailed, rc=0.
- Suite completa (`-n 4 tests`): **no corrida**, por orden del integrador wA:p1. Queda **para el integrador**, así que no tengo lista de fallas comparada con origin/main.
- Corrida manual (paso 4), en un desk sandbox en /dev/shm con git init + deskops init (ya borrado): `deskops review preflight task-contar-lineas --engine runtime-claude --run manual-claude --root .` dio rc=0. Imprimió `run_dir: runs/subagents/manual-claude/context-review/task-contar-lineas/preflight/9a9dbe11…/attempt-1`.
  - Recibo con technical_ok=true.
  - ReviewDoc con `engine: runtime-claude`.
  - output.md trae REFORMULACION, AMBIGUEDADES y DRY-RUN (y FUTURO).
  - Copia en `manual-run/`: manifest.json, output.md, receipt.json, stderr.log, input.md, review-preflight-1.md, runtime-claude.md y command-output.txt.
  - En el sandbox runtime-claude no existía: lo creé con `deskops add runtime-profile --from-yaml` y le puse el modelo con `deskops edit runtime-profile runtime-claude extra_args "[--print, --model, haiku]"`. No usé `--model-flag --model` por CLI porque argparse rechaza un valor que empieza con guion.

## Riesgos y decisiones para el integrador
1. **No toqué `desk/runtimes/runtime-claude.md` del desk real**, porque el brief prohíbe tocar desk/. El scope, en cambio, permitía completarlo. Ese perfil no tiene `--model`, así que hoy `deskops review ... --engine runtime-claude` en el desk real se rechaza con un mensaje claro. **Ojo:** runtime-claude también lo usa el lanzamiento de roles claude. Si se le agrega `--model haiku` a sus `extra_args`, todos los roles claude que se lancen con ese perfil quedarían forzados a haiku (este ejecutor incluido). Recomiendo un perfil aparte, por ejemplo `runtime-claude-haiku-reviewer` con `extra_args: [--print, --model, haiku]`, y no editar runtime-claude. Esa decisión le toca al coordinador.
2. `--setting-sources ""` también deja fuera los permisos y hooks del usuario. En el revisor no importa, porque corre sin tools.
3. claude imprime avisos (vencimiento del login, reglas de permisos) en stderr; quedan en stderr.log y no afectan technical_ok.

## Archivos tocados
- deskops/services/review.py
- tests/test_review_command.py
- runs/subagents/exec-deskops-e-2ea9647a5250/* (evidencia)
- Los cambios en `.sldb/` y los `runs/subagents/2026*` sin seguimiento ya estaban al empezar; no son míos.
