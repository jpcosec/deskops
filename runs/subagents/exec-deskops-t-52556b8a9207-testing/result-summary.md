FALLA

# Resultado del tester

Tarea: `task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea`
Commit del ejecutor: `5d10b2eb6284b96b27c9fc3bc7eeb8407644e682` ("deskops declara el namespace de tags host (y workspace/artifact/source planos, TaskDoc en tag_models)"). El trailer `Task-Id` coincide con la tarea.

## Veredicto

El codigo y los tests del commit son correctos y pasan, pero el entregable no esta completo: el `.sldb/store.yaml` **commiteado en el desk de deskops no declara `host` ni `TaskDoc`**. El propio `deskops desk update --root .` lo reporta como divergente, y el Done When exige que el store declare `host` y que el cambio quede commiteado. Por eso la tarea no puede cerrarse tal como esta.

## Verificacion

Comandos ejecutados (sin correr la suite completa, como pide el rol):

```
TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q tests/test_atom_tags.py
# 10 passed, 1 warning in 0.68s

TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q tests/test_domain_tree.py
# 10 passed, 1 warning in 262.10s

TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q tests/test_scaffold_golden.py
# 3 passed, 1 warning in 32.25s (fixtures golden/scaffold/*.json tocados por el commit)
```

El test nuevo `test_task_with_host_tag_raises_no_tag_alert` usa un desk sandbox real y pasa. El test `test_store_declares_flat_host_namespace_and_task_doc_model` fija `host`/`workspace`/`artifact`/`source` planos y `TaskDoc` en `tag_models`.

## Falla bloqueante: store del desk sin sincronizar/commitear

En `HEAD` (y en el arbol de trabajo):

```
$ grep -A3 '^tag_models:' .sldb/store.yaml
tag_models:
- AtomDoc
- ProtoAtomDoc
# sin TaskDoc
$ grep 'name: host' .sldb/store.yaml
# sin resultados

$ deskops desk update --root .
Desk divergence report:
- Tag namespace declaration: .sldb/store.yaml differs from desk/atoms/tag-namespaces.yaml
...
Run with --apply to repair these issues.
# exit 1
```

En un worktree limpio de `HEAD` (`/dev/shm/wt-host-test`, ya eliminado) ejecute `desk update --apply` y si produjo la declaracion esperada: `tag_models: [AtomDoc, ProtoAtomDoc, TaskDoc]` y `host`, `workspace`, `artifact`, `source` con `hierarchical: false`. Un TaskDoc con `host:robocop2` dejo de dar alertas de namespace. Es decir, el codigo esta bien; falta aplicar y commitear el store del desk, como pide el punto 4 del Implementation Path y el Done When.

## Observaciones no bloqueantes

- El commit del ejecutor modifica `.sldb/store.yaml` agregando las rutas de `sldb/relation_types/*` dentro de un `- model: RelationTypeDoc` que ya existia, duplicando esas entradas con la segunda seccion `RelationTypeDoc` identica. Es un cambio ajeno al alcance de la tarea; no hizo fallar los tests, pero conviene revisarlo al regenerar/commitear el store.
- `docs/atoms.md` (linea ~48) sigue diciendo `tag_models: [AtomDoc, ProtoAtomDoc]` y que las tareas no se chequean, lo que quedo desactualizado con este cambio. La linea pedida en `docs/workflow-policy-reference.md` si esta presente y con el texto esperado.
- El docstring de `test_tasks_and_pills_with_undeclared_namespaces_are_not_findings` tambien quedo desactualizado, aunque el test sigue pasando.

## Entorno

El `.venv` del workspace apunta a un Python 3.12 ausente; use `/workspace/sldb/.venv/bin/python` (Python 3.13.18), que resuelve `deskops` y `sldb` al workspace. No modifique codigo, tests ni el store del repo; el worktree temporal se elimino y no se creo commit.
