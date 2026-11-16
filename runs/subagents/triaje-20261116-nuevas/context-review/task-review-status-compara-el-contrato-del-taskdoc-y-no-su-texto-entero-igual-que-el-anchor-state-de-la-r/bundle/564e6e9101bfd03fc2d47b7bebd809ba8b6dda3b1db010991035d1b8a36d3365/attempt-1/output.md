REFORMULACION
Encargo ejecutable, no agregado: modificar `deskops review status` para que un TaskDoc solo quede `stale` cuando cambie su contrato (`TaskDoc.__contract__`: title, goal, scope, implementation_path, files, validation, done_when) o las demás fuentes del input de revisión; no por `sldb.at`, tags, status, current_node, history ni references. Resultado: preflight/bundle alineados con el `anchor_state` de la regla de activación, con tests. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no cambia `input.md`, el `input_sha256` registrado ni las reglas de activación.

AMBIGUEDADES
1. “el mismo digest que usa deskops para el contrato, si existe: buscar __contract__ en deskops/”: no fija algoritmo ni canonicalización si no existe; obligaría a inventar serialización, orden y normalización.
2. “recibos viejos sin el campo siguen con la comparacion actual”: no aclara si “actual” es el SHA del input entero ni cómo convive con el digest nuevo; obligaría a inventar el fallback y la transición.
3. “Para un TaskDoc, su estado coincide con el anchor_state del recibo que evalua la regla de activacion”: no identifica el recibo concreto ni si debe reutilizarse esa lógica; obligaría a inventar el mapeo.

DRY-RUN
Lecturas: `deskops/services/review.py` líneas 440-520 y 740-800; búsqueda de `__contract__`; `tests/test_review_command.py`; modelo `ReviewDoc`. Cambios previstos: helper de digest canónico del contrato; persistir ese digest al escribir el recibo si falta; `_state_for_key` compara digest guardado contra actual para claves de TaskDoc, manteniendo el SHA de evidencia. Tests: editar tags/status tras recibo aceptado deja `accepted`; editar goal deja `stale`. Dependencias: posible campo nuevo en `ReviewDoc`, sin tocar evidencia. Validaciones futuras: pytest de `test_review_command.py`, `test_review_doc.py` y suite completa; fallas nuevas contra worktree limpio de `origin/main`.

FUTURO
La suite y el worktree limpio producen evidencia de fallas; un humano decide la disposición del review y la aceptación del commit. Otro nodo puede ajustar el modelo `ReviewDoc` si el campo nuevo requiere migración.
