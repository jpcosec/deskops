## REFORMULACION

Encargo ejecutable (`task.code`, no agregado): en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, sustituir tres rodeos propios por APIs públicas ya integradas de sldb (`/mnt/ssd/herramientas/sldb`), sin cambiar comportamiento observable. Resultado: (a) `services/references.py` sin `_rewrite_mentions`/`_in_frontmatter`, usando `sldb.api.rewrite_references(..., graph=g, excluded_sources=[...])` y `referrers(..., graph=g)`; (b) `doc_access.py::template_placeholders` usando `sldb.api.template_anchors`, eliminando `TemplateExtractor` si queda huérfano; (c) `services/closure.py` creando recibos de evidencia con un solo `create` pinneado. Límites: no modificar sldb; si una API no cumple la nota, detener esa parte y avisar por inbox, continuando las demás; los tests existentes deben pasar sin tocar aserciones.

## AMBIGUEDADES

1. «deja el rodeo de create + update sin cambios en la misma transaccion y crea el recibo con un solo create»: se contradice («sin cambios» vs «un solo create»). Obliga a inventar si el requisito es preservar el patrón o eliminarlo.
2. «los tests que cubren esos caminos» entran en Scope, pero «sin tocar sus aserciones»: obliga a inventar si se permite editar tests (imports, mocks) sin cambiar aserciones.
3. «graph=g»: `g` no se define; obliga a inventar cómo construir/inyectar el grafo.
4. «excluded_sources=[...]»: contenido no especificado; obliga a inventar qué fuentes excluir.
5. «anchor_state intact»: no se define el valor esperado; obliga a inventar la comprobación.
6. «se deja nota a sldb por inbox»: no se indica ruta/formato del inbox ni quién lo cursa.
7. «cada falla se corre igual en un worktree limpio de origin/main»: no se define worktree, rama base ni criterio de comparación exacta.

## DRY-RUN

Lecturas: los tres módulos, tests citados, firmas vía `inspect.signature`, y `tests/api/test_doc_anchors.py` de sldb como referencia. Cambios previstos: reemplazos en `references.py`, `doc_access.py`, `closure.py`; posible retirada de imports. Dependencias: versión instalada de sldb, objeto grafo, semántica transaccional de `create`. Validaciones futuras: los cuatro pytest indicados, el `grep` sin resultados, suite completa `-n 4` y re-ejecución de fallas en worktree limpio. Sin ejecutar nada.

## FUTURO

Deciden otros: aprobación del draft y del alcance; resolución humana de las ambigüedades 1–7; eventual nota a sldb si una API discrepa; aceptación de fallas preexistentes listadas; y el merge/cierre del nodo.
