## REFORMULACION
El nodo es una tarea documental ejecutable (`task.docs`) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Su propósito es incorporar a la guía versionada de deskops la regla de que los cambios solo de desk se hacen en el checkout principal, sobre la rama de integración, con `git add` selectivo, commit `[skip ci]` y push; los worktrees quedan para cambios de código con PR. El resultado esperado es que esa regla aparezca, con el mismo contenido, en `.opencode/skills/use-deskops/SKILL.md` y en `docs/operator-manual.md`. Límites: solo esos dos archivos; no incluye aviso de deskops al ejecutar en worktree secundario ni `.pi/skills`.

## AMBIGUEDADES
1. «Copiar el parrafo de .claude/skills/deskops-workflow/SKILL.md:80-85 adaptado a cada archivo» junto a «con el mismo contenido»: no se incluye el texto fuente ni se define cuánto puede adaptarse. Obligaría a inventar la redacción final o a decidir si “adaptado” permite cambiar el contenido.
2. «seccion de commits del desk»: no se identifica el encabezado exacto ni la posición dentro de `docs/operator-manual.md`. Obligaría a inventar la ubicación definitiva.
3. «correr los tests»: no nombra cuáles en el cuerpo, aunque `Validation` enumera dos comandos concretos. Si se ignorara esa lista, obligaría a inventar el alcance de pruebas.

## DRY-RUN
Lecturas previstas: el TaskDoc, `.claude/skills/deskops-workflow/SKILL.md:80-85`, ambos archivos destino y los tests citados. Cambios previstos: insertar el párrafo equivalente en `.opencode/skills/use-deskops/SKILL.md` y en la sección de commits de `docs/operator-manual.md`; ningún otro archivo. Dependencias: que exista el fragmento fuente y que los destinos conserven estructura compatible. Validaciones futuras, sin ejecutarlas ahora: los dos `pytest` indicados y el `grep -n 'checkout principal'` sobre ambos archivos.

## FUTURO
Un humano o nodo revisor debe confirmar la redacción final y la ubicación en el manual; otro ejecutor realizará los cambios y correrá las validaciones. El cierre depende de que el grep encuentre la regla en ambos archivos y de que ambos tests pasen.
