**REFORMULACION**  
Tarea concreta y ejecutable, no agregado ni paquete. Propósito: eliminar las 4 alertas `store/structural-noise` que `sldb stores check` emite por cuatro AtomDocs con encabezados fuera del modelo AtomDoc. Resultado: editar esos 4 átomos en `desk/atoms` para que cada sección no-`Tags` pase al final de `answer` como párrafo con encabezado original en negrita, y los valores de `Tags` se añadan al campo `tags`, sin duplicados; `title` y `five_wh_one_plus` no cambian. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `deskops edit atom`; no tocar `.sldb/store.yaml`, no resolver las 117 alertas `doc_lost`, no cambiar el modelo AtomDoc.

**AMBIGUEDADES**  
1. “Cada seccion no-Tags pasa al final de answer como un parrafo”: obliga a inventar cómo convertir varias líneas, viñetas o líneas en blanco en “un párrafo” y qué separadores conservar.  
2. “sus valores se agregan al campo tags al final de los existentes, sin duplicados”: obliga a inventar el criterio de igualdad —mayúsculas, espacios, formato— y el orden de los nuevos tags.  
3. “la seccion Related Atoms queda igual, como '**Related Atoms:** atom-a, atom-b'”: obliga a inventar la normalización si el original trae varias líneas, viñetas o separadores distintos.  
4. “Sin perdida: cada linea no vacia... (git show HEAD:<ruta del atomo>)” frente a “`deskops show atom <id> --root .`”: obliga a decidir qué fuente manda si el working tree y `HEAD` difieren.

**DRY-RUN**  
Lecturas: documento de tarea; los 4 átomos con `deskops show atom`; versiones `HEAD` con `git show`; tags actuales y `.sldb/store.yaml` solo lectura. Cambios previstos: por átomo, generar en `/dev/shm` el `answer` sin encabezados y el JSON de `tags`; ejecutar `deskops edit atom <id> answer ...` y `deskops edit atom <id> tags ...`. Dependencias: CLI `deskops`, módulo `sldb`, venv, git, `/dev/shm` escribible e IDs válidos. Validaciones futuras: `sldb stores check --store .sldb --format json` sin `store/structural-noise` para esos IDs; `deskops graph missing --root .` con rc 0; comprobación de no pérdida de líneas no vacías y tags.

**FUTURO**  
Un nodo ejecutor aplicará las ediciones y devolverá diff y salidas de validación. Un humano o revisor decidirá si el pase es aceptable pese a otras alertas y si algún conflicto de tags requiere criterio semántico.
