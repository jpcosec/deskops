REFORMULACION
Propósito: alinear los tests de review de deskops con el cambio de sldb 477d1bc0, que hace que `create_document` pinnee las anclas a documentos. Resultado: los tres tests citados esperan `doc:TaskCodeDoc:<id>@sha256:<64 hex>` en el campo `subject` de recibos recién creados y pasan contra sldb de origin/main; solo cambian `tests/test_review_record.py` y `tests/test_review_command.py`, incluido el docstring que afirma que `create_document` no pinnea. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo aserciones sobre `subject` y ese docstring; no se toca `deskops/`, sldb ni otros tests; si falla por otra causa, se para.

AMBIGUEDADES
1. «Entra: solo las aserciones sobre el campo subject de los recibos (y el docstring…)» frente a «pasa a exigir el valor pinneado… re.fullmatch(…)». `tests/test_review_command.py` no importa `re`; habría que inventar si añadir `import re` entra en alcance.
2. «git diff --stat (solo los dos archivos de test)» y Done When no mencionan commit, pero el átomo dice «A task that modifies code is not closed until … descriptive git commit». Habría que inventar si se requiere commit, su mensaje y momento.
3. «contra el sldb instalado (origin/main con 477d1bc0)»: la validación no comprueba esa versión. Habría que inventar si verificar o reinstalar sldb si el entorno difiere.

DRY-RUN
Lecturas: TaskDoc, los dos archivos de test y átomos. Cambios previstos: en `test_review_record.py`, corregir el docstring y cambiar la aserción inicial de `test_subject_is_pinned_and_the_anchor_is_intact` y las dos de `subject` de `test_a_short_selector…` a `re.fullmatch`, usando `re.escape` para el id completo; en `test_review_command.py`, añadir `import re` si se admite y cambiar la aserción de `subject` del recibo preflight a `re.fullmatch`. Dependencias: sldb 477d1bc0 instalado, pytest y el entorno `../.venv`. Validaciones futuras: ejecutar los dos pytest indicados y `git diff --stat`, comprobando que solo cambian los dos tests. Sin ejecutar nada.

FUTURO
Otro nodo o un humano decide el commit de cierre si aplica el átomo; el responsable del entorno garantiza la versión de sldb; el closeout verifica el diff y las validaciones.
