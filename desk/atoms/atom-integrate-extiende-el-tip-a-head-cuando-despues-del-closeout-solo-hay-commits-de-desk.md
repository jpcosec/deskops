---
sldb:
  by: agent
  at: '2026-11-20T11:04:35Z'
  authority: generated
  via: create_document
id: atom-integrate-extiende-el-tip-a-head-cuando-despues-del-closeout-solo-hay-commits-de-desk
title: integrate extiende el tip a HEAD cuando después del closeout solo hay commits
  de desk
five_wh_one_plus: how
tags:
- system:deskops
- topic:integrate
---

# integrate extiende el tip a HEAD cuando después del closeout solo hay commits de desk

## Answer

extend_tip(root, tip) en deskops/integrate.py, llamada tras find_tip: si el commit de closeout es ancestro de HEAD y todos los commits del rango tocan solo desk/, .sldb/, runs/ o .deskops.log, el tip pasa a HEAD; imprime 'tip extendido a <sha>: solo commits de desk' y todos los gates y el push usan ese tip. Si algún commit posterior toca código, tests, docs, CHANGELOG u otra ruta, el tip sigue siendo el closeout. Así un arreglo de desk hecho después del cierre (p. ej. retirar una tarea vieja que deja una referencia colgante) no deja trabado el gate de grafo.
