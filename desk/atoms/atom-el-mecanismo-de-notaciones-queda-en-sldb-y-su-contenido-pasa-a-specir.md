---
sldb:
  by: agent
  at: '2026-11-26T02:59:38Z'
  authority: generated
  via: create_document
id: atom-el-mecanismo-de-notaciones-queda-en-sldb-y-su-contenido-pasa-a-specir
atom_type: atom.adr
status: accepted
five_wh_one_plus: why
decided_on: '2026-11-25'
decided_by: JP
supersedes: []
partial_supersedes: []
references:
- /mnt/ssd/proyectos/SLDB_1/sldb/docs/architecture/mechanism-in-sldb-content-in-specir.md
pointers: []
tags:
- system:deskops
---

# El mecanismo de notaciones queda en SLDB y su contenido pasa a specIR

## Context

SLDB trae ocho notaciones builtin y una clase de spec por tipo de diagrama; specIR, que reemplazó a spec2viz, las importa de módulos internos y agrega las suyas. Al preguntar dónde van BPMN, ORCA e IFML, el dueño trazó la línea por tipo de cosa: todo lo que es un modelo semántico proyectado a specs va a specIR; el mecanismo puede ser de SLDB.

## Decision

SLDB conserva el mecanismo (NotationDoc, GlyphDoc, LinkDoc, PaletteDoc, SpecDoc, SpecNodeDoc, ViewDoc y la resolución y validación de una vista contra una notación). specIR es dueño del contenido: toda notación que describe un estándar o un dominio y las clases de spec por tipo de diagrama. Un estándar es una notación, nunca código; graph_ui dibuja la notación que el store tenga.

## Consequences

Las notaciones builtin y diagram_specs salen de SLDB, que necesita una notación mínima propia para sus pruebas. specIR deja de importar internos de SLDB. Una notación BPMN es trabajo de specIR. SLDB debe aún tres piezas de mecanismo: notación que declara el estándar que implementa, documento sin glifo reportado como hueco, y predicado de regla sobre tags semánticos de un modelo.

## Alternatives
