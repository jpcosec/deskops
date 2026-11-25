## REFORMULACION

**Propósito:** declarar ViewDoc y NotationDoc concretos —datos sin ruta de store— para selecciones y notación ya soportadas por spec2viz, reutilizando el evaluador `evaluate_view` y `/api/views` de graph_ui y `resolve_documents` de spec2viz.

**Resultado:** ViewDocs/NotationDocs cuyos resultados, evaluados sobre un store real, coinciden con la selección de catálogo WS09 y contrato WS11; el ViewDoc repite y documenta qué selecciona; pruebas en `tests/`.

**Repo:** spec2viz, con `output_scope: sldb/views/` (base spec2viz) y `tests/`; la TaskDoc receptora se promueve allí por su supervisor/Executor.

**Límites:** no crear páginas UI declarativas ficticias; no portabilidad genérica, servicio, CLI ni runtime fuera de graph_ui; no extraer/compartir el evaluador; no inventar selección (si catálogo WS09 no la fija, detener promoción y corregir el contrato); deskops no escribe en spec2viz; no alegar equivalencia de payload completo entre dos stores.

**Dependencias:** WS09, WS11 (transitivas WS02–WS10); gate G_SPEC_VIEW per_delta.

## AMBIGUEDADES

Ninguna. La selección tiene productor nombrado (WS09/WS11) y regla explícita ante falta; la ruta exacta se delega a promoción; el store real está resuelto por las reglas comunes (store temporal o corpus WS40); el recibo G_SPEC_VIEW tiene resolutor y evidencia definidos.

## DRY-RUN

- **Lecturas:** `borradores/vistas.md` (WS09), `contratos/navegacion.md` (WS11), código de spec2viz (`resolve_documents`, modelo ViewDoc/NotationDoc) y de graph_ui (`evaluate_view`, `/api/views`); reconciliacion.md filas C-37/C-49.
- **Cambios previstos:** crear ViewDoc y NotationDoc concretos bajo la ruta confirmada al promover (`.../sldb/views/`), pruebas en `tests/`, sin tocar otros repos.
- **Dependencias:** selección mínima fijada por WS09/WS11; capacidad real de spec2viz/WS03; gate G_SPEC_VIEW recibido para el delta antes de promoción/ejecución.
- **Validaciones futuras:** ejecutar el camino existente de graph_ui sobre un store real; comparar resultado con la selección declarada; verificar que el ViewDoc documenta la selección; si falta selección o contrato, detener y registrar hueco con repo dueño.
- Nodo único de implementación, no agregado; no se ejecuta en deskops, solo se promueve en spec2viz.

## FUTURO

WS09/WS11 deben entregar selección y notación exigidas; P01/receptor de spec2viz emite el acta G_SPEC_VIEW del delta; el supervisor/Executor de spec2viz promueve y ejecuta la TaskDoc y corre las pruebas; deskops solo registra el enlace al recibo.
