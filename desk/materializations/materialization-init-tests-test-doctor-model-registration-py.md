---
sldb:
  by: agent
  at: '2026-11-21T10:43:43Z'
  authority: generated
  via: create_document
id: materialization-init-tests-test-doctor-model-registration-py
title: init tests-test_doctor_model_registration-py
source_atoms:
- atom-init-y-sus-tests-asumen-la-resolucion-por-nombre-de-enlaces-de-sldb-3
target_kind: test
target_identity: tests/test_doctor_model_registration.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_model_registration.py
tags:
- system:deskops
- topic:init
---

# init tests-test_doctor_model_registration-py

## Intent

materializa en tests/test_doctor_model_registration.py el atom atom-init-y-sus-tests-asumen-la-resolucion-por-nombre-de-enlaces-de-sldb-3
