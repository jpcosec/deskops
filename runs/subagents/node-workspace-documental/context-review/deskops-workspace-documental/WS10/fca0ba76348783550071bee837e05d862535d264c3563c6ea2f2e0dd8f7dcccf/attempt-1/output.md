## REFORMULACION

**Propósito:** fijar, como encargo de planificación, el índice y el esquema de capítulos conceptuales del manual documental, sin redactarlo completo.

**Resultado:** `borradores/manual.md` con índice, propósito/entradas/salidas por capítulo, referencia al ejemplo fijo P08 y etiqueta de disponibilidad.

**Repo dueño:** `deskops`.

**Límites:** no redactar el manual completo ni inventar pasos, capturas o estados; usar auditorías WS02–WS04 y el manual CLI existente; el ejemplo Taller (`graph_ui:.tmp/workspace-documental-ejemplo/`, productor WS40) se describe como corpus futuro mientras no exista.

## AMBIGUEDADES

1. **«reutilizar manual CLI»** — no identifica repo, archivo ni nombre del manual. Obliga a inventar cuál es la fuente a reutilizar y dónde está.
2. **«acta humana del recorrido y pasos verificados»** y **«remitir pruebas/actas futuras a sus productores»** — no se nombra qué nodo produce el acta ni las pruebas relevantes. Obliga a inventar el productor y el documento que acredita «disponible».

## DRY-RUN

**Lecturas previstas:** nodo WS10 en `dag.yaml`; `brief.md`, `alcance.md`, `decisiones.md`; auditorías WS02–WS04 (`auditoria/deskops.md`, `sldb.md`, `ui.md` si existen); manual CLI localizable; estado del corpus WS40. WS03/WS04 se alcanzan por la cadena WS06/WS07 indicada en el scope.

**Cambios previstos:** crear/actualizar solo `borradores/manual.md`.

**Dependencias:** WS02 aporta inventario Deskops; WS07 el registro de decisiones y G_PRODUCT; WS03/WS04 llegan transitivamente; WS40 produce el ejemplo Taller.

**Validaciones futuras:** cada etiqueta «disponible» debe citar versión/commit, pruebas y acta; lo demás queda «propuesto» o «bloqueado» con dependencia identificada; verificar que no haya pasos ni capturas ficticios; contrastar cada capítulo con las auditorías; comprobar que el ejemplo remite a WS40 o se declara corpus futuro.

## FUTURO

WS09 consume las definiciones de estado de WS10 para `borradores/vistas.md`. WS31 incorpora el índice a `docs/workspace-user-manual.md`. WS40 genera el corpus Taller; WS30/WS43 producen actas y pruebas que habilitarán etiquetas «disponible». WS11/WS12 aportan contratos para capítulos bloqueados. La aceptación humana del recorrido y la publicación quedan fuera de este nodo.
