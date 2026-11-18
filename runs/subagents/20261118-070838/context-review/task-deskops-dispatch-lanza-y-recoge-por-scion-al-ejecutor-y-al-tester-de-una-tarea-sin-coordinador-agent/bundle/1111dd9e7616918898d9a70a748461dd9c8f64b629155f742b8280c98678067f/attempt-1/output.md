REFORMULACION
Propósito: añadir `deskops dispatch` para que la cola del host lance y recoja agentes Scion de ejecución y test sin coordinador agente. Resultado: módulo `deskops/dispatch.py` con `start` y `reap`; campo `dispatch` en `DeskConfig`; registro en `deskops/cli/registry.py`; tests nuevos y guardianes; goldens de ayuda; ejemplo en `docs/operator-manual.md`. Repo: deskops, con los archivos enumerados en el TaskDoc. Límites: no integrar ni pushear, no declarar configuración/hooks reales, no modificar Scion, checkout principal sin worktree, rama, `git add` ni `git commit`. Es un nodo ejecutable, no un agregado; sus átomos actúan como restricciones.

AMBIGUEDADES
1. «decide, en este orden de prioridad, el motivo de termino: `phase` distinta de `running`... `activity` igual a `completed`...» frente al átomo: «using activity first and phase only as fallback». Obliga a inventar qué señal manda cuando `phase=running` y `activity=completed`.
2. «salen con codigo 2 y un mensaje». No define el texto ni el canal; obliga a inventar el mensaje.
3. «seguida del archivo Markdown completo del TaskDoc». No indica cómo localizar ese archivo; obliga a asumir `desk/tasks/<id>.md` o una búsqueda por modelo.
4. «en la carpeta `<templates_dir>/<nombre del rol>`» y «template igual al nombre del rol», pero la configuración declara `role` como «id o nombre del RoleDoc». Obliga a decidir si se usa el `name` del RoleDoc o el valor configurado.
5. «`labels["deskops.task_id"]`» presupone forma del JSON de `scion list`; el formato de etiquetas no está descrito.

DRY-RUN
Lecturas: TaskDoc, `DeskConfig`, RoleDocs/RuntimeProfiles, `deskops/runtime/scion.py`, registry, tests y goldens existentes, `docs/operator-manual.md`, salida JSON de `scion list`. Cambios previstos: crear `dispatch.py`; añadir el modelo/config `dispatch`; declarar `dispatch start|reap`; escribir `tests/test_dispatch.py`; actualizar guardianes y goldens; documentar `queue_jobs`. Dependencias: `task-un-runner-del-host...` para invocación desde cola; helpers `scion_child_identity`, `materialize_scion_template`, `scion_start_argv`, `record_scion_run`. Validaciones futuras: pytest indicados, goldens de ayuda y `tests/test_scion_runtime.py`, sin ejecutar ahora.

FUTURO
Otro nodo implementará y ejecutará pruebas; un humano resolverá las ambigüedades señaladas; la tarea de integración/commit y la cola del host consumirán el resultado.
