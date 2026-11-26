---
sldb:
  by: agent
  at: '2026-11-26T03:00:09Z'
  authority: generated
  via: create_document
id: atom-una-taxonomia-de-comandos-servida-por-fastmcp
atom_type: atom.adr
status: accepted
five_wh_one_plus: why
decided_on: '2026-11-25'
decided_by: JP
supersedes: []
partial_supersedes: []
references:
- /mnt/ssd/proyectos/SLDB_1/sldb/docs/architecture/one-command-taxonomy-served-by-fastmcp.md
pointers: []
tags:
- system:deskops
---

# Una taxonomía de comandos, servida por FastMCP

## Context

SLDB creció cuatro caras sin planearlas juntas: sldb.api (192 nombres públicos), la CLI (unos 20 grupos), sldb serve (unas 30 rutas sobre http.server, sin extensiones ni deshacer) y sldb mcp (15 herramientas sobre MCPServer, solo stdio). Los nombres difieren y cada cara cubre un subconjunto; un consumidor que necesita algo de dos caras lo pide dos veces. Diagnóstico del dueño: no hay taxonomía de comandos; y cuatro razones para fastmcp: no mantener ese código, modo código, una interfaz que los agentes ya conocen y un solo lugar declarativo.

## Decision

Primero una taxonomía: una tabla de operaciones con sustantivo, verbo, lectura o escritura y nivel de permiso, que el dueño aprueba. Luego un solo servidor FastMCP que declara cada operación una vez, las interfaces como clientes de ese servidor (sldb serve se retira) y la CLI alineada con la taxonomía. Una extensión (la de specIR) es un servidor montado en el de SLDB.

## Consequences

El pedido de sldb serve --extension queda sin efecto. Lo que sale de pron aterriza como operaciones de la taxonomía. El contrato de editores depende del paso 1. Las 30 rutas no tienen equivalente en 15 herramientas (extracción, render, lint, AST, similitud, notaciones): las rutas viejas siguen hasta que ambas interfaces migren. FastMCP no genera rutas REST ni CLI agrupada, y la autorización por herramienta no corre en stdio: los niveles 0, 1 y 2 se reconstruyen ocultando herramientas por tag.

## Alternatives
