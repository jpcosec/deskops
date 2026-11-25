FALLA

# Resultado del tester (intento 2)

Tarea: `task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea`

Commits del ejecutor (ambos con el trailer `Task-Id` de la tarea):

- `5d10b2eb6284b96b27c9fc3bc7eeb8407644e682` — implementación inicial (`deskops/atom_tags.py`, docs, tests, semilla del desk).
- `3b4c5ac8fff2660c95468fe24af7e9658468b60d` — intento de corregir la devolución del tester anterior.

`git log -1 --grep "Task-Id: ..."` devuelve `3b4c5ac8`, pero el estado final es la unión de ambos commits en `HEAD` (`80a6781d`, commit de run encima del ejecutor).

## Veredicto

El código y los tests del commit pasan, pero el punto bloqueante que motivó el retorno a ejecución **sigue sin resolverse**: el `.sldb/store.yaml` commiteado en el desk de deskops no se sincronizó.

Concretamente, en `HEAD`:

- `tag_models` sigue siendo `[AtomDoc, ProtoAtomDoc]`; no incluye `TaskDoc`.
- No existe ningún `name: host` en `tag_namespaces`; tampoco `workspace` pasó a plano ni están `artifact`/`source`.
- Sigue habiendo **dos secciones `- model: RelationTypeDoc`** (líneas 158 y 192) con las mismas 14 rutas `sldb/relation_types/*`; la duplicada que el tester pidió quitar no se eliminó ni se regeneró con la herramienta.
- El commit `3b4c5ac8` solo toca `.sldb/core/models/RuleDoc.yaml` y `tests/test_atom_tags.py`; no toca `.sldb/store.yaml`.

Por tanto no se cumplen los puntos 1-3 del intento 2 ni el `Done When` ("el store de deskops declara host").

## Evidencia

```
$ grep -A4 '^tag_models:' .sldb/store.yaml
tag_models:
- AtomDoc
- ProtoAtomDoc

$ grep -n 'name: host' .sldb/store.yaml
(none)

$ grep -n -- '- model: RelationTypeDoc' .sldb/store.yaml
158:- model: RelationTypeDoc
192:- model: RelationTypeDoc

$ python -m deskops desk update --root .
Desk divergence report:
- Tag namespace declaration: .sldb/store.yaml differs from desk/atoms/tag-namespaces.yaml
- Stale document hashes: ... (hallazgos ajenos a esta tarea)
Run with --apply to repair these issues.
EXIT=1
```

El `desk update --root .` sale 1 por la declaración de tags divergente (además de hashes obsoletos ya presentes en el árbol). No se ejecutó `--apply` sobre el repo para no modificar el entregable durante la verificación.

`git status --short -- .sldb/store.yaml` no muestra cambios: el store quedó exactamente como estaba, sin la declaración de `host` ni `TaskDoc`.

## Tests ejecutados (solo los del commit, sin suite completa)

Todos con `TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q` (el Python resuelve `deskops` a este worktree y `sldb` a `../sldb/src`):

```
tests/test_atom_tags.py        11 passed, 1 warning in 22.67s
tests/test_domain_tree.py      10 passed, 1 warning in 305.48s
tests/test_scaffold_golden.py   3 passed, 1 warning in 36.19s   # fixtures golden tocados por 5d10b2eb
```

Los tests nuevos pasan, incluido `test_desk_update_reports_no_divergence_after_declaring_host`, pero este corre sobre un desk sandbox en `tmp_path`: valida el código, no detecta que el store real del repo no se haya aplicado/commiteado.

## Conclusión

FALLA por entregable incompleto: falta (1) quitar manualmente/regenerar la sección `RelationTypeDoc` duplicada, (2) ejecutar `deskops desk update --apply --root .`, (3) commitear el `.sldb/store.yaml` resultante con `Task-Id`, y (4) comprobar que `deskops desk update --root .` sale 0 y que `sldb stores check --store .sldb` no agrega hallazgos de tags. El código de `atom_tags.py` y la documentación ya están correctos.
