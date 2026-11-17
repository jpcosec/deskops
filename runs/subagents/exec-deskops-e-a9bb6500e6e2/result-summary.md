# Resultado del ejecutor deskops-e-a9bb6500e6e2: FASE 1 (reproducción)

- run_id: deskops-e-a9bb6500e6e2 (RunDoc run-deskops-e-a9bb6500e6e2, kind claude)
- session: scion://agent/deskops-e-a9bb6500e6e2 (sesión de Claude Code; no tengo la ruta de un session.jsonl para calcular session_sha256)
- tarea: task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos (task.debug)
- fase: 1 de 2. No toqué código ni tests, no commiteé nada.

## Qué escribí

- Logs y scripts de la reproducción: `runs/subagents/repro-llaves-20261117/` (`repro-<caso>.log`, `sbx.sh`, `ab.sh`, `c.sh`).
- Desks sandbox: `.tmp/repro-llaves/<caso>/` (ignorado por git; cada uno es `git init` + `deskops init`).
- El único write a desk/ del checkout real: `deskops review record … --kind reproduction` →
  `review-…-reproduction-1` (verdict pending), es decir `desk/reviews/<tarea>/reproduction-1.md` y
  `.sldb/core/documents/ReviewDoc/…-reproduction-1.yaml`, más los cambios del store que esto arrastra
  (`.sldb/core/models/ReviewDoc.yaml`, `store_index.yaml`, `store.yaml`). input_sha256 2d3d07d1e77d….
- Evidencia de este run: `task.txt`, `board.txt`, `git-status.txt`, `validation.log`, `review-record.txt`, este archivo.
- `git-status.txt` también muestra archivos `task-se-retiran-del-drawer-…` y `runs/subagents/node-*`, que no son míos (son de otra sesión).

## Reproducción y origen de cada caso

Todas las corridas usan el checkout (`PYTHONPATH=/mnt/ssd/proyectos/SLDB_1/deskops`, `TMPDIR=/dev/shm`). La tarea es task.external
con una URL en references, para que verify y commit tengan un gate mínimo.

### (a) `closeout verify` escribe recibos: se reproduce. Origen: **deskops**

`repro-a.log`: con el árbol limpio, después de `deskops closeout verify --task …` (rc=0) quedan
`.sldb/core/documents/ReviewDoc/`, `desk/reviews/` y `.sldb/{store.yaml,store_index.yaml,models/ReviewDoc.yaml}` sin commitear.
Esto lo hace `deskops/cli/commands/closeout.py:87`, que llama a `verify(..., write_receipts=True)` y de ahí a
`closure._write_evidence_receipts` (`closure.py:1079`).

**Ambigüedad del contrato: el coordinador tiene que decidir antes de la FASE 2.** Hoy el contrato pide que verify
"no escriba nada (ni ReviewDoc ni desk/reviews), como dice su ayuda", pero eso choca con el diseño vigente:
- El gate de `closeout commit` es la regla `rule-closeout-<tipo>`, que pide un recibo evidence aceptado e intacto "(lo escribe
  deskops closeout verify)". Lo muestra `repro-b-*`: sin verify previo, commit se bloquea con
  "Run 'deskops closeout verify --task …' to write the evidence receipts the rule asks for". Log de esa corrida (modo
  noverify): `runs/subagents/exec-deskops-e-a9bb6500e6e2/repro-b-noverify.log`, que no está entre las evidencias del recibo.
- `tests/test_closeout_evidence_receipts.py` (CC33a) afirma que verify escribe un recibo por cada tipo de evidencia declarado.
- La ayuda de verify dice "Check … without committing", es decir, que no commitea. No dice que no escriba nada.

Si verify deja de escribir, hay que mover a otro sitio la escritura de los recibos (por ejemplo, que `closeout commit` los escriba dentro de
su propio commit) y reescribir los tests de CC33a. Eso sale del `files:` de la tarea y del mensaje de la regla.
La otra lectura posible es que el arreglo de (a) sea solo de texto: la ayuda de verify pasaría a decir que escribe recibos sin commitearlos.
No elijo ninguna de las dos: es decisión del coordinador.

### (b) `--reason` con llaves en `closeout commit`: se reproduce. Origen: **deskops**

Causa: `deskops/services/closure.py:857` hace `success_line.format(commit=…)` sobre una f-string que ya trae `{reason}` interpolado
(líneas 199/271/409/531; la 652 interpola `rel_run_dir`). El commit se crea antes de imprimir esa línea.

| caso | reason | trailer Closeout-Reason en el commit | salida / rc |
|---|---|---|---|
| b-1-open | `cierre {a}` | byte a byte | `Missing required field: 'a'`, rc=1 **después** de commitear |
| b-2-open | `cierre {{a}} docker {{.State}}` | byte a byte | rc=0, pero imprime `cierre {a} docker {.State}` (llaves a la mitad) |
| b-3-open | `cierre {{{a}}}` | byte a byte | `Missing required field: 'a'`, rc=1 tras commitear |
| b-1-close | `cierre a}` | byte a byte | `Invalid value: Single '}' encountered in format string`, rc=1 tras commitear |
| b-2-close | `cierre a}}` | byte a byte | rc=0, imprime `cierre a}` |
| b-3-close | `cierre a}}}` | byte a byte | `Single '}'…`, rc=1 tras commitear |

