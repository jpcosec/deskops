## REFORMULACION

**Propósito:** corregir en deskops que `deskops view task <tarea> --format json` / `show_task` entregue `holds: true` en el gate `task_activates -> ritual-testing` aunque su regla de activación (`rules/rule-activation-task-code`) emita un finding `level: error` con `seen` vacío.  
**Resultado:** reproducir el caso, localizar por qué holds y findings no coinciden, hacer que holds sea `false` ante un finding de error y añadir un test que falle antes y pase después; si la causa está en sldb, rutearla con reproducción mínima y dejar un `xfail strict`.  
**Repo:** deskops.  
**Límites:** entra el cálculo de holds/findings de los gates de `show_task` y `view task`, más tests; sale la UI de graph_ui y el texto de los findings.

## AMBIGUEDADES

1. “Si la causa esta en sldb … se manda deskops message send --to sldb con la reproduccion minima y en deskops queda un test xfail strict con esa nota como reason.” No define criterio para atribuir la causa a sldb, formato del mensaje ni contenido exacto de `reason`; obligaría a inventar el protocolo de ruteo.
2. “Registrar la reproduccion con deskops review record <tarea> --kind reproduction.” No indica evidencia, argumentos ni formato esperado; obligaría a inventar qué adjuntar.
3. “task.code sin recibos de preflight” no fija fixture, desk sandbox ni datos mínimos; obligaría a inventar el escenario reproducible.
4. “hacer que coincidan” no declara si `holds` se deriva de los findings o se corrigen ambos; obligaría a decidir la fuente de verdad.
5. “tests/test_view.py” frente al átomo “sandbox desk roots” no aclara si el nuevo test debe usar obligatoriamente `tmp_path`/sandbox; obligaría a elegir.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, sugerencia en inbox, `deskops/cli/commands/view.py`, `tests/test_view.py` y servicios/lifecycle que alimentan `_gates`. Cambios previstos: reproducir en sandbox, registrar reproducción, trazar `show_task` y origen de findings, unificar el criterio holds/error, añadir test de regresión y, si aplica, `xfail strict`. Dependencias: repo deskops, venv, pytest, sandbox de desk y herramienta de mensaje a sldb si se rutea. Validaciones futuras: ejecutar el pytest indicado y comprobar el JSON con holds `false` y sin contradicción con findings de error.

## FUTURO

Un nodo ejecutor implementará el cambio y aportará test/commit; el ritual o un humano aprobará el draft y aceptará el `review record`; sldb decidirá si recibe el ruteo; la validación/CI confirmará el resultado conjunto.
