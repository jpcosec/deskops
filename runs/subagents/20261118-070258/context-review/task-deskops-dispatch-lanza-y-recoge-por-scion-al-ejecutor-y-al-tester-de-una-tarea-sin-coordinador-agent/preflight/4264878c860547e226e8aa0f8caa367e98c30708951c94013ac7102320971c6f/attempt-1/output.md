## REFORMULACION

Encargo ejecutable (`task.code`) en el repo deskops, checkout principal. Propósito: quitar al coordinador agente el trabajo manual de identidad, template, prompt y `scion start/stop/delete` de ejecutores y testers, encadenando funciones ya existentes en `deskops/runtime/scion.py`. Resultado: grupo `deskops dispatch` con `start <executor|tester> --task <id> --root .` (valida ausencia de agente running, calcula identidad, materializa template y sincroniza, escribe prompt.md, lanza con prompt corto, imprime nombre y run_dir) y `reap --task <id> --root .` (detiene y borra terminados, informa motivo, códigos 0/4); más campo `dispatch` en `DeskConfig`, registro en `cli/registry.py`, tests y manual. Límites: no integrar/push, no configurar desks reales, no tocar scion, sin worktree/rama, sin git add/commit.

## AMBIGUEDADES

1. "materializa el template con las mismas funciones que usa deskops runtime template" — no nombra funciones; obligaría a inventar/descubrir cuáles.
2. "modo igual al rol" — no define qué es "modo".
3. "con sufijo -testing para el tester" — no aclara si aplica al agent_name, al run_dir o ambos.
4. "el texto del TaskDoc" — no especifica qué parte (cuerpo, frontmatter, campos).
5. "activity es completed, blocked o limits_exceeded, si su phase no es running, o si existe result-summary.md" — no define prioridad ni el motivo a imprimir cuando varios aplican.
6. "intento 1, o 2 si el run_dir del intento 1 ya existe" — no dice qué hacer si también existe el 2.
7. "los agentes cuya etiqueta deskops.task_id es la de la tarea" — formato exacto de etiqueta no indicado.

## DRY-RUN

Lecturas: `deskops/runtime/scion.py`, `config.py`, `cli/registry.py`, `docs/operator-manual.md`, tests existentes. Cambios previstos: nuevo `dispatch.py`, campo en config, registro CLI, tests nuevos, manual. Dependencia: la tarea de runner/cola (`task-un-runner-del-host...`). Validación futura: `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py` con scion falso en PATH y desk desechable. Nada se ejecuta ahora.

## FUTURO

Otro nodo integra y pushea; un humano decide configuración real en desks y el formato de etiqueta; la cola del host invoca estos comandos.
