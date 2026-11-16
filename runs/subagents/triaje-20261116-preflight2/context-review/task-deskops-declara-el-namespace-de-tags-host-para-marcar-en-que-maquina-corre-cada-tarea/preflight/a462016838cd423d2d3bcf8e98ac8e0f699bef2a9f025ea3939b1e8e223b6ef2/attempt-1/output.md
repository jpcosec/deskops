**REFORMULACION**  
Propósito: que deskops declare un namespace de tag `host` para indicar en qué máquina corre y se valida cada TaskDoc. Resultado: semilla de tags con `host` no jerárquico, valores documentados `host:local`/`host:robocop2`, textos indicados, sincronización de `tag_namespaces`/`tag_models`, una línea en `docs/workflow-policy-reference.md`, test ampliado en `tests/test_atom_tags.py` y store de deskops actualizado sin alertas de tag. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`, con dependencia de `../sldb`. Límites: no taggear tareas existentes; no inventar restricciones de valores; si sldb no lo admite sin alertas, detenerse, avisar a sldb y cerrar solo documentación.

**AMBIGUEDADES**  
1. “Agregar host a la semilla con tag_models que incluya TaskDoc” frente a “si TaskDoc entra en tag_models se declaran también workspace, artifact y source”: obliga a decidir si TaskDoc es obligatorio o condicional, y si basta con declararlo.
2. “Si sldb no admite eso sin alertas en tareas existentes”: no define dónde ni con qué alcance se comprueba; obliga a inventar criterio de aborto.
3. “la lista de esas fallas va en el informe de la tarea”: no define formato, ubicación ni contenido del informe; obliga a inventarlos.

**DRY-RUN**  
Lecturas previstas: `deskops/atom_tags.py`, `docs/workflow-policy-reference.md`, `.sldb/store.yaml`, `tests/test_atom_tags.py`, docs de tags de sldb y búsqueda de tests con `tag_namespaces`. Cambios previstos: añadir `host` a la semilla; ajustar `tag_namespaces`/`tag_models`; documentar el tag; ampliar el test con desk sandbox, `desk update --apply`, TaskDoc con `host:robocop2` y `sldb stores check`; aplicar en deskops y commitear store. Dependencias: semántica de sldb, CLI deskops, entorno pytest. Validaciones futuras: pytest de tags y árbol, `desk update --apply`, `sldb stores check`, suite completa y comparación de fallas contra `origin/main`.

**FUTURO**  
Decisión humana/otro nodo: abortar a documentación si sldb no soporta el modelo; enviar mensaje a sldb; revisar y commitear; coordinar el taggeo posterior de tareas existentes.
