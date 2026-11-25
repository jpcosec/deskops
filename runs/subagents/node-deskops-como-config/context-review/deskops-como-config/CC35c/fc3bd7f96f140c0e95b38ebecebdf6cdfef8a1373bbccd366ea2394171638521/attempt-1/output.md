## REFORMULACION

CC35c es un nodo de entrega de deskops: migrar las referencias entrantes de `atoms delete/split/merge`, `retire`, `drawer remove` y `closeout` a `referrers/rewrite_references` de sldb (GD22) dentro de una misma transacción, y declarar menciones `atom:<id>` en prosa y bullets del drawer como `MentionPattern` en la configuración de grafo que deja CC33. Resultado: funciones propias de referencias entrantes borradas, una sola vía transaccional, goldens de ayuda/salida idénticos, `doctor` sin hallazgos nuevos, líneas antes/después y CHANGELOG. Repo dueño: deskops. Límites: no escribe en sldb, no suple reglas con Python, no deja dos caminos vivos, mantiene formato del desk y gramática del CLI. Depende de CC35a (transacción) y CC33c (grafo); `G_GD22` está satisfecho.

## AMBIGUEDADES

1. El scope exige que «closeout usan referrers/rewrite_references (GD22) dentro de la misma transacción», pero `output_scope` solo enumera «deskops/services/, deskops/atom_references.py, deskops/graph/desk_graph.py (MentionPattern), tests/, CHANGELOG.md». Obliga a inventar si se puede tocar `closure.py`/closeout fuera del output_scope declarado.
2. La aceptación solo exige el grep de «_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references», mientras el scope nombra además `_retarget_atom_documents :809`, `_board_pill_updates :158`, `_drawer_bullets_removed :141`, `_tasks_recording :183` y `_board_routes/_board_reference_matches :572-584`. Permite dejar caminos viejos vivos y aun pasar la aceptación.
3. El scope incluye «atoms delete/split/merge» y «drawer remove», pero la aceptación solo comprueba «atoms merge reescribe menciones atom:<id> en prosa» y «retire de una pill...». No hay comprobación para delete, split, drawer remove ni closeout: el ejecutor debe inventar si esos casos quedan fuera o cómo probarlos.

## DRY-RUN

Lecturas: nodo y padre en `dag.yaml`, scope de CC35, salidas de CC35a y CC33c, contrato GD22, goldens, tests de atoms/retire/drawer/closeout. Cambios previstos: sustituir las funciones propias por `referrers/rewrite_references` dentro de la transacción de CC35a; declarar `MentionPattern` en la configuración de grafo; borrar las funciones viejas. Dependencias: transacción de CC35a, configuración de grafo de CC33c y GD22 ya satisfecho. Validaciones futuras: grep pactado, retire de pill en una transacción, merge reescribiendo prosa, goldens idénticos, tests de archivos tocados, `doctor` en 6 desks, líneas antes/después y CHANGELOG.

## FUTURO

CC35a entrega la API transaccional; CC33c deja la configuración de grafo donde se declara `MentionPattern`; sldb/GD22 aporta el contrato ya cerrado. Al promover, el TaskDoc fija archivos, tests y nombres exactos. El supervisor corre la suite integrada y `doctor`; el operador del desk dispone correcciones del TaskDoc.
