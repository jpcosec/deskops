## REFORMULACION
Propósito: eliminar las 4 alertas `store/structural-noise` producidas por encabezados fuera del modelo en cuatro AtomDocs de salud del desk. Resultado: los 4 átomos editados solo con `deskops edit atom`, sin encabezados no declarados, conservando su contenido; `sldb stores check` deja de emitir `store/structural-noise`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`; store `.sldb`; átomos en `desk/atoms/`.

Límites: solo esos 4 átomos; no declarar `structural_noise: allow` en `.sldb/store.yaml`; no tocar las 117 alertas `doc_lost`; no cambiar el modelo AtomDoc. El nodo es ejecutable, no agregado: `atoms: []`, `depends_on: []`.

## AMBIGUEDADES
1. “los Related Atoms al campo de referencias del AtomDoc”: no fija el nombre exacto ni el formato del campo (`references`, lista de ids/slugs, etc.). Obliga a inventar el esquema.
2. “el contenido de cada seccion pasa a prosa o vinetas dentro del campo answer”: no decide prosa frente a viñetas, orden de secciones ni si se conservan los rótulos. Obliga a inventar el formato.
3. “los Tags al campo tags”: no aclara si se conservan etiquetas previas ni el separador. Obliga a inventar la normalización.
4. “no se pierde informacion” y “conserva su contenido original en sus campos”: no definen una comprobación objetiva de pérdida. Obliga a inventar el criterio de aceptación.
5. “`deskops edit atom <id> <campo> <valor> --root .`”: no indica cómo pasar valores multilínea o listas. Obliga a inventar quoting/serialización.

## DRY-RUN
Lecturas: TaskDoc, `deskops show atom` de los cuatro IDs, esquema del AtomDoc y estado del store. Cambios previstos: por átomo, redactar `answer` sin encabezados, mover Tags a `tags` y Related Atoms a referencias; aplicar `deskops edit atom` campo a campo. Dependencias: `deskops`, `sldb`, `.venv` y root correcto. Validaciones futuras: `stores check --format json` sin códigos `store/structural-noise` y `deskops graph missing --root .` con rc 0. Sin ejecutar.

## FUTURO
Un humano o nodo posterior decide el mapeo exacto de secciones, el campo de referencias y la aceptación de conservación. Otro nodo ejecuta las ediciones y otro verifica `stores check` y `graph missing`. No hay hijos que transferir.
