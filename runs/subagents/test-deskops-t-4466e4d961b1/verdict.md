# Veredicto del tester deskops-t-4466e4d961b1

Tarea: `task-las-skills-y-el-script-de-diagramas-de-deskops-dejan-de-invocar-spec2viz-y-usan-specir-ir13`
Entrega: ejecutor deskops-e-dfba46e5c9d2 (5 archivos sin commitear). Evidencia: `validation.log` en esta carpeta.

**VEREDICTO: APROBADO**

## 1. Diff contra goal, scope y done_when

- `.claude/skills/deskops-workflow/SKILL.md`: las invocaciones pasan a `specir diagram validate`, `specir diagram render ... --out <dir> [--renderer ...]` y `specir catalog build --config ... --out ...` (líneas 27, 59-60, 101-103). Las menciones que quedan son un disparador (`description`, línea 3: "mentions ... specir, spec2viz"), una nota histórica (línea 14: "replaces the retired spec2viz") y el nombre del archivo de referencia (líneas 111-112). En la línea 114, la remisión a vocabulary.md ("spec2viz mirror-of-sldb") es texto preexistente y conceptual.
- `references/spec2viz-cli.md`: se reemplaza por una remisión a `IR/skills/use-specir/SKILL.md` y `IR/docs/spec2viz/correspondencia-cli.md`, con un mapa corto que sigue la tabla del goal. El archivo conserva su nombre, que está en `files`.
- `.opencode/skills/use-deskops/SKILL.md:159`: "Load `use-spec2viz`" pasa a `use-specir` (repo IR).
- `.opencode/skills/use-spec2viz/SKILL.md`: queda como remisión corta y no se borra, como pide la precisión del preflight 1. Su mapa coincide con la correspondencia.
- `desk/drawer/plans/workspace-documental/render_diagram.py`: el archivo existe (`test -f` rc 0). Las líneas 7 y 9 y el docstring ahora usan `specir diagram validate|render`, con las mismas opciones `--renderer`/`--out`. El archivo parsea como Python válido. No lo ejecuté.
- Comprobé contra specir (`IR/.venv/bin/specir --help` de cada subcomando) que existen `diagram render` (`--out`, `--renderer/--backend`, con los renderers mermaid, plantuml, vega, d2, antonia-html, graph y json), `diagram validate`, `diagram lint`, `diagram schema` (`--type`, `--out`), `catalog build` (`--config`, `--out`) y `catalog schema`. Contra sldb existen `notations sync` (`--catalog`, `--check`), `serve` y `notations from-graph`. Todos coinciden con correspondencia-cli.md (SV-K04/05/06/07/08/10/11/12/13/14/16).

## 2. Decisión `name: use-specir` en la carpeta use-spec2viz

- Es necesaria para cumplir el done_when. El comprobador marca cualquier `name:` que contenga spec2viz en las 10 primeras líneas de una skill (`IR/src/specir/visual/retirement.py:223`). Como la precisión obliga a no borrar el archivo, conservar `name: use-spec2viz` dejaría una dependencia listada.
- Cumple "remisión corta, no se borra": el archivo sigue en su ruta y remite a use-specir.
- Riesgo aceptable: opencode exige que `name` coincida con el nombre de la carpeta, así que puede ignorar esta skill o avisar al cargarla. Eso no rompe nada real. use-deskops ya rutea a use-specir del repo IR, y quien abra la ruta por archivo encuentra la remisión. Si se quisiera eliminar el riesgo, habría que renombrar la carpeta a `use-specir`, pero eso queda fuera de `files`.

## 3. Comprobador de IR

- Tal como está escrito en la Validation sale rc 2 ("no path given for: graph_ui, pron, sldb, spec2viz/.sldb"), lo mismo que le pasó al ejecutor.
- Con todas las rutas del inventario da rc 1 porque el gate global falla por otros repos (IR, etc.). Tiene **0 filas de deskops** (`grep -cP '\tdeskops\t'` = 0) y tampoco lista `desk_graph.py:75`, que ya se cerró en 42b752ea. El "rc=0" del log del ejecutor era el del `grep` de su tubería, no el del comprobador. No cambia el resultado, pero conviene corregir el comando de la Validation al cerrar.

## 4. Tests

- `tests/test_skill_cli_drift.py`: 2 passed, rc 0.
- `tests/test_closeout_skill_links.py`: 3 passed, rc 0.

## 5. grep spec2viz

Cada coincidencia que queda es histórica ("retired"/"replaces"), un disparador en `description`, un nombre de archivo o carpeta, o la ruta `docs/spec2viz/` de IR. Ninguna instruye a invocar spec2viz. La lista completa está en validation.log.

## Riesgos y pendientes (fuera de `files`, no bloquean)

- `AGENTS.md:25` sigue ruteando a `use-spec2viz` y `README.md:54` cita `references/spec2viz-cli.md`. Ambos son prosa y apuntan a la remisión, que sigue existiendo. Son candidatos a una tarea aparte.
- `.claude/skills/deskops-workflow/references/vocabulary.md` (líneas 1 y 14) describe spec2viz como concepto y no lo invoca.
- El paso 5 (nota a IR con el hash) se hace después del commit de cierre y corresponde al coordinador.
- No corrí la suite completa ni `stores build --check`, por orden del integrador.
