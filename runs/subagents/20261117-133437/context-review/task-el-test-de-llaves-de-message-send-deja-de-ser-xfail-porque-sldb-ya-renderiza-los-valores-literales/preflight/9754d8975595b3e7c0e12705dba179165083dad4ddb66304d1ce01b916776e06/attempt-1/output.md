## REFORMULACION

Propósito: retirar el `xfail(strict=True)` del test de llaves de `message send` porque el sldb instalado ya renderiza literales los valores de campo (d49f6ddc). Resultado: `tests/test_message_cli.py::test_message_send_keeps_braces_in_the_body_literal` pasa como test normal, sus 4 variantes pasan, y `SLDB_JINJA_VALUE_NOTE` se elimina si queda sin uso. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo ese archivo de test; fuera código de deskops, sldb y demás tests.

## AMBIGUEDADES

1. «se borra si ya no se usa»: exige comprobar referencias restantes; habría que inventar el criterio (¿solo en el archivo? ¿en todo el repo?) y qué hacer si aparece otro uso.
2. «sus 4 variantes pasan»: no se enumeran; habría que inventar cuáles son o deducirlas de la parametrización del test.
3. «Confirmar que el sldb que importa el venv incluye d49f6ddc (git -C ... merge-base --is-ancestor d49f6ddc HEAD)»: el comando verifica el repo, no qué paquete importa el venv; habría que inventar cómo comprobar la procedencia real del import.
4. «atom-code-changes-close-with-tests-and-commit» frente a Validation/Done When, que no mencionan commit: habría que inventar si el ejecutor debe commitear y con qué mensaje.
5. «lineas 359-365»: números potencialmente desactualizados; habría que inventar la localización exacta si no coinciden.

## DRY-RUN

Lecturas previstas: `tests/test_message_cli.py` (decorador xfail, constante, parametrización), estado git de sldb y del repo deskops, e identificación del intérprete del venv. Cambios previstos: eliminar el decorador/reason del test y borrar `SLDB_JINJA_VALUE_NOTE` si no tiene más referencias. Dependencias: `/mnt/ssd/herramientas/sldb` con d49f6ddc y `../.venv/bin/python`. Validaciones futuras: ejecutar el pytest indicado, confirmar ausencia de xfail/XPASS y que `git diff --name-only` solo liste `tests/test_message_cli.py`. Nada se ejecuta ahora.

## FUTURO

Otro nodo (tester/verificador) ejecutará la suite en el entorno real y comprobará el diff; un humano u otro nodo decidirá el commit y el cierre de la tarea.
