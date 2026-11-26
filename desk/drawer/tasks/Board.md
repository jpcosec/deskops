# Drawer Board

This board routes deferred work only.

## Remaining

Pedidos individuales diferidos el 2026-11-25 hasta después de las etapas E1-E4 (refactor, pluginización, responsabilidades a sldb, rediseño del testing); se reevalúan contra el deskops resultante:

- task-la-evidencia-de-tests-corre-la-validacion-de-la-tarea-y-registra-el-resultado-y-el-veredicto-del-tes: La evidencia de tests corre la validación de la tarea y registra el resultado, y el veredicto del tester es un recibo
- task-los-recibos-anclan-el-codigo-exponen-motor-y-autor-y-commit-respeta-el-resultado-de-verify: Los recibos anclan el código, exponen motor y autor, y commit respeta el resultado de verify
- task-la-activacion-puede-exigirse-antes-del-despacho-y-el-ruteo-por-board-es-una-regla: La activación puede exigirse antes del despacho y el ruteo por Board es una regla
- task-verificar-y-arreglar-dependencias-inexistentes-n7-y-la-autorreferencia-que-exime-del-gate-de-vinculo: Verificar y arreglar dependencias inexistentes (N7) y la autorreferencia que exime del gate de vínculos (N11)
- task-integrate-encuentra-el-cierre-por-el-trailer-task-id-y-distingue-closeout-mode: integrate encuentra el cierre por el trailer Task-Id y distingue Closeout-Mode
- task-una-pill-declara-el-trabajo-al-que-pertenece-y-como-termina-y-deskops-avisa-de-la-que-quedo-sin-trab: una pill declara el trabajo al que pertenece y cómo termina, y deskops avisa de la que quedó sin trabajo abierto (al drawer en la conciliación del 2026-11-26, decisión de JP; conserva 4 recibos aprobados en desk/reviews/)
- task-governance-closeout-no-borra-una-tarea-de-la-que-otras-heredan-inherits-from-o-las-herederas-siguen: Governance: closeout no borra una tarea de la que otras heredan (inherits_from), o las herederas siguen cargando
- task-el-gate-de-cierre-acepta-el-commit-de-la-tarea-como-vinculo-de-cada-archivo-de-files-en-vez-de-exigi: El gate de cierre acepta el commit de la tarea como vínculo de cada archivo de files en vez de exigir un átomo por archivo
- task-supertareas-y-alta-en-lote-campo-parent-en-taskdoc-y-add-task-from-yaml-con-varias-tareas: supertareas y alta en lote: campo parent en TaskDoc y add task --from-yaml con varias tareas
- task-governance-documento-de-pr-en-desk-prs-y-deskops-pr-check-en-ci: Governance: documento de PR en desk/PRS y deskops pr check en CI
- task-governance-el-cierre-de-la-tarea-ocurre-dentro-del-pr-y-deskops-reconcile-lo-cruza-con-github: Governance: el cierre de la tarea ocurre dentro del PR y deskops reconcile lo cruza con GitHub
- task-taskdoc-declara-el-pr-o-la-rama-que-la-realiza-como-referencia-a-un-pullrequestdoc-d4-de-governance: TaskDoc declara el PR o la rama que la realiza como referencia a un PullRequestDoc (D4 de Governance)
- task-el-inbox-admite-avisos-kind-alert-ademas-de-unclear-y-suggestion-d5-de-governance: El inbox admite avisos (kind alert) además de unclear y suggestion (D5 de Governance)
- task-lo-retirado-se-borra-y-la-tarea-guarda-un-puntero-a-git-para-ver-su-genealogia: Lo retirado se borra y la tarea guarda un puntero a git para ver su genealogía
- task-el-runner-de-revisiones-lanza-al-revisor-con-stdin-devnull-cuando-la-entrada-va-por-archivo: El runner de revisiones lanza al revisor con stdin DEVNULL cuando la entrada va por archivo
- task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar: dispatch start se niega a lanzar un rol cuyo env_config no declara volumes propios, para poder quitar el montaje global de SLDB_1 y /dev/shm de los agentes claude
- task-las-rutas-y-credenciales-de-maquina-de-dispatch-e-integrate-salen-de-desk-config-json-versionado-a-d: Las rutas y credenciales de máquina de dispatch e integrate salen del config.json versionado del desk a su config.local.json (no versionado) en deskops y sldb
- task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa: deskops trae un RoleDoc desk-identity instalable en cualquier desk y runtime template lo materializa como agente scion persistente (--mode identity)
- task-deskops-list-tasks-y-deskops-next-filtran-por-maquina-con-host-tag-host-valor-y-la-salida-de-list-ta: deskops list tasks y deskops next filtran por máquina con --host (tag host:<valor>) y la salida de list tasks muestra el host
- task-governance-concilio-y-pruebas-sin-contexto-como-mecanismos-que-deskops-levanta-en-scion: Governance: concilio y pruebas sin contexto como mecanismos que deskops levanta en scion
- task-despacho-flexible-sobre-runtimeprofiledoc-claude-headless-o-subagente-de-sesion-pi-y-scion-con-el-mi: Despacho flexible sobre RuntimeProfileDoc: claude (headless o subagente de sesión), pi y scion, con el mismo prompt y el mismo runner que la revisión
- task-deskops-doctor-marca-una-mutacion-como-alerta-y-solo-una-rotura-como-error: deskops doctor marca una mutación como alerta y solo una rotura como error
- task-doctor-dice-de-que-tarea-es-cada-cambio-sin-commitear-en-sldb-checkout-atrasado: doctor dice de que tarea es cada cambio sin commitear en .sldb (checkout atrasado)
- task-governance-puesta-al-dia-de-los-clones-base-de-la-maquina-coordinadora-y-doctor-que-valida-cada-tare: Governance: puesta al día de los clones base de la máquina coordinadora y doctor que valida cada tarea contra su modelo
- task-governance-registro-en-el-desk-de-los-artefactos-generados-por-claude-y-por-el-desk: Governance: registro en el desk de los artefactos generados por Claude y por el desk
- task-huecos-de-atomos-de-la-auditoria-de-chatbot-infra-renombrar-id-retire-de-atomos-validate-all-y-edita: Huecos de atomos de la auditoria de Chatbot_Infra: renombrar id, retire de atomos, validate --all y editar contexts/pills.md
- task-desk-update-en-seco-lista-los-tags-de-tareas-con-namespace-sin-declarar-y-apply-no-mete-taskdoc-en-t: desk update en seco lista los tags de tareas con namespace sin declarar y --apply no mete TaskDoc en tag_models mientras queden
- task-rol-de-desk-hitl-about-faq-y-doctor-documentan-cada-carpeta-del-desk-y-doctor-avisa-si-hitl-tiene-ar: rol de desk/hitl: about, faq y doctor documentan cada carpeta del desk y doctor avisa si hitl tiene archivos que no son para el humano
- task-los-botones-de-graph-ui-frontends-desk-llaman-a-las-operaciones-de-deskops: Los botones de graph_ui/frontends/desk llaman a las operaciones de deskops
- task-evaluar-el-code-mode-de-fastmcp-para-que-los-agentes-encadenen-operaciones-de-deskops-en-codigo: Evaluar el code mode de FastMCP para que los agentes encadenen operaciones de deskops en código

