# Brief: deskops pasa a ser un plugin sobre sldb

Fecha: 2026-11-25. Repo dueño: deskops (pedidos a sldb por su inbox).

## Encargo de JP (2026-11-25)

1. deskops debe ser un plugin sobre sldb, no una reimplementación ("el modelo es claro").
2. Primero se refactoriza y después se revisan las 53 tareas del Board: arreglando lo que está mal, el resto se ordena solo.
3. Se arrastra slop: documentación mala, tests añejos, código desorganizado y sin linteo. Se limpia como parte del refactor.

## Estado medido (2026-11-25, main 85f1f766)

- 27 236 líneas de Python en `deskops/` (117 archivos); sldb tiene 56 370.
- El núcleo del workflow ya es dato: aristas en `desk/lifecycle/*`, RuleDoc `rule-activation-*` y `rule-closeout-*`,
  ReviewDoc, ViewDoc `data/views/board.md` y `task.md`.
- Alrededor de ese núcleo, ~12 000 líneas sobran: ~6 500 reimplementan sldb, ~3 000 son dato escrito como código,
  ~2 300 son genéricas y deben ser de sldb, ~500 son legacy.
- Siete desacuerdos entre ritos y código (W1–W7, en `alcance.md`). W3 verificado: `closeout_rule_findings`
  (`deskops/services/closure.py`) fuerza `current_node = ritual-closeout` sin tomar la arista `task_completes`.
- sldb aplica RuleDoc y RelationDoc solo del store local (`sldb/docs/architecture/rules.md` §3); las vistas sí se leen
  por enlace (H9). Por eso deskops copia sus semillas a cada desk.
- Lint: sin configuración de ruff, 175 errores, 211 de 248 archivos sin formatear, sin pre-commit.
- Tests: 118 archivos, 30 507 líneas (más que el código), 232 goldens; el `--help` está fijado byte a byte.
- Docs: 32 Markdown, 5 623 líneas; algunos contradicen los ritos (W2).
- CI: rojo desde el 22-11 (golden de `add atom` en 3.13; `sldb stores build --check` por `domain:knowledge-management`),
  1 h 23 en serie.

## Forma

Cinco paquetes en orden (ver `dag.yaml`): F0 base (lint, CI, inventario de tests), F1 contrato del plugin,
F2 usar bien sldb, F3 workflow como dato, F4 pedidos a sldb (en paralelo), F5 limpieza y revisión de las 53 tareas.

## Reglas del plan

- Paridad es de capacidades, cada una con su test de aceptación; nunca de código ni de salida byte a byte
  (AGENTS.md del workspace). Los goldens de `--help` se regeneran a propósito cuando el CLI adelgaza.
- Lo genérico que falta en sldb se pide por su inbox (`deskops message send --to sldb --kind unclear`) y no se construye
  en deskops.
- Una regla de docs: el átomo primero, el doc lo materializa (AGENTS.md de deskops).
- Código en un worktree `refactor/plugin-sldb`, un PR por paquete, squash. El desk se edita en el checkout principal.

## Fuera de alcance

- Ejecutar o reorganizar las 53 tareas del Board antes de F5 (quedan congeladas).
- Cambios en sldb: este plan solo los pide.
- La UI de deskops (vive en `UIs/graph_ui/frontends/desk`).
