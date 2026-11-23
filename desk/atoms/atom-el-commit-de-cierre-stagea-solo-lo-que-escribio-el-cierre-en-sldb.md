---
sldb:
  by: agent
  at: '2026-11-23T10:31:26Z'
  authority: generated
  via: create_document
id: atom-el-commit-de-cierre-stagea-solo-lo-que-escribio-el-cierre-en-sldb
title: El commit de cierre stagea solo lo que escribio el cierre en .sldb
five_wh_one_plus: how
tags:
- system:deskops
- topic:closeout
---

# El commit de cierre stagea solo lo que escribio el cierre en .sldb

## Answer

_close toma una foto (porcelain, sha256) de .sldb al inicio y antes del commit; solo stagea rutas nuevas o cuyo estado o hash cambio, y commitea con pathspec explicito aun sin --paths, asi un .sldb ajeno (untracked o modificado antes) o un cambio ya staged no viaja en el commit de cierre; sin nada que stagear el error lista las rutas y sugiere --paths.
