REFORMULACION
Propósito: completar la parte (4) de CC35 migrando a sldb los tags y el reemplazo —`tag_namespaces`, `tag_tree`, `tag_folder` y `replace_text`— sin cambiar el formato del desk ni la gramática del CLI, borrando el código viejo en el mismo paso. Resultado: `tag-namespaces.yaml` sincronizado idempotentemente al store, `domain:a.b` sin crossroad de `domain:a` fallando como antes, `require_domain_parents` eliminado y `desk replace` con la misma guarda de conteo. Repo dueño: deskops. Límites: no escribe en sldb, no suple reglas con Python, no toca P4; depende de CC35b y del gate G_GD27, ya satisfecho.

AMBIGUEDADES
1. Contradicción con DO7: la aceptación pide «grep -rn "require_domain_parents" deskops/ vacío» y «desk update --apply sincroniza tag-namespaces.yaml al store», pero DO7 dice «CC35d se corta: entrega solo a4 (desk replace por `sldb.replace_text`). Árbol de dominios, `require_domain_parents`, `tag_namespaces` y `tag_folder` (b6) esperan a sldb H1-H3». Obliga a inventar si el nodo entrega todo o solo `replace_text`.
2. Cita: «Parte de los chequeos que CC38 dejó inventariados para CC33 (padres de domain, registro de namespaces) pueden resolverse aquí si GD27 los cubre; se anota cuáles.» Obliga a inventar qué chequeos entran y cuáles quedan fuera.
3. Cita de aceptación: «domain:a.b sin crossroad de domain:a falla como antes». DO7 difiere esa validación; obliga a inventar si se implementa o se conserva por otra vía.

DRY-RUN
Lecturas: `domain_tree.py`, `atom_tags.py`, `services/replace.py`, `cli/commands/desk.py`, tests y fixtures de tag-namespaces, CHANGELOG. Cambios previstos: `replace.py` pasa a `sldb.replace_text` con guarda de conteo; `atom_tags.axis_folder_relpath` → `tag_folder`; `desk update --apply` sincroniza `tag-namespaces.yaml` al store; `DomainTree.check/tree` a validación/`tag_tree` de GD27; se borra `require_domain_parents`; queda lo del caso (crossroads y protoátomos). Dependencias: CC35b integrado y G_GD27 satisfecho (pin `structuredLanguageDB>=0.1.13`). Validaciones futuras: greps, goldens de ayuda y salida, tests tocados, `doctor` en los 6 desks, idempotencia, líneas antes/después.

FUTURO
El coordinador o el dueño deben resolver el corte DO7: confirmar si CC35d entrega solo a4 o el alcance completo. sldb debe entregar H1-H3 para retomar b6 (árbol de dominios, `require_domain_parents`, `tag_namespaces`, `tag_folder`). CC35 cierra cuando cierren sus hijos; el cierre lo decide `deskops closeout commit`.
