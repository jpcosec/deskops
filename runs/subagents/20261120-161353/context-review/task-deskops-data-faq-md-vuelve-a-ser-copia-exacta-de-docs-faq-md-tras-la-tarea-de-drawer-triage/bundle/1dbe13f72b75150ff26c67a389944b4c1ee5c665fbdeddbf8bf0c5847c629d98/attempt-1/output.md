REFORMULACION
Propósito: restaurar `deskops/data/faq.md` como copia exacta de `docs/faq.md` tras el integrate fallido de drawer-triage. Resultado: copia byte a byte, sin otros cambios, y los dos tests indicados pasan. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops` (cwd). Límites: solo `deskops/data/faq.md`; fuera `docs/faq.md` y cualquier otro archivo. No es agregado: es tarea ejecutable.

AMBIGUEDADES
1. La instrucción pide incluir “los rituales enrutados por el Board, las pills ligadas, los átomos ligados”, pero el TaskDoc trae `pills: []`, `atoms: []`, `current_node: ritual-execution`. Obligaría a inventar rituales, pills, átomos o sus contenidos.
2. “commit … y deskops advance”: no se detalla la invocación ni los argumentos de `deskops advance`. Obligaría a inventar la sintaxis o el gate exacto si no es estándar.

DRY-RUN
Lecturas: TaskDoc; `docs/faq.md`; `deskops/data/faq.md`; `tests/test_packaging.py`; `tests/test_large_doc_materialization.py`; `git status/diff` para confirmar alcance. Cambios previstos: `cp docs/faq.md deskops/data/faq.md`; commit solo de esa ruta con trailer `Task-Id: task-deskops-data-faq-md-vuelve-a-ser-copia-exacta-de-docs-faq-md-tras-la-tarea-de-drawer-triage`. Dependencias: cwd en raíz del repo, git, Python/pytest, `/tmp` escribible. Validaciones futuras: `cmp docs/faq.md deskops/data/faq.md` sin salida y exit 0; `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_packaging.py tests/test_large_doc_materialization.py`; `git diff --name-only` solo la ruta objetivo; luego `deskops advance`. Nada ejecutado.

FUTURO
El nodo de ritual/Board ejecuta o rechaza; git produce el hash de commit; deskops produce el estado de avance; un humano decide integrar/cerrar o abrir corrección si falla la validación. Si `docs/faq.md` cambia después, hará falta re-sincronizar.
