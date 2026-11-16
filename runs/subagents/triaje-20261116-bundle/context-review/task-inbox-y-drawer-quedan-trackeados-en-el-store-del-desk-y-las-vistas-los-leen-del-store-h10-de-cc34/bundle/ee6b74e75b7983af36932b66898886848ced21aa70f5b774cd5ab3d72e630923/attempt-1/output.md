REFORMULACION
Propósito: que inbox y drawer queden trackeados en el store del desk y que `deskops view` los lea de `run_view`, no del disco (H10 de CC34). Resultado: `desk_declaration.yaml` con globs de inbox/drawer; `promote inbox-to-drawer-task` y el alta de items del drawer trackean al escribir; `view` proyecta drawer/inbox desde el store; tests, commit y nota a `graph_ui` con el hash del commit. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no verificación en navegador, no migrar desks ajenos, no “Backend, robocop2”.

AMBIGUEDADES
1. “deskops view saca drawer e inbox de run_view como board y task”, pero los archivos nombrados no incluyen ViewDocs (`deskops/data/views/`). Obligaría a inventar modelos, secciones y parámetros de esas vistas.
2. “los comandos que escriben en el drawer… y el alta de items del drawer” y “deskops/cli/commands/drawer.py si escriben en el drawer”: el “si” y la ausencia de `drawer.py` en `files` obligan a inventar qué comando concreto trackea y si ese archivo existe.
3. “desk_declaration.yaml incluye los globs de inbox y drawer”: no fija modelo ni patrón exacto ni exclusiones. Obligaría a inventar `InboxNoteDoc`/`TaskDoc`, globs y tratamiento de índices/README.
4. “No entra: … Backend, robocop2.”: no define esos términos. Obligaría a inventar qué superficies quedan fuera.
5. “Al cerrar, se avisa a graph_ui para que verifique en navegador” frente a Done When, que solo exige “nota a graph_ui enviada”. Obligaría a decidir si esa verificación ajena condiciona el cierre.

DRY-RUN
Lecturas: TaskDoc, `desk_declaration.yaml`, `view.py`, `message.py`, `promote.py`, `drawer.py`, tests citados y store. Cambios previstos: añadir includes de inbox/drawer; envolver escrituras de promote/drawer en transacción y `track`; sustituir lecturas de disco de `drawer_view`/`inbox_view` por `run_view` y proyectar; ampliar tests. Dependencias: ViewDocs de drawer/inbox en sldb, API de tracking y `desk update --apply`. Validaciones futuras: los tres pytest indicados, suite completa con `-n 4`, baseline en worktree de `origin/main` para fallas, y lista de fallas en el informe.

FUTURO
`graph_ui` verifica en navegador; un humano resuelve las ambigüedades; `desk update --apply` materializa includes; el commit produce el hash que usará `deskops message send --to graph_ui`; el informe recoge fallas preexistentes.
