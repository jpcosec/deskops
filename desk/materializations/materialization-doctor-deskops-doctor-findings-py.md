---
sldb:
  by: agent
  at: '2026-11-22T00:18:15Z'
  authority: generated
  via: create_document
id: materialization-doctor-deskops-doctor-findings-py
title: doctor deskops-doctor_findings-py
source_atoms:
- atom-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
target_kind: code
target_identity: deskops/doctor_findings.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_lost_receipts.py
tags:
- system:deskops
- topic:doctor
---

# doctor deskops-doctor_findings-py

## Intent

materializa en deskops/doctor_findings.py el atom atom-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
