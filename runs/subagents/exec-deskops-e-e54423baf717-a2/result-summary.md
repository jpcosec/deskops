# Result (segundo intento)
- tests/closeout_graph_oracle.py: `transitions_from_v1(..., manual=False)` ahora filtra por `attributes.manual` y rellena `Transition.manual`.
- tests/test_closeout_gates.py::test_transitions_match_the_linked_index: aserciones de que la arista manual de ritual-testing existe con `manual=True`, coincide con el oraculo y no aparece en la lectura normal.
- tests/test_packaging.py: esperados 8 RelationDoc y 24 seeds de lifecycle.
- Validacion (python3.13 + PYTHONPATH): test_closeout_gates, test_packaging, test_lifecycle_graph, test_lifecycle_seed_drift, test_desk_sync: 57 passed y 1 failed (la regresion); tras el arreglo, el test fallado pasa (1 passed). grep: no hay otros tests que cuenten transiciones/seeds.
- No se corrio `deskops advance`. Sin commits.
