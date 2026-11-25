REFORMULACION
Nodo TaskDoc ejecutable, no agregado. Propósito: actualizar documentación y estructura de la skill opencode para que deje de nombrar use-spec2viz y pase a use-specir. Resultado: AGENTS.md y README.md apuntan a la skill use-specir (`skills/use-specir/SKILL.md` del repo IR); `.opencode/skills/use-spec2viz` se renombra a `.opencode/skills/use-specir` con SKILL.md sin cambios de contenido. Repo: deskops, con validación en `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo AGENTS.md, README.md y el git mv de esa carpeta; fuera `.claude/skills/deskops-workflow`, el repo IR y menciones históricas de spec2viz.

AMBIGUEDADES
1. “AGENTS.md y README.md nombran la skill use-specir del repo IR” frente a “cd /mnt/ssd/proyectos/SLDB_1/deskops”: obliga a decidir si se editan archivos de deskops o del repo IR.
2. “Cambiar cada mencion ... por use-specir (skills/use-specir/SKILL.md del repo IR)”: obliga a inventar la redacción exacta: ¿“use-specir”, la ruta completa u otra frase?
3. “menciones historicas de spec2viz ... que se quedan” frente a “grep -rn use-spec2viz ... (sin coincidencias, rc 1)”: obliga a inventar qué menciones son históricas y cómo sobreviven al grep.
4. “atom-code-changes-close-with-tests-and-commit” sin mensaje, rama ni alcance del commit: obliga a inventar la política de commit.
5. “la carpeta ... tiene name: use-specir en su frontmatter” y “SKILL.md sin cambios de contenido”: si el frontmatter no coincide, obliga a decidir si se corrige pese a la restricción.

DRY-RUN
Lecturas: AGENTS.md, README.md, `.opencode/skills/use-spec2viz/SKILL.md` y `tests/test_skill_cli_drift.py`; grep de `use-spec2viz`/`spec2viz`. Cambios previstos: editar solo menciones instructivas en AGENTS.md y README.md; `git mv` de la carpeta; no tocar contenido de SKILL.md. Dependencias: checkout de deskops, git, `../.venv` y test existente. Validaciones futuras: pytest indicado y grep sin coincidencias; comprobar nombre de carpeta y frontmatter. Sin ejecutar nada.

FUTURO
Un ejecutor aplicará ediciones y `git mv`; un humano o planificador resolverá redacción y límites; el repo IR confirma la ruta `skills/use-specir/SKILL.md`; el nodo de cierre hará el commit según el átomo; la validación se ejecutará en el entorno indicado.
