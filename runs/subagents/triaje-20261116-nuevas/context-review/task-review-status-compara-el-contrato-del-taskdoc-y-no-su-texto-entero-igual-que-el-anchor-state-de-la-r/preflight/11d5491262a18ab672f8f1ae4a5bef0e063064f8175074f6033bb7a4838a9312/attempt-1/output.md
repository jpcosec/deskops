REFORMULACION

El encargo es una tarea de código ejecutable, no un agregado ni un paquete no ejecutable. En el repo `deskops` hay que hacer que `deskops review status` marque stale solo cuando cambie el contrato del TaskDoc o alguna fuente del input de revisión, y no cuando cambien cabecera `sldb`, `tags`, `status`, `current_node`, `history` o `references`. El resultado esperado es que `_state_for_key` compare un digest de contrato guardado en el ReviewDoc, con compatibilidad para recibos viejos, y que los tests cubran tags/status vs goal. Límites: tocar `deskops/services/review.py` y `tests/test_review_command.py`; no cambiar `input.md`, el `input_sha256` registrado ni las reglas de activación.

AMBIGUEDADES

1. «el mismo digest que usa deskops para el contrato, si existe: buscar `__contract__` en deskops/»: no se nombra función, algoritmo ni qué hacer si no existe. Obligaría a inventar el helper y su canonización.
2. «si el ReviewDoc no lo guarda, se agrega el campo al escribir el recibo; recibos viejos sin el campo siguen con la comparacion actual»: falta nombre del campo, serialización y detección de recibos viejos. Obligaría a inventar esquema y fallback exacto.
3. «para bundle: pills, atomos, rituales y archivos enlazados»: «archivos enlazados» no distingue `files`, `references` ni contenido. Obligaría a inventar el conjunto y cómo digerirlo.
4. «su estado coincide con el anchor_state del recibo que evalua la regla de activacion»: no define qué recibo si hay varios ni cómo emparejarlo. Obligaría a inventar selección e igualdad.
5. «- {'cd ... tests (suite completa ...)': 'cada test ...'}»: parece un comando con su política como valor, no una lista de comandos. Obligaría a inventar si se ejecuta la suite y luego el baseline.
6. «una tarea con recibos aceptados y tags editados da accepted»: usa plural «recibos» sin decir cuál manda. Obligaría a inventar el criterio de agregación.

DRY-RUN

Lecturas: `review.py:440-520` y `740-800`; búsqueda de `__contract__`; modelo/escritura de ReviewDoc; tests existentes. Cambios previstos: helper de digest de contrato; campo en ReviewDoc; uso en `_state_for_key` con fallback; tests de tags/status y goal. Dependencias: parser del TaskDoc, persistencia del ReviewDoc, utilidad de digest existente. Validaciones futuras: `pytest tests/test_review_command.py`, `tests/test_review_doc.py`, suite completa y baseline en worktree limpio para fallas. Sin ejecutar nada.

FUTURO

Otro nodo implementará y ejecutará pruebas; un humano decidirá si no existe digest compartido, el nombre/campo del ReviewDoc y la política de recibos viejos; el revisor comprobará el Done When.
