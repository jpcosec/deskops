## REFORMULACION

Encargo: modificar `deskops` para que la evidencia de commit con formato `<repo-id>:<sha>` resuelva `<repo-id>` primero en el registro del desk y, si no aparece, mediante `find_registered_desk` de `deskops/identity.py`; el `<sha>` debe existir y ser ancestro del HEAD de ese repo. Aplica a `closeout verify` (`RepositoryReferences` en `closeout_gates.py`) y a `closeout resolved-by --ref` (`closure.py`). Si el repo-id no resuelve, es ambiguo o el sha no existe, la referencia no cuenta y no se lanza excepción. Resultado: código, tests en los dos archivos indicados, sección documental en `docs/workflow-policy-reference.md` y nota a scion con el hash. Límites: no tocar el gate de tests, no cambiar qué evidencia exige cada tipo, no cerrar la tarea de scion. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Tests del registro del ecosistema deben usar un registro sandbox, nunca `~/setup/desk/registry`.

## AMBIGUEDADES

1. «la variable o fixture que ya usa find_registered_desk»: no nombra variable ni fixture; obligaría a inventar el mecanismo exacto de aislamiento del registro en tests.
2. «el registro del desk»: no define la ruta ni si es el desk actual, el del proyecto o el del cwd; obligaría a inventar la fuente de resolución primaria.
3. «<sha> es un commit alcanzable en ese repo (rev-parse --verify y ancestro de su HEAD)»: no aclara si «alcanzable» incluye solo ancestros de HEAD o cualquier objeto resoluble; obligaría a inventar el criterio exacto de validación.
4. «la seccion de evidencia de commit en docs/workflow-policy-reference.md»: no identifica encabezado ni contenido previo; obligaría a inventar dónde insertar y con qué redacción.
5. «Nota a scion con el hash del commit»: no define asunto, cuerpo ni confirmación de entrega; obligaría a inventar el formato del mensaje.

## DRY-RUN

Lecturas: `closeout_gates.py` (`RepositoryReferences`, `reference_points_to_commit`), `closure.py` (rama `resolved-by --ref`), `identity.py` (`find_registered_desk`), docs y tests citados. Cambios previstos: función de resolución compartida o duplicada en ambos puntos, manejo silencioso de fallos, tests de los cuatro casos, párrafo documental y mensaje a scion. Dependencias: `find_registered_desk`, repositorios registrados accesibles y git disponible. Validaciones futuras: dos pytest específicos, suite completa con `-n 4`, comparación de fallas en worktree limpio de `origin/main`, revisión de doc y envío de nota. Sin ejecución.

## FUTURO

Otro nodo o un humano deberá decidir la ruta y formato exactos del registro del desk, el aislamiento concreto del registro sandbox en tests, la redacción final de la documentación y la aceptación de fallas preexistentes. El cierre de la tarea de scion queda fuera.
