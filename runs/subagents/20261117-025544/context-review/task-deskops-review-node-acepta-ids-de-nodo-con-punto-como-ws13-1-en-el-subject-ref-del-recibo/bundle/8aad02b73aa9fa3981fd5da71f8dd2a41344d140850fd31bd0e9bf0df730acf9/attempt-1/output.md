## REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: que `deskops review node` acepte ids de nodo con punto, como `WS13.1`, en `subject_ref`. Resultado: `SUBJECT_REF_PATTERN` admite punto en el id; un `subject_ref` como `dag.yaml#node:WS13.1` valida y `review node` escribe el recibo; espacio o `#` extra siguen rechazados. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar el patrón en `deskops/models/review.py`, la declaración equivalente del store si existe, y tests en `tests/test_review_doc.py` y `tests/test_review_command.py`; fuera de alcance están el formato de ids de los planes y el formato de `review_id`.

## AMBIGUEDADES

1. “el modelo ReviewDoc del store si declara el mismo patron”: no se nombra archivo ni símbolo del store; obligaría a inventar dónde buscar o si existe duplicado.
2. “un id con espacio o con '#' sigue rechazado”: “# extra” puede significar un segundo `#`, un `#` dentro del id u otra variante; obligaría a inventar los casos exactos de test.
3. “si el punto choca en el review_id, se informa en el resultado sin cambiar su formato”: no define qué es “el resultado” ni cómo informarlo; obligaría a inventar canal y texto.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, `deskops/models/review.py`, `tests/test_review_doc.py`, `tests/test_review_command.py`, servicio/CLI de review y algún `dag.yaml` de prueba. Cambios previstos: ampliar la clase de caracteres del id de nodo para incluir `.`; replicar en la declaración del store si aparece; agregar tests de modelo válido y de rechazo con espacio/`#`; agregar test de `review node` en sandbox con nodo punteado y `pi` falso. Dependencias: pydantic, sldb, pytest y el `pi` falso existente; sin red. Validaciones futuras: ejecutar los dos comandos de pytest indicados y confirmar que los casos inválidos siguen fallando. Nada se ejecuta ahora.

## FUTURO

Otro nodo ejecutará cambios, tests y commit descriptivo según el átomo. Un humano decidirá si una colisión de `review_id` requiere política nueva. El resultado conjunto se valida con ambos pytest y revisión del recibo generado en sandbox.
