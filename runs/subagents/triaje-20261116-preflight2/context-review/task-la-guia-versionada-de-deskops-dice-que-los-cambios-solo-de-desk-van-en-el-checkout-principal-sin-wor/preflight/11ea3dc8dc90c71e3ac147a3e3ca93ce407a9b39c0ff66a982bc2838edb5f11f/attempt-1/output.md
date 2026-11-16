## REFORMULACION

Nodo ejecutable (`task.docs`), no agregado. Propósito: documentar que los cambios solo de desk (crear tarea, notas, editar campo, closeout) se hacen con deskops en el checkout principal, sobre la rama de integración, sin worktree. Resultado: el párrafo base en `.opencode/skills/use-deskops/SKILL.md` y una subsección nueva `### Cambios solo de desk` al final de `## Desk scaffold, migration, and repair` en `docs/operator-manual.md`, adaptando solo idioma y formato. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no tocar `.pi/skills` (no versionado) ni implementar el aviso de deskops al correr en worktree secundario.

## AMBIGUEDADES

1. «Se adapta solo el idioma y el formato del archivo» frente a un texto base en español y un encabezado literal en español («### Cambios solo de desk»). El input no declara el idioma de cada archivo; obliga a inventar si se traduce el párrafo y el encabezado o se dejan literales.
2. «grep -n 'checkout principal' .opencode/skills/use-deskops/SKILL.md docs/operator-manual.md» frente a la adaptación de idioma: si se traduce, el grep no encuentra la cadena. Contradicción entre Validación y Goal que obliga a decidir cuál prevalece.
3. «Copiar el parrafo de .claude/skills/deskops-workflow/SKILL.md:80-85»: referencia por número de línea; si el archivo difiere, hay que localizar el párrafo por contenido, no por línea.

## DRY-RUN

Lecturas: los dos archivos destino, `.claude/skills/deskops-workflow/SKILL.md` (líneas 80-85), `tests/test_skill_cli_drift.py`, `tests/test_operator_manual.py` y la sugerencia enlazada. Cambios previstos: insertar el párrafo adaptado en `SKILL.md` y añadir la subsección al final de la sección indicada del manual. Dependencias: `depends_on` vacío; solo la referencia de inbox. Validaciones futuras: los dos `pytest -q` indicados y el grep. Nada ejecutado.

## FUTURO

Un humano debe resolver la contradicción idioma/grep (traducir y ajustar la validación, o dejar la cadena literal). Otro nodo ejecutará commit con `[skip ci]` y push en el checkout principal, y el closeout; también decidir si se retoma el aviso en worktrees.
