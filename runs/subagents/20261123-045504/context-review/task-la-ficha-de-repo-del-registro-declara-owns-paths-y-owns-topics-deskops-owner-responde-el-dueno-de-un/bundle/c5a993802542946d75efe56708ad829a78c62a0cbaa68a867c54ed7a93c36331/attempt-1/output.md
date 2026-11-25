REFORMULACION
Propósito: que el registro de repos de deskops declare qué rutas y temas posee cada repo y haya un destino para lo no reclamado. Resultado: `RepositoryDoc` con `owns_paths`/`owns_topics` y flags en `repo register`; comando `deskops owner` con rc 0/1/2; `DeskConfig.unowned_target` y `message send --to unowned`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Nodo ejecutable (`task.code`), no agregado. Límites: no registrar Governance, no fijar `unowned_target` (lo confirma JP), no llenar `owns_paths`; sí tests, goldens, contrato de modelo y suite.

AMBIGUEDADES
1. “deskops owner <ruta|tema> --root .”: no dice cómo distinguir ruta de tema si el argumento puede ser ambos; obliga a inventar heurística o flag.
2. “el repo con el glob más largo que la cubre”: no define motor de globs (`**`, separadores, rutas relativas) ni si “más largo” es longitud de cadena o especificidad; obliga a inventar matching y desempate.
3. “si ninguno, el repo cuya raíz contiene la ruta”: con repos anidados puede haber varias raíces; no dice cuál gana; obliga a inventar criterio.
4. “si dos repos empatan, los lista y sale con código 2”: no fija formato/orden ni qué hacer con tres o más; obliga a inventar salida.
5. “message send --to unowned entrega al repo de unowned_target” y “unowned_target no configurado en desk/config.json ni en config.local.json”: no aclara si el config es el del desk emisor o el destino, ni qué pasa si el id no existe o no está registrado; obliga a inventar.
6. “el comando owner” no figura en los archivos ni se nombra el parser; obliga a inventar dónde implementarlo y registrarlo.

DRY-RUN
Lecturas: los cuatro módulos y dos tests citados; parser/ayudas, goldens y contrato de modelo; notas de referencia. Cambios previstos: campos y defaults; flags; rama `owner`; resolución por registro; campo de config y rama `--to unowned`; tests p1/p2; actualización de goldens y `sldb models update`; commit con trailer. Dependencias: modelo registrado en el store, registro cargable, worktree de dispatch, confirmación de JP para el valor. Validaciones futuras: los cinco pytest indicados y suite `-n 4`. Nada ejecutado.

FUTURO
JP confirma `unowned_target`; quien coordina registra Governance después; dispatch entrega el worktree; la ejecución futura produce goldens y commit.
