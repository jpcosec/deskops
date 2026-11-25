## REFORMULACION

Propósito: retirar el nombre `use-spec2viz` de las superficies de onboarding del repo `/mnt/ssd/proyectos/SLDB_1/deskops` y alinearlas con la skill `use-specir` del repo IR (IR13). Resultado esperado: `AGENTS.md` y `README.md` dejan de instruir a usar `use-spec2viz`/`references/spec2viz-cli.md`; la carpeta `.opencode/skills/use-spec2viz` pasa por `git mv` a `.opencode/skills/use-specir`. Límites: solo esos tres puntos; quedan fuera `.claude/skills/deskops-workflow`, el repo IR y las menciones históricas de spec2viz.

## AMBIGUEDADES

1. «nombran la skill use-specir … en vez de … references/spec2viz-cli.md» frente a «Sale: .claude/skills/deskops-workflow (ya migrada)»: README describe ese skill como portador de `references/spec2viz-cli.md`. ¿Se edita esa línea aunque el archivo exista fuera de alcance? Obliga a inventar el estado real del skill de Claude.
2. «menciones historicas de spec2viz (por ejemplo 'spec2viz se archiva'), que se quedan» frente a «grep -rn use-spec2viz … sin coincidencias»: el `SKILL.md` se titula «use-spec2viz → use-specir» y el README conserva «Spec2viz Boundary» y el átomo `atom-spec2viz-mirrors-sldb-for-diagrams`. ¿Cuenta como histórica? Habría que inventar el criterio.
3. «con su SKILL.md sin cambios de contenido» frente a «dejan de nombrar use-spec2viz»: el contenido se autodenomina `use-spec2viz`. Contradicción que exige decidir si se toca.
4. «grep … .opencode» cubre otras skills (`use-deskops`, `use-sldb`) no listadas en `files`; no hay inventario de esas menciones. Inventar qué archivos editar.
5. «use-specir (skills/use-specir/SKILL.md del repo IR)»: no hay copia local; se desconoce si se enlaza ruta remota o solo se nombra.

## DRY-RUN

Lecturas hipotéticas: `AGENTS.md`, `README.md`, árbol `.opencode/skills/`, `tests/test_skill_cli_drift.py`, `git status`. Cambios previstos: sustituir en `AGENTS.md` la viñeta `use-spec2viz` y las referencias de boundaries; en `README.md` la mención a `references/spec2viz-cli.md`; `git mv` de la carpeta. Dependencias: `git` disponible, nombre del frontmatter ya `use-specir`. Validaciones futuras: `pytest -q tests/test_skill_cli_drift.py` y el `grep` sin coincidencias; commit atómico vía `deskops closeout commit`.

## FUTURO

Un humano u otro nodo resuelve las ambigüedades 1–5 antes de implementar; el ejecutor aplica el plan; el closeout verifica evidencia y registra el commit.
