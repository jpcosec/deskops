## REFORMULACION

El encargo es producir, en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, `docs/config-vs-code.md`: medir líneas Python de `deskops/` por directorio de primer nivel en la base `827f3db7` y en el HEAD de `main` al medir, anotando ambos totales y el hash de cierre; inventariar la configuración declarada (modelos, `RelationDoc`, `RuleDoc`, `ViewDoc`, semillas y configuración de grafo) con su ubicación; y listar cada archivo de `git ls-files deskops` una sola vez como configuración declarada en Python, código justificado con razón o deuda con tarea/nota que la retira. Además: entrada en `CHANGELOG.md` bajo `[Unreleased]` y test `tests/test_config_vs_code_doc.py`. Límites: no cambiar código para reducir líneas; la tarea no arranca hasta que la dependencia fije `N`; la medición cuenta solo `.py`, la lista cubre todos los archivos.

## AMBIGUEDADES

1. “Entra: docs/config-vs-code.md y CHANGELOG.md. No entra: cambiar codigo” frente a “5) Test simple que todo archivo de deskops/ aparezca en el doc (tests/test_config_vs_code_doc.py)”. Obliga a inventar si crear el test está dentro del alcance o si “cambiar código” solo excluye código productivo.
2. “todo lo demas -> codigo justificado (con la razon de P4 si aplica, o una frase propia) o deuda (con la tarea o nota que lo retira)”. No se enumera qué archivo restante es justificado o deuda ni qué tarea/nota concreta lo retira; obliga a inventar la clasificación, la frase de razón y los identificadores de deuda.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, `desk/drawer/plans/deskops-como-config/dag.yaml`, `decisiones.md`, la tarea dependiente que fija `N` y el estado del repo. Crearía un worktree temporal en `827f3db7` solo para medir y lo retiraría; mediría el HEAD de `main`; ejecutaría el comando `find deskops -name '*.py' | xargs wc -l`, agrupando con `awk` por primer componente bajo `deskops/`; obtendría la lista con `git ls-files deskops`; redactaría el doc, añadiría la línea de CHANGELOG y el test. Dependencias: `N`, el hash de cierre, los hechos de CC33/CC34 y la base `827f3db7`. Validaciones futuras: `pytest -q tests/test_config_vs_code_doc.py` y que el total del HEAD sea menor que `N`.

## FUTURO

La tarea de decisión de JP fija `N`; el ejecutor anota el hash de cierre. Si el total no baja de `N`, reporta la diferencia y abre tareas de deuda; la revisión humana decide si el inventario y las justificaciones son aceptables.