El mensaje del commit es correcto en todos los casos. Lo que falla es la línea de éxito: con un número impar de llaves de apertura o de cierre seguidas,
el comando da rc=1 aunque el commit ya está hecho; con un número par, imprime el reason alterado.

Proyección sin commitear: es un problema aparte de las llaves.
- `repro-b-reverify-plain.log` (reason `cierre simple`, rc=0) y `repro-b-reverify.log`: verify, commit de los recibos,
  cambio de references, un segundo verify (escribe evidence-external-2) y luego `closeout commit --paths seed.txt`. El ReviewDoc
  de `.sldb` entra en el commit, porque el cierre hace `git add -A -- .sldb`, pero
  `?? desk/reviews/<tarea>/evidence-external-2.md` queda fuera. Es el mismo síntoma de la nota de scion.
- `repro-b-uncommitted.log`: un solo verify sin commitear seguido del cierre deja `?? desk/reviews/` igual.
- Si los recibos ya estaban commiteados (modo verify), el árbol queda limpio.

### (c) llaves en `edit task` y `message send`: se reproduce. Origen: **sldb**

Probé con `deskops --debug`, y los tracebacks completos están en los logs. Resultados:
- Una llave de apertura (`{a}`) y una, dos o tres de cierre (`a}`, `a}}`, `a}}}`) se guardan tal cual, rc=0.
- Dos o tres de apertura (`{{a`, `{{{a`, `docker inspect --format {{.State.Health.Status}}`,
  `this is not valid json {{{`) dan `TemplateSyntaxError`, rc=3, en edit task y en message send. El documento no cambia y no se crea la nota.
- Además hay un caso peor, sin error (`repro-c-jinja-eval.log`): `valor {{ 7*7 }} y {# oculto #} fin` se guarda como
  `valor 49 y  fin`, con rc=0, en el scope de la tarea y en el cuerpo de la nota. Se pierde texto sin que nada avise.

Cómo determiné el origen con la regla (2) del coordinador:
- La cadena de llamadas es `deskops/doc_access.py:404 write_doc` (o `deskops/cli/commands/message.py:109`) →
  `sldb/runtime/validation.py:68 render_model_markdown` → `sldb/core/renderer.py` →
  `/mnt/ssd/herramientas/sldb/src/sldb/core/renderer_engine/base.py:34 replace_markers`.
- `replace_markers` sustituye los valores de los marcadores dentro del texto fuente y después compila ese resultado con
  `jinja_env.from_string(source).render(**data)`. Por eso el valor del usuario se interpreta como Jinja.
- Los frames que quedan por debajo son de jinja2 (site-packages) y el `<unknown>` de la plantilla. jinja2 es una
  dependencia de sldb; deskops no importa jinja2 (`grep -rn jinja deskops/` no da nada).
- Si se lee la regla al pie de la letra, el frame más interno es de jinja2, no de sldb ni de deskops. El último frame de código propio
  es sldb (`/sldb/` bajo `src`), así que el origen es **sldb**. Si el coordinador entiende la regla de otra forma, conviene que lo diga.

## Para la FASE 2 (cuando el coordinador diga "sigue")

- (b): escapar el reason o formatear con concatenación en lugar de `.format` en `closure.py`, y añadir la proyección
  `desk/reviews/<tarea>/` a las rutas del commit de cierre. Tests en `tests/test_closeout.py`.
- (c): `deskops message send --to sldb` con la reproducción mínima, y un xfail(strict=True) en `tests/test_message_cli.py` cuyo reason
  sea el nombre de archivo que imprima message send. El contrato pide la nota antes del test; escribe en el inbox del repo sldb.
- (a): depende de la decisión de arriba.
- Validation: `tests/test_closeout.py`, `tests/test_message_cli.py`, `tests/test_output_goldens.py`. La suite completa queda
  **para el integrador**, según el brief.

## Riesgos

- Si en (a) se quita la escritura de verify sin moverla a otro sitio, `closeout commit` deja de poder cerrar cualquier tarea con regla de cierre.
- Tal como está el diseño, la proyección sin commitear de (b) y los recibos de (a) son el mismo problema visto desde los dos extremos:
  verify escribe y commit no incluye `desk/reviews`.

---

# FASE 2: arreglo (orden del coordinador: reproducción aceptada; (a) solo texto, (b) arreglo, (c) nota a sldb + xfail)

## Archivos tocados

