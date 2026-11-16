## REFORMULACION

Encargo de código en el repo `deskops`. **Propósito:** eliminar el `--harness-auth api-key` fijo que hoy escriben `scion_start_argv` y el `agents.md` del coordinador, porque impide arrancar hijos con suscripción (`CLAUDE_CODE_OAUTH_TOKEN`) y bloquea la fase 1 del piloto scion.

**Resultado:** que `scion_start_argv` reciba `harness_auth`, lo valide contra `HARNESS_AUTH_TYPES` y, sin valor, use `oauth-token` (mismo default que `deskops runtime template` para claude). Que `_render_coordinator_agents_md` escriba el auth resuelto del template del coordinador en los dos `scion start` (executor y tester): `--harness-auth` si se pasó; si no, el default del harness.

**Superficie:** `deskops/runtime/scion.py` (`scion_start_argv`, `scion_template_files`, `_render_coordinator_agents_md`) y `tests/test_scion_runtime.py`.

**Límites:** no tocar `RuntimeProfileDoc`, ni el CLI (`--harness-auth` ya existe), ni otros `agents.md`.

## AMBIGUEDADES

1. "el auth resuelto del template del coordinador (--harness-auth si se pasó; si no, el default del harness, oauth-token)". No queda claro si el valor sale del template persistido o del flag CLI, ni la precedencia entre ambos; obligaría a inventar el orden de resolución.
2. "validado contra HARNESS_AUTH_TYPES". El input no enumera los valores válidos ni dónde vive esa constante; obligaría a inventar el conjunto y su import.
3. "tests reales sin mocks en tests/test_scion_runtime.py en verde". No especifica si hay que reescribir tests existentes con mocks o solo añadir nuevos; obligaría a inventar el alcance de la refactorización de tests.
4. "el mismo default que 'deskops runtime template' para claude (HARNESS_AUTH)". Solo cubre claude; para otros harnesses el default podría diferir y el input no lo dice.
5. El Scope nombra `_render_coordinator_agents_md` pero no aclara si esa función renderiza ambos `agents.md` (executor y tester) o solo uno; obligaría a inventar el mapeo.

## DRY-RUN

**Lecturas:** el TaskDoc, `deskops/runtime/scion.py` (`scion_start_argv`, `scion_template_files`, `_render_coordinator_agents_md`), definición de `HARNESS_AUTH`/`HARNESS_AUTH_TYPES`, y `tests/test_scion_runtime.py`.

**Cambios previstos:** añadir parámetro opcional `harness_auth` a `scion_start_argv` con validación y default `oauth-token`; propagar el auth resuelto a `scion_template_files` y a los dos `scion start` del coordinador; ajustar/añadir tests.

**Dependencias:** constante `HARNESS_AUTH_TYPES`, default `HARNESS_AUTH`, y el paso del flag CLI ya existente.

**Validaciones futuras (sin ejecutar):** `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py`; `grep -n 'harness-auth api-key' deskops/runtime/scion.py` vacío.

## FUTURO

Un humano debe resolver las ambigüedades 1–5 antes de ejecutar. Otro nodo podría añadir el campo de auth a `RuntimeProfileDoc` (fuera de alcance aquí). La fase 1 del piloto scion valida el resultado conjunto tras el merge.
