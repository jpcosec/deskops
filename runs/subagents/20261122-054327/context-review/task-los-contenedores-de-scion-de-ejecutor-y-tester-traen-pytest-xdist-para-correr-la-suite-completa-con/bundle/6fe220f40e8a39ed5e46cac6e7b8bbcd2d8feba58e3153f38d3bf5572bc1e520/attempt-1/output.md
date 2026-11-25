## REFORMULACION

Propósito: evitar que los contenedores de scion de ejecutor y tester corran la suite completa sin paralelismo y tarden más de una hora. Resultado: el venv de ambos roles incluye `pytest-xdist` y su prompt ejecuta la suite completa con `-n 4`. Repo: `deskops`. Límites: dentro, el runtime template o imagen de scion de deskops (`deskops/templates` o configuración de rol en `desk/roles`) y su test; fuera, “el resto”.

## AMBIGUEDADES

1. “en la imagen o en el paso de preparación del runtime template de scion”: no define dónde añadir la dependencia; obligaría a inventar si se modifica la imagen o el paso de preparación.
2. “p1: localizar dónde se arma el venv … (grep -rn 'venv\|pip install' en los templates de scion de deskops)”: no nombra archivos concretos; obligaría a inventar la ruta exacta del template o del rol.
3. “su test” y validación “tests/test_dispatch.py”: no queda claro que ese test compruebe `import xdist` en un contenedor; obligaría a inventar el alcance y el contenido del test.
4. “los roles executor y tester” frente a “Un ejecutor lanzado con el template”: el cierre no menciona tester; obligaría a inventar si tester también debe validarse.
5. “el prompt de esos roles corre la suite completa con -n 4”: no fija el comando exacto ni el archivo de prompt; obligaría a inventar la instrucción concreta.

## DRY-RUN

Lecturas previstas: TaskDoc, templates de scion, configuración de roles executor/tester y tests relacionados. Cambios previstos, sin ejecutar: añadir `pytest-xdist` al venv del contenedor; ajustar el prompt de ambos roles a la suite con `-n 4`; añadir o ajustar una comprobación de `import xdist`. Dependencias: construcción del runtime template, pip/red, pytest y el test de dispatch. Validaciones futuras: ejecutar el comando indicado; lanzar un contenedor con el template y comprobar `python -c 'import xdist'`; verificar la suite con `-n 4`. Nada se ejecuta aquí.

## FUTURO

Otro nodo ejecutor localizará los archivos, implementará el cambio y aportará el commit con `Task-Id`. Un validador comprobará el contenedor y la suite. Un humano decidirá la ubicación definitiva si imagen y runtime template compiten, y aceptará el cierre para tester.
