## REFORMULACION

**Propósito:** corregir tres defectos de deskops: (a) `closeout verify` escribe recibos pese a su ayuda; (b) `closeout commit --reason` con llaves imprime error tras commitear y deja proyección sin commitear; (c) `edit task` y `message send` fallan con `TemplateSyntaxError` ante `{{`.

**Resultado:** recibo de reproducción de los tres casos; (a) y (b) con test verde; (c) con test verde o `xfail(strict=True)` y nota a sldb si el traceback apunta a ese paquete.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`; superficie: `services/closure.py`, `cli/commands/closeout.py`, `tests/test_closeout.py`, `tests/test_message_cli.py`.

**Límites:** no modificar sldb; no ampliar a otros comandos ni caminos.

## AMBIGUEDADES

1. «se manda deskops message send --to sldb con la reproduccion minima»: no define asunto, cuerpo ni cómo adjuntar logs; obligaría a inventar el formato del mensaje.
2. «cuyo reason es el nombre de archivo que imprime message send»: no identifica qué archivo ni en qué salida aparece; obligaría a inventar la referencia.
3. «Hay recibo de reproduccion de los tres casos» frente a «registrar el recibo»: no aclara si es uno global o uno por caso; obligaría a inventar la granularidad.
4. «la proyeccion ... entra en el mismo commit de cierre»: no dice si el commit la añade solo o exige staging explícito; obligaría a inventar el mecanismo.
5. «runs/subagents/repro-llaves-<fecha>/»: no fija formato de fecha ni zona; obligaría a inventar el nombre.
6. «Sandbox con `deskops init`»: no indica ruta, aislamiento ni limpieza; obligaría a inventar la ubicación.

## DRY-RUN

**Lecturas:** TaskDoc, notas de inbox referenciadas, `closure.py:788`, ayuda de `closeout verify`, tests existentes. **Cambios previstos:** impedir escrituras en verify; conservar `--reason` literal y stagear la proyección en el commit; tests nuevos. **Dependencias:** CLI deskops, render de sldb, pytest, `origin/main`. **Validaciones futuras:** los cuatro comandos pytest del apartado Validation y worktree limpio para fallas preexistentes. Todo hipotético, sin ejecutar.

## FUTURO

El equipo de sldb recibe la reproducción y decide si corrige el render; un humano valida el recibo, el `xfail` y las fallas preexistentes del informe.
