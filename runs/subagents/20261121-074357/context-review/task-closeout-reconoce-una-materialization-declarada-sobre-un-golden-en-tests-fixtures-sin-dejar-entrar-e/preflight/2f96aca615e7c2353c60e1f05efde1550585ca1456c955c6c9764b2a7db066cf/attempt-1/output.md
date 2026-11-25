## REFORMULACION

Encargo ejecutable (task.debug) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: que `closeout` reconozca una `MaterializationContractDoc` cuyo `target_identity` es un `.txt` bajo `tests/fixtures` como nodo del grafo y cobertura válida, sin dejar de excluir los archivos de fixtures no declarados. Resultado: recibo de reproducción registrado, corrección en `deskops/graph/desk_graph.py` (EXCLUSIONS / MATERIALIZATION_TARGETS) o, si el corte está en sldb, nota vía `deskops message send --to sldb` más test `xfail` citando esa nota; test de regresión en `tests/test_desk_graph_runs_target.py`. Límites: no modificar sldb; alcance acotado a `desk_graph.py`, el test y el recibo.

## AMBIGUEDADES

1. "un golden genuino bajo tests/fixtures respaldado por un atomo" — no se define qué vínculo exacto lo respalda; obligaría a inventar el formato de esa relación.
2. "MATERIALIZATION_TARGETS, alrededor de 83-93" — no se dice qué cambio se espera ahí; obligaría a inferir si hay que ampliar esa lista.
3. "Desk sandbox con un atomo, una materialization..." — no se especifica cómo se crea el sandbox ni sus rutas; obligaría a inventar el procedimiento.
4. "correr `deskops graph missing` y `deskops closeout verify`" — sin argumentos ni flags; obligaría a inventar la invocación.
5. "xfail(reason='<nombre de archivo de la nota>')" — el nombre sólo existe tras el envío a sldb; obligaría a inventarlo antes.

## DRY-RUN

Lecturas: `deskops/graph/desk_graph.py` (~83-93), `tests/test_desk_graph_runs_target.py`, `tests/test_materialization_targets_outside_package.py`, `tests/test_graph_declared_edges.py`, y en sólo lectura `sldb .../declared_target_nodes.py:55`. Cambios previstos: montar sandbox con átomo, materialization a `tests/fixtures/golden.txt` y cambio en ese archivo; ejecutar los dos comandos y volcar comando+salida en `runs/subagents/<run>/repro-fixture.log`; registrar recibo con `deskops review record ... --kind reproduction --reason 'reproducido: ...'`; quitar `tests/fixtures` de EXCLUSIONS en el sandbox como criterio de corte; aplicar la corrección en deskops o emitir nota a sldb; añadir test de regresión (o xfail). Dependencias: CLI deskops, `.venv`, respuesta de sldb si el corte es suyo. Validaciones futuras: los cuatro comandos pytest listados, incluida la suite completa con comparación en worktree limpio de `origin/main`.

## FUTURO

sldb produce el nombre de archivo de la nota (si el corte es suyo); un humano valida el recibo de reproducción y la lista de fallas preexistentes del informe; otro nodo ejecuta la suite completa y el cierre.
