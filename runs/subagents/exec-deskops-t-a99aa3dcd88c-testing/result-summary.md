PASA

# Verificación del tester

El commit del ejecutor cumple la Validation y el Done When de la tarea.

## Commit evaluado

- Commit: `3dfa88115c46245c5b3428405555ea2fc849d622`
- Mensaje: `tests: init repair of deskops link under sldb name resolution`
- Trailer: `Task-Id: task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk`
- Archivos:
  - `tests/test_doctor_model_registration.py`
  - `CHANGELOG.md`
- No toca módulos de código (`deskops/`), así que no hay `tests/test_<modulo>.py` adicionales que correr.

## Causa confirmada

Con el sldb del workspace (contiene el PR #3, `9d8584ad`), tras romper el enlace como hace `_point_deskops_link_at` y borrar el directorio destino, `store_links` devuelve:

```text
{'name': 'deskops', 'path': '../deleted/.sldb',
 'resolved': '/tmp/deskops-test-3dfa8811/.sldb', 'status': 'ok', 'by': 'name'}
```

Es decir, la ruta guardada no existe pero el nombre resuelve al store dueño. Por eso `_ensure_owner_link` no tiene nada que reparar y el test viejo, que exigía `Replaced broken`, estaba desactualizado. La opción (a) es la correcta.

## Pruebas ejecutadas

Worktree limpio y detached en `/tmp/deskops-test-3dfa8811` sobre el commit `3dfa8811`, con `PYTHONPATH=$PWD`.

Entorno: en este contenedor no existe `/mnt/ssd/herramientas/sldb`; usé el checkout disponible `/mnt/ssd/proyectos/SLDB_1/sldb` (HEAD `b8e564c2`, con `9d8584ad` como ancestro), Python 3.13.18 y pytest 9.1.1 de su `.venv`.

```text
$ TMPDIR=/tmp PYTHONPATH=$PWD python -m pytest -q -p no:cacheprovider tests/test_doctor_model_registration.py
.........                                                                [100%]
9 passed, 1 warning in 93.99s (0:01:33)
PYTEST_RC=0
```

También reejecuté aislado el test nuevo:

```text
$ ... pytest -q -p no:cacheprovider tests/test_doctor_model_registration.py::test_init_leaves_a_deskops_link_with_a_stale_path_that_resolves_by_name
1 passed, 1 warning in 11.17s
PYTEST_RC=0
```

## Qué cubre el commit

- `test_init_repairs_a_broken_deskops_link`: simula con `monkeypatch` un `store_links` que reporta `status=missing` y `resolved` al directorio borrado, y comprueba que `init` sí reemplaza el enlace e imprime `Replaced broken 'deskops' link`.
- `test_init_leaves_a_deskops_link_with_a_stale_path_that_resolves_by_name`: cubre el caso real de sldb #3; `init` no imprime reemplazo y el enlace queda `status=ok` resolviendo al dueño.
- `CHANGELOG.md` documenta el ajuste y que `bootstrap.py` no cambia.

No hay fallas de `tests/test_doctor_model_registration.py`. No corrí la suite completa, como indica el encargo.
