REFORMULACION
Encargo ejecutable (task.code, no agregado): en /mnt/ssd/proyectos/SLDB_1/deskops, hacer que `deskops review status` marque stale solo si cambió el contrato del TaskDoc (title, goal, scope, implementation_path, files, validation, done_when) o las demás fuentes del bundle, no la cabecera sldb, tags, status, current_node, history ni references. Resultado: `contract_sha256` calculado sobre `__contract__`, guardado en ReviewDoc y comparado en `_state_for_key`; tests que editar tags/status dejan accepted y editar goal deja stale. Límites: no cambiar input.md ni input_sha256 de evidencia; no tocar reglas de activación; recibos viejos conservan comparación actual.

AMBIGUEDADES
1. “el contract_sha256 del TaskDoc que sldb calcula sobre __contract__ … se ubica con grep -rn contract_sha256 deskops ../sldb/src”: asume fuente hermana y digest existente; obliga a inventar algoritmo/ubicación si no aparece.
2. “TaskDoc.__contract__: title, goal, scope, implementation_path, files, validation, done_when”: el TaskDoc y tests aportados no evidencian implementation_path ni done_when; obliga a inventar proyección o mapeo de campos.
3. “el ReviewDoc nuevo guarda ese valor en un campo contract_sha256”: el modelo ReviewDoc no está en `files` (solo review.py y tests); obliga a inventar dónde/diseñar el campo.
4. “la misma agregación que hoy (el recibo vigente más reciente)”: el código actual no usa recencia, sino prioridad accepted/rejected/pending/incomplete sobre todos los recibos actuales; obliga a inventar una regla nueva o contradecir el átomo.
5. “las demás fuentes … siguen entrando al hash como hoy; solo la parte del TaskDoc se reemplaza por su contract_sha256”: no define orden/formato del digest combinado del bundle; obliga a inventar serialización.
6. “su estado coincide con el anchor_state del recibo que evalúa la regla de activación”: no identifica recibo ni cálculo; obliga a inventar equivalencia.

DRY-RUN
Lecturas: review.py:440-520 y 740-800, modelos TaskDoc/ReviewDoc, `grep -rn contract_sha256`, tests. Cambios: helper `contract_digest(task)`; propagar digest a `_state_for_key`/`_status_task`/`_status_plan`; escribir `contract_sha256` en `_write_review`; fallback por input_sha256 para recibos viejos; tests tag/status accepted y goal stale. Dependencias: digest disponible en sldb, esquema ReviewDoc. Validaciones futuras: pytest test_review_command.py, test_review_doc.py y suite completa contra baseline.

FUTURO
sldb debe exponer o confirmar el digest de contrato; el dueño del modelo decide el campo ReviewDoc; un humano valida equivalencia con rule-activation y acepta fallas baseline; el revisor resuelve la ambigüedad 4.
