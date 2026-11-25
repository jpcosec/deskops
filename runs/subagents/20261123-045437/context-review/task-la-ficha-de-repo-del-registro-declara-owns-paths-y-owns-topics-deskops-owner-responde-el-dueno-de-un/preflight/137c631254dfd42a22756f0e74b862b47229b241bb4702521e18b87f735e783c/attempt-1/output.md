REFORMULACION
Propósito: que el registro de deskops declare qué rutas y temas pertenecen a cada repo y que lo sin dueño tenga un destino configurable. Resultado: RepositoryDoc con owns_paths/owns_topics vacíos por defecto; repo register con --owns-paths/--owns-topics; comando owner que resuelve ruta o tema; DeskConfig.unowned_target; message send --to unowned. Repo: /mnt/ssd/proyectos/SLDB_1/deskops. Es un nodo ejecutable task.code, no un agregado. Límites: no registrar Governance, no fijar unowned_target, no llenar owns_paths; solo la superficie listada.

AMBIGUEDADES
1. “el repo con el glob más largo que la cubre” no define semántica de glob, normalización, mayúsculas ni desempate entre raíces; obliga a inventar el algoritmo.
2. “si dos repos empatan, los lista y sale con código 2” no fija formato ni orden de la lista, ni si el empate aplica solo a globs o también a temas; obliga a inventar la salida.
3. “deskops owner <ruta|tema> --root .” no dice cómo distinguir ruta de tema si el texto coincide con ambos, ni el valor por defecto o la relatividad de --root; obliga a inventar la desambiguación.
4. “--owns-paths y --owns-topics separados por coma” no aclara repetibilidad, espacios, valores vacíos, reemplazo/anexado ni validación; obliga a inventar el parsing.
5. “unowned_target (id de repo registrado, opcional)” no define precedencia entre desk/config.json y config.local.json ni qué ocurre si el id no existe; obliga a inventar la política.
6. “message send --to unowned entrega al repo de unowned_target” no especifica la traducción a destino/inbox ni su relación con --to existente; obliga a inventar la entrega.

DRY-RUN
Lecturas: TaskDoc, nota y átomo referenciados, repository.py, config.py, repo.py, message.py, tests citados, goldens/contrato y registro/config del desk. Cambios previstos: añadir tests p1/p2; implementar campos y flags; owner con códigos 0/1/2; unowned_target y routing; actualizar goldens y modelo en el store. Dependencias: carga de fichas existentes con owns_* vacíos, precedencia de config, infraestructura de goldens y worktree de dispatch. Validaciones futuras: los cuatro pytest focalizados y la suite completa con -n 4; cierre cuando pasen los siete tests y las fichas existentes carguen.

FUTURO
Dispatch entrega el worktree; JP confirma unowned_target; el coordinador registra Governance después; el ejecutor produce el commit con Task-Id.
