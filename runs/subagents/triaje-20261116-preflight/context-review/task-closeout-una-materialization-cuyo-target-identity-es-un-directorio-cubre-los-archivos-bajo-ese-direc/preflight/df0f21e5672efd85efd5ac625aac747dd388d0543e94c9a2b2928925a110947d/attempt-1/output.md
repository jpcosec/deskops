## REFORMULACION

El nodo es una tarea ejecutable (`task.code`) de deskops. Propósito: que la compuerta de cierre considere cubierto un archivo cambiado cuando alguna materialization de la tarea declare como `target_identity` ese archivo o un directorio que lo contenga. Resultado esperado: una función `covers(target, path)` por prefijo de ruta normalizada, usada en la cobertura de `deskops/services/closure.py`, más tests; si `deskops graph missing` sigue reportando `missing_declared_target` para un directorio, enviar una nota a sldb sin esperar respuesta. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `closure.py` y tests; no modificar sldb ni la compuerta de átomos.

## AMBIGUEDADES

1. «alrededor de 1325-1340»: no fija la función exacta ni el rango vigente; obligaría a inventar el punto de inserción.
2. «comparacion por prefijo de ruta normalizada, con separador»: no define normalización (relativa/absoluta, `..`, symlinks, mayúsculas, barra final); obligaría a inventar reglas.
3. «el mismo archivo o un directorio que lo contiene»: no aclara cómo distinguir archivo de directorio ni si el directorio debe existir; obligaría a inventar esa semántica.
4. «se manda una nota a sldb pidiendo que declared_target_nodes acepte directorios»: no fija formato, contenido ni confirmación; solo aparece `deskops message send --to sldb`; obligaría a inventar el texto y el criterio de éxito.
5. «sin fallas nuevas respecto de main»: no define la referencia `main` ni cómo comparar; obligaría a inventar el baseline.

## DRY-RUN

Un ejecutor futuro leería `deskops/services/closure.py` en la zona indicada, `tests/test_materialization_targets_outside_package.py`, `tests/test_closeout_gates.py` y `tests/test_closeout.py`. Previsto: añadir `covers(target, path)` con comparación normalizada y separador; usarla en la cobertura; agregar el caso `pkg/sub` cubre `pkg/sub/a.py` y no `pkg/subzero.py`; ejecutar un desk sandbox con target directorio mediante `graph missing`; si falla, enviar nota a sldb. Dependencias: repo deskops, entorno `.venv`, sandbox de desk y mecanismo de mensajes. Validaciones futuras: los cuatro comandos pytest indicados, incluida la suite completa con `-n 4`.

## FUTURO

Otro nodo o un humano decidirá si sldb acepta directorios en `declared_target_nodes`; esta tarea no espera esa respuesta. También corresponderá al cierre verificar la nota citada en el commit y confirmar que no hay fallas nuevas frente a `main`.
