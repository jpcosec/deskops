REFORMULACION
Nodo: tarea hoja `task.code` (status `draft`, `current_node: ritual-execution`), ejecutable. Propósito: que cada TaskDoc declare con el tag `host` en qué máquina corre, para rutear trabajo (UI/navegador en local; suites, build, migraciones y scion en robocop2). Resultado: deskops declara `host` no jerárquico en su semilla de tags, incluye TaskDoc en `tag_models` con `workspace/artifact/source`, lo explica en `docs/workflow-policy-reference.md` y amplía `tests/test_atom_tags.py`; una tarea con `host:robocop2` deja de alertar en `sldb stores check`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no taggear tareas existentes, no restringir valores; si con workspace/artifact/source siguen alertas, detenerse, mensaje a sldb y cerrar solo con documentación.

AMBIGUEDADES
1. "agrega host como TagNamespace(name='host', hierarchical=False)" frente a `TagNamespace(name=name, anchored_by=...)` del archivo: no se fija `hierarchical`/`folder_axis` ni se usa `sldb.api.stores.tag_namespace`; obligaría a inventar cómo pasarlos.
2. "meaning, use_when y do_not_use_when de host van en el registro de atom tags que escribe deskops (DEFAULT_ATOM_TAG_NAMESPACES, mismo formato que las demas entradas)" pero `wanted_tag_declaration` arma namespaces desde `load_namespaces(default_registry_path(root))` (`desk/atoms/tag-namespaces.yaml`); obligaría a inventar cómo llega host al store.
3. "se declaran tambien workspace, artifact y source (hierarchical=False)": `DEFAULT_ATOM_TAG_NAMESPACES` solo trae system, topic, layer, domain; obligaría a inventar sus textos.
4. "la semilla de desk que la usa": no nombra archivo (¿`DEFAULT_ATOM_TAG_NAMESPACES`, `tag-namespaces.yaml`, `desk_declaration.yaml`?); obligaría a inventar cuál.
5. "agregar TaskDoc" a "tag_models es global en sldb": no dice si se edita `TAG_MODELS` del repo o `store.yaml`; obligaría a inventar el mecanismo.

DRY-RUN
Lecturas: `deskops/atom_tags.py` completo, `desk/atoms/tag-namespaces.yaml`, `.sldb/store.yaml`, `docs/workflow-policy-reference.md`, `tests/test_atom_tags.py`, `docs/architecture/tags.md` de sldb y el modelo `TagNamespace`. Cambios previstos: añadir `host` (`hierarchical`/`folder_axis` false) a semilla y declaración, declarar workspace/artifact/source, extender `TAG_MODELS` con TaskDoc, línea en "### Tasks" y test sandbox con TaskDoc `host:robocop2` y `stores check` sin alerta. Dependencias: campos de `TagNamespace`, sync de `desk update` y reglas de `stores check`. Validaciones futuras: los cuatro comandos del TaskDoc.

FUTURO
sldb decide/añade namespaces por modelo si `stores check` sigue alertando (message send); el coordinador etiqueta tareas existentes; Tester valida y closeout; el humano aprueba.
