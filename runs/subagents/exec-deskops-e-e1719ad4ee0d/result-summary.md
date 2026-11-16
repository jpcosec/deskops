# Resultado del ejecutor deskops-e-e1719ad4ee0d

- run_id: run-deskops-e-e1719ad4ee0d
- task: task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp
- session: scion://agent/deskops-e-e1719ad4ee0d (agente claude, sesión fresca)
- session_sha256: (no disponible desde dentro de la sesión)

## Qué cambió

Archivos tocados (ambos en `files` de la tarea), solo vía CLI de sldb:

- `.sldb/core/store_index.yaml`: sin la entrada `stores: spec2viz -> ../spec2viz/.sldb` (y `store_hash` recalculado por sldb). Lo escribió `sldb stores remove spec2viz --store .sldb`.
- `.sldb/store.yaml`: sin la entrada `links: spec2viz -> ../spec2viz/.sldb`. Lo escribió `sldb stores declare --store .sldb --write`.

Los enlaces sldb, pron y scion no cambian. Las líneas `include:` de RunDoc que muestra `git diff .sldb/store.yaml`
(exec-deskops-e-79646a51295e, test-deskops-t-ce38955d8076, exec-deskops-e-e1719ad4ee0d) ya estaban sin commitear
antes de empezar (las agregaron otras sesiones al despachar los runs); no son de esta tarea y el integrador debe
dejarlas fuera del commit de la tarea o commitearlas aparte.

No se tocó ningún otro archivo fuera del run dir. Ningún test se modificó.

## Hallazgo sobre el CLI de sldb (importante para el integrador y para sldb)

`sldb stores remove` solo edita `.sldb/core/store_index.yaml`; deja la declaración `links:` de `.sldb/store.yaml`
intacta. Pasó en vivo: tras el primer `remove` (17:06), otra sesión regeneró el índice desde `store.yaml` y el enlace
reapareció (mtime de store_index 17:06:16, sin intervención mía). La secuencia que deja ambos de acuerdo es
`sldb stores remove spec2viz` + `sldb stores declare --write` (verifiqué antes, cargando ambos YAML, que la
declaración que escribe `declare` difiere de la de `store.yaml` solo en el enlace spec2viz). Tras eso, 60 s de
vigilancia sin reaparición (ver `remove.txt`). Es un hueco de sldb (remove debería actualizar también la
declaración); queda anotado aquí para que el coordinador lo lleve al inbox de sldb (el brief no me permite escribir
fuera del scope).

## Herencia (precisión 6)

`grep '../spec2viz' .sldb/core/models` no encuentra nada. La única mención de spec2viz en modelos es la etiqueta
`system.spec2viz` de `ViewDoc.yaml` (model_ref `sldb.models.notation_models:ViewDoc`), que según la precisión (1) del
bundle-1 no se toca. `sldb stores remove` no rechazó (ningún modelo con origin spec2viz).

## Validación

Ver `validation.log` y los archivos antes-/despues-*.txt.

| Comando | Resultado |
|---|---|
| `sldb stores list --store .sldb` | pron, scion, sldb; sin spec2viz (antes: con spec2viz) |
| `sldb stores check --store .sldb` | rc=0; 224 líneas antes y después; 0 nuevas, 0 desaparecen |
| `deskops doctor --root .` | rc=0; 226 líneas antes y después ("Desk is healthy, with 220 alert(s)"); 0 nuevas, 0 desaparecen |
| `deskops graph missing --root .` | rc=1 antes y después; "37 missing" en ambos; 0 nuevas, 0 desaparecen (el hallazgo preexistente sobre .sldb/store.yaml no cuenta como nuevo) |
| `pytest -q tests/test_migrate_desk_stores.py` | 16 passed |
| tests que leen el `.sldb` real (ver abajo) | ver `pytest-stores.txt` |
| suite completa `pytest -n 4 -q tests` | NO corrida por orden del brief: **para el integrador** |

Comparación por conjunto de líneas (`comm` sobre `sort -u`) entre antes-*.txt y despues-*.txt.

Tests extra (de a un archivo, sin lock), elegidos porque leen el store real o sus índices:
- tests/test_doctor_model_registration.py: 8 passed
- tests/test_desk_sync.py: 8 passed
- tests/test_doctor_absolute_paths.py: 13 passed
- tests/test_domain_tree.py: 9 passed
- tests/test_model_contract_snapshot.py: 2 passed
- tests/test_task_types.py: 16 passed

Ningún test de `tests/` afirma sobre el enlace spec2viz del store real: las menciones a spec2viz en tests
(`test_doctor_absolute_paths.py`, `test_message_ecosystem_registry.py`, `test_migrate_desk_stores.py`) usan
sandboxes en tmp_path. No hubo tests rotos legítimamente, así que no hizo falta el worktree de origin/main.

## Riesgos

- Si otra sesión con el índice viejo en memoria reescribe `store_index.yaml` antes del commit, el enlace podría volver
  en el índice; `store.yaml` ya no lo declara, así que una regeneración desde la declaración ya no lo reintroduce.
  Revisar `git diff .sldb/core/store_index.yaml` al integrar.
- `store_hash` en store_index.yaml cambia con cualquier escritura concurrente; es esperable.
