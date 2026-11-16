# Veredicto del tester deskops-t-38a62e54c041

Tarea: task-deskops-atoms-citations-escanea-las-citas-codigo-atomo-reporta-citas-rotas-y-atomos-sin-cita-y-las-l
Rol: tester independiente (claude). Nada commiteado. Evidencia: validation.log en este directorio.

**VEREDICTO: APROBADO**, con el riesgo de sldb anotado abajo. Ese riesgo hay que rutear antes de correr `--write` en un repo real.

## Contrato frente a la entrega

- **Gramática** (`deskops/services/atoms.py:105-148`):
  - El bloque `Atoms:` se lee con ast, solo del docstring de módulo. Los ids cumplen `^atom-[a-z0-9-]+$` en columna 0.
  - El bloque termina en una línea vacía, en una línea que no es un id o en el fin del docstring.
  - En los demás archivos, `# Atom: <id>` usa la misma regex.
  - Se escanean los archivos de `git ls-files`; los que no son UTF-8 se saltan.
  - Lo cubren los tests y lo comprobé en el sandbox.
  - Matiz menor (`atoms.py:131`): una segunda línea `Atoms:` abre otro bloque. El contrato no lo prohíbe.
- **--check** (`deskops/cli/commands/atoms.py:254`):
  - Sale con 1 si hay al menos una cita rota, aunque también haya huérfanos.
  - Con solo huérfanos sale con 0 y los lista como `Warning:`.
  - Verificado en el sandbox y en los tests.
- **--write** (`atoms.py:947-1008`):
  - Crea el RelationTypeDoc `cited_by` si no existe, y un RelationDoc por cita (source = ruta, target = `AtomDoc:<id>`) por doc_access/sldb.
  - Es idempotente: una segunda pasada da 0 creadas.
  - Borra las relaciones que ya no tienen cita en el código.
  - Verificado en el sandbox.
- **show atom** (`deskops/cli/commands/operations.py:181-185, 345-347`):
  - Agrega la sección `Cited by:`, leída de los RelationDoc, tal como piden las precisiones del preflight.
  - Un átomo sin citas se muestra igual que antes.
- **Archivos fuera de `files`**: los cuatro son necesarios para el contrato.
  - `commands/atoms.py`: el handler de todos los verbos `atoms`.
  - `commands/operations.py`: la sección "Cited by:" que exige done_when.
  - Los 2 goldens de ayuda: done_when pide "goldens de ayuda al día".
  - `registry.py` sí está en `files`.
- **Goldens**: solo cambian `deskops_atoms.txt` y el nuevo `deskops_atoms_citations.txt`. No quedó ningún golden reescrito de más.
- **Reproducción**: con el código de HEAD (copia en /dev/shm), `test_atom_citations.py` falla en la colección (no existen `comment_citations`/`docstring_citations`), rc=2.
- **Tests** (de a uno, sin lock):

  | Archivo | Resultado |
  |---|---|
  | test_atom_citations | 5 passed |
  | test_output_goldens | 7 passed |
  | test_cli_help_examples | 13 passed |
  | test_graph_checks | 4 passed |
  | test_cli | 102 passed |

  Todos con rc=0.
- **Repo real**: `atoms citations --check --root .` da 0 citas y 170 átomos huérfanos (aviso), rc=0. No corrí `--write` en el repo real.

## Punto clave: aristas en el grafo de sldb

Lo que vi en el sandbox tras `--write`:

- `sldb stores check` da PASS.
- `deskops doctor` dice "healthy".
- `deskops graph missing` está limpio.
- `sldb edges check` sale con rc=1, con un error `[edges/invalid] relation 'cite-…': source '<ruta>' is not a tracked document` por cada cita.
- `sldb edges show AtomDoc:<id> --to` no muestra ninguna arista `cited_by`.
- Al borrar las citas, edges check vuelve a dar OK. Los errores los introduce exactamente esta entrega.

Por qué lo apruebo igual:

- Las "Precisiones del preflight 1" fijan el mecanismo de forma literal: un RelationDoc por cita, con sujeto la ruta del archivo, y `Cited by:` leído de esos RelationDoc.
- done_when pide tests, show atom y goldens. No pide aristas recorribles ni un `edges check` limpio.
- Los chequeos que usa deskops (stores check, doctor, graph missing) quedan limpios. Ningún gate de deskops corre `sldb edges check` (busqué con grep en deskops/, desk/rituals, docs/ y .github).
- La causa es una limitación de sldb: una ruta de archivo no es un extremo válido de RelationDoc.
- Aun así, el goal ("registra una arista cited_by … en el grafo de sldb") queda cumplido solo como documento, no como arista indexada.

## Riesgos y seguimiento antes del cierre o del uso real

1. **Gap de sldb a rutear al inbox de sldb**, según AGENTS.md: un nodo para archivos versionados (por ejemplo `file:<path>`) válido como extremo de RelationDoc. Hasta entonces, `--write` en un repo real deja un error de `sldb edges check` por cita, y las citas no se pueden recorrer como aristas.
2. `scan_citations` también escanea docs y Markdown. Un ejemplo `# Atom: atom-x` en la documentación cuenta como cita, como especifica el contrato.
3. Ubicación `desk/citations/` y nombre `cite-<sha1[:12]>`: los eligió el ejecutor; son reversibles.
4. La suite completa no la corrí, por orden del integrador.
