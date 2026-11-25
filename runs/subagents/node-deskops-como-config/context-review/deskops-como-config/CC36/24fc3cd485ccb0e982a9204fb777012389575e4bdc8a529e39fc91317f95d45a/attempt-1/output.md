## REFORMULACION

**Propósito:** sacar de `workspace.py` las plantillas del desk (config.json, Board, pills, rituales, drawer, tag-namespaces) y convertirlas en datos del paquete (`deskops/data/templates/`) declarados en `deskops/data/desk_declaration.yaml` (folders y seeds, `if_missing`), que deskops pasa a `sldb.api.scaffold_store(declaration=..., apply)` (GD26, DP3); `desk update` deja de adivinar modelos por ruta y usa includes `{model, glob}`.
**Resultado:** `init` y `update --apply` con las mismas rutas/sha256 y el mismo reporte created/preserved que el golden, segunda corrida sin cambios, `default_ritual_text` leyendo plantilla, y borradas `scaffold_desk`, `_write_if_missing` y los `*_template`. FAQ sigue en `docs/faq.md` con respaldo en `deskops/data/faq.md`; `init` no la escribe.
**Repo:** deskops. **Límites:** no escribe en sldb; no suple con Python; no cambia formato del desk ni gramática del CLI; `inspect_desk`/`migrate_desk` quedan.

## AMBIGUEDADES

1. «las de ciclo de vida, reglas y vistas que agreguen CC31/CC32/CC34 con modo managed» — CC36 no produce esos documentos y no depende de ellos; el ejecutor tendría que inventar si declara ya entradas `managed` vacías/placeholder o si eso queda enteramente a esos nodos.
2. «usa includes declarados {model, glob} (apply_includes de sldb)» — la evidencia de `G_GD26` solo cubre `scaffold_store(declaration=..., apply)` con modos `if_missing`/`managed`; no hay gate ni contrato suministrado para `apply_includes`, así que el ejecutor debería inventar esa API o detenerse.
3. «un desk de los 6 (copia) con desk update en dry-run no reporta cambios nuevos» — sin línea base explícita (desk aún sin migrar) no se sabe si «nuevos» se mide contra el golden de `init` o contra el estado previo; la aceptación no es comprobable tal cual.

## DRY-RUN

Leería `workspace.py`, `operations.ensure_workspace`, `lifecycle.default_ritual_text`, `cli/commands/desk.py`, `bootstrap.py`, la API de scaffold de sldb y los goldens. Capturaría el golden (rutas y sha256 de `init`, reporte de `update --apply` en desk viejo). Crearía `data/templates/` y `desk_declaration.yaml`, adaptaría esas funciones, borraría las nombradas y actualizaría tests, goldens y CHANGELOG. Validaría: pytest de archivos tocados, doble corrida idempotente, greps, goldens de ayuda de `init`/`desk`, `doctor` en copia de los 6 desks.

## FUTURO

CC31/CC32/CC34 declaran sus documentos `managed`; CC51 mide líneas; CC53 documenta. El TaskDoc fija nombres exactos; el supervisor corre la suite completa; sldb entrega `apply_includes` si falta.
