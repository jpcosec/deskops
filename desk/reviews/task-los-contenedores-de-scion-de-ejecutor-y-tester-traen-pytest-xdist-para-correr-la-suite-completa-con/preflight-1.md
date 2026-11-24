---
sldb:
  by: agent
  at: '2026-11-23T19:34:53Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-los-contenedores-de-scion-de-ejecutor-y-tester-traen-pytest-xdist-para-correr-la-suite-completa-con-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-los-contenedores-de-scion-de-ejecutor-y-tester-traen-pytest-xdist-para-correr-la-suite-completa-con@sha256:69764b2dd953649278f8fcaa456b2c6b0e26605a346e3cd796872c9f260bf2b6
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261122-054307/context-review/task-los-contenedores-de-scion-de-ejecutor-y-tester-traen-pytest-xdist-para-correr-la-suite-completa-con/preflight/b6ddcc0a8cc941412f57e813ad08ffc9ea317f72d3a6e51bbfd0a0fcffd0de31/attempt-1
input_sha256: b6ddcc0a8cc941412f57e813ad08ffc9ea317f72d3a6e51bbfd0a0fcffd0de31
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 608b7f7ad4e181751b62beb8ffc953e7066d352e49d709bc4c28db7c90e1458f
output_sha256: 84980b21fcb4f4d8650c23ddd4005d4aa5ce94fcf0239f0d429881aed6b9f574
# pending | accepted | rejected | incomplete
verdict: accepted
reason: "Aceptado. Resoluciones del coordinador, con lo que encontré en el código.\n\
  \nP1, B1 y B2) La capa concreta es el venv que arma el propio contenedor. No se\
  \ toca la imagen ni el Dockerfile.\n\n_render_python_env_section (deskops/runtime/scion.py:786)\
  \ le dice al agente que corra:\n\n    uv venv /tmp/ws-venv --python 3.12\n    VIRTUAL_ENV=/tmp/ws-venv\
  \ uv pip install -e \"<desk>[dev]\" -e <sldb>\n\nEl cambio es este:\n(a) Agregar\
  \ pytest-xdist a los extras [dev] de pyproject.toml de deskops. Hoy no está: grep\
  \ xdist pyproject.toml no devuelve nada. Así lo instala ese mismo uv pip install.\n\
  (b) En el bloque de ese mismo _render_python_env_section, cambiar la línea de ejemplo\
  \ 'python -m pytest -q -p no:cacheprovider <tests>' por dos líneas:\n    - una para\
  \ tests puntuales;\n    - otra para la suite completa: 'python -m pytest -n 4 -q\
  \ -p no:cacheprovider tests'.\n\nP2 y B5) El 'prompt de esos roles' es ese mismo\
  \ bloque, que dispatch inyecta en el prompt de executor y tester. Ese es el único\
  \ texto a cambiar, con el comando exacto de (b). desk/roles/deskops-executor.md\
  \ y deskops-tester.md no se tocan.\n\nP3 y B3) El test va en tests/test_dispatch.py,\
  \ o en el test que ya cubra _render_python_env_section (buscar con grep -rn _render_python_env_section\
  \ tests/). Hace dos aserciones:\n- que la sección renderizada contiene '-n 4';\n\
  - que tomllib, al leer pyproject.toml, da pytest-xdist entre los extras dev.\nNo\
  \ hace falta lanzar un contenedor real.\n\nP4) La validación queda así: tests/test_dispatch.py\
  \ más el test nuevo. Además, en el host: uv pip install -e '.[dev]' en un venv temporal\
  \ de /tmp y python -c 'import xdist' con rc 0. La salida va al run dir.\n\nB4) Cubre\
  \ a los dos roles, porque los dos reciben la misma sección. Basta comprobarlo en\
  \ el render.\n\nEl worktree es el que dispatch le da al ejecutor. El trailer es\
  \ 'Task-Id: <id de esta tarea>' en el cuerpo. CHANGELOG.md lleva una viñeta en la\
  \ sección sin publicar."
# ISO 8601 timestamp
created_at: '2026-11-22T05:43:20.023482+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T05:44:26.638174+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-los-contenedores-de-scion-de-ejecutor-y-tester-traen-pytest-xdist-para-correr-la-suite-completa-con

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261122-054307/context-review/task-los-contenedores-de-scion-de-ejecutor-y-tester-traen-pytest-xdist-para-correr-la-suite-completa-con/preflight/b6ddcc0a8cc941412f57e813ad08ffc9ea317f72d3a6e51bbfd0a0fcffd0de31/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador, con lo que encontré en el código.

P1, B1 y B2) La capa concreta es el venv que arma el propio contenedor. No se toca la imagen ni el Dockerfile.

_render_python_env_section (deskops/runtime/scion.py:786) le dice al agente que corra:

    uv venv /tmp/ws-venv --python 3.12
    VIRTUAL_ENV=/tmp/ws-venv uv pip install -e "<desk>[dev]" -e <sldb>

El cambio es este:
(a) Agregar pytest-xdist a los extras [dev] de pyproject.toml de deskops. Hoy no está: grep xdist pyproject.toml no devuelve nada. Así lo instala ese mismo uv pip install.
(b) En el bloque de ese mismo _render_python_env_section, cambiar la línea de ejemplo 'python -m pytest -q -p no:cacheprovider <tests>' por dos líneas:
    - una para tests puntuales;
    - otra para la suite completa: 'python -m pytest -n 4 -q -p no:cacheprovider tests'.

P2 y B5) El 'prompt de esos roles' es ese mismo bloque, que dispatch inyecta en el prompt de executor y tester. Ese es el único texto a cambiar, con el comando exacto de (b). desk/roles/deskops-executor.md y deskops-tester.md no se tocan.

P3 y B3) El test va en tests/test_dispatch.py, o en el test que ya cubra _render_python_env_section (buscar con grep -rn _render_python_env_section tests/). Hace dos aserciones:
- que la sección renderizada contiene '-n 4';
- que tomllib, al leer pyproject.toml, da pytest-xdist entre los extras dev.
No hace falta lanzar un contenedor real.

P4) La validación queda así: tests/test_dispatch.py más el test nuevo. Además, en el host: uv pip install -e '.[dev]' en un venv temporal de /tmp y python -c 'import xdist' con rc 0. La salida va al run dir.

B4) Cubre a los dos roles, porque los dos reciben la misma sección. Basta comprobarlo en el render.

El worktree es el que dispatch le da al ejecutor. El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo. CHANGELOG.md lleva una viñeta en la sección sin publicar.
