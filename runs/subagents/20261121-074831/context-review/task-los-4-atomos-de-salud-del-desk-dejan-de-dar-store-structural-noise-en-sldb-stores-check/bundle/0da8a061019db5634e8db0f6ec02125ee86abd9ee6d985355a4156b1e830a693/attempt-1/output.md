## REFORMULACION

Propósito: eliminar las alertas `store/structural-noise` de `sldb stores check` en los 4 AtomDocs de salud del desk, moviendo encabezados no declarados por AtomDoc a `answer` y los valores de Tags al campo `tags`. Resultado: los 4 átomos sin encabezados fuera del modelo, sin pérdida de contenido, y `stores check` sin `store/structural-noise` para ellos. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo esos 4 átomos en `desk/atoms/`, editados con `deskops`; fuera: declarar `structural_noise: allow`, las 117 alertas `doc_lost` y cambiar el modelo AtomDoc.

## AMBIGUEDADES

1. Rutas: "desk/atoms (los 4 atomos nombrados)" y "git show HEAD:<ruta del atomo>" no dan rutas explícitas. Obligaría a inventar `desk/atoms/<id>.md`.
2. Tags: "sus valores se agregan al campo tags al final de los existentes, sin duplicados" no define separador ni orden. Obligaría a inventar el parseo y el orden.
3. Comando de tags: "se agregan ... al final de los existentes" frente a "deskops edit atom <id> tags '<lista JSON>'". Obligaría a inventar si la lista JSON es la final completa o solo los nuevos.
4. Validación: "sin codigos store/structural-noise" no aclara si es global o solo para esos 4; el Goal dice "para estos 4 atomos". Obligaría a inventar el alcance.
5. Formato: "cada seccion no-Tags pasa al final de answer como un parrafo" y "cada linea no vacia ... aparece en el answer nuevo" no fijan saltos ni concatenación exacta. Obligaría a inventar el formato.

## DRY-RUN

Lecturas: TaskDoc; los 4 ids del Rationale; `deskops show atom <id> --root .`; `git show HEAD:<ruta>` para texto y tags; estado actual de `answer` y `tags`. Cambios previstos: redactar en `/dev/shm` un `answer` por átomo, conservar `title` y `five_wh_one_plus`, convertir secciones no-Tags en párrafos con encabezado en negrita, mantener Related Atoms como lista y fusionar Tags sin duplicados; aplicar `deskops edit atom ... answer` y `... tags`; no tocar `.sldb/store.yaml` ni otros átomos. Dependencias: CLI `deskops`, git, entorno Python/sldb y rutas válidas. Validaciones futuras: `sldb stores check --store .sldb --format json` sin `store/structural-noise` para los 4 y `deskops graph missing --root .` con rc 0. No se ejecuta nada.

## FUTURO

Un nodo ejecutor leerá el cold-bundle completo, resolverá rutas y aplicará las ediciones; otro verificador correrá las validaciones. Un humano decidirá el alcance de la validación si no se aclara antes.
