---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T22:47:57'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# IR13 pide migrar las habilidades y el script de deskops de spec2viz a specIR

_Describe the incoming message with enough evidence to triage._

IR13 (gate de retiro de spec2viz, repo IR) pide migrar las dependencias de deskops sobre spec2viz. El retiro no está declarado y no se borra nada todavía: esto es el pedido de migración que exige el gate (G4). Salida del comprobador `specir retirement check` (IR, solo lectura) sobre deskops:

1. Habilidad de agente que instruye a invocar spec2viz:
   - `.claude/skills/deskops-workflow/SKILL.md:27, 59, 60, 101, 102, 103` (`spec2viz diagram render|validate`, `spec2viz catalog build`).
   - `.claude/skills/deskops-workflow/references/spec2viz-cli.md` (líneas 8 a 84, toda la referencia del CLI de spec2viz).
   - `.opencode/skills/use-spec2viz/SKILL.md:2` (habilidad use-spec2viz).
   Sustituto: la habilidad `skills/use-specir/SKILL.md` del repo IR y la tabla `IR/docs/spec2viz/correspondencia-cli.md` (`spec2viz diagram render` -> `specir diagram render`, `spec2viz diagram validate` -> `specir diagram validate` (provisional hasta que sldb tenga su comando), `spec2viz catalog build` -> `specir catalog build`, `catalog sync/validate` -> `sldb notations sync --catalog [--check]`, `catalog serve` -> `sldb serve`, `diagram generate/from-graph` -> `sldb notations from-graph`).
2. Invocación del comando: `desk/drawer/plans/workspace-documental/render_diagram.py:7` y `:9` (`spec2viz diagram validate` y `diagram render`) -> `specir diagram validate` y `specir diagram render` (mismos argumentos; `--renderer` igual).
3. Regla de rutas del grafo del desk (no la cuenta el comprobador, pero la lista el inventario): `deskops/graph/desk_graph.py:75` `FileRule(kind="spec", path_prefixes=("spec", "docs/architecture/spec2viz"))`. Depende de la decisión sobre el YAML de spec frente al grafo (G7, propuesta pendiente de JP en `IR/docs/decisiones/fuente-de-verdad-del-diagrama.md`); no hace falta tocarla hasta que JP decida.

Cuando esté resuelto, respondan con la referencia del commit para registrarla en `IR/docs/spec2viz/acta-de-retiro.md`. Verificación: `cd IR && .venv/bin/specir retirement check --path deskops=<ruta> ...` no debe listar nada de deskops.
