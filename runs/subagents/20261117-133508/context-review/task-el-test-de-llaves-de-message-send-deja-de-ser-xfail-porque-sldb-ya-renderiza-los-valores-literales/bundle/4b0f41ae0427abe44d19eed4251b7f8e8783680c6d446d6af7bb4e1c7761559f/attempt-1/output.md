## REFORMULACION

Propósito: devolver la suite de deskops a verde tras el arreglo de sldb d49f6ddc, que ya renderiza literales los valores de los campos. Resultado: `test_message_send_keeps_braces_in_the_body_literal` deja de ser `xfail(strict=True)` y sus 4 variantes pasan contra el sldb instalado; se borra `SLDB_JINJA_VALUE_NOTE` si queda sin uso. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `tests/test_message_cli.py`; quedan fuera el código de deskops y de sldb y el resto de tests.

## AMBIGUEDADES

1. Cita: «Entra: el decorador xfail y la constante SLDB_JINJA_VALUE_NOTE en tests/test_message_cli.py». El bloque de comentario que precede a la constante explica la causa ya resuelta y quedaría obsoleto; decidir si se elimina obliga a inventar el alcance exacto.
2. Cita del átomo: «recorded in a descriptive git commit», frente a Done When: «git diff solo toca ese archivo». No se especifica si este nodo debe commitear o solo dejar el diff; habría que inventar el protocolo de cierre.
3. Cita: «Confirmar que el sldb que importa el venv incluye d49f6ddc (git -C /mnt/ssd/herramientas/sldb merge-base --is-ancestor d49f6ddc HEAD)». Comprobar el HEAD del repo no prueba qué versión importa el venv si la instalación no es editable; habría que inventar cómo resolver una discrepancia.

## DRY-RUN

Lecturas: TaskDoc, `tests/test_message_cli.py` (decorador, constante y comentario), átomos ligados y `git -C /mnt/ssd/herramientas/sldb merge-base --is-ancestor d49f6ddc HEAD`.

Cambios previstos: quitar `@pytest.mark.xfail(...)`, borrar `SLDB_JINJA_VALUE_NOTE` y, sujeto a la ambigüedad 1, el comentario asociado. Ningún otro archivo.

Dependencias: `pytest`, venv `../.venv`, sldb instalado con d49f6ddc, entorno `PYTHONPATH`/`TMPDIR`.

Validaciones futuras: `pytest -q tests/test_message_cli.py`, inspección de `git diff`/`status` limitada a ese archivo y, si se decide, commit descriptivo.

## FUTURO

Decisión humana sobre el comentario obsoleto y sobre si el commit corresponde a este nodo o al ritual de cierre. El tester/CI valida después que la suite completa de deskops queda verde.
