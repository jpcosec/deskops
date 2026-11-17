# Veredicto del tester deskops-t-e83f943bfb0b

Tarea: task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi
Entrega: ejecutor deskops-e-c5247d70fb6a (cambios sin commitear)

**VEREDICTO: APROBADO**

## Comprobaciones

1. **git rm**: el índice tiene 128 borrados, todos dentro de los 5 directorios del scope. Cada uno coincide con lo que HEAD tenía: workspace-documental 45/45, gates-por-tipo 5/5, deskops-ui 6/6, deskops-como-config 5/5 y desk/drawer/tasks/workspace-documental 67/67. No hay otros cambios en el índice. desk/drawer/plans/ ya no existe en el árbol.
2. **Fixture** tests/fixtures/plans/gates-por-tipo/: tiene dag.yaml (cabecera, gates, external_references y los nodos ROOT→PC01→GC01, GC02 y GC03) y brief.md. Los tests nombran ROOT, GC01 y GC03. GC02 tiene que estar porque GC03 depende de él (`depends_on: [GC02]`), y PC01 porque es el padre. Es el mínimo coherente. PLAN_SRC apunta al fixture y las rutas del sandbox no cambiaron.
3. **Ayuda**: registry.py y los 3 goldens (deskops_review, deskops_review_node y deskops_review_status) usan `desk/drawer/plans/mi-plan N01` o `desk/drawer/plans/mi-plan`, como pide la precisión (3)/(4).
4. **Docs**: operator-manual.md:1137 pasó a `mi-plan N01`. deskops-ui.md:209 tiene el texto exacto de la precisión (5).
5. **Tests**, uno por archivo, con PYTHONPATH al checkout, TMPDIR=/dev/shm y sin lock. Todos terminaron con rc=0:
   - test_review_command.py: 29 passed
   - test_review_doc.py: 22 passed, 1 xfailed
   - test_cli_help_examples.py: 13 passed
   - test_output_goldens.py: 7 passed
6. **graph missing**: pasa de 35 a 50. El diff contra graph-before.txt da 15 entradas nuevas y 0 perdidas. Las 15 son `missing_declared_target` hacia archivos de los 4 planes borrados, y vienen exactamente de los 8 TaskDocs que describe el ejecutor. Según la decisión del coordinador, no aparece ninguna entrada nueva fuera de esas.
7. **grep** de rutas a los planes en deskops, tests, docs, README.md, AGENTS.md y .claude:
   - tests/test_review_command.py: solo rutas dentro del sandbox temporal.
   - tests/test_review_doc.py: solo literales de validación (precisión 2).
   - Además, el contenido del propio fixture (comentario de origen, frozen_note, external_references y brief.md) nombra rutas del drawer. Son datos copiados del plan. Comprobé que ningún código de deskops lee `external_references`, así que no son rutas vivas. No lo cuento como hallazgo.

## Observaciones (no bloquean)

- La entrada que esta misma tarea añade a graph missing (su `files` declara gates-por-tipo/dag.yaml) sigue ahí después del cierre, salvo que se edite el `files`. El brief la cuenta entre las 15 aceptadas.
- No corrí la suite completa, como pide el brief.
