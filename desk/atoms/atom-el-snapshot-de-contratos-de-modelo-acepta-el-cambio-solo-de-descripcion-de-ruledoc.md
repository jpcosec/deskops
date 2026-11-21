---
sldb:
  by: agent
  at: '2026-11-21T12:02:24Z'
  authority: generated
  via: create_document
id: atom-el-snapshot-de-contratos-de-modelo-acepta-el-cambio-solo-de-descripcion-de-ruledoc
title: El snapshot de contratos de modelo acepta el cambio solo de descripción de
  RuleDoc
five_wh_one_plus: how
tags:
- system:deskops
- topic:models
---

# El snapshot de contratos de modelo acepta el cambio solo de descripción de RuleDoc

## Answer

tests/fixtures/model_contract_hashes.json actualiza solo la entrada RuleDoc (f2d2b1e3... pasa a 411e41fc...), recalculada con _contract_hashes() del propio test. Es un cambio solo de la description de where en sldb 22cfafb2 (retiro de incomplete), sin migración: sldb stores check sobre los stores de deskops y sldb no da hallazgos nuevos de RuleDoc.
