**REFORMULACION**

Encargo ejecutable en el repo `deskops`: modificar el cálculo del tip en `deskops/integrate.py` para que, si entre el commit de closeout y `HEAD` solo hay commits acotados a `desk/`, `.sldb/` o `runs/`, integre usando `HEAD`; si hay código, tests o docs, mantiene el closeout. Debe emitir `tip extendido a <sha>: solo commits de desk`, empujar la punta y añadir tests en `tests/test_integrate.py` más CHANGELOG. Límite: solo ese cálculo y sus tests; no otros gates. Validación: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py`.

**AMBIGUEDADES**

1. «la punta local (HEAD de la rama)» no nombra rama; obligaría a inventar si es la rama actual, una rama de tarea o un SHA concreto.
2. «nada de código, tests ni docs» frente a «CHANGELOG»: obligaría a decidir si `CHANGELOG.md` cuenta como doc permitido o bloquea la extensión.
3. «empuja la punta» no fija remoto, ref ni si hay force; obligaría a inventar `origin/main`, la rama de destino y el comportamiento ante divergencia.
4. «una referencia colgante en otra tarea» no define el dato exacto del grafo; obligaría a inventar cómo construir el fixture inválido y qué gate lo detecta.
5. «find_tip o el cálculo del tip» deja abierto el punto de cambio; obligaría a elegir función y firma sin más contexto.

**DRY-RUN**

Lecturas: `deskops/integrate.py` (cálculo actual del tip y push), `tests/test_integrate.py`, CHANGELOG y quizá utilidades de git/gates. Cambios previstos: helper que obtiene `git diff --name-only <closeout>..HEAD`, valida rutas permitidas y devuelve `HEAD` o closeout; mensaje de salida; tests de closeout con referencia colgante corregida por commit de desk y de commit posterior que toca `src/`; entrada de CHANGELOG. Dependencias: git, pytest y el gate de grafo existente. Validaciones futuras: ejecutar el pytest indicado, comprobar ambos escenarios y revisar que no se alteran otros gates.

**FUTURO**

El coordinador decide si acepta el push y resuelve divergencias; el owner del gate de grafo confirma que la referencia corregida es válida; CI/revisión humana valida el CHANGELOG y el commit con `Task-Id`.
