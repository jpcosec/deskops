## REFORMULACION

Propósito: que `dispatch start` no falle cuando el RunDoc de una identidad ya está trackeado pero su `run_dir` no existe. Resultado: `start` detecta el RunDoc trackeado antes de reutilizar la identidad, lo actualiza o re-trackea con force para el run nuevo, continúa sin error y limpia carpetas vacías dejadas por un fallo; un RunDoc con `run_dir` presente sigue contando como intento hecho. Repo/superficie: `deskops/dispatch.py` (`start` y paso `record_scion_run`) o `deskops/runtime/scion.py`, más `tests/test_dispatch.py` y `CHANGELOG`. Límite: fuera de alcance el resto de dispatch. Validación: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`. Es un TaskDoc ejecutable (`task_type: task.code`), no un agregado.

## AMBIGUEDADES

1. "lo actualiza o lo re-trackea con force" — no dice qué API/método ni cuál de las dos ramas elegir; obligaría a inventar el comportamiento exacto y el manejo de `force`.
2. "o deskops/runtime/scion.py (record_scion_run)" — ofrece dos localizaciones alternativas; obligaría a elegir el punto de cambio sin criterio.
3. "Si un fallo deja una carpeta vacía, se borra" — no especifica qué carpeta, quién la borra ni en qué ruta del flujo; obligaría a inventar la política de limpieza.
4. "con `_scion` simulado" — no define la interfaz del doble ni qué simula exactamente; obligaría a inventar el mock.
5. "lanza" en p1: "start lanza (con _scion simulado) y no falla" — redacción contradictoria; obligaría a inventar qué excepción se espera antes del fix.

## DRY-RUN

Lecturas: TaskDoc, `deskops/dispatch.py` (`start`, `record_scion_run`), `deskops/runtime/scion.py`, `tests/test_dispatch.py`, `CHANGELOG`. Cambios previstos: p1 test reproducible del store con RunDoc trackeado sin `run_dir`; p2 lógica de update/re-track forced; p3 entrada CHANGELOG y commit con `git commit -- <rutas>` y trailer Task-Id. Dependencias: API de tracking/force del store y doble de `_scion`. Validaciones futuras: el pytest indicado; limpieza de carpeta vacía no cubierta por el comando.

## FUTURO

Un humano decide entre las dos ramas de actualización y la ubicación del cambio; otro nodo aporta el contrato del store y de `_scion`; la limpieza de carpetas vacías queda a criterio del revisor.
