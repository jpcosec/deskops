## REFORMULACION
**Propósito:** integrar en la UI de graph_ui la captura interna con destino elegido explícitamente por la persona usuaria —candidato de drawer o protoátomo— sin exigir tarea, usando solo operaciones permitidas por el contrato WS12 y la capacidad con origen ya probada por WS46, pasando toda escritura por la admisión común de WS48.

**Resultado:** UF02 cumplida: una captura persiste tras recargar en el destino elegido, con origen tipado —ruta o mensaje— registrado y visible, sin tarea implícita, con permisos del contrato aplicados y colisión controlada sin sobrescritura silenciosa; cada destino se prueba por separado.

**Repo dueño:** graph_ui. Salidas en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`.

**Límites:** no crear API, modelo ni wrapper por reflejo; no mutar el desk real; no habilitar uso de mutaciones en UI sin G_HUMAN_READ; no cumplir declarando la captura no disponible; no ejecutar closeout ni commits; no ampliar destinos ni operaciones fuera de WS12.

## AMBIGUEDADES
ninguna.

Las referencias a representación de origen, permisos, colisiones y endpoints quedan delegadas a WS12, que tiene productor nombrado y regla de parada si falta. La capacidad de captura con origen queda producida por WS46 y la admisión por WS48, ambos dependencias explícitas. Los textos de pantalla, archivos exactos y casos detallados corresponden al TaskDoc de promoción.

## DRY-RUN
**Lecturas previstas:** contrato WS12 (whitelist, canal, origen, colisión, permisos); inventario y pruebas de WS46 para drawer y protoátomo; módulo de admisión WS48; código y tests existentes de captura/workspace en graph_ui.

**Cambios previstos:** vista de captura con selector explícito de destino, envío por endpoints autorizados, visualización del origen tras recarga, manejo de colisión según contrato y consulta previa a WS48; pruebas separadas para drawer y protoátomo, incluyendo persistencia, origen ruta/mensaje, ausencia de tarea activa y rechazo de colisión.

**Dependencias:** WS12, WS46 y WS48; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, evaluados por delta.

**Validaciones futuras:** pruebas sobre store temporal; verificación de que no se crea tarea ni se sobrescribe; acta de recepción P01 del delta en graph_ui; acta humana de lectura antes de habilitar mutaciones en UI. Si falta contrato, API o permiso, detenerse y registrar el hueco.

## FUTURO
WS12 produce el contrato de operaciones y representación; WS46 produce y prueba la capacidad de captura con origen para cada destino; WS48 produce el punto común de admisión de escrituras. El TaskDoc de promoción fija archivos, escenarios y textos. La persona P01 emite el acta G_UI_WRITE por delta y WS16 produce el acta G_HUMAN_READ; la habilitación real del uso de mutaciones en UI queda a decisión humana.
