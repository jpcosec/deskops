## REFORMULACION

Encargo ejecutable: en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, modificar `deskops view task <id>` para que el contrato de la vista incluya `task.receipts`: lista de un objeto por `ReviewDoc` cuyo `subject` sea la tarea, con `id`, `kind`, `verdict`, `anchor_state` y `created_at`, ordenada por `created_at`. Debe funcionar en JSON, YAML y texto —en texto, una línea por recibo— y documentarse en `docs/deskops-ui.md` junto a `gates`. `anchor_state` debe reutilizar el cálculo actual de `deskops review status`. Límites: no tocar `view board`, la UI de `graph_ui` ni el modelo `ReviewDoc`; cambios acotados a `deskops/cli/commands/view.py`, `docs/deskops-ui.md` y `tests/test_view.py`. Validación: ejecutar los dos pytest indicados en un sandbox desk.

## AMBIGUEDADES

1. «ordenada por `created_at`» no indica dirección: obligaría a inventar ascendente o descendente.
2. «en text una linea por recibo» no define columnas, etiquetas ni separador: obligaría a inventar el formato textual.
3. «cuyo subject es la tarea» no define coincidencia exacta, normalización ni prefijos: obligaría a inventar la regla de filtrado.
4. «con id, kind, verdict, anchor_state y created_at» no aclara si son nombres exactos del `ReviewDoc` o del JSON ni su serialización: obligaría a inventar el mapeo.
5. «se avisa a graph_ui con `deskops message send --to graph_ui`» no especifica asunto ni cuerpo: obligaría a inventar el mensaje.

## DRY-RUN

Lecturas previstas: `view.py`, `docs/deskops-ui.md`, `tests/test_view.py`, la implementación de `review status` y el modelo/almacén de `ReviewDoc`. Cambios previstos: extraer los recibos de la tarea reutilizando el cálculo de `anchor_state`; añadir `receipts` a la tarjeta de `view task` en JSON/YAML/texto; documentar el campo; añadir tests con un recibo creado mediante `deskops review record` en sandbox. Dependencias: lógica existente de `review status`, raíz desk de pruebas y CLI instalable. Validaciones futuras: los dos pytest de `Validation`; comprobación de lista poblada y vacía. No se ejecuta nada.

## FUTURO

`graph_ui` consumirá y dibujará el campo cuando exista. Un humano o nodo de cierre decidirá el contenido del aviso, ejecutará validaciones y commit, y confirmará el cierre.
