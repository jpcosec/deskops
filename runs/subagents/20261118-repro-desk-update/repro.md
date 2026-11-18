# Reproducción: desk update --apply vacía el path de los modelos en el repo de deskops

2026-11-18, integrador. Checkout /mnt/ssd/proyectos/SLDB_1/deskops con herramientas en 31460a48. Se corrió `deskops desk update --root . --apply`.

- desk-update-apply.log: salida del comando y diff del git status antes y después (rc 0; "Lifecycle graph: tracked" las dos semillas testing->execution, que ya estaban).
- archivos-cambiados.txt: los archivos que el update cambió. Son todos .sldb/core/models/*.yaml, más store_index.yaml, store.yaml, sldb/relation_types/has_model.md y los nuevos reltype-links_to y RelationTypeDoc/type-task_returns_to_execution.
- En cada modelo, el diff era `-path: deskops/models/<modelo>.py` / `+path: ''` (p. ej. RoleDoc: deskops/models/role.py).
- Se revirtió entero sin commitear. En sldb (93af34c7) e IR (6884ff2) el mismo comando no tocó .sldb/core/models.
