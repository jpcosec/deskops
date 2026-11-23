---
sldb:
  by: agent
  at: '2026-11-23T19:59:55Z'
  authority: generated
  via: create_document
id: atom-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript
title: El gate de tests del closeout acepta archivos de test de TypeScript
five_wh_one_plus: how
tags:
- system:deskops
- topic:closeout
---

# El gate de tests del closeout acepta archivos de test de TypeScript

## Answer

CloseoutGates.reference_points_to_test acepta ademas de .py los archivos .test.ts, .test.tsx, .spec.ts y .spec.tsx existentes en un directorio tests o __tests__ o declarados en files, fuera de node_modules, site-packages y directorios ocultos; el mensaje de Unresolvable --test nombra esos sufijos.
