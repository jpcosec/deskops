## REFORMULACION
PK06 es un agregado de publicación básica en **deskops**: coordina WS43 (navegación documental del desk real) y WS31 (manual documental básico probado) para publicar manual y entradas del desk real sobre recorridos ya demostrados. Resultado esperado: manual versionado con instrucciones enlazadas a acta/versión y límites; `desk/README.md` y mapa/índices authored probados; átomos y procedencia atom→doc verificada. Repo dueño: **deskops**. Límites: no tiene ejecución propia ni autoriza tareas/aristas; no declara disponibles Scion, modelos o Changes no demostrados; no sustituye actas humanas ni contratos; su cierre depende de sus hijos e integración, no de revisiones de comprensión.

## AMBIGUEDADES
ninguna

## DRY-RUN
Agregado no ejecutable: se cumpliría por hijos. Orden por aristas: primero WS43, luego WS31, porque WS31 depende de WS43. Antes deben existir WS17 (plantillas/índices), WS30 (acta manual) y WS10 (índice/convención); WS43 también consume contrato WS11 transitivo y P09. **Lecturas:** WS43 lee WS17, acta WS30, contrato de navegación, registry/list repositories y decisiones; WS31 lee WS10, acta WS30, acta/versión WS43, decisiones y contratos. **Cambios previstos:** WS43 escribe `desk/README.md`, mapa/índices, átomos y acta de publicación con commit; WS31 escribe `docs/workspace-user-manual.md`, assets y átomos. **Transferencia:** WS43 entrega a WS31 acta/versión publicada, mapa y átomos; WS30 y WS10 entregan acta e índice. **Validación conjunta futura:** WS43 exige recorrido real de Markdown/UI, links/roots resolubles, commit y acta; WS31 exige links/etiquetas, límites y atom→doc con fuente, verificado por Tester independiente; el paquete se acepta si cada instrucción remite a acta WS30 o WS43, las entradas/mapa están probados y los no demostrados siguen propuestos. No ejecutar.

## FUTURO
Deciden/ejecutan otros: WS17 y WS10 producen plantillas/índice; WS30 y WS43 requieren acta humana/P08 y commit; el Tester independiente valida WS31; los gates G_HUMAN_MANUAL, G_PRODUCT y G_WRITE_CONTRACT siguen pendientes; WS38/WS29 condicionan capítulos propuestos.
