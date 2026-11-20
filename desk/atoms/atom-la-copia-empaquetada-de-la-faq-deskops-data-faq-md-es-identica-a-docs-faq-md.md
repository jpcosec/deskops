---
sldb:
  by: agent
  at: '2026-11-20T16:25:23Z'
  authority: generated
  via: create_document
id: atom-la-copia-empaquetada-de-la-faq-deskops-data-faq-md-es-identica-a-docs-faq-md
title: La copia empaquetada de la FAQ, deskops/data/faq.md, es idéntica a docs/faq.md
five_wh_one_plus: how
tags:
- system:deskops
- topic:docs
---

# La copia empaquetada de la FAQ, deskops/data/faq.md, es idéntica a docs/faq.md

## Answer

deskops/data/faq.md es una copia byte a byte de docs/faq.md, y tests/test_packaging.py y tests/test_large_doc_materialization.py lo verifican. Quien edite docs/faq.md tiene que copiarlo también a deskops/data/faq.md, porque no hay comando que lo regenere.
