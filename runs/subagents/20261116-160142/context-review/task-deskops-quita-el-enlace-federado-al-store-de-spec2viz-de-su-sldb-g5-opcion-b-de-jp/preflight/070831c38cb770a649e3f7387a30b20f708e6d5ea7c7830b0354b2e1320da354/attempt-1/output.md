REFORMULACION
Encargo: en el repo `deskops` (`/mnt/ssd/proyectos/SLDB_1/deskops`), quitar el enlace federado al store de spec2viz de su `.sldb`. Propósito: evitar que una sesión sldb mcp que federa deskops abra unos 1233 archivos del store real de spec2viz e impida el Done When de otra tarea; JP eligió la opción b y G5 archivará spec2viz. Resultado: ninguna entrada `spec2viz` en `links` de `.sldb/store.yaml` ni en `.sldb/core/store_index.yaml`, usando `sldb stores remove spec2viz --store .sldb`; conservar los enlaces `sldb`, `pron` y `scion`; `sldb stores check`, `deskops doctor` y `deskops graph missing` sin hallazgos nuevos; ningún modelo o documento de deskops dependiendo del store de spec2viz. Límites: no tocar el repo spec2viz ni archivarlo; no quitar menciones en átomos, drawer, tareas ni `deskops/graph/desk_graph.py`; no tocar tests que crean un vecino spec2viz en sandbox; si el CLI rechaza por herencia de un modelo, parar y reportarlo.

AMBIGUEDADES
1. “Guardar antes la salida […] en el run dir”: no se indica la ruta ni el formato del run dir; obliga a inventar dónde y cómo conservar el baseline.
2. “los tests de deskops que se rompan legitimamente porque esperaban ese enlace en el store real”: no identifica cuáles; obliga a decidir qué fallo es legítimo.
3. “sin hallazgos nuevos respecto de antes”: no define el criterio de comparación —texto, conteo o severidad—; obliga a inventarlo.

DRY-RUN
Lecturas: el TaskDoc, `.sldb/store.yaml`, `.sldb/core/store_index.yaml`, `.sldb/core/models`, `tests/test_migrate_desk_stores.py` y el estado git. Cambios previstos: solo mediante `sldb stores remove spec2viz --store .sldb`; capturar salidas antes y después, buscar `spec2viz` y no editar YAML a mano. Dependencias: `sldb`, `deskops`, `../.venv/bin/python`, `pytest`, `TMPDIR=/dev/shm` y `git worktree origin/main`. Validaciones futuras: `sldb stores list`, `sldb stores check`, `deskops doctor`, `deskops graph missing`, el test de stores y la suite completa; comparar contra el baseline y repetir fallas en un worktree limpio. No se ejecuta nada.

FUTURO
JP o un humano confirma la opción b y decide si un rechazo por herencia o una falla no reproducible se acepta; G5 archiva el store de spec2viz; otra tarea elimina las menciones en reglas de specs/graph. El ejecutor no decide esas políticas.
