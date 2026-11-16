# REFORMULACION

**Propósito:** que las compuertas `atom|materialization` de `closeout verify` y `closeout commit` reconozcan como evidencia de átomo los ids del campo `atoms` del frontmatter de la tarea, no solo los `atom-*` presentes en `references`. Hoy `closeout_gates.py:100-113` recorre únicamente `references` y `closure.py:1241` y `1288-1293` usan `reference_evidence['atom']`, por lo que una tarea con `atoms: [atom-x]` falla con `missing_atom_or_materialization_link`.

**Resultado:** código modificado en `deskops/services/closeout_gates.py` y `deskops/services/closure.py` que une `task.atoms` a la evidencia de átomo, más test en `tests/test_closeout_gates.py` con dos casos (pasa con atoms sin atom-* en references; sigue fallando sin ninguno), y las cuatro validaciones pytest en verde sin fallas nuevas respecto de main.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** no tocar otras compuertas ni el formato del reporte.

# AMBIGUEDADES

1. "Unir task.atoms a los atom-* de references" — ¿se filtran los valores de `atoms` por prefijo `atom-` o se aceptan todos? Obliga a inventar criterio de filtrado.
2. "compuerta atom|materialization" frente a "evidencia los ids del campo atoms" — no aclara si los ids de materialización también deben ampliarse; obliga a decidir alcance.
3. "sin fallas nuevas respecto de main" — no define cómo obtener la línea base; obliga a inventar el procedimiento de comparación.
4. `files:` lista solo `tests/test_closeout_gates.py`, pero Validation ejecuta además `test_closeout_declared_evidence.py` y `test_closeout.py`; obliga a decidir si esos tests pueden editarse.
5. `status: draft` con `current_node: ritual-execution`; no indica si el ejecutor debe promocionar el estado antes de codificar.

# DRY-RUN

**Lecturas:** `closeout_gates.py:100-113`, `closure.py:1241,1288-1293`, los tres ficheros de test, la pill `pill-closeout-knowledge-gates-require-traceable-evidence.md` y el ítem del drawer citado. **Cambios previstos:** construir el conjunto de evidencia de átomo como unión de `task.atoms` y los `atom-*` de `references`, preservando la forma del reporte; añadir los dos casos de test. **Dependencias:** acceso al campo `atoms` en el modelo de tarea y estabilidad de las claves del reporte. **Validaciones futuras (no ejecutadas):** los cuatro comandos pytest indicados, el último con `-n 4` sobre `tests`.

# FUTURO

Un humano resuelve las ambigüedades 1–3 y 5 antes de ejecutar. Otro nodo ejecuta el cambio, corre las validaciones y produce el commit; el ritual de closeout verifica la evidencia de átomo y actualiza `status`/`history`.
