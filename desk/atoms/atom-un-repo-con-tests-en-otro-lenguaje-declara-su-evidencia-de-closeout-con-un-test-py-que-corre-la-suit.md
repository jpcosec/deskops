---
sldb:
  by: agent
  at: '2026-11-16T17:16:31Z'
  authority: generated
  via: create_document
id: atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit
title: Un repo con tests en otro lenguaje declara su evidencia de closeout con un
  test .py que corre la suite con deskops.testing
five_wh_one_plus: how
tags:
- system:deskops
- topic:closeout
provenance: docs/workflow-policy-reference.md
---

# Un repo con tests en otro lenguaje declara su evidencia de closeout con un test .py que corre la suite con deskops.testing

## Answer

El gate de tests de closeout solo acepta un .py bajo tests/ y no cambia para otros lenguajes (decision de JP, 2026-11-16). Un repo cuya suite es vitest, go test u otra declara su evidencia con tests/test_<suite>_suite.py, que llama deskops.testing.foreign_suites.run_foreign_suite(VITEST|GO_TEST|<argv>, cwd=<raiz del repo>): el test pasa si la suite da rc 0 y, si no, falla con el comando, el cwd, el rc y las ultimas 200 lineas de stdout y stderr. El puente vive en deskops y nunca se reimplementa en cada repo; un repo sin entorno Python propio lo corre con uv run --no-project --with pytest --with-editable <checkout de deskops> python -m pytest -q tests/test_<suite>_suite.py.
