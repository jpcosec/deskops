## REFORMULACION

Encargo: añadir al CLI de `deskops` (repo `/mnt/ssd/proyectos/SLDB_1/deskops`) el verbo `atoms citations [--check] [--write] --root .`. Escanea citas código→átomo: bloque `Atoms:` en docstrings de módulo `.py` (ids con regex `^atom-[a-z0-9-]+$`, columna 0, termina en línea vacía, fin de docstring o línea no válida) y `# Atom: <id>` en el resto de archivos de `git ls-files` (saltando no-UTF-8). `--check` sale 1 si hay cita rota y 0 con solo huérfanos (avisados). `--write` crea RelationTypeDoc/RelationDoc `cited_by` (sujeto=ruta, objeto=id) y `show atom` lista citadores en sección `Cited by:`. Entra: `services/atoms.py`, `cli/registry.py`, tipo de relación, `graph/checks.py`, tests. No entra: repos de AntonIA ni renombrar átomos.

## AMBIGUEDADES

1. «sujeto la ruta del archivo» — no fija ruta relativa a `--root` ni absoluta; obligaría a inventar formato almacenado y comparación en `show atom`.
2. «--check sale con 1 … avisa (exit 0)» — no define comportamiento ni precedencia si se combinan `--check` y `--write`; obligaría a inventar semántica conjunta.
3. «el tipo de relacion cited_by si hay que declararlo» — condicional sin esquema ni API concreta; obligaría a inventar estructura y detección de existencia.
4. «show atom agrega una seccion 'Cited by:'» — sin formato exacto (orden, viñetas, rutas); obligaría a inventar salida y goldens.
5. «avisa … por cada atomo sin cita» — sin formato ni orden de avisos; obligaría a inventar texto de salida.

## DRY-RUN

Lecturas: TaskDoc, `git ls-files`, archivos para parsear con `ast`/regex, API de sldb para tipos/relaciones. Cambios previstos: parser en `atoms.py`; verbo y ayuda en `registry.py`; declaración `cited_by`; listado en `show atom`; chequeo en `graph/checks.py`; `tests/test_atom_citations.py` con sandbox (cita válida, rota exit 1, huérfano aviso). Dependencias: sldb, git, pytest del venv. Validaciones futuras: los cinco comandos pytest listados y comparación de fallas contra worktree limpio de `origin/main`.

## FUTURO

Otro nodo ejecuta la implementación y la suite; produce el informe de fallas preexistentes frente a `origin/main`. Un humano decide si procede declarar el tipo de relación en sldb y revisa los goldens de ayuda actualizados.
