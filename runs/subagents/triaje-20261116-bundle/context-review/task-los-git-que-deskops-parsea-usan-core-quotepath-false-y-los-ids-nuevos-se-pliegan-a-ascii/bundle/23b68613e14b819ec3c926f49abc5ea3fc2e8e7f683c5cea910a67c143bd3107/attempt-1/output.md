REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: evitar que las rutas citadas por git y los ids acentuados rompan deskops. Resultado: helper único `ascii_slug` en `deskops/slugs.py` (NFKD + regla actual), usado por compiler.py, doc_access.py y drawer.py; toda llamada git cuya salida se parsea recibe `-c core.quotepath=false` o `-z`; los ids existentes acentuados siguen resolviendo sin renombrar; test `tests/test_ascii_ids.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no migrar ni renombrar ids commiteados, no tocar el hook externo de worktrees, no cambiar la longitud máxima, no cubrir llamadas git dinámicas fuera del grep literal.

AMBIGUEDADES
1. Goal: “pasa `-c core.quotepath=false` o usa -z”; Done When: “`grep -rn quotepath deskops/` muestra la opcion en las llamadas git parseadas”. Si se usa `-z`, no aparece `quotepath`; obligaría a inventar si la validación exige quotepath o acepta `-z`.
2. Scope: “cualquier otra llamada git con salida parseada que muestre `grep -rn '"git"' deskops/`”; Implementation Path: “llamadas armadas dinamicamente que no aparezcan con grep … quedan fuera”. Obligaría a decidir si una llamada construida por variables pero detectada por grep cuenta.
3. Test: “un archivo sin trackear con nombre acentuado en .sldb no rompe el parseo de git del cierre”. No define ubicación/fixture exacto ni qué salida de cierre se simula; obligaría a inventar el montaje.
4. Goal: “Los ids nuevos que se derivan de un titulo se pliegan a ASCII”; no aclara si un `id` explícito acentuado se pliega. Obligaría a decidir si solo se sanea el slug derivado o todo id nuevo.

DRY-RUN
Lecturas: los cuatro módulos, tests relevantes, `grep -rn '"git"' deskops/` y `grep -rn quotepath deskops/`. Cambios previstos: crear `deskops/slugs.py`; reemplazar `_slugify`/`slugify`/`_slug` por el helper; añadir opciones git en closure.py y demás coincidencias; crear `tests/test_ascii_ids.py` con sandbox de desk. Dependencias: sldb, CLI deskops, TaskDoc, pytest. Validaciones futuras: los cuatro comandos del TaskDoc; suite completa y comparación de fallas en worktree limpio de origin/main.

FUTURO
Un nodo ejecutor implementa y ejecuta las validaciones; un humano o closeout decide aceptar fallas baseline, registrar evidencia y hacer el commit descriptivo.
