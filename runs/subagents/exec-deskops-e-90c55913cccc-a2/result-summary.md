# Result summary (intento 2)

- run_id: exec-deskops-e-90c55913cccc-a2
- Store: se revirtió en .sldb/store.yaml el hunk del commit anterior que había metido las rutas `sldb/relation_types/*` dentro de la primera sección `RelationTypeDoc` (vuelve a la forma previa: sección desk + sección sldb). `deskops desk update --apply` regeneró tag_models (+TaskDoc) y tag_namespaces (host, artifact, source, workspace planos).
- `deskops desk update --root .` ya no informa "Tag namespace declaration". Sigue saliendo 1 solo por "Stale document hashes" (5 docs de inbox/reviews, data_mutation) preexistentes y ajenos a la tarea, que `--apply` no repara; también ocurre en el checkout principal.
- `sldb stores check --store .sldb`: 0 alertas de tags (solo anchors/doc_lost, doc_changed, link-absent y structural-noise preexistentes).
- Test nuevo en tests/test_atom_tags.py: desk sandbox, `desk update --apply`, `desk update` sin divergencia, tarea con host:robocop2, `sldb stores check` sin alerta de tag.
- Validación: tests/test_atom_tags.py + tests/test_domain_tree.py = 21 passed. Suite completa con -n 4: cortada a los ~50 min en ~86 % sin ninguna falla visible (por la instrucción del coordinador del límite de 30 min); no se comparó contra origin/main.
- Archivos: .sldb/store.yaml, .sldb/core/store_index.yaml, .sldb/core/models/RuleDoc.yaml, tests/test_atom_tags.py (más los del commit anterior).
- Revisar: el cambio de RuleDoc.yaml lo generó la herramienta con `desk update --apply`.
