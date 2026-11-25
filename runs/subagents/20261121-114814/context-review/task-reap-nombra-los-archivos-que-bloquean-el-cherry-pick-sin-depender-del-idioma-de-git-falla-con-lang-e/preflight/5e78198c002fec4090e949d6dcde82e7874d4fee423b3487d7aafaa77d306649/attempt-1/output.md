## REFORMULACION

Propósito: corregir `dispatch reap` para que nombre los archivos locales que bloquean un cherry-pick sin depender del idioma de git, tras el fallo reproducible con locale español. Resultado: mensaje que nombra archivos y sugiere commitearlos, mismo `rc 8`, y tests que pasan con español e inglés. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`; superficies: `deskops/dispatch.py` (reap), `deskops/runtime` si allí se ejecuta git, `tests/test_dispatch.py` y `CHANGELOG`. Límites: fuera “el resto”; el commit se hace desde el worktree provisto por dispatch con trailer `Task-Id`.

## AMBIGUEDADES

1. “o corre los comandos de git cuya salida parsea con `LC_ALL=C` y `LANGUAGE=` en el entorno, o calcula los archivos con `git status --porcelain` y la lista de archivos del commit”. Obliga a inventar cuál de las dos estrategias elegir y con qué criterio.
2. “deskops/runtime si es donde se corre git”. Obliga a inventar si debe modificarse `runtime` o si el cambio queda solo en `dispatch`.
3. “El test pasa con cualquier locale”. Obliga a inventar la matriz de locales; la validación solo enumera `es_ES` y `en_US`.
4. “forzar `LC_ALL=C` en esos subprocess, o reemplazar el parseo por porcelain”. Repite la elección abierta del objetivo y obliga a inventar el alcance del reemplazo.

## DRY-RUN

Lecturas: TaskDoc, implementación de reap en `deskops/dispatch.py`, invocaciones de git en `deskops/runtime`, test de línea 514 y `CHANGELOG`. Cambios previstos: agregar test con `LANG/LC_ALL/LANGUAGE=es`; ajustar los subprocess que parsean salida de git mediante `LC_ALL=C`/`LANGUAGE=` o calcular archivos por porcelain; conservar mensaje y `rc 8`; documentar en `CHANGELOG`; commit con trailer. Dependencias: locales españoles instalados, worktree entregado por dispatch y runner de tests. Validaciones futuras: ejecutar pytest con locale español e inglés, y la suite indicada con `-n 4`. Sin ejecutar nada.

## FUTURO

Dispatch o el entorno debe entregar el worktree; otro nodo o CI ejecutará las suites completas; un humano decidirá la estrategia si se mantiene la ambigüedad; el commit/merge incorporará el cambio con el trailer indicado.
