---
sldb:
  by: agent
  at: '2026-11-23T14:58:52Z'
  authority: generated
  via: save_document_payload
id: task-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-deskops-owner-responde-el-dueno-de-un
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/cli/commands/message.py
- deskops/cli/commands/repo.py
- deskops/cli/registry.py
- deskops/config.py
- deskops/models/repository.py
- tests/fixtures/golden/help/deskops.txt
- tests/fixtures/golden/help/deskops_add_repository.txt
- tests/fixtures/golden/help/deskops_owner.txt
- tests/fixtures/golden/help/deskops_repo_register.txt
- tests/fixtures/golden/output/list_repositories.json
- tests/fixtures/golden/output/show_repository.json
- tests/fixtures/golden/output/show_repository.text
- tests/fixtures/model_contract_hashes.json
- tests/test_cli.py
- tests/test_cli_grammar.py
- tests/test_config.py
- tests/test_message_ecosystem_registry.py
- 05ac75a9952b657734dd767351b0c0e7feef4d49
depends_on: []
pills: []
files:
- deskops/cli/commands/message.py
- deskops/cli/commands/repo.py
- deskops/cli/registry.py
- deskops/config.py
- deskops/models/repository.py
- tests/fixtures/golden/help/deskops.txt
- tests/fixtures/golden/help/deskops_add_repository.txt
- tests/fixtures/golden/help/deskops_owner.txt
- tests/fixtures/golden/help/deskops_repo_register.txt
- tests/fixtures/golden/output/list_repositories.json
- tests/fixtures/golden/output/show_repository.json
- tests/fixtures/golden/output/show_repository.text
- tests/fixtures/model_contract_hashes.json
- tests/test_cli.py
- tests/test_cli_grammar.py
- tests/test_config.py
- tests/test_message_ecosystem_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno
---

# La ficha de repo del registro declara owns_paths y owns_topics, deskops owner responde el dueño de una ruta o tema, y message send --to unowned va al destino de config unowned_target

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234458 (scion-coordination, workflow scion + deskops de JP): no hay dónde declarar qué rutas y temas son de cada desk ni a dónde va lo que no es de nadie. Caso real: heyantonia/mepu#459, dos notas que eran de etlkit (shared_etl-plataforma) quedaron en tareas de mepu. El piloto registró un acuerdo provisional en atom-sin-dueno-lo-que-no-tiene-dueno-en-sldb-1-va-al-inbox-de-deskops (JP no lo confirmó; por eso el destino va en config y no en código).

## Goal

_Describe the concrete result this task must produce._

(1) RepositoryDoc (deskops/models/repository.py) gana owns_paths (lista de globs relativos a la raíz del ecosistema, por defecto vacía) y owns_topics (lista de strings, por defecto vacía); deskops repo register acepta --owns-paths y --owns-topics separados por coma. (2) deskops owner <ruta|tema> --root . responde el id del repo dueño: para una ruta, el repo con el glob más largo que la cubre (y, si ninguno, el repo cuya raíz contiene la ruta); para un tema, el repo que lo lista en owns_topics; si nadie, imprime "sin dueno" y sale con código 1; si dos repos empatan, los lista y sale con código 2. (3) DeskConfig gana unowned_target (id de repo registrado, opcional); deskops message send --to unowned entrega al repo de unowned_target, y si no está configurado falla con "unowned_target no configurado en desk/config.json ni en config.local.json".

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/models/repository.py, deskops/config.py, deskops/cli/commands/repo.py, deskops/cli/commands/message.py, el comando owner, goldens de ayuda y de contrato del modelo, tests/test_message_ecosystem_registry.py y tests/test_config.py. No entra: registrar Governance (project_identity repo-governance, heyantonia/Governance) en el registro (lo hace quien coordina el registro con deskops repo register, después de esta tarea), fijar el valor de unowned_target (lo confirma JP), llenar owns_paths de cada repo.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_message_ecosystem_registry.py sobre un ecosistema temporal con dos repos registrados: test_owner_resolves_path_by_longest_glob, test_owner_resolves_topic, test_owner_without_owner_exits_1, test_owner_tie_exits_2, test_send_to_unowned_uses_unowned_target, test_send_to_unowned_without_config_fails. p2: test en tests/test_config.py de unowned_target en config.local.json. p3: implementar. p4: goldens (ayuda y contrato de RepositoryDoc) y sldb models update del modelo en el store del desk. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_ecosystem_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los siete tests nuevos pasan y las fichas de desk/registry existentes siguen cargando sin cambios (owns_* vacíos por defecto).
