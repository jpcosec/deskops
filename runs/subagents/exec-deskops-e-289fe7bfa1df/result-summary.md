# Resultado del ejecutor deskops-e-289fe7bfa1df

Tarea: `task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r`

## Qué cambió

- `deskops/services/review.py`
  - `_task_contract_text(markdown)`: reutiliza `deskops.runtime.scion.task_contract_sha256` (el digest sldb de `TaskDoc.__contract__`; precisión 1 y 2). Import diferido. Si la tarea no parsea devuelve `None` y el estado vuelve a la comparación de siempre.
  - `_preflight_input` / `_bundle_input` aceptan `task_text=` (solo keyword): si se pasa, reemplaza el texto del TaskDoc **en la misma posición** con la misma serialización `Bundle` de hoy (precisión 5). Sin el argumento el input queda byte a byte igual, así que `input.md` y el `input_sha256` registrado no cambian.
  - `_contract_sha(mode, task_path, task_id)`: sha256 del input preflight/bundle con el TaskDoc reemplazado por su `contract_sha256`. Para bundle, pills, átomos, rituales y archivos de `files` siguen entrando como hoy.
  - `run_task` → `_run_one` → `_write_review` guardan ese valor en el nuevo campo `contract_sha256` del ReviewDoc (solo preflight/bundle de modelo; los recibos de `record` y de `node` lo dejan vacío).
  - `_state_for_key(key, input_data, contract_sha="")`: un recibo con `contract_sha256` es vigente si coincide con el digest actual; un recibo sin ese campo (los viejos, `record`, `node`) sigue comparando `input_sha256` como hoy (precisión 3). La agregación accepted > rejected > pending > incomplete no cambia (precisión 4). `_status_task` y `_input_for_key` (status sin target) pasan el digest; los nodos de plan pasan "".
- `deskops/models/review.py`: campo opcional `contract_sha256` (vacío por defecto, validado como 64 hex o vacío), línea en el `__template__`, y el validador `before` lo trata como ausente en recibos viejos (igual que `fact`/`value`).
- `tests/test_review_command.py`: tres tests nuevos en sandbox `tmp_path` con fake pi:
  - `test_receipts_record_the_task_contract_digest`: preflight y bundle guardan `contract_sha256` (hex, distinto del input_sha256).
  - `test_edited_tags_and_status_keep_accepted_receipts_and_goal_stales_them`: con preflight y bundle aceptados, `edit task tags` + `deskops advance task` (cambia status, current_node, history y la cabecera sldb; la regla de activación lo deja pasar con anchor intact) → ambos siguen `accepted`; `edit task goal` → ambos `stale` (paso 4 de la Implementation Path).
  - `test_bundle_state_still_follows_the_linked_files`: cambiar un archivo de `files` deja bundle `stale` y preflight `accepted`.
- `tests/fixtures/model_contract_hashes.json` (**fuera de `files`**): el hash de contrato de ReviewDoc cambia al agregar el campo autorizado por la precisión 3 (`e389118d…` → `f16882ab…`); `tests/test_model_contract_snapshot.py` falla si no se actualiza. Mismo precedente que CC33a (fact/value).

## Validación (validation.log)

- `pytest -q tests/test_review_command.py` → 29 passed, rc=0
- `pytest -q tests/test_review_doc.py` → 22 passed, 1 xfailed, rc=0
- Extra: `test_model_contract_snapshot.py` 2 passed; `test_review_record.py` 21 passed; `test_closeout_evidence_receipts.py` 5 passed; `test_activation_rules.py` 10 passed.
- `deskops review status <esta tarea> --root .` en el desk real (solo lectura): preflight accepted, bundle stale (recibos viejos sin `contract_sha256`; los archivos de `files` cambiaron con esta entrega, así que es lo esperado).
- **Para el integrador**: la suite completa (`pytest -n 4 -q tests`) no la corrí por orden del brief.

## Riesgos y notas para el integrador

1. **Cambio de contrato de modelo ReviewDoc**: requiere regenerar `.sldb` con el CLI (`sldb stores update` + `stores build`), como en CC33a. No toqué `.sldb/` (prohibido por el brief). CHANGELOG no tocado (fuera de alcance).
2. **Done When en el desk real**: los recibos existentes no tienen `contract_sha256` y siguen con la comparación de antes; solo los recibos escritos desde ahora con `deskops review preflight|bundle` sobreviven a ediciones de tags/status. La prueba "tarea con recibos aceptados y tags editados da accepted" está hecha en sandbox; en el desk de deskops se observa con la primera tarea que se revise después de integrar.
3. Decisión de lectura: para preflight, el campo guarda el sha del input preflight con el TaskDoc reemplazado (no el `contract_sha256` puro), por simetría con la precisión 5 del bundle; equivale al contrato porque el resto del input preflight es la instrucción fija con el id de la tarea.
4. El atajo "unchanged" de `review preflight|bundle` (no re-correr si el input no cambió) sigue usando `input_sha256`; no entra en alcance (Scope: el input_sha256 sigue igual).
5. Coordinación: la tarea de ids de nodo con punto commiteó sus cambios en `deskops/models/review.py` y tests durante esta corrida (9dbcfc7c); mi diff queda encima sin conflicto.
