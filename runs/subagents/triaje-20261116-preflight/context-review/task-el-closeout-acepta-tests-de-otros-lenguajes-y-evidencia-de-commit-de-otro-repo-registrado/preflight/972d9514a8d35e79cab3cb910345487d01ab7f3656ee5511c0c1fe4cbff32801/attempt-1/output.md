## REFORMULACION
Propósito: ampliar las evidencias aceptadas por el closeout y por `resolved-by`. Resultado: aceptar tests de otros lenguajes, `runs/<run>/validation.log` y referencias `repo:<nombre>@<sha>` de repos registrados; documentarlo y cubrirlo con tests. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `closeout_gates.py`, la rama `resolved-by` de `closure.py`, `docs/workflow-policy-reference.md`, `tests/test_closeout_gates.py` y `tests/test_closeout_resolved_by.py`; no cerrar las tareas de scion ni cambiar qué evidencia exige cada tipo.

## AMBIGUEDADES
1. «archivo existente con el comando y su salida»: no define formato ni validación del contenido; obligaría a inventar un parser o criterio de suficiencia.
2. «convencion reconocible (*_test.go, *.test.sh, *.bats)»: no aclara si la lista es cerrada ni dónde debe estar el archivo; obligaría a inventar sufijos admitidos y reglas de ruta.
3. «para artefactos sin framework de tests»: no da criterio para decidir cuándo un artefacto “no tiene framework”; obligaría a inventar esa detección.
4. «nota a scion con el hash»: no especifica canal, formato ni destinatario concreto; obligaría a inventar el mecanismo de notificación.

## DRY-RUN
Lecturas: `closeout_gates.py:140-260`, rama `resolved-by` de `closure.py`, doc de evidencia, tests citados; localizar la función de resolución usada por `message send --to` y el registro de repos. Cambios previstos: tabla de sufijos de test, detección de `validation.log`, resolución `repo:<nombre>@<sha>` mediante `git -C <raíz> merge-base --is-ancestor <sha> HEAD`, misma lógica en `resolved-by`, doc y tests. Dependencias: registro de repos, raíces existentes, git, logs en `runs/` y entorno pytest. Validaciones futuras: los tres pytest indicados y la suite completa con `-n 4`, comparando fallas nuevas contra `main`.

## FUTURO
El ejecutor producirá el hash de su cambio; el coordinador de scion cerrará las tres tareas afectadas; la recepción de la nota y la decisión final de aceptación o merge corresponden a otro nodo o a un humano.
