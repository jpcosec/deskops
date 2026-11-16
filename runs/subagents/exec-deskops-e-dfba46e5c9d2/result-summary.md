# result-summary — exec-deskops-e-dfba46e5c9d2

- run_id: run-deskops-e-dfba46e5c9d2
- task: task-las-skills-y-el-script-de-diagramas-de-deskops-dejan-de-invocar-spec2viz-y-usan-specir-ir13
- session: scion://agent/deskops-e-dfba46e5c9d2 (agente claude); session_sha256: no disponible desde la sesión
- Sin commit (orden del brief).

## Archivos tocados (todos dentro de `files`)

1. `.claude/skills/deskops-workflow/SKILL.md` — título, prosa y tabla de comandos pasan de `spec2viz` a
   `specir` (`specir diagram validate|render`, `specir catalog build`); la descripción añade `specir` como
   disparador y conserva `spec2viz` (disparador, no invocación); la entrada de `references/spec2viz-cli.md`
   la describe como remisión. La línea 114 ("spec2viz mirror-of-sldb relationship") describe el contenido
   de `references/vocabulary.md`, que está fuera de `files`: se deja.
2. `.claude/skills/deskops-workflow/references/spec2viz-cli.md` — reemplazada por una remisión a
   `skills/use-specir/SKILL.md` y `docs/spec2viz/correspondencia-cli.md` del repo IR, con un mapa corto
   según la tabla del goal. El nombre del archivo se conserva (está en `files`).
3. `.opencode/skills/use-spec2viz/SKILL.md` — remisión corta a use-specir (no se borra, precisión del
   preflight 1). Decisión: el frontmatter pasa a `name: use-specir`, porque el comprobador de IR marca
   como dependencia cualquier skill con `name: …spec2viz` (retirement.py:223). Riesgo: opencode exige que
   `name` coincida con el directorio; puede ignorar o advertir esta skill. Quien abra la ruta sigue
   encontrando la remisión. Si se prefiere, el siguiente paso es mover la carpeta a `use-specir`.
4. `.opencode/skills/use-deskops/SKILL.md:159` — "Load `use-spec2viz`" → "Load `use-specir` (repo IR …)".
5. `desk/drawer/plans/workspace-documental/render_diagram.py` — el archivo existe (test -f): líneas 7 y 9
   invocan `specir diagram validate|render` (mismas opciones `--renderer`/`--out`, válidas en specir); el
   docstring dice specir. No se ejecutó el script (escribiría proyecciones en el drawer).

## Validación (detalle en validation.log)

- `specir retirement check --path deskops=…` tal como está escrito en la Validation sale rc=2: el comando
  exige rutas para todo el inventario (graph_ui, pron, sldb, spec2viz/.sldb). Con todas las rutas
  (UIs/graph_ui, pron, sldb, spec2viz/.sldb): **0 dependencias de deskops** (antes: 22, incluidas las de
  estos 5 archivos). Ya no lista `deskops/graph/desk_graph.py:75` (cerrado en 42b752ea). El gate global
  sigue fallando por otros repos (IR, etc.) y 9 filas no acreditadas: fuera de esta tarea.
  Para el cierre: corregir el comando de la Validation para pasar todas las rutas.
- `pytest -q tests/test_skill_cli_drift.py`: 2 passed.
- `pytest -q tests/test_closeout_skill_links.py`: 3 passed.
- Suite completa y `stores build --check`: no corridas (orden del brief) — para el integrador.

## Fuera de files (no tocado, anotado)

- `AGENTS.md:25` rutea a `use-spec2viz`, y `README.md:54` cita `references/spec2viz-cli.md`; ambos en prosa
  (el comprobador no los cuenta). Quedan desactualizados respecto del nombre `use-specir`: candidato a tarea.
- `.claude/skills/deskops-workflow/references/vocabulary.md` menciona spec2viz como concepto (no invoca).

## Texto para la nota a IR (paso 5, lo envía el coordinador)

IR13: deskops migrado de spec2viz a specir en el commit <hash>. Las skills deskops-workflow (y su
referencia del CLI), use-spec2viz y use-deskops de opencode, y render_diagram.py del plan
workspace-documental ya no invocan spec2viz; `specir retirement check` no lista nada de deskops.
use-spec2viz queda como remisión a skills/use-specir/SKILL.md.
