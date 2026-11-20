PASA

# Veredicto del tester

El commit del ejecutor implementa el salto del push del sha de código cuando ya es ancestro de `origin/main`, informa `código ya en origin: <sha>` y continúa con el push de la punta. El test nuevo reproduce el fallo `push` non-fast-forward en el commit padre y pasa con el commit evaluado; toda la suite de `tests/test_integrate.py` pasa.

## Commit evaluado

- Commit: `6ca104ec87462c2459ac1164da569231e6e5d468`
- Mensaje: `integrate: skip code push when sha is already in origin`
- Trailer: `Task-Id: task-integrate-no-intenta-empujar-el-sha-de-codigo-cuando-ya-es-ancestro-de-origin-main`
- Archivos:
  - `deskops/integrate.py`
  - `tests/test_integrate.py`
  - `CHANGELOG.md`

## Cambio verificado

En `deskops/integrate.py`, tras el `fetch`, los checks de suite/grafo y antes del push:

```python
code_in_origin = _run(["git", "merge-base", "--is-ancestor", code, remote_ref], copy).returncode == 0
if code_in_origin:
    print(f"código ya en origin: {code[:SHORT]}")
pushes = [] if code_in_origin else [f"git push origin {code}:{branch}"]
pushes.append(f"git push origin {tip}:{branch}")
```

Cumple el Goal: si el sha de código ya está en `origin/<branch>` no se intenta empujarlo, se informa y se sigue con el push de la punta; si no es ancestro, el comportamiento previo se conserva.

## Pruebas ejecutadas

Worktree limpio del commit en `/tmp/deskops-test-6ca104ec`, con Python 3.13.18 y pytest 9.1.1 de `/workspace/sldb/.venv/bin/python` (el `.venv` del proyecto apunta a un Python 3.12 ausente en este contenedor):

```text
$ PYTHONPATH=$PWD TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_integrate.py
20 passed, 1 warning in 61.43s
```

El commit toca `deskops/integrate.py`, cuyo test correspondiente es `tests/test_integrate.py` (también modificado por el propio commit). No hay otros módulos de código tocados.

## Verificación del test nuevo (falla antes, pasa después)

En un worktree del commit padre (`b75894c3`) con el `tests/test_integrate.py` del commit evaluado:

```text
$ ... pytest -q -p no:cacheprovider tests/test_integrate.py -k code_already
FAILED tests/test_integrate.py::test_code_already_behind_origin_main_is_not_pushed
AssertionError: fallo: push: git push origin e98803f...:main: ... (non-fast-forward)
1 failed, 19 deselected
```

Con el commit evaluado, el mismo test pasa junto con los otros 19. Esto confirma que el test detecta exactamente la regresión descrita y que el arreglo la resuelve.

## Entorno

El `.venv` de `/workspace`/`/mnt/ssd/proyectos/SLDB_1` está roto en este contenedor (enlaces a Python 3.12 ausente; `python` resuelve a 3.11 sin pytest). No modifiqué el repositorio; la validación se hizo en worktrees temporales y con el Python 3.13 de `sldb/.venv`.
