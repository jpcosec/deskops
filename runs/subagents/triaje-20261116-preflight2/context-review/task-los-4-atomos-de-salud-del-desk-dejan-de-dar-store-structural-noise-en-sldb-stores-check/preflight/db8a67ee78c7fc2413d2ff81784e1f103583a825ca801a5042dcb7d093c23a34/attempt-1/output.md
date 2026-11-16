REFORMULACION

Corregir en `/mnt/ssd/proyectos/SLDB_1/deskops` los cuatro AtomDocs de salud del desk nombrados en el input (delegates-store-diagnostics, measured-by-cli-diagnostics, workspace-integrity-state, repair-owned-by-deskops) para que `sldb stores check` deje de emitir `store/structural-noise`. Resultado: el contenido de cada sección con encabezado no declarado por AtomDoc pasa a `answer` como párrafo con rótulo en negrita, en el orden actual; `Tags` se fusiona en `tags`; `Related Atoms` queda en `answer`. Solo se edita con `deskops edit atom`. Fuera: `.sldb/store.yaml`, las 117 alertas `doc_lost` y el modelo AtomDoc.

AMBIGUEDADES

1. "**Evidencia:**" frente a "Evidence": no fija idioma ni texto de los demás rótulos. Obliga a inventar la traducción.
2. "cada linea no vacia de las secciones originales ... aparece en el answer nuevo" frente a "los Tags se suman al campo tags": las líneas de Tags no pueden estar en `answer` y en `tags`. Obliga a decidir la excepción.
3. "Los 4 atomos quedan sin encabezados fuera del modelo" frente a "cada linea no vacia de las secciones originales": ¿los encabezados cuentan como líneas? Obliga a definir si se conservan.
4. "AtomDoc solo declara id, title, five_wh_one_plus, answer y tags" y "el contenido de cada seccion pasa al campo answer": no dice qué ocurre con `five_wh_one_plus`. Obliga a inventar si se deja intacto.
5. "Boundary Rationale, Delegation Pattern, Diagnostic Surface, Repairability, Owned Operations, Not Owned": no hay mapa a rótulos ni orden. Obliga a inventar la correspondencia.
6. "los Tags se suman al campo tags conservando los que ya tiene": no define duplicados, orden ni JSON final. Obliga a inventar la fusión.
7. "sin codigos store/structural-noise": no aclara si exige cero alertas o solo ausencia de ese código. Obliga a inventar el criterio de pase.

DRY-RUN

Lecturas: `deskops show atom <id> --root .` y `git show HEAD:desk/atoms/<id>` para los cuatro. Cambios previstos: redactar en `/dev/shm` un `answer` por átomo, sin encabezados, con rótulos y `Related Atoms`; preparar JSON de tags; ejecutar `deskops edit atom <id> answer "$(cat archivo)" --root .` y `deskops edit atom <id> tags '[...]' --root .` por átomo; nunca editar archivos a mano. Dependencias: deskops, git, `/dev/shm`, sldb. Validaciones futuras: `stores check --format json` sin `store/structural-noise`; `graph missing` rc 0; comparar cada línea no vacía original con `answer`; verificar ausencia de encabezados Markdown.

FUTURO

Un nodo ejecutor aplicará las cuatro ediciones y entregará los AtomDocs actualizados; un nodo de validación ejecutará `stores check` y `graph missing` e informará; un humano confirmará idioma/rótulos, `five_wh_one_plus` y política de tags antes de cerrar.
