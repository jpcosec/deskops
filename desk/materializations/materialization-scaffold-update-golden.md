---
sldb:
  by: agent
  at: '2026-11-16T13:00:11Z'
  authority: generated
  via: create_document
id: materialization-scaffold-update-golden
title: Scaffold update golden
source_atoms:
- atom-la-estructura-inicial-de-un-desk-se-declara-en-el-paquete-de-deskops-y-la-aplica-sldb
target_kind: test
target_identity: tests/fixtures/golden/scaffold/update.json
validation:
- pytest tests/test_scaffold_golden.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-la-estructura-inicial-de-un-desk-se-declara-en-el-paquete-de-deskops-y-la-aplica-sldb.md
---

# Scaffold update golden

## Intent

Golden del reporte de deskops desk update sobre un desk incompleto: lista la estructura que el paquete declara como exigida (sin desk/reviews/, que crea el primer recibo).
