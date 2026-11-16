# Veredicto del tester deskops-t-79da9372a710

- task: task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi
- role: tester (independiente, agente claude, sesión fresca)
- run_id: run-deskops-t-79da9372a710; session: scion://agent/deskops-t-79da9372a710; session_sha256: (lo registra el coordinador)
- entrega revisada: diff sin commitear sobre HEAD ee9bc3cd en los 5 archivos de `files`
- evidencia: validation.log (cada comando, su salida y su rc)

## VEREDICTO: APROBADO

## Contrato frente al diff

- **Orden de resolución.** `RepositoryReferences.split(..., ecosystem=True)` busca primero en `self.entries`, que es el registro del desk (`deskops/services/closeout_gates.py:318`). Solo si ahí no está va a `_ecosystem_entry` (`:320`, `:327`), que usa `load_ecosystem_registry`: lee `DESKOPS_ECOSYSTEM_REGISTRY` y, si no está, `~/setup/desk/registry`. Por eso el registro local gana. Lo cubre `test_commit_evidence_prefers_the_desk_registry_over_the_ecosystem`. Usa `load_ecosystem_registry` en vez de `find_registered_desk`; el preflight-1 (2) admite las dos.
- **Alcanzable reutilizado.** `points_to_commit` (`closeout_gates.py:338`) delega en `self.gates(entry).reference_points_to_commit(value)`, que es `CloseoutGatesService` sobre la raíz del otro repo. `full_commit_sha` hace lo mismo. No hay lógica de git duplicada.
- **Referencias que no resuelven.** Un id desconocido da `None`. Un id ambiguo o un registro ilegible caen en `except Exception` y resuelven nada (`:333`). Un sha inexistente devuelve False en `reference_points_to_commit`. Un root ausente devuelve False por `missing_root_message`; verify agrega `registered_repository_missing` (`closure.py:994`) y resolved-by rechaza con ese mensaje (`closure.py:303`). Un error del registro local en verify tampoco lanza excepción (`_verify_repository_references`, `closure.py:416`). Todo esto está probado con el registro sandbox y, para sha inexistente e id desconocido, también con el registro real (ver validation.log).
- **resolved-by.** Solo `--ref` pasa `ecosystem=True` (`closure.py:303`, `:306-310`). `--test` sigue con `split` sin ecosistema. Lo prueba `test_resolved_by_test_does_not_resolve_through_the_ecosystem_registry`.
- **Decisión de JP: el gate de tests no cambia.** `closeout_reference_evidence` solo cambia la clasificación de `commit` (`closeout_gates.py:107`, `:123`). `evidence["tests"]` sigue saliendo de `reference_points_to_test`, que no se tocó, y es lo único que lee el gate de tests (`closure.py:969`). Además el parámetro es opcional y su valor por defecto es el comportamiento anterior, así que otros llamadores no cambian. `test_closeout_test_paths.py` pasa entero (31).
- **Aislamiento de los tests.** Los dos archivos usan `monkeypatch.setenv("DESKOPS_ECOSYSTEM_REGISTRY", <tmp_path>/registry)`, y los subprocesos de resolved-by heredan el entorno. Ningún test escribe en `~/setup/desk/registry`. Comprobé que el mtime de `~/setup/desk/registry/repo-sldb.md` no cambió y que `git -C ~/setup status desk/registry` está limpio.
- **Scope.** Los archivos tocados son exactamente los 5 de `files`. La doc está en la subsección "Commit evidence from another repository", después de "Tests evidence from a suite in another language", como pide el preflight-1 (4). El `result-summary.md` del ejecutor trae el texto para la nota a scion, según el preflight-1 (5).

## Validaciones (rc)

| Comando | Resultado |
|---|---|
| pytest tests/test_closeout_gates.py | 12 passed, rc=0 |
| pytest tests/test_closeout_resolved_by.py | 25 passed, rc=0 |
| pytest tests/test_closeout_resolved_by_xrepo.py | 12 passed, rc=0 |
| pytest tests/test_closeout_test_paths.py | 31 passed, rc=0 |
| pytest tests/test_foreign_suites.py | 10 passed, rc=0 |
| pytest tests/test_message_ecosystem_registry.py | 1.ª corrida: 4 failed, rc=1. Reintento: 6 passed, rc=0 |

El primer fallo de test_message_ecosystem_registry.py no viene de esta entrega. Lo causó `ModuleNotFoundError: No module named 'sldb.code.lang_ts'`: el checkout hermano `../sldb` estaba a mitad de una edición de otra sesión, y `scan.py` ya importaba `lang_ts.py` antes de que ese archivo existiera. Cuando el archivo apareció, el mismo comando pasó 6/6.

**Reproducción en HEAD.** Copié HEAD ee9bc3cd con `git archive` a /dev/shm y le agregué los tests nuevos. Fallan los 6 casos positivos:
- test_closeout_gates.py: 3 failed / 9 passed (resuelve solo por el ecosistema, el local gana, root ausente con `registered_repository_missing`);
- test_closeout_resolved_by.py: 3 failed / 22 passed (`--ref infra:<sha>` cierra, root ausente con `missing_root_message`, `--test` sin ecosistema).

Los casos negativos pasan también en HEAD, como corresponde: allí ya no contaban.

**Caso real (solo lectura).** Armé un desk sandbox en /dev/shm sin `desk/registry`, con una tarea task.docs (`--evidence commit document`) y `references: [sldb:7cc3599266]`, que es el HEAD real de ../sldb. Con la entrega, el gate de commit da `ok: true` y `evidence: ["sldb:7cc3599266"]`. Con HEAD da `missing_commit_evidence`. El gate de document falla en los dos casos porque la tarea no tiene documento, y eso es lo esperado. Con el registro real, `sldb:deadbeef00` y `noexiste-xyz:7cc3599266` no cuentan y no lanzan excepción.

No corrí la suite completa ni `stores build --check`, por orden del integrador (wA:p1).

## Riesgos que anotó el ejecutor

1. **verify lee el registro real en solo lectura para prefijos desconocidos.** Lo acepto. Es la misma fuente que ya usa `message send --to`, la carga es diferida (una vez por instancia) y solo ocurre con prefijos con forma de repo-id (`REPO_ID_PATTERN`). Efecto secundario: verify de un desk cualquiera con una referencia `x:y` que no está en el registro local depende de lo que haya en el registro del ecosistema de la máquina. Un id real del ecosistema puede convertir en commit una referencia que antes no contaba, pero solo si el sha es un ancestro real de ese repo, así que no hay falso positivo.
2. **Un prefijo igual a `project_identity` ahora cuenta como commit local en verify.** Lo acepto. Es coherente con resolved-by y con el docstring de la clase, que ya lo definía así. Solo amplía lo que se acepta, con el mismo criterio de alcanzable.
3. **Un id repetido en el ecosistema invalida todo el ecosistema.** Es más conservador de lo necesario, pero cumple "ambiguo no cuenta y no lanza excepción". El costo es que un duplicado ajeno en `~/setup/desk/registry` deja sin resolver todas las referencias por ecosistema, sin aviso en verify (el finding es solo `missing_commit_evidence`). Lo dejo como seguimiento posible (un finding que diga "ecosystem registry unreadable"), no como bloqueo.

## Observaciones menores (no bloquean)

- `_ecosystem_entry` atrapa `Exception` en general (`closeout_gates.py:333`) y no solo `SLDBStoreError`. Va más allá del contrato, pero no lanza excepción, que es lo que se pide.
- El ejecutor no corrió la suite completa con comparación contra origin/main (se lo prohibía el brief). Queda para el integrador.
