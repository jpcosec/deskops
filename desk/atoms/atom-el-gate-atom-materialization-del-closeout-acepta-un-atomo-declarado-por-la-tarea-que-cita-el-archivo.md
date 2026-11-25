---
sldb:
  by: agent
  at: '2026-11-25T01:56:24Z'
  authority: generated
  via: create_document
id: atom-el-gate-atom-materialization-del-closeout-acepta-un-atomo-declarado-por-la-tarea-que-cita-el-archivo
title: El gate atom|materialization del closeout acepta un atomo declarado por la
  tarea que cita el archivo cambiado, de cualquier tipo
five_wh_one_plus: how
tags:
- system:deskops
- topic:closeout
provenance: deskops/services/closure.py
---

# El gate atom|materialization del closeout acepta un atomo declarado por la tarea que cita el archivo cambiado, de cualquier tipo

## Answer

Para cada ruta de files sin arista de grafo ni materialization, deskops/services/closure.py busca en los atomos que la tarea declara (campo atoms o un atomo en references) la ruta o un directorio de al menos dos partes que la contenga, como token completo en la provenance o el texto; si la encuentra el enlace es atom-cites:<atomo> -> <ruta> y el recibo de atom nombra ese atomo. Sirve para archivos que el grafo no tiene como nodos (.ts, .tsx, .css, un directorio de build). Un atomo que no se declara, o que cita otra ruta con el mismo prefijo, no enlaza. El hallazgo missing_changed_file_link dice que formas de enlace se aceptan. Lo prueba tests/test_closeout_atom_cites_file.py; lo documenta docs/operator-manual.md.
