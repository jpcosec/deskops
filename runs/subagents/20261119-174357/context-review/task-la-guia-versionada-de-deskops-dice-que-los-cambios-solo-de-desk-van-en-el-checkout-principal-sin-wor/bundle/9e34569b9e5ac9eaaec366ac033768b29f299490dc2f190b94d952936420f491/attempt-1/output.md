## REFORMULACION
Tarea documental ejecutable (`task.docs`), no un agregado. **Propósito:** incorporar a la guía versionada de deskops la regla de que los cambios solo de `desk/` se hacen en el checkout principal, nunca en un worktree. **Resultado:** el párrafo inglés indicado en el Goal, “igual en ambos archivos”, dentro de `.opencode/skills/use-deskops/SKILL.md` y en una nueva subsección `### Desk-only changes` de `docs/operator-manual.md`. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** solo esos dos archivos; quedan fuera el aviso de deskops dentro de worktrees secundarios y `.pi/skills`.

## AMBIGUEDADES
1. “en `.opencode/skills/use-deskops/SKILL.md` y en `docs/operator-manual.md` (subseccion nueva '### Desk-only changes' al final de la seccion '## Desk scaffold, migration, and repair')”. Solo se ubica la subsección del manual, no el punto de inserción en `SKILL.md`; obligaría a inventar sección y posición.
2. “Copiar el parrafo de `.claude/skills/deskops-workflow/SKILL.md:80-85` adaptado a cada archivo”, frente a “La regla aparece en inglés, igual en ambos archivos”. “Adaptado” no define diferencias admisibles; obligaría a decidir si se copia literal o se contextualiza.
3. “correr los tests” no identifica cuáles, aunque Validation los concreta; obligaría a inventar cobertura adicional si se interpretara literalmente como suite completa.

## DRY-RUN
- **Lecturas previstas:** TaskDoc; `desk/tasks/Board.md`; rituales enrutados; pills y átomos ligados; ambos archivos destino; `.claude/skills/deskops-workflow/SKILL.md:80-85`; tests citados.
- **Cambios previstos:** insertar el párrafo exacto en `SKILL.md` y crear `### Desk-only changes` en el manual con el mismo texto.
- **Dependencias:** ubicación existente de la sección del manual, contenido fuente de `.claude`, y expectativas de `test_skill_cli_drift.py` y `test_operator_manual.py`.
- **Validaciones futuras:** ejecutar ambos `pytest` y el `grep`, esperando una línea por archivo. No se ejecutó nada.

## FUTURO
Otro nodo aplicará las ediciones y ejecutará las validaciones; el cierre requerirá que el grep encuentre ambos textos y que pasen los dos tests. Un humano decidirá la ubicación concreta en `SKILL.md` si no se deduce de los rituales o del test.
