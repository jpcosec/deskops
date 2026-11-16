## REFORMULACION

**Propósito:** que el closeout reconozca una `MaterializationContractDoc` declarada cuyo `target_identity` es un `.txt` bajo `tests/fixtures` como nodo del grafo y cobertura de ese archivo, sin admitir fixtures no declarados.
**Resultado:** recibo de reproducción; diagnóstico del punto de corte; corrección en deskops (exclusión que no aplique a targets declarados) o nota a sldb y test `xfail`; test de regresión; suite completa con fallas baseline justificadas.
**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.
**Límites:** no modificar sldb; solo `deskops/graph/desk_graph.py` (~83-93), test de regresión y recibo.

## AMBIGUEDADES

1. «MATERIALIZATION_TARGETS, alrededor de 83-93»: no se define qué contiene ni cómo interactúa con EXCLUSIONS; obliga a inventar su semántica y el rango exacto.
2. «si el target declarado aparece como nodo»: no fija comando ni salida observable; obliga a inventar el criterio de comprobación.
3. «un test marcado xfail con el id de esa nota» frente a «xfail(reason='<nombre de archivo de la nota>')»: obliga a inventar si se usa id o nombre de archivo.
4. «los archivos de tests/fixtures no declarados siguen excluidos»: no indica cómo verificarlo; obliga a inventar el aserto o comando.
5. «materialization a tests/fixtures/golden.txt»: no especifica campos mínimos ni formato del documento; obliga a inventar el esquema.
6. «guardar la salida como recibo (`deskops review record ... --evidence <archivo>`)»: no aclara si `<archivo>` es el log o su ruta; obliga a inventar el enlace.

## DRY-RUN

**Lecturas:** TaskDoc; `deskops/graph/desk_graph.py`; `tests/test_desk_graph_runs_target.py`; tests citados en Validation; ruta de sldb solo lectura.
**Cambios previstos:** sandbox con átomo, materialization y edición de `tests/fixtures/golden.txt`; log `runs/subagents/<run>/repro-fixture.log`; comando de reproducción; corrección en `desk_graph.py` más test, o nota a sldb más `xfail`.
**Dependencias:** CLI `deskops`, sandbox desk roots, `.venv`, pytest, comando `deskops message send`.
**Validaciones futuras:** los tres pytest específicos, suite completa, y repetición en worktree limpio de `origin/main` de cada falla.

## FUTURO

Un humano/revisor decide si el corte es deskops o sldb y acepta el recibo; el equipo sldb implementa si hay nota; otro nodo ejecuta commit/cierre conforme al átomo de tests y commit; la lista de fallas baseline se valida en revisión.
