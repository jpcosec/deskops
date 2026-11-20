---
sldb:
  by: agent
  at: '2026-11-20T12:15:14Z'
  authority: generated
  via: create_document
id: atom-build-neighbours-de-absolute-paths-resuelve-el-registro-con-resolve-registered-root
title: build_neighbours de absolute_paths resuelve el registro con resolve_registered_root
five_wh_one_plus: how
tags:
- system:deskops
- topic:registry
---

# build_neighbours de absolute_paths resuelve el registro con resolve_registered_root

## Answer

En deskops/absolute_paths.py, build_neighbours resuelve la ruta de cada repo del registro con resolve_registered_root (la misma función que usa repo register), así una ruta guardada relativa a la raíz del repo del registro se resuelve igual que en el resto de deskops.