| archivo | en `files:` | por qué |
|---|---|---|
| `deskops/services/closure.py` | sí | (b) la línea de éxito llena solo su `{commit}` inicial con `str.replace(..., 1)` en lugar de `str.format`, así el reason (y un `{commit}` literal dentro de él) sale intacto y no hay rc=1 después de commitear; además el cierre agrega `desk/reviews/<tarea>/` (la proyección de los recibos de verify) a su propio commit, junto al `.sldb` que ya agregaba. |
| `tests/test_closeout.py` | sí | (b) `test_closeout_commit_keeps_braces_in_the_reason_byte_for_byte` (7 variantes: 1/2/3 llaves de apertura y de cierre, `{commit}` literal: trailer byte a byte, primera línea impresa exacta, rc 0) y `test_closeout_commit_folds_the_verify_receipt_projection_into_the_closing_commit` (desk real con store, task.external, verify deja `?? desk/reviews/`, el cierre con `--paths` lo commitea y el árbol queda limpio). Los 8 fallan con el closure.py de HEAD y pasan con el arreglo. |
| `tests/test_message_cli.py` | sí | (c) `test_message_send_keeps_braces_in_the_body_literal`, `xfail(strict=True, reason=<nombre de la nota>)`, 4 variantes (formato Go, `{{a`, `{{{`, pérdida silenciosa `{{ 7*7 }}`/`{# #}`); + `import pytest`. |
| `deskops/cli/registry.py` | **no** | (a) la ayuda de `closeout verify` vive en el registro, no en `deskops/cli/commands/closeout.py` (que está en files y no toqué): ahora dice que escribe los recibos de evidencia sin commitearlos, y un párrafo `Writes:` explica dónde y que `closeout commit` los lee como gate y los mete en su commit. **También `mutates=False → True`** para verify: escribe store y desk, y la regla del integrador del brief pide declararlo; consecuencia: sin `--root` explícito verify respeta el sandbox de test igual que `closeout commit` (antes podían divergir). Si el coordinador prefiere solo texto, revertir esa línea y la de abajo. |
| `tests/test_command_registry.py` | **no** | `("closeout", "verify")` en `MUTATING_COMMANDS`, por el cambio de arriba. |
| `tests/fixtures/golden/help/deskops_closeout.txt`, `deskops_closeout_verify.txt` | **no** | goldens de ayuda regenerados a mano con `COLUMNS=80 deskops <cmd> --help` (no corrí `--update-golden` global); el diff es solo el texto nuevo. |

Fuera del repo: la nota a sldb `/mnt/ssd/proyectos/SLDB_1/sldb/desk/inbox/20261117-015212-suggestion-render-model-markdown-interpreta-como-jinja-el-valor-de-los-campos-llaves-dobles-rompen-expresiones-se-evaluan.md` (trackeada en el store de sldb por `message send`; sin commitear allá). La nota no puede llevar llaves dobles literales (pasa por el mismo render), así que usa la notación LL/LLL/RR/L#, explicada en la nota. Salida de message send: `message-send.txt`.

## (c) decisión aplicada

Origen sldb: no se toca deskops; queda el xfail estricto con reason = nombre de archivo de la nota (`SLDB_JINJA_VALUE_NOTE`). Cuando sldb lo arregle, el XPASS estricto hará fallar el test y avisa que hay que quitar el xfail. `edit task` comparte el mismo camino (`doc_access.write_doc → render_model_markdown`) y no lleva test propio en deskops (test_message_cli.py es el archivo que el contrato asigna a (c)).

## Comprobación de punta a punta

`after-fix-b-reverify.log`: el escenario de la nota de scion (verify, recibos commiteados, references cambiadas, segundo verify sin commitear, `closeout commit --no-run --reason 'cierre {{{a}}} y a}' --paths seed.txt`) da rc=0, imprime el reason intacto, el trailer es byte a byte, `evidence-external-2.md` entra en el commit y el árbol queda limpio.

## Validación

Ver `validation.log` (sección FASE 2). Suite completa: **para el integrador** (brief).

| comando | resultado |
|---|---|
| tests/test_closeout.py | 70 passed, rc 0 |
| tests/test_message_cli.py | 9 passed, 4 xfailed (strict), rc 0 |
| tests/test_output_goldens.py | 7 passed, rc 0 (regresión de salidas, 17 min con load ~36) |
| tests/test_command_registry.py | 3 passed, rc 0 |
| tests/test_cli_grammar.py | 2 passed, rc 0 |
| tests/test_closeout_evidence_receipts.py | 5 passed, rc 0 (CC33a: verify sigue escribiendo recibos) |
| suite completa `-n 4 tests` | **no corrida: para el integrador** (orden del brief) |

## Riesgos

- `mutates=True` en verify (ver tabla de archivos): cambio de comportamiento solo cuando no se pasa `--root` y hay sandbox de test configurado.
- El cierre ahora commitea todo lo que haya sin commitear bajo `desk/reviews/<tarea>/`, también en supersede/resolved-by/retire (el camino de commit es común). Es lo que pide "el cierre no deja archivos sin commitear", pero incluye cualquier archivo que alguien haya dejado a mano en esa carpeta.
- La nota en el repo sldb queda sin commitear allá (la commitea quien trabaje en sldb).
