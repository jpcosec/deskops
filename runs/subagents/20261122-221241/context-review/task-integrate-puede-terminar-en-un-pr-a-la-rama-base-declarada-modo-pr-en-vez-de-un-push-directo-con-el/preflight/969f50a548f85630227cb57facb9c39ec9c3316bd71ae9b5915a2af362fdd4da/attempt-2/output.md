## REFORMULACION

Encargo: en el repo `deskops`, añadir `IntegrateConfig.mode` con valores `push` (por defecto, comportamiento actual) y `pr`. En modo `pr`, el ciclo dispatch start/reap/integrate debe terminar en un PR hacia `integrate.branch`, sin push directo a la base ni merge local: reap lleva los commits a `task/<task-id>` creada desde la base; el closeout se commitea en esa rama; integrate ejecuta las compuertas sobre su punta, empuja `task/<task-id>` y abre/actualiza el PR con `gh pr create` (base, título de la tarea, cuerpo con id y resumen del closeout), imprimiendo la URL. El modo `push` no cambia. La configuración por máquina va en `config.local.json` no versionado, documentando la división. Fuera: migrar rutas de máquina en deskops/sldb y configurar desks de heyantonia. Éxito: test con remoto de `dev` protegida y `gh` falso, tests de modo push intactos y suite completa verde.

No es ejecutable por sí solo: es un TaskDoc de implementación; las fases p1–p6 actúan como hijos lógicos. p1 aporta el test de aceptación; p2 verifica no regresión; p3 implementa; p4 documenta; p5 valida la suite; p6 entrega el commit con trailer.

## AMBIGUEDADES

1. «Si el PR ya existe, solo empuja» y «abre o actualiza el PR»: no define cómo detectar el PR ni qué significa actualizar. Obligaría a inventar consulta (`gh pr view/list`) y formato de actualización.
2. «El closeout de la tarea se commitea en esa misma rama»: no delimita qué archivos o pasos constituyen el closeout. Obligaría a inventar su contenido y comando.
3. «corre las mismas compuertas sobre la punta»: no enumera las compuertas de integrate. Obligaría a inventar el conjunto exacto.
4. «cuerpo con el id de la tarea y el resumen del closeout»: no fija formato ni fuente del resumen. Obligaría a inventar plantilla y extracción.
5. «start (simulado)»: no aclara si start requiere cambios en modo `pr`. Obligaría a inventar su comportamiento.

## DRY-RUN

Lecturas hipotéticas: `deskops/config.py`, `deskops/dispatch.py`, `deskops/integrate.py`, `tests/test_integrate.py`, `tests/test_dispatch.py`, docs de configuración, CHANGELOG y `.gitignore`. Cambios previstos: p1 test con remoto bare, hook que rechaza `dev` y `gh` falso; p2 test de no regresión; p3 modo `pr` en reap/integrate/closeout; p4 docs; p5 suite; p6 commit. Dependencias: git, pytest, plugin `-n`, `gh` simulado. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py tests/test_dispatch.py`, suite completa y revisión del PR.

## FUTURO

Governance configurará los desks de heyantonia; el coordinador migrará rutas de máquina a `config.local.json`; un humano revisará y aprobará el PR.
