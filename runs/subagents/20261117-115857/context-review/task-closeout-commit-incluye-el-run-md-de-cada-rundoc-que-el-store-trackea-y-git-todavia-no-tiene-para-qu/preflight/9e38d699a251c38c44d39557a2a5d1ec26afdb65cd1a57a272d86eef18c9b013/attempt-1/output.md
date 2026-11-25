## REFORMULACION

**Propósito:** corregir `deskops closeout commit` para que todo commit de cierre incluya el `run.md` de cada RunDoc registrado en `.sldb/store.yaml` que git aún no conoce (ni índice ni HEAD), evitando que un clon limpio falle en `sldb stores build` con `missing: runs/subagents/<run>/run.md`.

**Resultado:** modificación del armado de rutas del commit de cierre en `deskops/services/closure.py` y test nuevo en `tests/test_closeout.py`; pasa el test nuevo y la suite indicada.

**Repo:** deskops, en `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** fuera de alcance el runtime template (sigue registrando el RunDoc al anotar la intención), los demás archivos del run dir (solo `run.md`) y la CI de graph_ui. Nodo ejecutable (`task.code`), no agregado.

## AMBIGUEDADES

1. «en cualquier modo» — no enumera los modos de `closeout commit`; obliga a inventar cuáles existen y si todos comparten el armado de rutas.
2. «además de lo de hoy» — no detalla qué rutas agrega hoy; obliga a inferirlas leyendo el código.
3. «listar los path de RunDoc de .sldb/store.yaml» — no indica campo/clave del esquema ni cómo derivar el `run.md`; obliga a inventar el formato del store.
4. «que existen en disco» — no define qué hacer si un RunDoc registrado no tiene `run.md` (fallar, ignorar, avisar); obliga a inventar política.
5. «git clone del sandbox + sldb stores build da rc 0» — no dice cómo invocar `sldb` (binario, módulo, PYTHONPATH) ni cómo sembrar `.sldb/store.yaml` en `tmp_path`; obliga a inventar fixture y comando.
6. «otra corrida con su run.md sin commitear» — no aclara si el sandbox debe ser repo git con commit base; obliga a inventar el setup.

## DRY-RUN

**Lecturas:** TaskDoc, `closure.py` (armado de rutas y `git add .sldb`), `tests/test_closeout.py`, esquema de `.sldb/store.yaml` y helpers de sandbox. **Cambios previstos:** recolectar `run.md` registrados no trackeados (consulta a git) y sumarlos a las rutas del commit; test en `tmp_path` con repo git init, dos RunDoc, ejecución de closeout, verificación en HEAD, clon y `stores build`. **Dependencias:** git CLI, `../.venv`, pytest, utilidades de desk root sandbox. **Validaciones futuras:** `PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py`, comprobando también que el test falla sin el cambio. Sin ejecutar nada.

## FUTURO

El ejecutor produce el diff y el test; el nodo de validación ejecuta pytest; un humano decide aceptar el cierre y el commit.
