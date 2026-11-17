# Veredicto del tester deskops-t-806c1355739d

Tarea: `task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible`
Entrega revisada: cambios sin commitear en `deskops/services/review.py` y `tests/test_review_command.py` (ejecutor deskops-e-2ea9647a5250).
Evidencia: `validation.log`, `manual-run/`, `isolation-probe.txt` e `isolation-control.txt`.

## Resultado: APROBADO

### Contrato frente a la entrega
- **Rama claude** (`review.py:219-239`). Usa `-p` (y quita un `--print` duplicado del perfil), el `--model` del perfil y `--system-prompt` con el prompt del perfil o, si no hay, SYSTEM. Agrega los flags de aislamiento. El input va por stdin (`subprocess.run(input=...)`), nunca como `@ruta`. Cumple el goal y las precisiones del preflight.
- **Rama pi.** `_argv` no cambió, y `input=None` equivale a la llamada anterior. Lo cubre `test_pi_profile_argv_is_unchanged`.
- **Default.** `DEFAULT_ENGINE` sigue siendo `runtime-pi-deepseek-flash`.
- **Manifest.** Registra `binary`, `model`, `input_delivery`, `isolation_flags` y un `selection_reason` según la rama. Lo comprobé en la corrida real.
- **Done when.** El test del argv claude pasa. La corrida real deja un recibo con `technical_ok` y un ReviewDoc con el engine del perfil claude, y su output trae REFORMULACION, AMBIGUEDADES y DRY-RUN.

### Aislamiento
- Los 6 flags de CLAUDE_ISOLATION existen en el claude instalado (2.1.326, según `claude --help`).
- **Prueba empírica, desde el checkout real con haiku:**
  - Con los flags, el modelo dice no ver CLAUDE.md, AGENTS.md, MEMORY.md, tools ni skills.
  - Corrida de control sin `--setting-sources ""` ni `autoMemoryEnabled:false`: el modelo cita la primera línea del CLAUDE.md global, la del AGENTS.md y una entrada de MEMORY.md.
  - Los flags son, por lo tanto, necesarios y suficientes para lo que pide el contrato.

### Rechazo sin --model y recomendación del ejecutor
- **Rechazo de un perfil claude sin `--model`** (`review.py:230`). Es correcto: evita revisar en silencio con el modelo por defecto de claude, y el mensaje dice cómo arreglarlo.
- **Perfil aparte para el revisor.** Comparto la recomendación de no editar `desk/runtimes/runtime-claude.md`. Ese perfil lo usa el lanzamiento de roles claude: agregarle `--model haiku` forzaría haiku en todos ellos, y su `--append-system-prompt` y su `system_prompt_delivery: file` sirven a roles, no al revisor. Lo recomendable es crear un perfil `runtime-claude-haiku-reviewer`. Lo validé en el sandbox con `deskops add runtime-profile --from-yaml`.
- **Choque con el done_when literal.** El done_when habla de un recibo con "engine runtime-claude". En el desk real, `--engine runtime-claude` hoy se rechaza. Tiene que decidirlo el coordinador antes del closeout.

### Tests (sin lock, PYTHONPATH al checkout)
| Archivo | Resultado |
|---|---|
| `test_review_command.py` | 25 passed |
| `test_review_doc.py` | 19 passed, 1 xfailed |
| `test_review_record.py` | 21 passed |
| `test_command_registry.py` | 3 passed |

Contra HEAD, los 4 tests nuevos fallan; el e2e lo hace con `KeyError: 'binary'`. Prueban el cambio de verdad.

### Riesgos menores (no bloquean)
1. **Override del aislamiento** (`review.py:237`). La deduplicación `if flag[0] not in argv` deja que el perfil anule un flag de aislamiento: por ejemplo, `--tools Read` en `extra_args` omite el `--tools ""`. Aun así, el manifest (`review.py:253`) registra siempre CLAUDE_ISOLATION completo y puede decir algo que no pasó. Además, una forma `--flag=valor` no se detecta y el flag se pasa dos veces. Hoy ningún perfil lo hace.
2. **Suite completa sin correr.** Ni el ejecutor ni yo corrimos la suite completa (el brief lo excluye). Queda pendiente para el integrador, como pide la Validation de la tarea.
3. **Avisos en stderr.** El aviso de vencimiento del login de claude cae en `stderr.log` y no afecta `technical_ok`.

### Nota de método
Además de la única corrida de `review preflight` con haiku, hice 2 llamadas directas a `claude -p --model haiku` sin tools ni sesión, como sonda y como control del aislamiento (punto 2 del brief). Borré el sandbox y las copias de `/dev/shm`.

VEREDICTO: APROBADO
