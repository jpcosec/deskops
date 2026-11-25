## REFORMULACION
Propósito: aplicar DK6 a las invariantes de un documento, sacándolas de servicios/tests a validadores pydantic en `deskops/models/`, y clasificar las de entre documentos hacia CC32/CC33. Resultado: inventario en el TaskDoc, validadores con test de rechazo, chequeo viejo borrado, doctor y goldens sin cambios, CHANGELOG. Repo dueño: deskops; depende de CC30; sin `requires`. Límites: no toca la consistencia status↔current_node↔history de TaskDoc (CC37); no implementa las RuleDoc de CC32/CC33, solo las asigna; no escribe en sldb ni sustituye con Python una regla de sldb.

## AMBIGUEDADES
1. «deskops doctor sin hallazgos nuevos en los 6 desks y los desks existentes cargan sin errores de validación nuevos (o el TaskDoc lista los documentos inválidos encontrados y los corrige vía deskops)»: la disyunción deja dos aceptaciones vivas y el ejecutor elige sin criterio.
2. «entre documentos → RuleDoc, asignada a CC32 (activación) o CC33 (cierre y campos) en el inventario…; lo que lea un archivo fuera del documento (p. ej. tag-namespaces.yaml) se clasifica como entre documentos»: un chequeo de namespaces no es activación ni cierre; obliga a inventar destinatario o forzar uno de los dos.
3. «su función vieja ya no existe (grep de los nombres del inventario…)» frente a «chequeos… que hoy viven fuera del modelo o solo en tests»: para los que solo existen en tests no hay función ni nombre que borrar/grep; obliga a inventar qué eliminar.

## DRY-RUN
Lecturas: dag, brief/alcance/decisiones (DK6, DK3), salida de CC30 (`doc_access.py`, fachada), `models/`, `domain_tree.py`, `atom_tags.py`, `doctor.py`, servicios y tests; grep de payloads inválidos; goldens de ayuda/salida.
Cambios: inventario en el TaskDoc; validadores en `deskops/models/`; borrado del chequeo viejo en el mismo paso en domain_tree/atom_tags/doctor/servicios; tests migrados a `ValidationError`; asignaciones a CC32/CC33; CHANGELOG. Sin tocar ciclo de vida.
Dependencias: CC30 integrado; comportamiento de `sldb fields/docs update` asumido por DK6; sin gate sldb.
Validaciones futuras: pytest de archivos tocados; goldens idénticos; `deskops doctor` en los 6 desks; `sldb fields update` en copia con atom y crossroad; greps del inventario.

## FUTURO
CC32/CC33 implementan las RuleDoc asignadas; CC37 valida el ciclo de vida de TaskDoc con el mismo mecanismo; CC35a consume el resultado. El coordinador fija grep y lista de archivos al promover; el supervisor corre la suite completa; DO5 cierra CC38 con `closeout resolved-by`.
