# Veredicto del tester deskops-t-16e62e0d9f56

- task: task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp
- entrega: run-deskops-e-e1719ad4ee0d (cambios sin commitear en .sldb/store.yaml y .sldb/core/store_index.yaml)
- evidencia: validation.log (este directorio)

## VEREDICTO: APROBADO

## Comprobaciones

1. **Diff**: `spec2viz -> ../spec2viz/.sldb` desaparece de `links` (store.yaml) y de `stores` (store_index.yaml). Los enlaces sldb, pron y scion no cambian. El resto del diff son líneas `include:` y `store_hash`: 4 de RunDoc (incluido el de este tester) y además 2 de **ReviewDoc** (preflight-1 y bundle-1 de la tarea `task-la-regla-de-desk-graph-...-spec2viz-...`). Esas dos son de otra sesión/tarea, no de esta. El brief solo menciona includes de RunDoc, pero son igual de ajenas. El integrador debe dejarlas fuera del commit de esta tarea (o commitearlas aparte).
2. **Stores**: `sldb stores list` muestra pron, scion y sldb, sin spec2viz. `grep -rn '../spec2viz' .sldb` no encuentra nada (rc=1).
   Comparación por conjunto de líneas contra los antes-*.txt del ejecutor:
   - `stores check`: rc=0, 217 alertas, igual que antes. 0 alertas nuevas y 0 que desaparecen. La única línea distinta es el conteo `775 → 778 documents`, que sube por las escrituras concurrentes de otras sesiones; no es un hallazgo.
   - `deskops doctor`: rc=0, "Desk is healthy, with 220 alert(s)". 0 nuevas, 0 que desaparecen.
   - `deskops graph missing`: rc=1, "37 missing" antes y después. 0 nuevas, 0 que desaparecen.
3. **La sesión federada ya no lee spec2viz**: `api.select_documents(.sldb, include_linked=True)` es la misma ruta que usa `select_documents` de `sldb mcp` con include_linked. Lo corrí bajo `strace -f -e trace=openat`: devolvió 5294 filas.
   - Filas por store enlazado (prefijo de `export_id`): sldb 3592, pron 782, scion 142, spec2viz 0.
   - Archivos abiertos (openat): bajo `../spec2viz` **0**. Como control positivo de que la federación sí se ejerció: 3666 bajo `../sldb/.sldb`, 837 bajo `../pron/.sldb` y 180 bajo `../scion/.sldb`. La nota de IR medía unos 1233 abiertos bajo spec2viz.
   - `sldb models list` y `sldb docs list` no abren stores enlazados (control sldb=0), así que no sirven como prueba de federación. Por eso usé la API.
4. **Tests**, de a un archivo y sin lock:
   - test_migrate_desk_stores.py: 16 passed
   - test_doctor_model_registration.py: 8 passed
   - test_desk_sync.py: 8 passed
   - test_doctor_absolute_paths.py: 13 passed
5. **Hallazgo del ejecutor**: lo confirmo en el código. `sldb/api/stores/unlink_store.py::drop_link` solo hace `save_store_index` y no toca la declaración `links:` de `store.yaml`. Si se regenera el índice desde la declaración, el enlace vuelve. Tras `stores declare --write`, los dos archivos coinciden: los links de store.yaml y los stores de store_index son ambos {pron, scion, sldb}. Ambos se reescribieron a las 17:27 (otra sesión agregó includes de RunDoc) y el enlace no reapareció. El store queda coherente y estable frente a regeneraciones.
6. No corrí la suite completa ni `stores build --check`, por orden del integrador.

## Riesgos y pendientes

- **Suite completa pendiente** (Done When: "la suite no tiene fallas nuevas"). Le toca al integrador antes del closeout.
- **El diff trae includes ajenos** (RunDoc y 2 ReviewDoc de otra tarea). Hay que separarlos al commitear.
- **Hueco de sldb**: `stores remove` no actualiza `store.yaml`. Debería ir al inbox de sldb. El coordinador lo rutea; el tester no escribe allí.
