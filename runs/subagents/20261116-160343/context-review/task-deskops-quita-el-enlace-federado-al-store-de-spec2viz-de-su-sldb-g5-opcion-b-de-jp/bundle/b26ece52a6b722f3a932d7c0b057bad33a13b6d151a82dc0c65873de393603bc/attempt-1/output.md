## REFORMULACION

Propósito: eliminar del store de deskops el enlace federado al store de spec2viz, decidido por JP como opción b, para que una sesión `sldb mcp` que federa deskops no arrastre ~1233 archivos del store real de spec2viz. Resultado: `.sldb/store.yaml` (links) y `.sldb/core/store_index.yaml` sin entrada `spec2viz`, hecha vía `sldb stores remove spec2viz --store .sldb`; `sldb stores check`, `deskops doctor` y `deskops graph missing` sin hallazgos nuevos; ningún modelo/documento de deskops dependiendo del store de spec2viz; enlaces `sldb`, `pron`, `scion` intactos. Repo: deskops. Límites: no tocar spec2viz ni archivarlo, ni menciones en átomos/drawer/tareas/`desk_graph.py`, ni tests que simulan un vecino spec2viz; si `sldb stores remove` rechaza por herencia de modelo, parar e informar sin forzar.

## AMBIGUEDADES

1. "ningun modelo ni documento de deskops depende del store de spec2viz" choca con `store_index.yaml`, donde `ViewDoc` declara `system.spec2viz`; obligaría a inventar si esa semántica cuenta como dependencia.
2. "los tests de deskops que se rompan legitimamente porque esperaban ese enlace en el store real": no se listan; obligaría a inventar cuáles son legítimos.
3. "Guardar antes la salida ... en el run dir": no se define ruta ni formato; obligaría a inventar el directorio de ejecución.
4. "no empeoran (mismos hallazgos que antes, salvo los que desaparecen)": no fija formato de comparación ni baseline; obligaría a inventar el criterio de diff.
5. `tests/test_migrate_desk_stores.py` aparece en Validación pero no en Scope; obligaría a inventar si se debe modificar.
6. "Si sldb stores remove rechaza porque un modelo de deskops hereda": no define cómo detectar esa herencia; obligaría a inventar el criterio previo.

## DRY-RUN

Lecturas: `.sldb/store.yaml`, `.sldb/core/store_index.yaml`, `.sldb/core/models/*`, `tests/test_migrate_desk_stores.py`. Cambios previstos: guardar salidas base de los tres comandos; `sldb stores remove spec2viz --store .sldb`; ajustar tests legítimos. Dependencias: CLI `sldb`, CLI `deskops`, venv `../.venv`, `origin/main` para worktree. Validaciones futuras: `sldb stores list`, repetir `check`/`doctor`/`graph missing` y comparar, pytest de stores y suite completa con worktree base para fallas.

## FUTURO

Un ejecutor futuro realiza los comandos y el commit descriptivo (átomo de cierre); un humano/JP ya fijó la opción b y valida el informe de fallas; otro nodo cubre menciones a spec2viz en `desk_graph.py` y reglas de specs.
