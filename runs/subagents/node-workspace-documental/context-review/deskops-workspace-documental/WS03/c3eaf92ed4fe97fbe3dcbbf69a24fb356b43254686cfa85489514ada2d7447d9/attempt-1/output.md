## REFORMULACION
**Propósito:** auditar en solo lectura la persistencia, consultas y notaciones reales de sldb/pron/spec2viz, separando API comprobada, ausencia y hueco. **Resultado:** `auditoria/infraestructura.md`, documental. **Repo dueño:** deskops. **Límites:** sin cambios interrepo; Kimun solo referencia; inventariar fuente/payload, conflictos y locks reales (CAS/revisión/hash, archivo o DB), referencias documentales, búsquedas/índices y alcance real ViewDoc. **Dependencia:** WS01. **Aceptación:** salida única con lecturas citadas del estado actual, ausencias y huecos distinguidos.

## AMBIGUEDADES
Ninguna. El nodo nombra alcance, repo, salida, límites, dependencia y criterio comprobable; las precisiones técnicas quedan dentro de la auditoría, no obligan a inventar un resultado distinto.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml` (WS03/WS01), `brief.md`, `alcance.md` y `decisiones.md`; después inspeccionaría en solo lectura sldb/pron/spec2viz. Inventariaría fuente/payload, CAS/locks, referencias, búsquedas y ViewDoc, citando path/símbolo/estado cuando exista. Redactaría `auditoria/infraestructura.md` marcando explícitamente API comprobada, ausencia y hueco. Dependencia: el brief de WS01; si falta, se detendría y registraría el hueco según las reglas comunes. Validaciones futuras: que no haya cambios interrepo, que las citas sean verificables, que Kimun aparezca solo como referencia y que la salida distinga los tres estados exigidos. No ejecuta nada ahora.

## FUTURO
WS06 consumirá esta auditoría para su matriz de alcance; el coordinador o responsable humano revisará la aceptación y decidirá la promoción. Cualquier contrato o delta de otros nodos corresponde a sus productores y receptores, no a WS03. No hay gates propios en este nodo.
