## REFORMULACION
PU01 es un agregado de planificación: agrupa la entrega de la vista de datos y el shell de la UI. Su propósito es que UI01 produzca en deskops la vista (`deskops view` y contrato) y que UI02 levante en graph_ui el servidor y shell que la consumen. El resultado es que ambos hijos terminen y queden satisfechos G_VIEW y G_SHELL. `owner_repo: deskops`; UI01 ejecuta en deskops y UI02 en graph_ui. Límites: no es ejecutable, no escribe, no tiene lógica propia y termina cuando terminan sus hijos.

## AMBIGUEDADES
1. «resolver: UI02-UI06 integradas en graph_ui y cerradas en su desk» frente a «children: - UI01 - UI02» y «scope: UI01 escribe… UI02 levanta…». Obliga a inventar si el cierre de PU01 exige UI03–UI06 —no suministrados como hijos— o solo UI01 y UI02.
2. «Pendiente declarado: las capturas comparadas con Stitch quedaron en /tmp de la sesión y no están anotadas en los TaskDocs» y «la suite completa de graph_ui no está verde por fallas previas o de entorno», junto a `G_SHELL: state: satisfied`, frente a la aceptación de UI02 («diferencias anotadas en el TaskDoc») y a alcance.md («Validación en robocop2 (suite completa del repo tocado) antes de mergear»). Obliga a inventar si esos pendientes invalidan la satisfacción del gate o si se aceptan como excepción.

## DRY-RUN
PU01 no se ejecuta. Un ejecutor futuro solo leería `dag.yaml`, los estados de G_VIEW/G_SHELL y los cierres de UI01 y UI02; no modificaría código ni documentación. El único cambio posible sería registrar el cierre del agregado cuando consten sus hijos terminados. Dependencias: UI01 produce la vista y G_VIEW; UI02 depende de UI01, la importa por Python y reusa `DeskRoutes` para `advance`. Validación conjunta: tests de UI01 sobre desks temporales; tests de rutas de UI02 comparando cada `/api/view/*` con `deskops view`; e2e sobre desk temporal; ausencia de textos de Stitch; capturas comparadas; verificación de que ninguna vista escribe. Todo ello ya pertenece a los hijos; el agregado solo comprobaría evidencia y estados.

## FUTURO
Un humano decide si los pendientes declarados de G_SHELL se aceptan o se corrigen. Otro nodo o plan, si existen UI03–UI06, aportaría el resto del shell. La ejecución de robocop2, la comparación visual y la fijación de nombres de archivos y tests corresponden a los hijos y al TaskDoc al promover, no a PU01.
