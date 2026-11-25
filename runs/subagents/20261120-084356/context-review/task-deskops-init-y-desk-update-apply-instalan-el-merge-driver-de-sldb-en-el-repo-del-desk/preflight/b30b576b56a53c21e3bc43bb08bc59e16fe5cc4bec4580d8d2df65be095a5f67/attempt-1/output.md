## REFORMULACION
Propósito: que los desks gestionados por deskops tengan instalado el merge driver de sldb. Resultado: `deskops init` (`BootstrapService.init_local_store`) y `desk update --apply` llaman a `install_merge_driver` sobre el store del desk si es repo git; idempotente, no-op fuera de git, y si git falla avisa por stderr sin romper. Repo: deskops (`bootstrap.py`, `cli/commands/desk.py`, tests, `docs/operator-manual.md`, CHANGELOG). Límites: no tocar sldb; si `install_merge_driver` no se puede importar, omitir sin error.

## AMBIGUEDADES
1. "desk update --apply (deskops/cli/commands/desk.py:200 update y lo que llame)" — no identifica la función exacta donde insertar la llamada; obligaría a inventar el punto de hook.
2. "llamando a install_merge_driver de sldb sobre el store del desk" — no da firma ni parámetros (ruta, config); obligaría a inventar la invocación.
3. "cuando el desk es un repo git" — no define cómo detectarlo (¿`.git`?, ¿`git rev-parse`?).
4. "si git falla avisa por stderr sin romper" — no fija mensaje, formato ni código de salida.
5. "las tres líneas merge=sldb" — no transcribe el contenido exacto de `.gitattributes` ni las claves de config.
6. "uno nuevo en tests/test_bootstrap*.py o tests/test_desk_update*.py" — ubicación y nombre sin decidir.
7. "si existe /workspace/sldb ... sldb 9007f78a" — paso condicional sin criterio de obligatoriedad.
8. "fuera de git no escriba nada" — no aclara si el store igual se inicializa y solo el driver es no-op.

## DRY-RUN
Lecturas: `bootstrap.py` (`init_local_store`, `_init_store`), `cli/commands/desk.py` (`update`), docs, CHANGELOG, tests existentes y golden. Cambios previstos: test rojo (init/update en repo git temporal; no-git sin escritura), helper con `try/except ImportError`, llamada desde init y desde `update --apply`, docs y CHANGELOG. Dependencias: `sldb.api.stores.merge_driver_install.install_merge_driver`; `git` en PATH. Validaciones futuras: pytest de tests nuevos y `tests/test_lifecycle_seed_drift.py` con `TMPDIR=/tmp`; opcional con sldb 9007f78a vía `PYTHONPATH`; inspección de `.gitattributes` y `merge.sldb.driver`. Sin ejecutar.

## FUTURO
El nodo implementador escribe test, código, docs, commit con rutas y `Task-Id`, y ejecuta `deskops advance`. El integrador decide si corre la suite completa y contra qué sldb (workspace o 9007f78a). CI/integrate valida el golden y el cierre.