- task-governance-levantamiento-de-que-puede-juzgar-jev-typesafe-en-el-workflow-de-deskops: exploración, diferida (JP, 2026-11-25).
- task-governance-agente-interno-por-desk-en-scion-activado-por-hooks-de-deskops: idea afín al agente de coherencia, diferida con él (JP, 2026-11-25).
- task-decidir-si-se-construye-el-agente-de-coherencia-del-desk-y-como: decidir si se construye el agente de coherencia del desk; propuesta en desk/drawer/plans/deskops-plugin-de-sldb/propuesta-agente-coherencia.md. Diferida por JP el 2026-11-25.

Nada. Triaje del 2026-11-16: los 14 ítems sueltos se botaron (5 ya resueltos y 9 cubiertos por una tarea activa que los cita en from_drawer). Detalle en reports/triaje-deskops-20261116.md.


## Retired

The covered use-cases, stress-tests (the CI gap closed by task-test-ci-knowledge-integrity-flow, which added scripts/ci-knowledge-check.sh and tests/test_ci_integration.py), findings archive, answered questions, drawer rituals, attention review, and obsolete feature outlines were retired on 2026-10-19. The runtime-and-launcher feature and the tmux launcher task were retired the same day by the coordinator's decision: `deskops runtime supervise` plus the external harness (Herdr) cover what the tmux launcher would have done. Each retirement commit names the test or replacement that covers it, and git history is the durable record.

## Rule

Nothing in `desk/drawer/` executes. When an item is ready, author a full task with `deskops add task --from-drawer <item>` and remove the drawer item by hand once that task supersedes it; there is no drawer-to-task promotion.
