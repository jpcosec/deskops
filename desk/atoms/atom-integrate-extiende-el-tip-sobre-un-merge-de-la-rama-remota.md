---
sldb:
  by: agent
  at: '2026-11-21T04:33:23Z'
  authority: generated
  via: create_document
id: atom-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota
title: integrate extiende el tip sobre un merge de la rama remota
five_wh_one_plus: how
tags:
- system:deskops
- topic:integrate
---

# integrate extiende el tip sobre un merge de la rama remota

## Answer

extend_tip(root, tip, remote_sha) devuelve HEAD cuando la rama remota (sha de git ls-remote <remote_url> refs/heads/<branch>) es ancestro de HEAD y los commits de HEAD que no están ni en el tip ni en el remoto, sin merges, solo tocan desk/, .sldb/ o runs/. Así un desk que mergeó origin/main después del closeout, porque otros pushearon, integra sin reescribir los sha que citan los recibos. Si no, sigue la regla anterior (solo commits de desk) o devuelve el tip.
