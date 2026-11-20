PASA

# Resultado del tester

Tarea: `task-integrate-evalua-el-gate-de-grafo-en-la-punta-local-actual-no-solo-en-el-commit-de-closeout-cuando-d`
Commit del ejecutor: `a9952c2974ae8862990ef13c6deb258837fee29c` — *integrate: extend the tip over later desk-only commits*.

## Archivos del commit

- `deskops/integrate.py`: agrega `extend_tip()`, que compara `git diff --name-only <closeout>..HEAD` y usa HEAD como tip solo cuando todos los archivos cambiados están bajo `desk/`, `.sldb/` o `runs/`; imprime `tip extendido a <sha>: solo commits de desk`.
- `tests/test_integrate.py`: dos tests nuevos:
  - `test_tip_extends_over_later_desk_only_commits`: reproduce el closeout con referencia colgante, verifica que integra falla, y que tras el commit de desk que la retira integra termina ok, extiende el tip y empuja HEAD.
  - `test_tip_stays_at_closeout_when_a_later_commit_touches_code`: un commit posterior que toca `src/` impide la extensión y mantiene el fallo del gate de grafo.
- `CHANGELOG.md`: entrada en Fixed.

## Pruebas ejecutadas

- `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_integrate.py`
  - **22 passed**, 1 warning (opción desconocida `asyncio_default_fixture_loop_scope`), exit 0, 264.48 s.
- Ese es el único archivo `tests/*.py` del commit y también el test del módulo tocado (`tests/test_integrate.py`); no hay otro `tests/test_<modulo>.py` que corresponda.

No se ejecutó la suite completa (la corre integrate en el host).

## Verificación contra el Goal

- Con solo commits posteriores de desk, el tip se extiende a HEAD, se corre el gate de grafo sobre esa punta y se empuja (los tests comparan `_remote_head(root) == head`).
- Con un commit posterior que toca código (`src/later.py`), no se extiende el tip y el gate sigue evaluando el closeout.
- El mensaje impreso coincide con el pedido: `tip extendido a <sha>: solo commits de desk`.

## Entorno

El `.venv` del workspace apunta a un Python 3.12 ausente y no hay `pytest` en el Python del sistema. La validación se corrió con `/dev/shm/t311/bin/python` (3.11, pytest 9.2.0) y `PYTHONPATH=/workspace/deskops:/workspace/sldb/src`. No se modificó código, tests, `desk/` ni `.sldb/`.
