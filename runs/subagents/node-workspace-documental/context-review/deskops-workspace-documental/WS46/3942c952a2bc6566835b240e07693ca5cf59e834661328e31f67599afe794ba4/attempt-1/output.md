REFORMULACION
WS46 es un nodo de implementación en deskops que debe probar la composición pública existente para capturar un candidato de drawer y un protoátomo, verificando origen preservado, ausencia de tarea activa y rechazo de colisiones; solo si falta conducta, completar lo mínimo en deskops con tarea propia. Resultado: inventario con ruta, símbolo y commit, y pruebas reales separadas en `tests/` usando store temporal. Límites: no mutar el desk real, no crear tarea activa, no introducir wrapper/modelo/API por reflejo ni duplicar código si la composición cumple; depende de WS12/G_WRITE_CONTRACT y no acredita por sí mismo la capacidad para WS25.2.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: contrato WS12 —incluida la representación del origen y HO-11/HO-11b—, `dag.yaml` y gates, código deskops (`services/drawer.py`, `domain_tree.py`, `cli/commands/atoms.py`), API sldb/DrawerService y pruebas existentes. Cambios previstos: primero ninguno; elaborar inventario y pruebas con store temporal en `tests/`; si la composición no cumple, tocar solo los archivos listados. Dependencias: WS12 y G_WRITE_CONTRACT por delta; salida hacia WS25.2. Validaciones: ejecutar pruebas de drawer y protoátomo por separado; origen ruta/mensaje persistido y visible tras recarga; ninguna tarea activa en Board ni `list tasks`; colisión rechazada sin sobrescribir, incluido archivo no rastreado; registrar evidencia. Sin ejecutar.

FUTURO
WS12 fija la representación del origen y el recibo por delta de G_WRITE_CONTRACT; la promoción fija archivos y escenarios de prueba; WS25.2 consume la capacidad probada. La aceptación humana del delta y la disponibilidad de producto corresponden a otros actores/gates, no a este nodo.
