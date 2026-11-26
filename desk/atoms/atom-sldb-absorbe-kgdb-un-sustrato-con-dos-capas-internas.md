---
sldb:
  by: agent
  at: '2026-11-26T02:58:18Z'
  authority: generated
  via: create_document
id: atom-sldb-absorbe-kgdb-un-sustrato-con-dos-capas-internas
atom_type: atom.adr
status: accepted
five_wh_one_plus: why
decided_on: '2026-09-20'
decided_by: JP
supersedes: []
partial_supersedes: []
references:
- /mnt/ssd/proyectos/SLDB_1/sldb/docs/architecture/sldb-absorbs-kgdb.md
pointers: []
tags:
- system:deskops
---

# SLDB absorbe KGDB: un sustrato con dos capas internas

## Context

El ADR del 2026-06-19 dividió el ecosistema en SLDB (texto) y KGDB (grafo). Tres meses de práctica mostraron que el grafo tipado nunca fue independiente del store: era una proyección con proceso propio, mantenerla fuera costaba un protocolo de frescura (snapshot, comparación de hash, fallback), y dos repos para una derivación implicaban dos ciclos de release y un límite de subproceso. El 2026-09-17 se absorbió la mitad de ensamblado (índice de aristas en el store); faltaba la mitad de consulta.

## Decision

SLDB es un solo producto con dos capas internas, texto y grafo; KGDB deja de ser un producto aparte y sus capacidades pasan a SLDB, con el paquete kgdb como shim de compatibilidad. La frontera que el ADR anterior trazó entre repos sobrevive como frontera entre módulos.

## Consequences

SLDB gana un módulo de grafo (consulta, recorrido, snapshots portables) y un diario de escritura; stores check verifica la cadena. kgdb queda como shim. pron cede su fachada de store, su lector de grafo y su corpus. La superficie MCP se parte en dos niveles. El ADR previo queda como historia, reemplazado, no borrado.

## Alternatives
