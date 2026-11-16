# Encargo del tester deskops-t-4466e4d961b1 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-las-skills-y-el-script-de-diagramas-de-deskops-dejan-de-invocar-spec2viz-y-usan-specir-ir13` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" del scope son parte del contrato).
Entrega del ejecutor: cambios sin commitear en .claude/skills/deskops-workflow/SKILL.md, .claude/skills/deskops-workflow/references/spec2viz-cli.md, .opencode/skills/use-spec2viz/SKILL.md, .opencode/skills/use-deskops/SKILL.md y desk/drawer/plans/workspace-documental/render_diagram.py, más su evidencia en runs/subagents/exec-deskops-e-dfba46e5c9d2/ (result-summary.md, validation.log). No confíes en ese resumen: compruébalo.

1. Lee el diff de esos 5 archivos contra el goal (tabla de correspondencia), el scope y el done_when. Cada invocación de spec2viz pasa a su equivalente (specir diagram render|validate, specir catalog build, sldb notations sync --catalog [--check], sldb serve, sldb notations from-graph); las menciones históricas se pueden quedar; use-spec2viz queda como remisión corta (no se borra). Coteja con /mnt/ssd/proyectos/SLDB_1/IR/docs/spec2viz/correspondencia-cli.md y IR/skills/use-specir/SKILL.md (solo lectura) que los comandos y opciones que ahora citan las skills y render_diagram.py existen en specir (por ejemplo con `/mnt/ssd/proyectos/SLDB_1/IR/.venv/bin/specir diagram render --help`).
2. Juzga la decisión del ejecutor de poner `name: use-specir` en el frontmatter de .opencode/skills/use-spec2viz/SKILL.md (la carpeta sigue llamándose use-spec2viz): ¿cumple la precisión "remisión corta, no se borra"? ¿rompe algo real? Lo dices en el veredicto; un riesgo aceptable no es motivo de rechazo.
3. Corre el comprobador de IR (solo lectura): el comando de la Validation tal cual sale rc 2 porque exige todas las rutas del inventario; córrelo como lo corrió el ejecutor (validation.log) y confirma que no lista nada de deskops.
4. Corre tú, de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py` y lo mismo con tests/test_closeout_skill_links.py.
5. `grep -rn spec2viz .claude .opencode desk/drawer/plans/workspace-documental/render_diagram.py`: cada coincidencia que quede es histórica, de disparador o de nombre de archivo, no una instrucción de invocar spec2viz.
6. NO corras la suite completa ni stores build --check (orden del integrador wA:p1). No ejecutes render_diagram.py (escribiría en el drawer).

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-4466e4d961b1/ y /dev/shm (nada en IR), y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-4466e4d961b1/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
