FALLA

# Resultado del tester

Tarea: task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio
Run: run-deskops-t-6a1436989fc7
Commit evaluado: 2373f55deeff3db66bc4a6791264ff8a8490f0b3 ("doctor and init report the old .sldb layout with the migrate-layout remedy", trailer Task-Id correcto).

## Veredicto

Los tests nuevos del commit pasan y el camino principal (runtime/, journal y líneas exactas
`.sldb/core/` / `.sldb/runtime/` en `.gitignore`) funciona. Pero la implementación **no cumple
las resoluciones aceptadas de preflight-1/bundle-1** y deja pasar señales reales del layout viejo:

1. **No detecta las variantes `/**` y `/*` del `.gitignore`.** La resolución aceptada exige quitar
   un `/` inicial y los sufijos `/**`, `/*` o `/` final, y dar señal si queda exactamente
   `.sldb/core` o `.sldb/runtime`. `deskops/sldb_layout.py` solo quita `/` inicial y final, así que
   `.sldb/core/**`, `.sldb/core/*`, `.sldb/runtime/**` y `.sldb/runtime/*` no producen señal.
   Verificado con un repo recién inicializado: tras añadir `.sldb/core/**` al `.gitignore`,
   `deskops doctor` sale 0 y dice "Desk is healthy. No issues found.".
2. **`deskops init` no está condicionado a que `.sldb/` exista.** La resolución aceptada pide el
   chequeo en `deskops/bootstrap.py` (`init_local_store`, antes de `_init_store` y de cualquier
   escritura) **solo si `.sldb/` ya existe**. Aquí el chequeo vive en `InitCLI.run`, antes del
   bootstrap, y también rechaza repos nuevos que solo heredan una línea vieja en `.gitignore`
   sin tener `.sldb/`. Verificado: directorio vacío + `.gitignore` con `.sldb/runtime/` ->
   `init` sale 1 y no inicializa, aunque no hay store que migrar.
3. **Texto y ubicación no son los resueltos.** La resolución pide la función en
   `deskops/doctor_findings.py` y el texto `old .sldb layout (SENALES): run sldb stores
   migrate-layout --store RUTA_DEL_REPO/.sldb` (ruta absoluta). El commit crea
   `deskops/sldb_layout.py` y emite `Old .sldb layout (...). Migrate with: ...`. Contiene el
   remedio, pero no la frase exacta que podrían exigir los tests de aceptación.
4. **Documentación:** README y skill sí contienen los 7 pasos en orden, pero el README no usa el
   encabezado pedido ("Migrar el layout viejo de .sldb") y la skill los pone en un párrafo, no en
   lista numerada. Además queda en README.md:187 la frase vieja "The store under `.sldb/core/` is
   derived and not versioned", que contradice la sección nueva y la premisa de la tarea.

## Tests ejecutados (de a uno)

El `.venv` del checkout apunta a un Python 3.12 ausente y no tiene pytest utilizable; usé
`/home/scion/.local/share/uv/python/cpython-3.12.16-linux-x86_64-gnu/bin/python3.12` con
`PYTHONPATH=/mnt/ssd/proyectos/SLDB_1/.venv/lib/python3.12/site-packages:/mnt/ssd/proyectos/SLDB_1/sldb/src:/mnt/ssd/proyectos/SLDB_1/deskops`.

```text
TMPDIR=/tmp .../python -m pytest -q tests/test_doctor_sldb_layout.py   -> 6 passed
TMPDIR=/tmp .../python -m pytest -q tests/test_doctor_alerts.py        -> 5 passed
TMPDIR=/tmp .../python -m pytest -q tests/test_gitignore_policy.py     -> 2 passed
```

`deskops doctor --root .` sobre el desk de deskops: sale 1 por errores preexistentes ajenos al
layout (inbox/reviews/registry), pero **no** imprime "Old .sldb", "migrate-layout" ni
"Desk is healthy"; el desk está migrado. No se corrió la suite completa (la integra el host).

## Evidencia de aceptación

Con el código del commit:

```text
$ python -c 'old_layout_signals(...)'
'.sldb/core/'      -> ['.gitignore ignores .sldb/core']
'/.sldb/core/'     -> ['.gitignore ignores .sldb/core']
'.sldb/core/**'    -> []        # la resolución aceptada exige señal
'.sldb/core/*'     -> []        # idem
'.sldb/runtime/**' -> []        # idem
```

```text
$ mkdir /tmp/wildprobe && deskops init /tmp/wildprobe   # OK
$ echo '.sldb/core/**' >> /tmp/wildprobe/.gitignore
$ deskops doctor --root /tmp/wildprobe
Desk is healthy. No issues found.                       # exit 0, no debe pasar
```

```text
$ mkdir /tmp/initprobe && echo '.sldb/runtime/' > /tmp/initprobe/.gitignore
$ deskops init /tmp/initprobe
Error: Old .sldb layout (.gitignore ignores .sldb/runtime). Migrate with: ...
# exit 1; según la resolución aceptada, sin .sldb/ no debía rechazar el init
```

## Acción sugerida para el ejecutor

- Normalizar el `.gitignore` quitando `/` inicial y sufijos `/**`, `/*` y `/` final (una sola
  vez, como en preflight-1) y añadir tests para esas variantes.
- Mover el chequeo de init a `SLDBBootstrap.init_local_store`, solo cuando `local_store.exists()`,
  antes de `_init_store`, y devolver != 0 con el mismo texto.
- Emitir la frase exacta resuelta y ubicar la función en `deskops/doctor_findings.py` (o confirmar
  con el coordinador que la ubicación nueva es aceptable).
- Ajustar README/skill al encabezado y lista pedidos y corregir la frase contradictoria de
  README.md:187.

## Datos del run

- Task id: task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio
- Role: tester
- Run id: run-deskops-t-6a1436989fc7
- Commit del ejecutor: 2373f55deeff3db66bc4a6791264ff8a8490f0b3
- Revisiones de referencia: desk/reviews/task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio/{preflight-1,bundle-1}.md
