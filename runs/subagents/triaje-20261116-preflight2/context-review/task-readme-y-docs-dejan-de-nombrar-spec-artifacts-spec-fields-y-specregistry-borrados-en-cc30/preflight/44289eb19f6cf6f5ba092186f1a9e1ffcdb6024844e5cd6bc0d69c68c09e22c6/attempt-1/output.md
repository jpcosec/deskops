## REFORMULACION

Encargo: en `/mnt/ssd/proyectos/SLDB_1/deskops`, actualizar `README.md` y `docs/` para que dejen de nombrar `spec/artifacts`, `spec/fields` y `SpecRegistry`, borrados en CC30 (squash `93cc1943`). Resultado esperado: cada mención remite a los atributos de clase de los modelos en `deskops/models`, a `deskops/doc_access.py`, o se borra la frase remitiendo a `deskops/models`; el `.mmd` se edita junto con su `.md`. Límites: solo `README.md` y `docs/`; no reescribir diagramas ni migrar a specir; validación con grep vacío y `test_operator_manual.py`.

## AMBIGUEDADES

1. "3) Volver a correr el grep y los tests de docs." — Validation solo lista `test_operator_manual.py`; obliga a inventar qué son "los tests de docs".
2. "si habla de SpecRegistry o del loader -> se borra la frase y se remite a deskops/models" — no fija qué frase ni redacción; obliga a inventar el texto exacto.
3. "si habla de cargar o resolver artefactos -> deskops/doc_access.py" — no nombra funciones ni símbolos; obliga a inventar el API a citar.
4. "CC30 ... borro ... deskops/specs/loader.py y deskops/specs/mermaid.py" frente al grep, que solo cubre tres patrones; obliga a decidir si esas menciones también se eliminan.
5. "el commit lo dice" — no define si el nodo ejecuta commit ni su formato; obliga a inventar la convención.
6. "README.md:90, ...:63 y su .mmd:29" — las líneas pueden desplazarse; no hay criterio de verificación por línea.

## DRY-RUN

Lecturas: los cuatro archivos listados, grep inicial y consulta de `deskops/models` y `deskops/doc_access.py` para mapear cada mención. Cambios previstos: reescribir o borrar frases según el mapeo indicado y editar `.mmd` y `.md` en el mismo cambio. Dependencias: atributos de clase reales en `deskops/models` y funciones existentes en `deskops/doc_access.py`. Validaciones futuras: grep sin coincidencias y `pytest -q tests/test_operator_manual.py`. Nada ejecutado.

## FUTURO

Decisión humana: aclarar "tests de docs", alcance sobre `loader.py`/`mermaid.py` y convención de commit. Otro nodo: ejecución real de ediciones, grep y pytest.
