## REFORMULACION

Propósito: actualizar la documentación ritual para que refleje el flujo vigente de revisión y el gate de activación. Resultado: `desk/rituals/context-review.md` describe la revisión como `deskops review preflight` y `deskops review bundle` (con `--engine <perfil>` y default `runtime-pi-deepseek-flash`), su recibo en `desk/reviews/<tarea>/` y su cierre con `deskops review dispose`; `desk/rituals/phase.md` nombra `rule-activation-<tipo>` como gate de paso a ejecución. Ninguno instruye `pi` manual. Repo: proyecto `deskops` (`/mnt/ssd/proyectos/SLDB_1/deskops`). Límites: solo esos dos rituales, editados con `deskops edit ritual`, nunca a mano; fuera otros rituales, reglas de `desk/lifecycle`, `docs/` y el plan `gates-por-tipo`.

## AMBIGUEDADES

1. «Los rituales se cambian con deskops edit ritual <id> <campo> <valor> --root .»: no se especifica el nombre del campo ni cómo representar la lista completa de pasos; obligaría a inventar la interfaz exacta de edición.
2. «tomando la redacción de docs/operator-manual.md sobre deskops review»: ese documento no está en el bundle; obligaría a inventar la redacción de referencia.
3. «su recibo en desk/reviews/<tarea>/»: no se define nombre de archivo, formato ni contenido del recibo; obligaría a inventarlos.
4. «la regla rule-activation-<tipo> como el gate que deja pasar una tarea a ejecución»: no se indica si sustituye un paso existente de `phase`, se añade uno nuevo o modifica el precondicionado; obligaría a inventar la posición y redacción.
5. «deskops doctor --root . (sin hallazgos nuevos sobre rituales)»: no se aporta la línea base de hallazgos; obligaría a inventar el criterio de comparación.
6. «sin 'pi --provider' ni 'preflight.md' como instruccion»: no aclara si pueden permanecer menciones históricas o explicativas; obligaría a inventar el criterio textual de aceptación.

## DRY-RUN

Lecturas: `deskops show ritual context-review --root .` y `deskops show ritual phase --root .`; `docs/operator-manual.md` (no suministrado). Cambios previstos: reescribir los pasos de `context-review` que citan `pi --provider` y `preflight.md`; ajustar el gate de `phase` para nombrar `rule-activation-<tipo>`. Dependencias: CLI `deskops edit ritual`, perfil default `runtime-pi-deepseek-flash`, convención `rule-activation-<tipo>`, redacción de `docs/operator-manual.md`. Validaciones futuras: `deskops show ritual context-review` sin las cadenas prohibidas, `deskops doctor` sin hallazgos nuevos y `pytest tests/test_skill_cli_drift.py`; cierre con tests y commit según el átomo.

## FUTURO

El retiro del plan `gates-por-tipo` corresponde a otro nodo o a un humano. La aceptación final del cambio y el commit descriptivo quedan a cargo del ejecutor y del coordinador; el Board enruta el bundle y decide la prioridad.
