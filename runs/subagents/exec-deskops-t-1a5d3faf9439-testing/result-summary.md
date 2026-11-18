FALLA

# Resultado del tester

Tarea: task-los-git-que-deskops-parsea-usan-core-quotepath-false-y-los-ids-nuevos-se-pliegan-a-ascii
Commit del ejecutor: `af79c143553a6ef94d45e1b29c3d746bc511605e` (HEAD `e5c28661`).

## Motivo bloqueante: regresión de ids existentes con acentos

El cambio centraliza `slugify` en `deskops.slugs.ascii_slug`, pero `deskops/doc_access.py:slugify`
también lo usa `deskops/models/atom.py:check_slug_id` para validar ids de AtomDoc/Protoatom. Al plegar
acentos, los ids ya commiteados dejan de cumplir la convención y no resuelven:

    $ deskops show atom 'atom-en-deskops-el-store-de-sldb-se-versiona-entero-y-solo-la-caché-se-ignora'
    Error: 1 validation error for AtomDoc
    id
      Value error, atom id must follow slug convention atom-<slug>: ... [type=value_error]
    exit=1

En un worktree limpio de `origin/main` (`708a92fe`) el mismo comando sale 0 y muestra el átomo.
Hay 8 ids de átomos con acentos commiteados bajo `desk/atoms/` (y los protoatoms usan el mismo
chequeo). Esto viola el objetivo (3): "los ids existentes con acentos siguen resolviendo por
selector exacto; no se renombran ni se migran". Evidencia completa en
`logs/accented-atom-regression.log`.

Los tests nuevos no cubren este caso: solo prueban un id de tarea acentuado, y TaskDoc no pasa por
`check_slug_id`. Hace falta aceptar también la forma de slug heredada en `check_slug_id` (o plegar
solo en la generación de ids nuevos, sin cambiar la validación de ids existentes) y agregar un test
con un átomo acentuado ya commiteado.

## Pruebas corridas (cada archivo por separado, `TMPDIR=/tmp`, `/dev/shm/t311/bin/python`)

- `tests/test_ascii_ids.py`: 5 passed.
- `tests/test_integrate.py`: 19 passed (corrido solo).
- `tests/test_specs.py`: 5 passed.
- `tests/test_add_task_from_drawer.py`: 3 passed.
- `tests/test_closeout.py`: 73 passed.
- `tests/test_cli.py`: 102 passed.
- Extra por módulos tocados: `test_closeout_evidence_receipts.py` 5, `test_transaction.py` 11,
  `test_closeout_resolved_by.py` 25, `test_tracked_selector_resolution.py` 15,
  `test_taskdoc_read_without_overlay.py` 1; todos passed.

No se corrió la suite completa (la corre integrate en el host). En una corrida inicial de
`test_integrate.py` con otros dos pytest en paralelo aparecieron 2 fallas de limpieza
(`test_failing_suite_stops_before_any_push`, `test_a_tip_already_on_the_remote_is_a_noop`);
ambas y el archivo completo pasan corridos solos y no se reproducen.

## Lo que sí cumple

- `grep -rn quotepath deskops/`: `deskops/integrate.py:_run` y
  `deskops/services/closure.py:_git/_git_knows` agregan `-c core.quotepath=false`; las demás
  llamadas literales a git no parsean rutas o ya usan `-z` (`deskops/services/atoms.py`).
- `deskops add task --title 'Transacción ñandú'` genera id solo ASCII; un id explícito acentuado
  se conserva y `deskops show task` lo resuelve.
- Un archivo sin trackear con acentos en `.sldb` no aparece con escapes octales en
  `ClosureService._git status` y `_git_knows` lo encuentra al stagearlo (verificado a mano).
- `integrate` encuentra el recibo de una tarea con id acentuado (test incluido, pasa).

## Artefactos

- `logs/test_ascii_ids.log`
- `logs/accented-atom-regression.log`
- `validation.log`
