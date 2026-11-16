# Parte D: inbox de deskops (worker, 2026-11-15)

## Commits (deskops main, sin push)
- 1081659c: `message send --to` resuelve el destino en el registro del ecosistema.
- da68b6e2: desk, triaje del inbox. 9 tareas nuevas, 3 notas promovidas, 6 acks, y los recibos preflight/bundle de la tarea --to. [skip ci]
- 329599b3: closeout resolved-by de la tarea --to.
- 22540bc9: desk(inbox), nota ajena 20261115-215933. El closeout 329599b3 arrastró su yaml del store (bug ya conocido "closeout arrastra .sldb sin trackear"), y este commit agrega su .md para que el store y git queden coherentes. [skip ci]
- ~/setup 3a75d10 (pusheado): registro de deskops, sldb y spec2viz con `deskops repo register`, con path `~/proyectos/SLDB_1/<repo>`.

## Notas → tareas
Las notas de MEPU del 15-11 no estaban en el inbox de deskops: no llegaron porque `--to deskops` no resolvía. Las tareas se escribieron a partir del brief.
- status lento y obsoleto → task-deskops-status-deja-de-ser-solo-un-aviso-deprecated-y-entrega-el-estado-rapido-del-desk. La tarea dice que la implementa V1 y que se cierra con resolved-by.
- --to no resuelve → task-message-send-to-resuelve-el-destino-en-el-registro-del-ecosistema-cuando-el-registro-propio-no-lo-li (IMPLEMENTADA y cerrada).
- checkout atrasado con .sldb sin commitear → task-doctor-dice-de-que-tarea-es-cada-cambio-sin-commitear-en-sldb-checkout-atrasado (se cruza con H1/H2).
- supertareas y alta en lote → task-supertareas-y-alta-en-lote-campo-parent-en-taskdoc-y-add-task-from-yaml-con-varias-tareas. `--from-yaml` ya existe, pero carga una sola tarea.
- rol de desk/hitl → task-rol-de-desk-hitl-about-faq-y-doctor-documentan-cada-carpeta-del-desk-y-doctor-avisa-si-hitl-tiene-ar
- init en worktree → task-init-en-un-worktree-usa-el-nombre-del-repo-y-doctor-lee-el-pythonpath-del-store
- Recibos "lost" (inbox 20261114-022915, promovida) → task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
- Board no refleja edit task goal (20261112-132201, promovida) → task-board-no-refleja-deskops-edit-task-goal (task.debug)
- ftcourier derrama reglas (20261110-094518, promovida) → task-advance-y-closeout-no-derraman-reglas-de-activacion-ni-runtimes-centrales-sin-trackear-en-el-desk-co. Se ve también hoy en ~/setup: hay 7 rule-activation-* sin trackear.

Las 3 promovidas siguen en el drawer como candidatas (desk/drawer/tasks), enlazadas con from_drawer.

## Ya resueltas (ack, sin tarea nueva; no se reimplementa nada)
- GD21 → CC33c 120bb672 (closeout f0ae2737): desk_graph.py ya no existe.
- GD25 → CC34 dc3ed05a (closeout 2e9f6f84): desk_view.py y el tablero a mano ya no existen.
- GD22 → CC35c 8c583005 (closeout 60f1ec37).
- GD27 → CC35d 6d55bb40 y 38b23982 (closeouts 8d3dd4f8 y e0d43a76): domain_tree y atom_tags usan la API de tags de sldb.
- GD26 → CC36 d4b49ff6 (closeout d4e8f445).
- task.refactor no puede cerrar → CC33b 4338f90b: rule-closeout-task-refactor lee el recibo goldens (`deskops review record --kind goldens`).

## Fix de --to
- deskops/identity.py:
  - `ecosystem_registry_dir()`: usa `$DESKOPS_ECOSYSTEM_REGISTRY`; si no está, `~/setup/desk/registry`.
  - `load_ecosystem_registry()` y `find_registered_desk()`: buscan primero en el registro propio, después en el del ecosistema. Funcionan también sin store local. Si la raíz registrada no existe en esta máquina, dan error y no escriben nada.
  - `expanduser` en `resolve_registered_root`.
