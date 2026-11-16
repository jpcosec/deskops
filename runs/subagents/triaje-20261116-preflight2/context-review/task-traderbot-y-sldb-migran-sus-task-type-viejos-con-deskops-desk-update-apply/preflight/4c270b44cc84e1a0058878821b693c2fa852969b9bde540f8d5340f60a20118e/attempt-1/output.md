## REFORMULACION

**Propósito:** pedir a los desks externos TraderBot (21 tareas) y sldb (1 tarea) que migren sus `task_type` legacy usando `deskops desk update --apply`, y registrar la evidencia.

**Resultado:** ambos desks reportan un commit de migración citado en `references`; ningún `task_type` queda fuera de la lista vigente de `deskops add task --help`.

**Repo:** desks de TraderBot (sin ruta registrada en robocop2) y `/mnt/ssd/proyectos/SLDB_1/sldb`.

**Límites:** no se escribe en esos repos desde deskops; solo se envía el pedido y se registran respuestas.

## AMBIGUEDADES

1. «Preflight solo-TaskDoc de la tarea…» no concuerda con `task_type: task.external` ni con el Implementation Path, que exige mensajes y commits. Obligaría a inventar si el nodo valida solo el documento o ejecuta la coordinación.
2. «`--to traderbot` (si `--to traderbot` no resuelve en robocop2, pedirlo a JP…)»: no define el comando ni el canal alternativo; obligaría a inventar cómo se contacta a JP.
3. «agregando el commit (repo:sha o URL) al campo `references`»: no fija el formato exacto ni si admite varias entradas; obligaría a inventar un esquema.
4. «ninguna tarea … usa ya code/implementation/test/docs/spec/design/external sin prefijo task» frente a la validación que admite «task.code, task.docs, … task.external»: no aclara el mapeo legacy→nuevo de cada valor; obligaría a inventarlo.
5. «Cada respuesta se registra»: no indica quién la registra, ni si una respuesta parcial permite cerrar; obligaría a inventar el criterio de cierre.

## DRY-RUN

**Lecturas:** task doc, drawer de origen, `~/setup/desk/registry/repo-traderbot.md`, `desk/tasks` y `desk/drawer/tasks` de sldb.
**Cambios previstos:** `deskops message send --to sldb`, intento a traderbot o escalado a JP, y `deskops edit task` para añadir commits a `references`.
**Dependencias:** resolución de destinatarios en robocop2 y respuesta de JP.
**Validaciones futuras:** `grep` de `task_type` en sldb y commit de TraderBot citado.

## FUTURO

JP o un humano aporta la ruta/máquina de TraderBot; sldb y TraderBot responden con sus commits; el coordinador valida y cierra.
