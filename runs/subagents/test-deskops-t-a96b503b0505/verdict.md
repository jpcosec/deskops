# Veredicto del tester deskops-t-a96b503b0505

Tarea: task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references
Entrega: run-deskops-e-72feadf3fc22 (cambios sin commitear en el checkout)

**VEREDICTO: APROBADO**

## Comprobaciones (detalle y rc en validation.log)

1. **Diff contra el contrato.**
   - `deskops/services/closeout_gates.py:120-128`: después de `references` se suman a `evidence["atom"]` todos los valores no vacíos de `payload["atoms"]`, sin filtro de prefijo y sin duplicados. Cumple la precisión 1 del preflight. La compuerta de materialization no cambia y el formato del reporte tampoco.
   - `closure.py` no cambia, y no hace falta: `_closeout_link_gate` (closure.py:1241 y 1289) parte de `reference_evidence["atom"]`, que ahora incluye `atoms`. `closeout commit` (closure.py:803) llama a `verify_task_closeout`, la misma ruta, así que el arreglo cubre verify y commit.
   - `tests/test_closeout_gates.py:230-251`: test nuevo con los dos casos del done_when, parametrizado bare_desk/store_desk. `:219-220`: se ajusta la aserción de `task-skill-guard`, que ya tenía `atoms: [ATOM]`. La rompe una razón legítima y lo permite el scope.
   - Goldens `view_board.json` y `view_task.json`: solo cambia la compuerta `atom_or_materialization_link` (evidence, findings y state), más `found` y `summary` de las tareas fixture que tienen `atoms`. `ok` sigue en false. Es una consecuencia directa de contar `atoms`; no hay nada más.
2. **Tests (de a uno, sin lock):** test_closeout_gates 5 passed; test_closeout_declared_evidence 19 passed; test_closeout 59 passed; test_view_goldens 1 passed. Todos con rc=0.
3. **Reproducción con HEAD:** en una copia en /dev/shm con `closeout_gates.py` de HEAD (idéntico, comprobado con diff), `test_task_atoms_field_satisfies_the_link_gate[bare_desk|store_desk]` falla con `assert False is True`. La aserción ajustada de `test_closeout_reports_cover_each_gate_case` también falla allí, como se esperaba.
4. **Reproducción del item por CLI:** en copias en /dev/shm, la tarea real con `files: []`, `references: []` y `atoms` con 2 ids. Con HEAD, `closeout verify` da `missing_atom_or_materialization_link` ("encontré nada"). Con la entrega, la compuerta da `ok: true` con los 2 átomos como evidencia. Se cumple el done_when.
5. **Suite completa (no la corrí; la revisé en validation.log del ejecutor):** 3 failed, 1053 passed. Las 3 fallas (e2e first-task-to-closeout y 2 de test_ci_integration) fallan igual en el worktree limpio de origin/main ee9755e3, con rc 127: falta `python`/`pytest` en el PATH. Son preexistentes y de entorno; ninguna es nueva.

## Hallazgos no bloqueantes y riesgos (para el coordinador)

- **`files` del TaskDoc no coincide con la entrega:** declara `deskops/services/closure.py`, que no se tocó, y no incluye los dos goldens modificados. Conviene ajustar `files` antes del closeout (quitar closure.py y agregar `tests/fixtures/golden/output/view_board.json` y `view_task.json`).
- **Riesgo de diseño (lo trae el contrato):** como no se filtra por prefijo ni se exige que el AtomDoc exista, un id inexistente satisface la compuerta. El golden lo muestra: `atom-does-not-exist` pasa a `holds`. Con `references`, en cambio, `reference_points_to_atom` exige que el archivo exista. Si se quiere validar la existencia, es una tarea aparte.
- El checkout no se tocó: `git status` es idéntico al del inicio. Solo escribí en este run_dir y en /dev/shm, que ya limpié.
