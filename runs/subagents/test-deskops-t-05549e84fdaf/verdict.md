# Veredicto del tester deskops-t-05549e84fdaf

Tarea: task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0
Entrega: deskops-e-bae0befe2582 (sin commitear)

**VEREDICTO: APROBADO**

## Contrato vs diff

- deskops/cli/commands/desk.py:231-232 (HEAD): se quita el `if` que agregaba `desk/reviews/` a `missing_desk_files`, y nada más. Era el código que pedía quitar el preflight 1. No quedan menciones de `reviews` en desk.py ni en doctor.py.
- tests/fixtures/golden/scaffold/update.json:44: el golden nombraba `desk/reviews/`, así que el cambio correspondía, y es solo esa línea. test_scaffold_golden.py pasa.
- tests/test_cli.py:3162-3202: el test nuevo hace lo que pide el preflight: tmp_path, subprocess, `git init -b main`, `deskops init .`, add/commit, clone a otro directorio y `desk update --root <clon>` sin --apply. El helper `run` exige rc 0. Además comprueba que la salida no nombre desk/reviews/, que el dry-run no cree la carpeta y que `review record` cree `desk/reviews/task-x/owner-1.md` (done_when: "el primer recibo crea desk/reviews/"). No usa .gitkeep: se respeta el "no entra".
- review.py: confirmado que el escritor crea la carpeta. `out.mkdir(parents=True, exist_ok=True)` en deskops/services/review.py:459 y el test nuevo lo ejercita de punta a punta.

## Archivos fuera de `files`

- tests/test_review_doc.py:172-182: el test viejo afirmaba que `desk update --apply` recrea desk/reviews, justo el comportamiento que la tarea quita, así que se rompía legítimamente. Ahora el test borra la carpeta, `--apply` da rc 0 y la salida no nombra desk/reviews/. Afirma la regla nueva y no debilita nada: el comportamiento viejo dejó de ser deseado. `test_init_creates_the_reviews_directory` sigue intacto.
- tests/test_legacy_task_states.py:374-389: el test usaba desk/reviews solo como ejemplo de "estructura faltante" para probar que `--apply` sigue reparando con un documento inválido (g2/g4b). Cambiar a desk/drawer (todavía se exige y se re-andamia) mantiene la intención entera: sigue afirmando "Missing desk structure", "Scaffolded", el directorio recreado, "Updated store derived indexes" y que no hay "Skipped".

## Validación (validation.log)

| archivo | resultado | rc |
|---|---|---|
| tests/test_cli.py | 102 passed | 0 |
| tests/test_output_goldens.py | 7 passed | 0 |
| tests/test_review_command.py | 21 passed | 0 |
| tests/test_scaffold_golden.py | 3 passed | 0 |
| tests/test_review_doc.py | 19 passed, 1 xfailed (xfail strict que ya existía, G_SLDB_ANCHORS) | 0 |
| tests/test_legacy_task_states.py | 46 passed | 0 |

Reproducción: en una copia `git archive HEAD` en /dev/shm con el test_cli.py nuevo, el test falla con el desk.py de HEAD (rc 1, "Missing desk structure: desk/reviews/", tests/test_cli.py:3177). En la misma copia, con el desk.py de la entrega, pasa. Copia ya borrada.

No corrí la suite completa: según el brief, la corre el integrador.

## Riesgos / observaciones

- `desk update --apply` ya no recrea desk/reviews/ en un desk que la perdió. Es lo buscado, porque los escritores la crean al escribir el primer recibo. Cualquier lector que asuma que la carpeta existe tendría que tolerar su ausencia; el ejecutor dice que `review status` usa `exists()`. No lo audité más allá de que los tests de review pasan.
- El test nuevo importa `os` dentro de la función. Es un detalle de estilo, no bloquea.
- La suite completa del ejecutor tiene 3 fallas de entorno (pytest/python fuera del PATH). Él dice que fallan igual en origin/main. No lo verifiqué; queda para el integrador.