- message.py: el destino se resuelve con `find_registered_desk`. Para la identidad del remitente, el último recurso es su raíz en el registro del ecosistema.
- repo.py: usa la misma resolución de rutas.
- tests/test_message_ecosystem_registry.py: 6 tests con el CLI real en subprocess, sin mocks. Se fija PYTHONPATH al checkout porque el venv importa deskops-runtime. Resultado: 6 passed.
- Tests relacionados de a uno: test_message_delivery (6), test_repo_identity (8), test_registry_robustness (5), test_message_cli (10). Todos en verde.
- Preflight-1 y bundle-1 (pi): las ambigüedades se resolvieron como precisiones p1-p8 (scope) y b1-b3 (done_when), y ambos recibos se dispusieron accepted. Al editar la tarea después de cada revisión, los recibos quedaron "stale". No se repitió la revisión porque el pedido era una sola vez. La tarea se cerró con resolved-by.

## Suite completa
- `flock sldb1-tests.lock`, `-n 4`, TMPDIR=/dev/shm: rc 1, con 5 failed, 1047 passed, 3 skipped y 1 xfailed (30 min 45 s).
- 3 fallos son de entorno: `python` y `pytest` no estaban en PATH porque se invocó el python del venv sin activarlo.
  - test_ci_integration (2)
  - e2e test_reference_solutions[first-task-to-closeout]
  - Repetidos con el venv en PATH: 2 passed y 1 passed.
- 2 fallos son ajenos y vienen de 02fb01b7 (otro worker, role y runtime-profile por CLI): artifact.role no declara status_default.
  - test_extension_points::test_every_creatable_artifact_model_declares_its_defaults
  - test_specs::test_every_artifact_model_declares_its_artifact_defaults
- graph missing: rc 0 ("No missing graph references found") antes de cada commit de desk y después del closeout.

## Mensaje a MEPU: NO enviado
- `--to mepu` no resuelve en esta máquina. El registro de ~/setup tiene:
  - `mepu` → /home/jp/proyectos/mepu
  - `antonia-mepu-ocs-dev` → /home/jp/AntonIA/repos/mepu/mepu_ocs_dev
  - Ninguna de las dos rutas existe en robocop, y el fix ahora lo informa como error en vez de escribir.
- El MEPU real está en /home/robocop/AntonIA/repos/legacy/mepu/mepu (heyantonia/mepu, rama dev, project_identity mepu_ocs_dev). No hay ningún `~/...` común entre las dos máquinas, así que no cambié el registro de JP ni escribí en el repo de MEPU.
- Decide JP o el coordinador. Hay dos opciones:
  - un symlink `~/AntonIA/repos/mepu/mepu_ocs_dev` → `~/AntonIA/repos/legacy/mepu/mepu` en robocop, con `path: ~/AntonIA/repos/mepu/mepu_ocs_dev` en ~/setup;
  - o enviar con `--root /home/robocop/AntonIA/repos/legacy/mepu/mepu`.
- Texto listo para enviar: "Mientras H2 (merge driver de sldb) no exista: no crear un segundo store en dev. Primero mergear la rama de ontología con su .sldb/, después deskops init sobre dev. Ante un conflicto en un archivo generado, tomar un lado y correr sldb stores build, más sldb stores check."

## Limpieza
- Borrados /dev/shm/dk-tasks.txt, dk-gm.txt y dk-suite.txt.
- Los pytest-of-robocop de /dev/shm son de pytest y no tienen el prefijo dk-.
- ~/setup quedó con .sldb_cache/ sin trackear: la creó sldb al registrar. Sigue sin trackear porque .gitignore no la cubre.

## Pendientes
- Enviar el mensaje a MEPU (ver arriba).
- Corregir la ruta de mepu y antonia-mepu-ocs-dev en ~/setup.
- Los 2 fallos de artifact.role de 02fb01b7.
- La nota nueva 20261115-215933 del coordinador está sin triar.
- Push de deskops: lo hace el coordinador.
