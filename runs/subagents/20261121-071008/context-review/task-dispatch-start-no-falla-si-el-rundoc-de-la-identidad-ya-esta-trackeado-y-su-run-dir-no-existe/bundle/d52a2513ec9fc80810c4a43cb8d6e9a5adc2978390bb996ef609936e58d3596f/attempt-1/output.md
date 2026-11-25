## REFORMULACION

Propósito: que `dispatch start` no falle cuando el RunDoc de una identidad ya está trackeado pero su `run_dir` no existe. Resultado: identidad reutilizable sin error (`record_scion_run` no revienta), sin carpetas vacías residuales, y comportamiento intacto cuando el `run_dir` existe. Repo: deskops; superficie: `deskops/dispatch.py` (start y paso `record_scion_run`) o `deskops/runtime/scion.py`, más `tests/test_dispatch.py` y CHANGELOG. Límites: fuera el resto de dispatch. Es tarea ejecutable (`task.code`), no agregado.

## AMBIGUEDADES

1. "lo actualiza o lo re-trackea con force" — dos estrategias sin criterio de elección; obliga a inventar cuál usar (y si difieren en efectos).
2. "deskops/dispatch.py ... o deskops/runtime/scion.py (record_scion_run)" — la "o" no fija capa; obliga a inventar dónde implementar.
3. "p2: implementar con track forzado o update del RunDoc" — repite la disyuntiva sin decisión; obliga a inventar API concreta.
4. "Si un fallo deja una carpeta vacía, se borra" — no dice qué fallos, ni quién limpia (start, scion, cola); obliga a inventar alcance y punto de limpieza.
5. "sigue contando como intento hecho, como hoy" — "como hoy" remite a comportamiento no mostrado; obliga a inventar la semántica de intento.
6. "start lanza (con _scion simulado) y no falla" — "lanza" ambiguo (¿lanza el dispatch, lanza excepción?); obliga a inventar la aserción del test.
7. No se define cómo se construye/identifica `run-<name>` ni el store de prueba; obliga a inventar fixtures.

## DRY-RUN

Lecturas: TaskDoc, `dispatch.py`, `scion.py`, `tests/test_dispatch.py`, CHANGELOG, referencias al store. Cambios previstos: test nuevo que reproduce store con RunDoc trackeado y sin `run_dir`; ajuste en start/`record_scion_run` para actualizar o re-trackear con force y limpiar carpeta vacía; entrada CHANGELOG; commit con `git commit -- <rutas>` y trailer Task-Id. Dependencias: pytest, `_scion` simulado, store temporal. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`, más el test nuevo.

## FUTURO

Un humano debe decidir update vs force, capa de implementación y política de limpieza; otro nodo podría aportar la API real del store y la semántica de intento.
