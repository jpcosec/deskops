## REFORMULACION

Encargo ejecutable (no agregado) en el repo **deskops**: añadir el campo opcional `roles_root` al bloque `dispatch` de `desk/config.json`, usado por `dispatch start` y `reap` para localizar RoleDocs y armar el runtime template (`root=roles_root`, `task_root` y `task_repo` de la tarea). Además, `integrate` debe devolver rc 0 sin push, imprimir `ya integrado: <tip>` y registrar esa línea en `events.log` cuando el tip ya sea ancestro de `origin/<branch>`.

**Resultado:** tests nuevos y suite pasando; con `roles_root=/mnt/ssd/proyectos/SLDB_1/deskops` configurado en sldb, `deskops dispatch start executor --task <tarea sldb> --root sldb` alcanza el `scion start` simulado.

**Límites:** no copiar RoleDocs a otros desks. Incluye tests, implementación, `docs/operator-manual.md` y CHANGELOG.

## AMBIGUEDADES

1. «en el bloque dispatch de desk/config.json»: no precisa si es el config del desk de la tarea, el de deskops o ambos; obligaría a inventar la resolución cuando `--root` y `roles_root` difieren.
2. «task_repo=nombre del repo de la tarea»: no define si es basename del directorio, campo de config o remoto; obligaría a inventar la fuente.
3. «origin/<branch>»: no indica cómo se obtiene `<branch>`; obligaría a inventar branch actual vs. default.
4. «escribe esa línea en events.log»: no da ruta ni formato; obligaría a inventar ubicación y esquema.
5. «dispatch start y reap funcionan»: solo detalla `start`; obligaría a inventar el comportamiento esperado de `reap`.

## DRY-RUN

Leería TaskDoc, `desk/config.json`, `deskops/dispatch.py` (incluida línea 92), implementación de `integrate`, tests de dispatch/integrate, manual y CHANGELOG. Cambios previstos: `DispatchConfig.roles_root`; uso en `find_role_doc` y template de `start/reap`; rama no-op en integrate; tests primero; docs y CHANGELOG. Dependencias: estructura de config existente, simulación de `scion`, helpers de git. Validaciones futuras: `TMPDIR=/dev/shm python -m pytest -q tests/test_dispatch.py tests/test_integrate.py` y suite completa. Sin ejecutar nada.

## FUTURO

El integrador ejecutará la suite completa; un humano decidirá la aceptación, configurará `roles_root` en sldb y verificará el `scion start` simulado.
