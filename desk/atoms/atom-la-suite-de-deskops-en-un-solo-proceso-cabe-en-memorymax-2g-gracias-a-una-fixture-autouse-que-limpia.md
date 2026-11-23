---
sldb:
  by: agent
  at: '2026-11-23T16:11:38Z'
  authority: generated
  via: create_document
id: atom-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-gracias-a-una-fixture-autouse-que-limpia
title: La suite de deskops en un solo proceso cabe en MemoryMax=2G gracias a una fixture
  autouse que limpia los caches globales
five_wh_one_plus: how
tags:
- system:deskops
- topic:tests
---

# La suite de deskops en un solo proceso cabe en MemoryMax=2G gracias a una fixture autouse que limpia los caches globales

## Answer

tests/conftest.py gana la fixture autouse _clear_global_caches que tras cada test invalida runtime_cache, el indice de store_io, built_cache y alert_sink de sldb, y vacia _DOC_PAYLOADS, _READ_HASHES e _INDEX_ENTRIES de deskops/doc_access.py.
