REFORMULACION
El encargo es ejecutar en robocop2 una verificación de solo lectura sobre seis desks —deskops, sldb, spec2viz, scion, pron y graph_ui— y dejar constancia de resultados. El resultado esperado es una tabla en `docs/config-vs-code.md` y en este TaskDoc con rc y resumen de cinco comandos por desk, suites de deskops y sldb sin fallas nuevas frente a main, y medianas de `deskops view board --root .` en frío y caliente, con caliente < 1 s. El repo principal de trabajo es deskops; sldb y los demás desks son superficies de verificación. Límites: no arreglar desks ajenos, solo reportar por inbox; en deskops, aplicar `desk update --apply` únicamente si el dry-run muestra divergencias y corregir solo fallas causadas por código de deskops, cada arreglo con test y commit propio. No incluye UI en navegador.

AMBIGUEDADES
1. «Bucle por desk con los 5 comandos»: solo se explicita `--root .` para la medición de view board, no cómo invocar los comandos en los otros cinco desks; obligaría a inventar cwd y flags `--root`.
2. «Suite completa de deskops y de sldb con -n 4: sin fallas nuevas contra main»: la validación detalla el worktree base solo para deskops y para sldb únicamente da el comando pytest; obligaría a inventar el baseline de sldb.
3. «El resumen por comando es rc + numero de errores y de alertas»: no define cómo extraer errores/alertas de cada salida; obligaría a inventar un parser o criterio de conteo.
4. «las demas se reportan por inbox al repo dueño» y «deskops message send --to <repo>»: no fija asunto, formato ni destinatario exacto; obligaría a inventar el mensaje.
5. «solo se arreglan en deskops las fallas cuya causa este en codigo de deskops»: la atribución de causa exige juicio no reglado; obligaría a inventar el criterio de atribución.

DRY-RUN
Leería este TaskDoc, `desk/drawer/plans/deskops-como-config/dag.yaml`, `docs/config-vs-code.md`, `tests/` y el estado git de los repos. Previsto: ejecutar los cinco comandos por desk; correr ambas suites; medir view board con borrado de caches y calentamiento; escribir tablas en doc y TaskDoc; abrir commits separados por arreglo; enviar mensajes a desks ajenos. Dependencias: repos montados, venv, CLI deskops/sldb, git worktree y `/usr/bin/time`. Validaciones futuras: rc y resúmenes, suites contra main, medianas y umbral caliente.

FUTURO
Otro nodo o humano decidirá la aceptación de atribuciones, revisará/mergeará commits, y los dueños de desks ajenos decidirán si corrigen sus hallazgos.
