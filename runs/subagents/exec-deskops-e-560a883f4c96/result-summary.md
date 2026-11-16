# Resultado del ejecutor deskops-e-560a883f4c96

- run_id: run-deskops-e-560a883f4c96
- task: task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi
- session: scion://agent/deskops-e-560a883f4c96 (agente claude; el ejecutor no tiene acceso a su transcript)
- session_sha256: (vacío: lo registra el coordinador)

## Qué cambié

Todos los archivos tocados están en `files` del TaskDoc. No toqué desk/ ni .sldb/; los cambios de .sldb/ y runs/subagents/2026* que muestra git-status.txt ya estaban antes de empezar (son de otra sesión o del lanzamiento).

- `deskops/services/closeout_gates.py`
  - `RepositoryReferences` recibe `ecosystem=` (un cargador, `load_ecosystem_registry`). `split(ref, ecosystem=True)` busca el prefijo primero en el registro del desk y, si no está, en el del ecosistema. El registro local gana. Al ecosistema solo se va con un prefijo con forma de repo-id (`REPO_ID_PATTERN`: sin `/` ni espacios), así que `tests/x.py::t` o `pytest ...` nunca lo leen. Un registro del ecosistema que no se puede leer o que repite un id (`_raise_on_duplicate_ids`) no resuelve nada y no lanza excepción.
  - Métodos nuevos: `points_to_commit(ref, local)` y `full_commit_sha(ref, local)`. Este último devuelve `<repo-id>:<sha completo>` para el recibo. También `missing_commit_roots(refs)`. Los tres reutilizan `CloseoutGatesService(root del otro repo).reference_points_to_commit` y `full_commit_sha` sin duplicarlos. Si el root registrado no existe en esta máquina, la referencia no cuenta.
  - `closeout_reference_evidence` acepta `points_to_commit=` opcional, keyword con default; el gate de tests no cambia.
- `deskops/services/closure.py`
  - `_repository_references` le pasa `ecosystem=load_ecosystem_registry`. `_verify_repository_references` es la versión de verify: un error del registro local deja una lista vacía y no lanza excepción.
  - verify (`_closeout_reference_evidence`) cuenta `<repo-id>:<sha>` como commit. Si el gate de commit falla y la referencia es de un repo cuyo root no está en la máquina, sus findings agregan `registered_repository_missing` con el mensaje de `missing_root_message`. El recibo de evidencia de commit guarda `<repo-id>:<sha completo>`.
  - resolved-by: solo `--ref` usa el ecosistema (`points_to_commit`, `ref_is_url` y `_missing_registered_root(..., ecosystem=True)`). `--test` queda igual: solo el registro del desk.
- `docs/workflow-policy-reference.md`: subsección nueva "Commit evidence from another repository", justo después de "Tests evidence from a suite in another language". Explica la forma `<repo-id>:<sha>`, el orden de resolución (local y luego ecosistema), el criterio de alcanzable, que lo que no resuelve no cuenta y no lanza excepción, el caso del root ausente y que `--test` y el gate de tests no cambian.
- `tests/test_closeout_gates.py`: 7 casos de verify con `DESKOPS_ECOSYSTEM_REGISTRY` apuntando a un registro sandbox en tmp_path (monkeypatch.setenv):
  - repo-id que solo lista el ecosistema y sha ancestro: pasa (y el sha completo calificado del recibo);
  - no cuentan: sha inexistente, repo-id desconocido, sha del desk calificado por el otro repo, id ambiguo en el ecosistema;
  - el registro local gana sobre el ecosistema;
  - root ausente: no encontrada, con `registered_repository_missing`.
- `tests/test_closeout_resolved_by.py`: 5 casos de resolved-by `--ref` con el ecosistema sandbox:
  - cierra en un desk sandbox con `infra:<sha>`;
  - se rechazan: sha inexistente, repo-id desconocido y root ausente (mensaje de `missing_root_message`);
  - `--test infra:...` sigue sin resolverse por el ecosistema.

## Validación

Ver validation.log (comando, salida y rc de cada uno):

- `pytest -q tests/test_closeout_gates.py`: 12 passed, rc=0
- `pytest -q tests/test_closeout_resolved_by.py`: 25 passed, rc=0
- extra, regresión de XREPO: `pytest -q tests/test_closeout_resolved_by_xrepo.py`: 12 passed, rc=0
- extra: `pytest -q tests/test_closeout_test_paths.py`: 31 passed (llama a `closeout_reference_evidence`)

**Para el integrador:** la suite completa (`pytest -n 4 -q tests`) y la comparación de sus fallas con origin/main. No la corrí por la orden del brief, así que no puedo listar fallas de la suite comparadas con origin/main.

## Riesgos

- verify ahora lee el registro del ecosistema real (`~/setup/desk/registry`, solo lectura) cuando una referencia tiene la forma `<id>:<algo>` y el desk no lista ese id. Los tests nuevos aíslan el ecosistema; los tests viejos con prefijos como `nope:` o `gone:` lo leen en solo lectura, y esos ids no están en el registro real.
- Un prefijo igual a la `project_identity` del desk ahora cuenta en verify como commit local (`<id>:<sha>`); antes verify no contaba nada calificado. Es coherente con resolved-by.
- Que un id esté repetido en el registro del ecosistema invalida todo el ecosistema para la resolución, no solo ese id, porque `load_repository_registry` falla sobre el registro entero.

## Texto propuesto para la nota a scion (la manda el coordinador con el hash)

deskops <HASH>: la evidencia de commit `<repo-id>:<sha>` resuelve el repo-id en `desk/registry` del desk y, si no está, en el registro del ecosistema (`~/setup/desk/registry` o `$DESKOPS_ECOSYSTEM_REGISTRY`), igual que `message send --to`.
Vale para `closeout verify` (en `references` de la tarea) y para `closeout resolved-by --ref`; `--test` sigue leyendo solo el registro del propio desk.
El sha debe ser hex en minúsculas, existir en ese repo y ser ancestro de su HEAD. Ejemplo: `deskops closeout resolved-by --task <id> --reason "..." --ref deskops:4a7707a5 --ref deskops:4c745c18 --ref deskops:881e177a --test <test local>`.
Una referencia que no resuelve no cuenta y no lanza excepción; si el root registrado no está en la máquina, el cierre se rechaza con ese mensaje.
