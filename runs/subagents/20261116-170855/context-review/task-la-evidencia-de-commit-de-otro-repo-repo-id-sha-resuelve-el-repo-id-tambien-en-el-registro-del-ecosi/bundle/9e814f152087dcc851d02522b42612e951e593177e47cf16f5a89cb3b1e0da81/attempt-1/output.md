## REFORMULACION

Propósito: que en deskops una evidencia de commit cualificada `<repo-id>:<sha>` resuelva el `repo-id` primero en el registro del desk y, si no está, con `find_registered_desk` de `deskops/identity.py` (registro del ecosistema), tanto en `closeout verify` como en `closeout resolved-by --ref`. El `sha` debe ser commit alcanzable (`rev-parse --verify` y ancestro de `HEAD`); si el repo-id no resuelve, es ambiguo o el sha no existe, la referencia no cuenta y no hay excepción.

Resultado: cambios en `deskops/services/closeout_gates.py` (`RepositoryReferences` y su uso), `deskops/services/closure.py` (rama resolved-by), doc en `docs/workflow-policy-reference.md` y tests en `tests/test_closeout_gates.py` y `tests/test_closeout_resolved_by.py`.

Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`.

Límites: no entra el gate de tests, no cambia qué evidencia exige cada tipo, no cierra la tarea de scion. En tests el registro del ecosistema es sandbox (`tmp_path` y la variable/fixture que ya usa `find_registered_desk`), nunca `~/setup/desk/registry`.

## AMBIGUEDADES

1. «primero en el registro del desk y, si no esta, con find_registered_desk» no define qué pasa si el repo-id existe en ambos con roots distintos; obligaría a inventar precedencia (aunque «primero» sugiere desk).
2. «la variable o fixture que ya usa find_registered_desk» no la nombra; obligaría a inventar el mecanismo sandbox concreto.
3. «closeout resolved-by --ref acepta ese mismo formato con la misma resolucion» no aclara si `--test` también debe resolverse en ese repo; obligaría a inventar alcance.
4. «la nota a scion con el hash del commit (deskops message send --to scion)» está fuera del Scope y no define contenido ni condición de fallo; obligaría a inventar.
5. «sha es un commit alcanzable en ese repo (rev-parse --verify y ancestro de su HEAD)» no aclara el caso de root registrado ausente en la máquina; obligaría a inventar si es no-evidencia o error.

## DRY-RUN

Lecturas: `closeout_gates.py` (`RepositoryReferences.split`, `reference_points_to_commit`), `deskops/identity.py` (`find_registered_desk`), `closure.py` (rama resolved-by), tests y doc citados. Cambios previstos: fallback de resolución de repo-id en `split`; construir gates del root resuelto; misma resolución en closure; tests sandbox; doc. Dependencias: registro del ecosistema e identidad del desk. Validaciones futuras: los tres comandos pytest indicados y worktree limpio para fallas.

## FUTURO

El ejecutor implementa; el tester valida; el coordinador de scion cierra su tarea y recibe la nota; un humano resuelve las ambigüedades y aprueba.
