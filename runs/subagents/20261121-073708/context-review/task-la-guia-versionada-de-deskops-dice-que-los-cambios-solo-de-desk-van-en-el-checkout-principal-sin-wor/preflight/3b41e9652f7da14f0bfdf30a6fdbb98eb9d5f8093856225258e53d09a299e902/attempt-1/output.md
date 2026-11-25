## REFORMULACION

Nodo ejecutable de documentación en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: documentar que los cambios solo de desk se hacen en el checkout principal, nunca en un worktree. Resultado: el mismo párrafo en inglés en `.opencode/skills/use-deskops/SKILL.md` y en `docs/operator-manual.md`, dentro de una subsección nueva `### Desk-only changes` al final de `## Desk scaffold, migration, and repair`. Límites: solo esos dos archivos; quedan fuera el aviso de deskops al ejecutarse en un worktree secundario y `.pi/skills`.

## AMBIGUEDADES

1. «en `.opencode/skills/use-deskops/SKILL.md` y en `docs/operator-manual.md` (subseccion nueva… )»: se fija la ubicación del manual, pero no dónde insertar el párrafo en `SKILL.md`; obligaría a inventar sección o punto de inserción.
2. «Copiar el parrafo… adaptado a cada archivo» frente a «La regla aparece en inglés, igual en ambos archivos»: obligaría a decidir si «adaptado» permite variar redacción o formato, aunque el texto exigido parece único.

## DRY-RUN

Lecturas previstas: tarea, nota referenciada, `.claude/skills/deskops-workflow/SKILL.md:80-85`, ambos destinos y tests citados. Cambios previstos: insertar el párrafo literal en `SKILL.md` y añadir la subsección con el mismo párrafo en `operator-manual.md`; sin tocar otros archivos. Dependencias: que exista el texto fuente y la sección del manual. Validaciones futuras, sin ejecutar: `pytest` de `test_skill_cli_drift.py` y `test_operator_manual.py`, más `grep` de la frase inicial en ambos archivos, con una línea por archivo.

## FUTURO

Otro nodo ejecutará los tests y el `grep`; el humano revisará el diff, resolverá la ubicación en `SKILL.md` y aprobará el cierre. El commit/push seguirá la regla documentada, fuera de este preflight.
