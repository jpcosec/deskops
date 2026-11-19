---
sldb:
  by: agent
  at: '2026-11-19T18:24:08Z'
  authority: generated
  via: create_document
id: atom-el-vocabulario-de-esquema-de-los-artefactos-de-deskops-vive-en-los-modelos-no-en-spec-artifacts-ni-s
title: El vocabulario de esquema de los artefactos de deskops vive en los modelos,
  no en spec/artifacts ni spec/fields
five_wh_one_plus: where
tags:
- system:deskops
- topic:docs
---

# El vocabulario de esquema de los artefactos de deskops vive en los modelos, no en spec/artifacts ni spec/fields

## Answer

Los esquemas de los artefactos del desk (ids, defaults, tags, plantillas) están en los atributos de clase de los modelos de deskops/models (__artifact__, __semantics__, __template__) y en deskops/doc_access.py. Los antiguos deskops/spec/artifacts y deskops/spec/fields y SpecRegistry se borraron en CC30; en deskops/spec solo queda workflows/. README, el vocabulario del grafo y el diagrama de workflow lo dicen así.
