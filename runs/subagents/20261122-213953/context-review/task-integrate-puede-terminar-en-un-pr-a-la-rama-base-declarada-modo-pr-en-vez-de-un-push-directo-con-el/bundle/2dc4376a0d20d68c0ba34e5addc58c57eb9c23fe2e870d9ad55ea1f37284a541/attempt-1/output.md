## REFORMULACION
Encargo del nodo: hacer que `deskops` soporte integración por PR además del push directo. Propósito: cumplir la regla de que todo cambio entre por rama de tarea y PR a la base declarada, también con `dev` protegida. Resultado: `IntegrateConfig.mode` (`push` por defecto, `pr`); en `pr`, `reap` lleva commits a `task/<task-id>`, el closeout se commitea ahí, `integrate` valida esa punta, la empuja y abre/actualiza un PR hacia `integrate.branch` con `gh`, imprimiendo la URL; `push` no cambia. Repo: `deskops`. Límites: dentro `config.py`, `dispatch.py`, closeout si aplica, `integrate.py`, tests, docs y CHANGELOG; fuera mover rutas de máquina de deskops/sldb y configurar desks de heyantonia.

## AMBIGUEDADES
1. «el closeout si hace falta para commitear en la rama de la tarea»: no define dónde vive el closeout ni cuándo “hace falta”; obligaría a inventar su flujo y punto de commit.
2. «título = el de la tarea, cuerpo con el id de la tarea y el resumen del closeout»: no fija formato ni fuente exacta del título/resumen; obligaría a inventar plantilla.
3. «abre o actualiza el PR … con gh pr create»: no especifica cómo detectar/actualizar un PR existente; obligaría a inventar `gh pr view/edit` u otra estrategia.
4. «task/<task-id>, creada desde la base»: no cubre rama existente, reintentos ni limpieza; obligaría a inventar política.
5. «corre las mismas compuertas»: no enumera cuáles; obligaría a inventar el conjunto exacto.
6. «start (simulado)»: no indica cómo simularlo; obligaría a inventar fixture o sustitución.

## DRY-RUN
Lecturas: `deskops/config.py`, `dispatch.py`, `integrate.py`, `tests/test_integrate.py`, `test_dispatch.py`, docs de configuración, CHANGELOG y nota de Governance. Cambios previstos: campo `mode`; `reap` a rama de tarea en `pr`; commit de closeout en esa rama; `integrate` valida, empuja `task/<id>` y crea PR; tests con remoto bare protegido y `gh` falso; documentación. Dependencias: hooks remotos, `gh` autenticado o falso, closeout existente, rama base configurada. Validaciones futuras: pytest indicado, suite completa `-n 4`, verificación de URL y de que `dev` no cambia. Sin ejecutar nada.

## FUTURO
Un humano decide/mueve rutas de máquina a `config.local.json`; Governance configura los desks de heyantonia; revisión/QA y merge del PR; aceptación final de la suite.
