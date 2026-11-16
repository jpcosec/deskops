# result-summary: exec-deskops-e-312954356a7f

- run_id: run-deskops-e-312954356a7f
- task: task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc
- session: scion://agent/deskops-e-312954356a7f (agente claude; sin archivo de sesión local) · session_sha256: (no disponible)

## Cambios

- `deskops/services/closure.py` (en files):
  - Nuevas funciones de módulo `target_covers(target, path)` y `_normalize_target_path`: rutas POSIX relativas tal como están escritas (sin `./` inicial, sin barra final, sin resolver symlinks, sensibles a mayúsculas). Hay cobertura si son iguales o si `path` empieza con `target + '/'`. El directorio no tiene que existir.
  - `_changed_file_link_evidence`: se quitó el `return` temprano cuando el archivo cambiado no es nodo del grafo (un archivo bajo un directorio target casi nunca lo es) y se añadió la cobertura por directorio: evidencia `materialization:<id>-><path>`.
  - `_directory_materialization_targets` (cacheado por graph_context) y `_materialization_target_identity`: el grafo de sldb no crea nodo para un target directorio (`declared_target_nodes` exige `is_file()`), así que esa materialization queda en `invalid_materializations` por `missing_declared_target`. Se acepta para la cobertura por prefijo solo si su ÚNICO faltante es su propio `target_identity` (leído del frontmatter del documento). Si falta otra cosa (p. ej., un source atom inexistente), sigue siendo inválida.
- `tests/test_materialization_targets_outside_package.py` (en files):
  - Test parametrizado de `target_covers`: `pkg/sub` cubre `pkg/sub/a.py` y no cubre `pkg/subzero.py`; también cubre barra final, `./`, mayúsculas, igualdad y target vacío.
  - Test de integración `test_closeout_verify_covers_files_under_a_directory_target`: `closeout verify` con una materialization de target `pkg/sub` ya no reporta `missing_changed_file_link` para `pkg/sub/a.py`, sí lo reporta para `pkg/subzero.py` y la evidencia nombra la materialization.
  - `_cli` ahora antepone la raíz del checkout a `PYTHONPATH`. Motivo: con cwd en el repo sandbox, `python -m deskops` importaba la copia instalada en `/mnt/ssd/herramientas/deskops` y no el código bajo prueba. Con eso el test nuevo fallaba aunque el cambio era correcto. Afecta a todos los tests del archivo, que siguen pasando (17/17).

No toqué archivos fuera del campo files, salvo la evidencia de esta carpeta.

## Paso 4: nota a sldb

`deskops graph missing` en el desk sandbox (`.tmp/deskops-dir-target`, ya borrado) con target directorio falló con rc=1 (ver `graph-missing-sandbox.log`):

```
- missing_declared_target: materialization:materialization-pkg-sub -> pkg/sub
  reason: declared target was not found among extracted graph nodes
```

Nota enviada con `deskops message send --to sldb --kind suggestion`, título "declared_target_nodes: aceptar un directorio como target declarado", y en el cuerpo la salida y el caso.
- id: `20261116-054845-suggestion-declared-target-nodes-aceptar-un-directorio-como-target-declarado`
- ruta: `/mnt/ssd/proyectos/SLDB_1/sldb/desk/inbox/20261116-054845-suggestion-declared-target-nodes-aceptar-un-directorio-como-target-declarado.md`

Hay que citarla en el commit de cierre (done_when). Ver `message-send.log`.

## Validación (validation.log)

- `test_materialization_targets_outside_package.py`: 17 passed, rc=0
- `test_closeout_gates.py`: 5 passed, rc=0
- `test_closeout.py`: 59 passed, rc=0
- Suite completa (`-n 4`, bajo lock): 3 failed, 1066 passed, 3 skipped, 1 xfailed (`full-suite.log`). Las 3 fallan igual en un worktree limpio de origin/main (`base-failures.log`), así que no hay fallas nuevas:
  - `tests/e2e_agent/test_agent_scenarios.py::test_reference_solutions[first-task-to-closeout]`: `pytest: command not found`
  - `tests/test_ci_integration.py::test_ci_check_passes_on_a_fresh_desk`: `python: command not found` en `scripts/ci-knowledge-check.sh`
  - `tests/test_ci_integration.py::test_ci_check_fails_on_a_dangling_source_atom`: misma causa

  Las tres son de entorno: el PATH no tiene `python` ni `pytest`.
- Después de la suite solo cambié líneas en blanco en closure.py (formato PEP8) y volví a correr los tests focalizados de directorio y `target_covers`: 13 passed.

## Riesgos

- Cobertura léxica: un target que sea un archivo inexistente cubre el mismo path si se lo cambia (p. ej., al borrarlo). La precisión del preflight lo admite ("no hace falta que exista").
- Mientras sldb no acepte directorios, `deskops graph missing` seguirá reportando `missing_declared_target` para esas materializations. La cobertura de closeout ya no depende de eso.
- `_skill_guard_test_evidence` / `_atom_linked_test_paths` siguen sin considerar materializations con target directorio. Está fuera del alcance.

## Corrección 1

Origen: nota de inbox `desk/inbox/20261116-070913-suggestion-closeout-una-materialization-cuyo-target-es-un-directorio-dentro-de-tests-no-cubre-nada-prefijo-test-file-sin-normalizar.md`. La leí y no la toqué ni la ackeé, igual que las demás notas nuevas del inbox.

- Bug: en `_directory_materialization_targets`, `entry.target_id` del faltante viene tipado por ubicación (`test_file:tests/notations`). Se comparaba sin quitar el prefijo, así que un directorio dentro de `tests/` nunca cubría nada.
- Arreglo en `deskops/services/closure.py`: nueva función `_missing_target_path(target_id)`. Quita un prefijo `<kind>:` (kind alfanumérico/`_`, sin `/`) y normaliza como `_normalize_target_path`. La comparación con el `target_identity` declarado usa esa función. Se actualizó la docstring.
- Test en `tests/test_materialization_targets_outside_package.py`: `test_closeout_verify_covers_files_under_a_directory_target` quedó parametrizado con un segundo caso: target `tests/notations` cubre `tests/notations/test_a.py` y no cubre `tests/notationszero.py`.
- Falla sin el arreglo: con la comparación revertida temporalmente, el caso `tests/notations` falla (`'tests/notations/test_a.py' not in {...}` ⇒ missing_changed_file_link) y el caso `pkg/sub` pasa. Con el arreglo restaurado pasan los dos. Está en validation.log.
- Re-validación, de a un archivo y sin lock (validation.log, sección "Re-validación"):
  - test_materialization_targets_outside_package.py: 18 passed, rc=0
  - test_closeout_gates.py: 5 passed, rc=0
  - test_closeout.py: 59 passed, rc=0

  Esta re-validación corrió con el arreglo ya aplicado, antes de la prueba de falla. El archivo restaurado es byte a byte el mismo, porque se copió y se restauró.
- No volví a correr la suite completa, como pidió el coordinador. La corrida anterior (3 fallas de entorno, idénticas en origin/main) es previa a esta corrección.
- `git status` muestra cambios ajenos en `.sldb/` y en `desk/inbox/` (notas de otras sesiones). No son míos y no los toqué. `deskops message send` pudo haber tocado `.sldb/core/models/InboxNoteDoc.yaml` al rastrear la nota enviada a sldb; queda a criterio del cierre.
