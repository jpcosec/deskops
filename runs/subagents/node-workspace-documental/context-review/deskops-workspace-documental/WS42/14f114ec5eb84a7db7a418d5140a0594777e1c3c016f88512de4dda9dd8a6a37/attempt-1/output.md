## REFORMULACION
**Propósito:** que la UI del workspace documental invoque operaciones reales de conocimiento ya contratadas —split/merge de átomos y proto typing— y inspeccione/valide materializaciones existentes, con confirmación humana que muestra origen y efecto antes de ejecutar.

**Resultado:** UF03 con persistencia, referencias y conflictos reales; materializaciones válidas operables e inválidas marcadas como no operables; capability no soportada declarada no disponible, bloqueando solo su escenario/etiqueta y sin simularse.

**Repo dueño:** `graph_ui`.

**Límites:** endpoints solo de la whitelist WS12; no crear destinos arbitrarios; validar materializaciones por API pública SLDB contra `MaterializationContractDoc`, no con renderer propio; mutaciones en UI sujetas a `G_HUMAN_READ`/`G_UI_WRITE`/`G_WRITE_CONTRACT`; desarrollo y pruebas aisladas de API pueden avanzar; si falta contrato/API, WS12 registra hueco y la UI queda no disponible. Es implementation/delivery ejecutable, no agregado.

## AMBIGUEDADES
ninguna

## DRY-RUN
Un ejecutor futuro leería el nodo, `dag.yaml`, el contrato WS12, los inventarios WS02/WS03, el módulo de admisión WS48, `deskops/models/materialization.py`, el TaskDoc y el store temporal/manifiesto WS40. Verificaría gates por delta: con `G_HUMAN_READ` pendiente solo cabrían desarrollo y pruebas aisladas; la habilitación real de mutaciones esperaría su acta y los recibos `G_UI_WRITE`/`G_WRITE_CONTRACT`.

Cambios previstos en `frontends/mindmap/views/workspace/knowledge/` y `tests/`: confirmación con origen/efecto, invocación de endpoints whitelist, admisión única vía WS48, inspección y validación de materializaciones por API SLDB, estados de capability no disponible. Dependencias: WS12 (contrato), WS19 (edición/conflicto), WS24 (vista de conocimiento) y WS48 (admisión de escritura). Validaciones futuras: pruebas con store temporal real para split/merge/typing, conflictos y materialización inválida; verificación de que no se crean destinos ni se usa renderer propio; entrega a WS30 para UF03.

## FUTURO
WS12 debe publicar el contrato por operación o registrar productor/hueco; WS40/TaskDoc deben fijar el store y el manifiesto; WS30 ejecuta la validación humana de UF03; P01 emite el acta de recepción del delta; WS16 produce `G_HUMAN_READ`. Un fallo de guion lo abre el responsable del repo dueño, no este nodo.
