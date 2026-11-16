REFORMULACION

Propósito: corregir el piloto scion para que el coordinador no lance hijos con `--harness-auth api-key` fijo, sino con el auth derivado del template/harness.

Resultado: `scion_start_argv(..., harness_auth='oauth-token')` valida contra `HARNESS_AUTH_TYPES`, usa `DEFAULT_HARNESS_AUTH` y con `None` omite `--harness-auth`; `scion_template_files` calcula `child_auth` por precedencia; `_render_coordinator_agents_md` escribe ese valor en los dos ejemplos `scion start`; se ajustan dos tests y se agrega uno.

Repo: deskops. Superficie: `deskops/runtime/scion.py` y `tests/test_scion_runtime.py`.

Límites: sin cambios en `RuntimeProfileDoc`, CLI ni otros `agents.md`; no se lee template persistido. El nodo es una tarea de implementación ejecutable por un futuro ejecutor, no un agregado.

AMBIGUEDADES

1. `"harness_auth=None omite --harness-auth"` frente a `"recibe child_auth y escribe '--harness-auth <child_auth>' en ambos"`: no queda claro si `None` también aplica al `child_auth` del coordinador. Obligaría a inventar si debe omitirse o renderizar `None`.

2. `"grep -n 'harness-auth api-key' deskops/runtime/scion.py da vacío"` frente a `"salvo que se pida api-key explícitamente"`: no se sabe si prohíbe toda aparición literal o solo el default generado. Obligaría a inventar cómo representar el caso explícito sin ese texto.

3. `"HARNESS_AUTH.get(harness)"` y `"DEFAULT_HARNESS_AUTH = HARNESS_AUTH['claude']"`: el input no define `HARNESS_AUTH` ni sus claves. Obligaría a inventar su forma si no existe ya.

4. `"se agrega uno nuevo"`: no se especifica nombre ni casos exactos del test nuevo. Obligaría a inventar sus aserciones.

DRY-RUN

Lecturas: TaskDoc, `deskops/runtime/scion.py`, `tests/test_scion_runtime.py` y constantes existentes; sin ejecutar.

Cambios previstos: ajustar firma/validación/default de `scion_start_argv`; calcular `child_auth` en `scion_template_files`; pasar `child_auth` al render del coordinador; actualizar los dos tests citados y añadir uno.

Dependencias: existencia de `HARNESS_AUTH_TYPES` y `HARNESS_AUTH`; flag CLI ya existente; `tmp_path` para tests sin mocks.

Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py`; grep indicado; casos `sin flag`, `api-key`, `auth-file` y `harness_auth=None`. No se ejecuta nada.

FUTURO

Un ejecutor implementa y valida; un humano o nodo revisor resuelve las ambigüedades; el Board/ritual cierra la tarea.
