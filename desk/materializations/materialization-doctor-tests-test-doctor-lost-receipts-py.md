---
sldb:
  by: agent
  at: '2026-11-22T00:18:25Z'
  authority: generated
  via: create_document
id: materialization-doctor-tests-test-doctor-lost-receipts-py
title: doctor tests-test_doctor_lost_receipts-py
source_atoms:
- atom-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
target_kind: test
target_identity: tests/test_doctor_lost_receipts.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_lost_receipts.py
tags:
- system:deskops
- topic:doctor
---

# doctor tests-test_doctor_lost_receipts-py

## Intent

materializa en tests/test_doctor_lost_receipts.py el atom atom-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
