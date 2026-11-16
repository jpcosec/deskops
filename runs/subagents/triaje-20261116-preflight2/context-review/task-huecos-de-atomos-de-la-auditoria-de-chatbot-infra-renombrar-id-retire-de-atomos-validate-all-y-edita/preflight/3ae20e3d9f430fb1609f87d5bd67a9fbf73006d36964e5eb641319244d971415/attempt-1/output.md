## REFORMULACION

Encargo: cerrar cinco huecos (1, 3, 4, 5, 6) detectados en la auditoría de Chatbot_Infra sobre el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Resultado: por hueco, un recibo de reproducción (o constancia de no-reproducción con comando y salida) y, si se reproduce, corrección con test. Superficie: `deskops/services/atoms.py`, `deskops/cli/registry.py`, `deskops/cli/commands/doctor.py`, `tests/test_atom_materialization.py` y tests de doctor. Límites: un sandbox en `/dev/shm` por hueco; fuera de alcance citas código→átomo y repos de AntonIA. Rename y retire tienen contrato fijado en el preflight.

## AMBIGUEDADES

1. "`deskops atoms retire <id> --reason <texto> --root .`" — no se dice dónde persiste ese `--reason` (¿campo del átomo, status, registro aparte?). Obligaría a inventar el esquema.
2. "Cada hueco corregido suma su test en el archivo de tests que corresponda (test_atom_materialization.py para rename y retire, test_doctor*.py para el 6)" — huecos 4 y 5 quedan sin archivo asignado.
3. "validate --all sin falsos positivos" — no define qué cuenta como falso positivo ni umbral aceptable.
4. "copiar un desk con store enlazado a deskops a otra profundidad de directorio" — no fija profundidad ni ruta destino; no especifica el criterio de reproducción.
5. "menciones atom-* en prosa que sldb trate como MentionPattern" — apela a un detalle interno de sldb no listado en `files:` ni en `references:`; obligaría a inspeccionar la dependencia.
6. "Sin verificar: 'atoms validate --all' marca toda la provenance…" — el propio input declara que es hipótesis, no hecho.

## DRY-RUN

Lecturas: taskdoc, `references` (tarea índice de auditoría), `pills`, ficheros listados y dependencia sldb. Cambios previstos: verbo `atoms rename` (transacción, `rewrite_references`, validación `^atom-[a-z0-9-]+$`, error si existe), verbo `atoms retire`, ajuste de `doctor` para resolver store enlazado, tests. Dependencias: API sldb de reescritura de referencias, `deskops init` para sandbox. Validaciones futuras: los cuatro comandos pytest y `pytest -n 4 -q tests` con comparación en worktree limpio.

## FUTURO

Un ejecutor reproduce y registra con `deskops review record`; un humano valida fallas preexistentes y decide ambigüedades 1–5.
