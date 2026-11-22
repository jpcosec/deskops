---
sldb:
  by: agent
  at: '2026-11-22T00:18:04Z'
  authority: generated
  via: create_document
id: materialization-doctor-deskops-cli-commands-doctor-py
title: doctor deskops-cli-commands-doctor-py
source_atoms:
- atom-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
target_kind: code
target_identity: deskops/cli/commands/doctor.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_lost_receipts.py
tags:
- system:deskops
- topic:doctor
---

# doctor deskops-cli-commands-doctor-py

## Intent

materializa en deskops/cli/commands/doctor.py el atom atom-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
