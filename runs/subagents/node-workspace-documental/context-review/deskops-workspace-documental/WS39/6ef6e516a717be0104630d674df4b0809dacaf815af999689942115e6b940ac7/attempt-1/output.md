REFORMULACION
WS39 es un nodo de implementación (delivery) en graph_ui. Encargo: integrar la inspección y edición de modelos/clases ya existentes en el lector, sin reimplementar modelos. Desde el documento activo, el panel lateral Context del lector WS13 (node/workspace-view.js) debe mostrar el Schema/clase origen y abrir el editor existente inventariado en WS04, usando draft/validate/promote de sldb. Resultado: UF09 de inspección y mutación probado en store temporal real, con efectos/errores del contrato WS12, acta humana en graph_ui:.../modelos/acta.md y G_HUMAN_MODEL. Límites: G_HUMAN_READ solo habilita uso de mutaciones en UI, no desarrollo/pruebas aisladas de API; no habilitar promote sin API/autoridad; ruta/selector exacto en TaskDoc.

AMBIGUEDADES
1. «acceso desde documento activo muestra Schema/clase origen de ese documento»: no se define cómo resolver la clase origen de un documento; obliga a inventar el mapeo documento→modelo/clase.
2. «UF09 inspección y mutación en store temporal real de prueba»: UF09 no se define en el input ni se nombra su productor; obliga a inventar sus pasos/resultado o a asumir una dependencia ausente.

DRY-RUN
Lecturas: contrato WS12, lector WS13 (node/workspace-view.js), módulo de admisión WS48, inventario WS04 y gates. Cambios previstos: shell/dialogs.js, views/models/, tests/ y acta en runs/.../modelos/. Dependencias: WS12 (canal/efectos/errores), WS13 (Context del lector), WS48 (admisión de escritura), WS04 transitiva (editor inventariado). Validaciones futuras: abrir documento activo, ver Schema/clase origen y abrir editor; ejecutar UF09 de inspección y mutación en store temporal real; comprobar efectos/errores WS12; no habilitar promote sin API/autoridad; registrar acta humana y pasar G_HUMAN_MODEL; G_HUMAN_READ solo para uso de mutaciones; G_UI_WRITE y G_WRITE_CONTRACT por delta. Sin ejecutar.

FUTURO
WS12 produce contrato; WS13 entrega lector/Context; WS48 entrega admisión; WS04 inventario del editor; WS31 publica capítulo 15 del manual; P08/P01 aportan participante y acta; WS16 resuelve G_HUMAN_READ; receptor P01 acepta deltas G_UI_WRITE; WS12 resuelve G_WRITE_CONTRACT.
