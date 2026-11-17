# Veredicto del tester deskops-t-a963945f7a8c

Tarea: task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo

## Diff
- `deskops/models/review.py`: único cambio `SUBJECT_REF_PATTERN` `[A-Za-z0-9_-]+` -> `[A-Za-z0-9_.-]+`. El prefijo `[^\s#]+` y la clase sin espacio ni `#` se mantienen, así que espacio y segundo `#` siguen rechazados. Nada más cambia (REVIEW_ID_PATTERN ya admitía `.`, según preflight-1).
- `tests/test_review_doc.py`: acepta `#node:WS13.1`; rechaza `WS 13` y `WS13#x` (parametrizado, verifica que el error menciona subject_ref).
- `tests/test_review_command.py`: `review node` sobre un dag.yaml sandbox con nodo `WS13.1` escribe `review-deskops-con-punto-ws13.1-node-1` con subject_ref `...dag.yaml#node:WS13.1` y verdict pending.
- Cumple las precisiones de preflight-1 y bundle-1 (fixtures lifecycle_desk/fake_pi, plan en desk/drawer/plans/<nombre>/ del sandbox, casos de rechazo indicados).

## Validación (validation.log)
- tests/test_review_doc.py: 22 passed, 1 xfailed (xfail strict preexistente G_SLDB_ANCHORS).
- tests/test_review_command.py: 26 passed.
- Reproducción con review.py de HEAD (copia en /dev/shm, ya borrada): los 2 tests de punto FALLAN (string_pattern_mismatch); los 2 de rechazo pasan en ambos lados (guardas de regresión, como corresponde).

No se corrió review node sobre planes reales ni la suite completa (fuera del encargo).

VEREDICTO: APROBADO
