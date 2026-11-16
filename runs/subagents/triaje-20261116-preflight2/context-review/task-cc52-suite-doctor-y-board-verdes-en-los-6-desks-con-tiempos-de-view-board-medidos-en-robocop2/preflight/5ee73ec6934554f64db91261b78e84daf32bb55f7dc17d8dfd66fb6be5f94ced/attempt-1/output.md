## REFORMULACION

Encargo ejecutable (`task_type: task.code`, no agregado): en robocop2, verificar y dejar verdes suite, doctor y Board en seis desks —deskops, sldb, spec2viz, scion, pron y graph_ui (este en `UIs/graph_ui`)—. Para cada desk, ejecutar `deskops desk update` en dry-run (sin `--apply` en ajenos), `deskops doctor`, `deskops view board`, `sldb stores check` y `sldb rules check`, registrando rc y recuento de errores/alertas. Correr suites completas de deskops y sldb con `-n 4` y demostrar ausencia de fallas nuevas contra `origin/main`. Medir `deskops view board --root .` en deskops: tres corridas frías —borrando antes `.sldb_cache` y cache XDG—, calentamiento descartado y tres calientes; reportar medianas, exigiendo caliente < 1 s. Publicar tabla en `docs/config-vs-code.md` (sección Verificación) y en el TaskDoc. En deskops, aplicar `desk update --apply` solo si el dry-run muestra divergencias y commitearlo aparte; corregir únicamente fallas causadas por código de deskops, cada una con test y commit. Hallazgos ajenos se envían por `deskops message send --to <repo>`. Límites: solo lectura en desks ajenos; no arreglarlos ni tocar UI de navegador.

## AMBIGUEDADES

1. «`sldb stores check` y `sldb rules check`»: no se indica si se ejecutan con `--root` del desk ni desde qué directorio; obligaría a inventar invocación.
2. «rc + numero de errores y de alertas»: no define cómo extraer esos conteos ni qué salida cuenta como alerta; obligaría a inventar parsing.
3. «3 corridas en frio… y 3 en caliente; se reportan medianas; caliente < 1 s»: no aclara si hay umbral para frío; obligaría a inventar criterio de aceptación frío.
4. «Sin fallas nuevas contra main»: no fija si “main” es local o `origin/main`; Validation sugiere `origin/main`, pero el Goal dice «main»; obligaría a elegir.
5. «lo que falle ahi se manda con `deskops message send --to <repo>`»: no especifica asunto/cuerpo/formato ni adjuntos; obligaría a inventar contrato del mensaje.

## DRY-RUN

Lecturas: TaskDoc, `desk/drawer/plans/deskops-como-config/dag.yaml`, `docs/config-vs-code.md`, `tests/`. Cambios previstos: añadir tabla de resultados; posible `desk update --apply` en deskops (commit aparte); correcciones acotadas en `deskops/` y `tests/`, una por commit con test; mensajes a repos ajenos. Dependencias: CC30–CC38 cerradas, venv compartido, binarios `deskops`/`sldb`, host robocop2, caches borrables. Validaciones futuras: pytest de ambas suites con `-n 4`; reproducción de cada falla en worktree limpio de `origin/main`; protocolo de tiempos frío/caliente y medianas; revisión de tabla y envíos.

## FUTURO

Los repos dueños deciden y corrigen sus hallazgos; un humano autoriza/valida el cierre y posibles `--apply`; otro nodo puede reejecutar mediciones o suites.
