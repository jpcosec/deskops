---
sldb:
  by: agent
  at: '2026-11-26T03:00:32Z'
  authority: generated
  via: create_document
id: atom-specir-cumple-capacidades-no-reproduce-el-codigo-de-spec2viz
atom_type: atom.adr
status: accepted
five_wh_one_plus: why
decided_on: '2026-11-25'
decided_by: JP
supersedes: []
partial_supersedes: []
references:
- /mnt/ssd/proyectos/SLDB_1/IR/docs/decisiones/paridad-por-capacidades.md
pointers: []
tags:
- system:deskops
---

# specIR cumple capacidades, no reproduce el código de spec2viz

## Context

specIR reemplazó a spec2viz el 2026-11-23 con la regla de demostrar paridad con sus pruebas; el resultado fue paridad de código: unas 6.000 líneas portadas, 12 renderers y pruebas byte a byte contra salidas guardadas. Esa mitad visual corría en paralelo a sldb y graph_ui, que ya resuelven y dibujan lo mismo; una medición del 2026-11-25 mostró que las 38 specs válidas del corpus se dibujan en graph_ui sin errores ni avisos.

## Decision

La paridad con spec2viz es por capacidades: cada una se acredita con una prueba de aceptación de lo que hace, nunca con una salida idéntica. Los goldens de spec2viz y sus pruebas se borran. specIR declara y extrae, no dibuja (lo dibuja y edita graph_ui), no tiene interfaz propia y es dueño del contenido de las notaciones.

## Consequences

Quedan sin efecto las tareas U2, U3, U4, U5 y U9 de IR/ui y las decisiones D1, D7 y D10 del plan del diccionario. CatalogAnnotationsDoc y la página HTML del catálogo se retiran al cumplirse las capacidades 1 a 4 y 6. mcp_extension de specIR se monta como servidor en el de SLDB cuando su API esté sobre fastmcp. Al mapear ORCA e IFML aparecen huecos del modelo de dominio de specIR que ninguna notación tapa.

## Alternatives
