## REFORMULACION

Encargo ejecutable de código en el repo deskops: (a) añadir `roles_root` opcional al bloque `dispatch` del `desk/config.json` del desk de la tarea (por defecto, la raíz de la tarea); (b) `dispatch.start` lo usa para `find_role_doc` y para resolver el template (`root=roles_root`), manteniendo `task_root`=raíz de la tarea y `task_repo`=`project_identity`, con run_dir/RunDoc bajo la raíz de la tarea; (c) `dispatch.reap` debe funcionar con `--root sldb` sin roles, localizando agentes por etiqueta `deskops.task_id` y leyendo `result-summary.md`; (d) `integrate` debe devolver rc 0, imprimir `ya integrado: <tip corto>`, no pushear y registrar una línea en `<raíz>/runs/hooks/events.log` cuando el tip ya sea ancestro de `origin/<branch>` (rama del bloque `integrate`). Fuera de alcance: copiar RoleDocs. Resultado: tests nuevos y suite completa en verde, más verificación manual con scion simulado.

## AMBIGUEDADES

1. "ruta absoluta del repo" — ¿se admite ruta relativa o `~`? Obligaría a inventar resolución/normalización.
2. "task_repo es el project_identity del desk/config.json de la tarea" — clave y fallback no confirmados; obligaría a inventar default si falta.
3. "runtime template (root=roles_root)" — no dice qué template ni cómo se resuelve; obligaría a inventar nombre/plantilla.
4. "la rama es el campo branch del bloque integrate del config" — no aclara de qué raíz (tarea vs roles_root); obligaría a elegir.
5. "mismo formato de las líneas ok/fallo" — formato no citado; obligaría a inventar campos/orden.
6. "encuentra los agentes por la etiqueta deskops.task_id" — no indica comando/mecanismo de listado; obligaría a inventar.
7. "(b) ... y en dispatch.start/reap" vs "(c) dispatch.reap no usa roles" — contradicción; obligaría a decidir si reap toca roles.
8. "el tip ya es ancestro de origin/<branch>" — no dice si hace fetch previo; obligaría a asumir.

## DRY-RUN

Lecturas: `desk/tasks/task-...md`, `deskops/dispatch.py` (línea 92), `deskops/integrate.py`, `desk/config.json` de deskops/sldb/IR, `tests/test_dispatch.py`, `tests/test_integrate.py`, `docs/operator-manual.md`, `CHANGELOG`. Cambios previstos: esquema `DispatchConfig.roles_root`; `start`/`reap`; rama "ya integrado" en integrate con log; tests p1/p3; docs/changelog. Dependencias: RoleDocs en deskops, scion simulado, configs de sldb/IR. Validación futura: pytest de dispatch/integrate, suite completa, prueba manual con scion simulado.

## FUTURO

Implementador ejecuta p1–p4; integrador corre suite completa; JP/humano valida la prueba manual con `--root sldb` y decide el merge.
