REFORMULACION
Nodo hoja ejecutable. Propósito: que deskops declare en su semilla de tag namespaces el namespace `host` para que un TaskDoc indique la máquina donde se ejecuta y valida. Resultado: `deskops/atom_tags.py` con `host` no jerárquico, documentado con `host:local`/`host:robocop2`, texto de política y test; tras `desk update --apply`, un TaskDoc con `host:robocop2` no genera alertas de tag en `sldb stores check`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no taggear tareas existentes; no restringir valores; si sldb no admite la declaración sin alertas en tareas existentes, detener la parte de código, avisar a sldb y cerrar solo documentación.

AMBIGUEDADES
1. "Agregar host a la semilla con tag_models que incluya TaskDoc" frente a "si TaskDoc entra en tag_models se declaran tambien workspace, artifact y source". Obliga a inventar si TaskDoc debe entrar obligatoriamente en `TAG_MODELS` o si basta declarar `host` y el test solo comprueba ausencia de alerta.
2. "host con hierarchical: false y folder_axis: false" frente al código mostrado, que construye `TagNamespace(name=..., anchored_by=...)`. Obliga a inventar si hay que añadir esos campos explícitamente o confiar en defaults.
3. "los valores documentados host:local y host:robocop2" y "Los valores no se restringen". Obliga a inventar dónde documentarlos: no está claro si en `examples`, en `meaning` o en un campo nuevo.
4. "docs/workflow-policy-reference.md (una linea que explique el tag host)" no fija texto ni ubicación. Obliga a inventar la redacción exacta y el punto del documento.

DRY-RUN
Lecturas: `deskops/atom_tags.py`, `tests/test_atom_tags.py`, `.sldb/store.yaml`, `docs/workflow-policy-reference.md` y `sldb docs/architecture/tags.md`. Cambios previstos: añadir `host` a `DEFAULT_ATOM_TAG_NAMESPACES`; ajustar `TAG_MODELS`/declaración si se decide incluir TaskDoc y sus namespaces; ampliar test con desk sandbox, `desk update --apply`, TaskDoc con `host:robocop2` y comprobación de `sldb stores check`. Dependencias: API `TagNamespace`, `tag_check`, `tag_namespaces`; tags existentes `workspace:`, `artifact:`, `source:`. Validaciones futuras: los dos pytest, `desk update --apply` + `sldb stores check` sin alertas por host, suite completa y comparación de fallas en worktree limpio.

FUTURO
El coordinador decide si acepta incluir TaskDoc en `tag_models`; sldb puede requerir namespaces por modelo; cada coordinador taggea sus tareas; el cierre exige test, commit y recibo de átomo/materialización.
