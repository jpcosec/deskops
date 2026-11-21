---
sldb:
  by: agent
  at: '2026-11-21T12:46:32Z'
  authority: generated
  via: create_document
id: atom-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-con-cualquier-idioma-de-git
title: reap nombra los archivos que bloquean el cherry-pick con cualquier idioma de
  git
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# reap nombra los archivos que bloquean el cherry-pick con cualquier idioma de git

## Answer

_git de deskops/dispatch.py corre git con LC_ALL=C y LANGUAGE vacío, y _dirty_overwrite_hint detecta solo el texto inglés estable ('would be overwritten'). Con el timer en LANG=es_ES.UTF-8, el reap volvía a no nombrar los archivos y su test fallaba en la suite completa; ahora pasa con es_ES y con en_US.
