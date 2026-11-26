---
sldb:
  by: agent
  at: '2026-11-26T03:00:20Z'
  authority: generated
  via: create_document
id: atom-la-superficie-es-un-contrato-de-editores-texto-y-grafo-son-sus-dos-casos
atom_type: atom.adr
status: accepted
five_wh_one_plus: why
decided_on: '2026-11-25'
decided_by: JP
supersedes: []
partial_supersedes: []
references:
- /mnt/ssd/proyectos/SLDB_1/sldb/docs/architecture/surface-is-an-editor-contract.md
pointers: []
tags:
- system:deskops
---

# La superficie es un contrato de editores; texto y grafo son sus dos casos

## Context

El workspace tiene más interfaces que productos: sldb/surface, graph_ui/mindmap con otros tres frontends y dos apps, sldb-ui y marcado-ui archivados, y un plan de app de specIR revertido dos veces en un día. Cada una se escribió a mano con sus tokens, su manejo de estado y su forma de llegar al store.

## Decision

surface es un contrato, no una aplicación: cómo se construye un editor. Dos casos: el editor de texto (de SLDB, documento como segmentos, anclas y conversación con un agente) y el editor de grafo (graph_ui). Astryx es la estructura externa y nuestros editores son componentes paralelos a los suyos; XState es nuestro; Zustand guarda vista y borrador y XState el flujo de guardado; la validación vive en SLDB; un solo editor de texto sobre CodeMirror; el agente llega al store por el MCP de SLDB; specIR no tiene interfaz propia.

## Consequences

surface y mindmap pasan a React 19 y mindmap gana un build. Las tareas de paneles embebibles de graph_ui se rehacen como el caso de grafo del contrato. Los dos dibujos de grafo dentro de surface se reemplazan por el editor de grafo y ProseMirror sale. El compositor de componentes y operaciones necesita la taxonomía de comandos. El panel de nodo es el caso de texto. Sin verificar: la documentación de integración de Astryx (beta 0.7.17), la coexistencia de estilos con React Flow y Lexical frente a los segmentos.

## Alternatives
