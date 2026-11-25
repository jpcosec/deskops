## REFORMULACION

Encargo ejecutable de código (`task.code`) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: eliminar el límite artificial de un solo agente por proyecto scion en `dispatch start`. Resultado: `start` lanzará agentes en paralelo si la memoria supera el gate de cola y si esa misma tarea no tiene ya un agente running; en caso contrario saldrá con `EXIT_BUSY` (3) y motivo. Incluye tests primero, cambio en `deskops/dispatch.py`, documentación, CHANGELOG y commit con rutas y Task-Id. Límites: no añadir tope configurable de agentes; no modificar `queue.py` salvo importar `wait_reason`; no tocar scion ni los `config.json`; validar con `tests/test_dispatch.py`.

## AMBIGUEDADES

1. “imprime el motivo ('ocupado: memoria ...' o 'ocupado: la tarea ya tiene agente <nombre>')”: el texto exacto tras `memoria ...` y el formato de `<nombre>` no están definidos; obligaría a inventar el mensaje y su estabilidad para tests.
2. “por el prefijo de identidad de scion_child_identity de esa tarea”: no se especifica cómo se construye o compara ese prefijo; obligaría a inventar la regla de pertenencia agente-tarea.
3. “reusando wait_reason”: no se detalla su firma, valores de retorno ni cómo separar motivo de memoria y disponibilidad; obligaría a inventar la interfaz de integración.
4. “commit con rutas nombradas y Task-Id”: no se indica de dónde tomar el Task-Id ni el formato del mensaje; obligaría a inventar convención de commit.

## DRY-RUN

Lecturas previstas: TaskDoc, `deskops/dispatch.py:144-147`, `deskops/queue.py` (`wait_reason`, parámetros `queue_min_available_gb`, `queue_max_psi_avg60`), `tests/test_dispatch.py`, `docs/operator-manual.md` y `CHANGELOG`. Cambios previstos: añadir tests fallidos con `_list_agents` y memoria simuladas; sustituir el bucle “cualquier agente running” por gate de memoria y comprobación de agente de la misma tarea; emitir `EXIT_BUSY` con motivo; actualizar docs/CHANGELOG; commit. Dependencias: `_list_agents`, identidad `scion_child_identity`, `wait_reason`, pytest. Validación futura: ejecutar `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`; después, suite completa por integrate. No se ejecuta nada.

## FUTURO

Otro nodo `integrate` ejecutará la suite completa; un humano o el flujo de revisión aceptará el commit y el comportamiento paralelo.
