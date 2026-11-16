---
sldb:
  by: agent
  at: '2026-11-16T22:30:24Z'
  authority: generated
  via: create_document
id: atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba
title: Un archivo de codigo cita los atomos que implementa y deskops atoms citations
  lo comprueba
five_wh_one_plus: how
tags:
- system:deskops
- topic:atoms
provenance: tests/test_atom_citations.py
---

# Un archivo de codigo cita los atomos que implementa y deskops atoms citations lo comprueba

## Answer

Un modulo Python cita los atomos que implementa con un bloque Atoms: en su docstring de modulo (un id atom-... por linea, en columna 0, hasta una linea vacia); cualquier otro archivo versionado usa comentarios '# Atom: <id>'. deskops atoms citations recorre git ls-files, reporta las citas, las citas rotas (atomo inexistente) y los atomos sin cita; --check sale 1 si hay una cita rota; --write registra cada cita como un RelationDoc cited_by (archivo -> AtomDoc) y deskops show atom muestra 'Cited by:'. Limitacion vigente de sldb (2026-11-16): una ruta de archivo no es extremo valido de RelationDoc, asi que la cita es un documento y no una arista recorrible, y sldb edges check da un error por cita.
