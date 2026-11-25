## REFORMULACION
**Propósito:** eliminar tres rodeos propios de deskops sustituyéndolos por APIs públicas ya integradas de sldb, sin cambiar comportamiento observable.

**Resultado:** (a) `deskops/services/references.py` sin `_rewrite_mentions` ni `_in_frontmatter`, usando `sldb.api.rewrite_references(..., graph=g, excluded_sources=[...])` y `referrers(..., graph=g)`; (b) `deskops/doc_access.py::template_placeholders` usando `sldb.api.template_anchors`, sin `TemplateExtractor` si no queda otro uso; (c) `deskops/services/closure.py` creando recibos de evidencia con un solo `create` pinneado, sin el par create+update en la misma transacción.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`; sldb instalado en `/mnt/ssd/herramientas/sldb`. Entra también el código de tests que cubre esos caminos; no entra modificar sldb.

**Límites:** si una API no se comporta como la nota, se detiene esa parte y se deja nota por inbox; las demás siguen. No se cambian aserciones existentes. La suite completa se corre una vez antes de entregar.

## AMBIGUEDADES
1. "tests de references/retire" — no nombra archivos; obligaría a inventar rutas de test.
2. "subject con @sha256 y anchor_state intact" — no indica campo, formato ni comprobación; obligaría a inventar el criterio de verificación.
3. "si alguna API no se comporta como dice la nota, se para esa parte y se deja nota a sldb por inbox" — no define formato ni ubicación de esa nota; obligaría a inventar el protocolo de parada.
4. "graph=g" — no dice de dónde sale `g` en cada call site; obligaría a inventar la construcción del grafo.
5. "lineas ~143-230", "~linea 546", "~lineas 1102-1171" — rangos aproximados; obligarían a localizar por símbolo, no por línea.
6. "la suite completa pasa sin cambiar aserciones existentes" frente a "solo se acepta si falla igual ahi" — no aclara si fallos preexistentes bloquean el cierre; obligaría a inventar el criterio.

## DRY-RUN
**Lecturas:** `references.py`, `doc_access.py`, `closure.py`, tests citados; firmas vía `inspect.signature` de `rewrite_references`, `referrers`, `template_anchors`; confirmación del pinneo en `tests/api/test_doc_anchors.py` de sldb.
**Cambios previstos:** sustituir los tres rodeos de a uno, corriendo el test del archivo tocado tras cada uno; borrar imports muertos; ajustar llamadas para pasar `graph` y `excluded_sources`.
**Dependencias:** versión de sldb instalada y semántica real de las APIs; helpers existentes para obtener el grafo.
**Validaciones futuras:** los tres pytest unitarios, el grep sin resultados y la suite completa con comparación contra `origin/main` en worktree limpio. Nada se ejecuta aquí.

## FUTURO
La ejecución real de los comandos y la decisión de aceptar fallos preexistentes corresponden al ejecutor/humano. Si una API discrepa, la nota a sldb y la aceptación parcial las decide un humano; otro nodo puede aportar el grafo o el formato del recibo.
