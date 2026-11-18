REFORMULACION
Propósito: que el despacho automático funcione en tareas de sldb e IR reutilizando los RoleDoc de deskops, y que repetir un integrate ya hecho sea no-op.
Resultado: (1) campo opcional `roles_root` en el bloque dispatch del desk/config.json del desk de la tarea, expandido y resuelto a absoluto, por defecto la raíz de la tarea; dispatch.start lo usa para find_role_doc y como root del runtime template; task_root y task_repo (project_identity o nombre del directorio) son de la tarea; run_dir/RunDoc bajo la raíz de la tarea; reap sin cambios (solo test). (2) integrate: tras el fetch, si el tip es ancestro de origin/<branch>, rc 0, imprime "ya integrado: <tip corto>", sin push ni suite, y registra "ya-integrado" en runs/hooks/events.log.
Repo: deskops. Límites: no copiar RoleDocs a otros desks.

AMBIGUEDADES
1. "se guarda absoluta": no dice si reescribe el config o solo normaliza en memoria; obliga a inventar persistencia.
2. "task_repo es el campo project_identity… o el nombre del directorio de la raíz si falta": no define el tipo de project_identity ni qué cuenta como "falta"; obliga a inventar parseo y fallback.
3. "la rama es el campo branch del bloque integrate": sin comportamiento si falta o está vacío; obliga a inventar un default.
4. "con la misma función que escribe hoy las líneas ok/fallo": no fija campos ni formato de "ya-integrado"; obliga a inventar el esquema del log.
5. "llega al scion start (verificable con scion simulado)": no define el umbral observable ni qué config de sldb editar; obliga a inventar la aceptación manual.
6. "como root de la misma llamada a runtime template": no aclara si el template sale de roles_root o de la raíz de la tarea.

DRY-RUN
Lecturas: deskops/dispatch.py (DispatchConfig, start, find_role_doc :92, _list_agents :45), deskops/integrate.py (:213 log, :261 fetch), config de sldb, tests/test_dispatch.py, tests/test_integrate.py, docs/operator-manual.md, CHANGELOG. Cambios: roles_root en DispatchConfig con expanduser/resolución; start lo pasa a find_role_doc y al root del template; salida temprana en integrate tras el fetch con comprobación de ancestro, rc 0 y log "ya-integrado"; tests p1-p3 y docs. Dependencias: helper de ancestro git, runtime template, scion simulado. Validaciones futuras: pytest de dispatch e integrate (TMPDIR=/dev/shm), suite completa (integrador), prueba manual.

FUTURO
Editar desk/config.json de sldb e IR con roles_root (fuera del repo deskops) lo aplica un humano u otro nodo; el integrador corre la suite completa; la verificación manual con scion simulado queda para revisión humana.
