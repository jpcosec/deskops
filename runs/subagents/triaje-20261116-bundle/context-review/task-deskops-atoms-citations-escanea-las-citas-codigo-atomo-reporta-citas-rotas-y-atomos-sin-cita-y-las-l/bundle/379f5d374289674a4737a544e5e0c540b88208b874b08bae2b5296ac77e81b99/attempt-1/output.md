REFORMULACION

Propósito: añadir a deskops un verbo que audite las citas código→átomo. Resultado: `deskops atoms citations [--check] [--write] --root .`, que escanee bloques `Atoms:` del docstring de módulo en `*.py` y `# Atom: <id>` en el resto de archivos versionados; `--check` debe salir 1 ante citas rotas y 0 con huérfanos avisados; `--write` debe crear aristas `cited_by` módulo→átomo y hacer que `deskops show atom <id>` liste citadores. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `deskops/services/atoms.py`, `deskops/cli/registry.py`, posible relación `cited_by`, `deskops/graph/checks.py` y tests; no cambiar repos de AntonIA ni renombrar átomos.

AMBIGUEDADES

1. “en archivos no Python como comentario '# Atom: <id>'” frente a “el resto de archivos versionados (git ls-files)”: no queda claro si se escanean todos los no-Python o solo ciertos formatos. Obligaría a inventar la lista de extensiones y el tratamiento de Markdown/JSON/YAML.
2. “Cada repo tiene su propio tests/test_atoms_citados.py” frente a “tests/test_atom_citations.py”: hay dos nombres posibles para el test nuevo. Obligaría a inventar cuál es el path exigido.
3. “--write registra una arista cited_by módulo->atomo […] por la API de sldb”: no se define idempotencia ni qué ocurre si la arista ya existe. Obligaría a inventar si se reemplaza, duplica o ignora.
4. “show atom agrega una seccion 'Cited by:' con las rutas”: no se especifica orden ni formato exacto. Obligaría a inventar presentación y criterio de ordenación.

DRY-RUN

Lecturas: TaskDoc, átomos enlazados, `deskops/services/atoms.py`, `deskops/cli/registry.py`, `deskops/graph/checks.py`, tests existentes, registro de relaciones y goldens de ayuda. Cambios previstos: parser de citas, flags/ayuda del verbo, tipo `cited_by` si falta, creación de RelationDoc, sección en `show atom`, chequeo de citas rotas y tests con sandbox. Dependencias: `git ls-files`, API de sldb, fixtures CLI y goldens. Validaciones futuras: los cuatro pytest indicados, suite completa con `-n 4`, comparación de fallas en worktree limpio de `origin/main` y registro en el informe. No se ejecuta nada.

FUTURO

Otro nodo implementará y ejecutará pruebas/commit; un humano resolverá los nombres y formatos ambiguos y decidirá el cierre.
