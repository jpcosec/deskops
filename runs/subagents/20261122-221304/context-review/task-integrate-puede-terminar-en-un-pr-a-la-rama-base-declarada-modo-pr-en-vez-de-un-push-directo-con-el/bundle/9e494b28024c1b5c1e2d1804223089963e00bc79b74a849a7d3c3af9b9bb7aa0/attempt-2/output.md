## REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: que `integrate` pueda terminar en un PR a la rama base declarada en vez de un push directo. Resultado: `IntegrateConfig.mode` (`push` por defecto, `pr`); en modo `pr`, `reap` lleva los commits a `task/<task-id>` desde la base, el closeout se commitea ahí, `integrate` corre compuertas, empuja `task/<task-id>`, abre/actualiza el PR hacia `integrate.branch` con `gh` e imprime la URL; el modo `push` no cambia. Repo: deskops (`deskops/config.py`, `dispatch.py`, `integrate.py`, tests, docs, CHANGELOG). Límites: dentro esos archivos y tests; fuera migrar configs de máquina de deskops/sldb y configurar los desks de heyantonia.

## AMBIGUEDADES
1. “el cierre va dentro del PR” y “El closeout de la tarea se commitea en esa misma rama”: no define qué artefactos ni en qué orden; obligaría a inventar alcance y secuencia del closeout.
2. “corre las mismas compuertas”: no enumera cuáles; obligaría a inventar el conjunto exacto.
3. “Si el PR ya existe, solo empuja”: no dice cómo detectarlo; obligaría a inventar `gh pr view/list` y la clave head/base.
4. “abre o actualiza el PR ... con gh pr create”: `gh pr create` no actualiza; obligaría a inventar `gh pr edit` o una excepción.
5. “start (simulado)”: no define el seam de simulación; obligaría a inventar dobles o sustitución.

## DRY-RUN
Lecturas: TaskDoc, nota de inbox referenciada, `deskops/config.py`, `dispatch.py`, `integrate.py`, `tests/test_integrate.py`, `tests/test_dispatch.py`, docs de configuración, CHANGELOG, `.gitignore`/`config.local.json`. Cambios previstos: campo `mode`; rama `task/<id>` en `reap`; commit de closeout; push de rama y `gh` en `integrate`; tests con remoto bare/hook y `gh` falso; docs. Dependencias: git, gh, worktree de dispatch, compuertas existentes. Validaciones futuras: `pytest` indicado, suite `-n 4`, `dev` remota/local intacta, argumentos `--base dev` y URL.

## FUTURO
Coordinador migra rutas de máquina a `config.local.json`; Governance configura los desks de heyantonia; revisión/merge del PR por humano; ejecución del commit desde el worktree con trailer `Task-Id`.
