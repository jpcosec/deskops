---
sldb:
  by: agent
  at: '2026-11-20T09:22:11Z'
  authority: generated
  via: create_document
id: atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk
title: deskops init y desk update --apply instalan el merge driver de sldb en el repo
  del desk
five_wh_one_plus: how
tags:
- system:deskops
- topic:merge-driver
---

# deskops init y desk update --apply instalan el merge driver de sldb en el repo del desk

## Answer

ensure_sldb_merge_driver(root) en deskops/bootstrap.py llama a install_merge_driver de sldb sobre root/.sldb cuando el desk es un repo git; la llaman BootstrapService.init_local_store y DeskCLI.update con --apply. Es idempotente; fuera de git no hace nada; si git falla avisa por stderr; si sldb no trae el módulo, se omite. Así un desk nuevo no muestra el alert stores/merge_driver_missing en deskops doctor.
