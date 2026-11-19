---
sldb:
  by: agent
  at: '2026-11-19T14:54:09Z'
  authority: generated
  via: create_document
id: atom-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-sea-nodo-del-grafo-o-missing
title: closeout verify cubre los archivos bajo un directorio target, sea nodo del
  grafo o missing
five_wh_one_plus: how
tags:
- system:deskops
- topic:closeout
---

# closeout verify cubre los archivos bajo un directorio target, sea nodo del grafo o missing

## Answer

En deskops/services/closure.py, una materialization cuyo target_identity declarado es un directorio cubre los archivos bajo él (target_covers) en los dos casos: cuando sldb reporta el directorio como missing (materialization inválida, sldb anterior a 6f14a3b5) y cuando el directorio es un nodo del grafo (materialization válida, sldb 6f14a3b5 en adelante). La fuente de verdad es el target_identity del documento: un directorio existente bajo la raíz. Un hermano con prefijo parecido (pkg/subzero.py junto a pkg/sub) no queda cubierto.
