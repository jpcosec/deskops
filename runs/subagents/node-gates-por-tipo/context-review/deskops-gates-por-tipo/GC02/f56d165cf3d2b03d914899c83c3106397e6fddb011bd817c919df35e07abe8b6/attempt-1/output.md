REFORMULACION
GC02 (delivery, repo deskops, hijo de PC01) debe crear el modelo `ReviewDoc` en `deskops/models/review.py`: recibo de revisión con `kind` y `verdict` cerrados, `subject` en `__doc_anchors__`, `subject_ref` para nodos de plan, registro en `MODEL_REFS` y directorio `desk/reviews/`. No escribe ReviewDocs desde comandos (eso es GC03), no toca sldb ni autentica. Límite: modelo, validación al escribir y rechazo de edición del veredicto.

AMBIGUEDADES
1. «hipótesis: la versión actual de sldb acepta en un campo __references__ un valor con prefijo doc: o GC02 lo declara solo en __doc_anchors__ y espera a GO07; el TaskDoc fija cuál» frente a «sldb edges show lo enlaza a la tarea por subject» y `requires: []`. Obliga a inventar si se implementa `__references__` ya, si la aceptación corre sin GO07, y por qué se omite `G_SLDB_ANCHORS`, que alcance.md asigna a GC02.
2. «id (review-<task>-<kind>-<n>)» y «desk/reviews/<task-id>/<kind>-<n>.md» frente a «subject ... o vacío para revisiones de nodos de plan». Obliga a inventar el id y la ruta cuando no hay tarea, y si el modelo valida ese formato.
3. «edit review verdict falla con el mensaje que remite a review dispose»: no existe esa gramática y `output_scope` no incluye `deskops/cli/registry.py`. Obliga a inventar dónde se engancha el rechazo y si se excede el alcance.

DRY-RUN
Lecturas: `models/run.py` como molde, `bootstrap.py` (MODEL_REFS), `workspace.py`, `operations.py` (edit), fixture `model_contract_hashes.json`. Cambios previstos: nuevo `review.py` y export; registro del modelo; creación de `desk/reviews/` en init/update; validadores de kind, verdict, subject y disposed_by; rechazo de edición de verdict; fixture y CHANGELOG. Dependencias: ninguna declarada, aunque la aceptación invoca sldb. Validaciones futuras: roundtrip render/extracción, kind fuera de vocabulario, verdict accepted sin reason, subject inválido/válido, escritura tracked y enlace por subject en desk temporal, `edit review verdict` falla, hash de contrato actualizado.

FUTURO
GC03 consume el modelo y escribe los ReviewDoc desde `deskops review`; GO07 de sldb debe pinnear el hash y producir `anchor_state`; el TaskDoc de promoción o el dueño decide entre `__references__` y solo `__doc_anchors__` antes de GO07; GC05 usará `subject` y `anchor_state` en las reglas de activación.
