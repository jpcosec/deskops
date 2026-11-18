## REFORMULACION

**Propósito:** automatizar como trabajo de cola el ritual de integración que hoy hace a mano el integrador (receta `integrate-recipe.md` en `.bootstrap`): copia limpia del repo, gates de memoria, fast-forward, suite completa, verificación de store y grafo, push del commit de código y luego del tip, y actualización del checkout de herramientas.

**Resultado:** comando `deskops integrate --task <id> --root .` (con `--dry-run` y `--task-from-env`), módulo nuevo `deskops/integrate.py`, campo `integrate` en `DeskConfig` (`remote_url`, `branch`, `suite`, `suite_timeout`, `tests_lock`, `tools_checkout`, `push_env`), registro en `cli/registry.py`, tests nuevos y goldens, sección `Integrate` en `docs/operator-manual.md`. Códigos: 0 éxito, 1 fallo de paso (`fallo: <paso>: <detalle>`), 2 precondición incumplida.

**Repo:** workspace desk (`/mnt/ssd/proyectos/SLDB_1/deskops`), checkout principal, sin worktree ni commit; remoto simulado con repo bare en `tmp_path`.

**Límites:** fuera configurar desks reales, timer del host, reintentos/rebase, cambios en sldb; los tests nunca tocan remoto real.

## AMBIGUIDADES

1. "su ultima entrada de history es el registro de cierre" — no define forma/campos del registro; obligaría a inventar el criterio de cierre.
2. "el sha de 40 caracteres que aparece en `references`" — no dice qué hacer si hay varios; obligaría a inventar selección.
3. "reutilizando la funcion que ya los calcula en el modulo de la cola" — no nombra la función; obligaría a adivinarla.
4. "cada ruta `path:` de `.sldb/store.yaml`" — no da la estructura YAML; obligaría a inventar el parser.
5. "la cuenta de faltantes de `deskops graph missing`" — no define formato de salida ni qué se cuenta; obligaría a inventar el parseo.
6. "`<fecha UTC ISO>`" — formato exacto (¿con `Z`? ¿segundos?) no fijado.
7. "con tope `suite_timeout`" — no dice código/mensaje al expirar; obligaría a inventar `fallo: suite` por timeout.
8. "`--task-from-env`" y "`--task`" — no define exclusividad ni precedencia.

## DRY-RUN

Lecturas: `deskops/config.py`, `deskops/queue.py` (gates), `cli/registry.py`, tests guardianes y goldens, `docs/operator-manual.md`, tarea y `.sldb/store.yaml` en el tip. Cambios previstos: módulo `integrate.py`, campo `integrate`, registro CLI, `tests/test_integrate.py`, declaraciones en los tres tests de CLI, goldens de ayuda, manual. Dependencias: tarea de runner de cola (cola operativa), utilidades git y `fcntl`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_integrate.py`, tests guardianes de CLI, `tests/test_queue.py`, regeneración de goldens.

## FUTURO

El runner de host encola y ejecuta `integrate` vía `queue_jobs`; el integrador declara `integrate` en desks reales y decide política de reintentos; un humano valida el manual y los goldens regenerados.
