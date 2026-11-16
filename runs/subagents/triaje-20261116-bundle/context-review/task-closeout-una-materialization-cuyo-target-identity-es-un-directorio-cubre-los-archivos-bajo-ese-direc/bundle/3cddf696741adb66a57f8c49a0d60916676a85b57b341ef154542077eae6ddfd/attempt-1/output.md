# REFORMULACION

Nodo ejecutable de tipo `task.code` en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: que la compuerta de cobertura de materializations acepte como cubierto un archivo cambiado cuando alguna materialization de la tarea declara un `target_identity` que es ese archivo **o un directorio que lo contiene** (hoy solo hay match exacto, lo que obligó a crear 62 materializations para 66 archivos en sldb). Resultado: función `target_covers(target, path)` junto a la cobertura en `deskops/services/closure.py`, usada por la compuerta, más un test de prefijo con separador; si `deskops graph missing` reporta `missing_declared_target` para un target directorio, se envía nota a sldb y la tarea no espera respuesta. Límites: no se modifica sldb ni la compuerta de átomos; normalización POSIX relativa, sin symlinks, sin barra final, case-sensitive; no exige que el directorio exista. Cierre: test verde, y si el paso 4 falló, nota enviada y citada en el commit.

# AMBIGUEDADES

1. Nombre de la función: el Scope dice «la funcion se llama target_covers(target, path)» y el Implementation Path dice «Funcion covers(target, path) por prefijo». Obliga a inventar cuál es el nombre canónico.
2. Ubicación: «vive junto a la cobertura de materializations en closure.py (se ubica por nombre, los numeros de linea son orientativos)» frente a «deskops/services/closure.py:1325-1340»; obliga a decidir si el rango manda.
3. Nota a sldb: «exito = nota entregada» no define cómo se comprueba la entrega; obliga a inventar evidencia (exit code, id de mensaje).
4. Alcance de la nota: «si el paso 4 fallo» no aclara si "fallo" incluye fallo del comando o solo del reporte `missing_declared_target`.
5. Prefijo: «path empieza con target + '/'» no dice cómo tratar targets con `./` inicial o rutas absolutas; obliga a inventar normalización extra.

# DRY-RUN

Lecturas: `deskops/services/closure.py` (bloque de cobertura de materializations, localizado por nombre), `tests/test_materialization_targets_outside_package.py`, utilidades de normalización de rutas existentes. Cambios previstos: nueva `target_covers` por prefijo con separador; sustitución del match exacto en la compuerta; test `pkg/sub` cubre `pkg/sub/a.py` y no `pkg/subzero.py`. Dependencias: helpers de rutas del repo, fixture de repo temporal ya presente. Validaciones futuras (no ejecutadas): los tres pytest del TaskDoc, la suite completa `-n 4`, y comparación de fallas en worktree limpio de `origin/main`; `graph missing` en desk sandbox (raíz desechable, no `desk/` real) y, si procede, `deskops message send --to sldb`.

# FUTURO

Un humano commitea con mensaje descriptivo y decide si la nota basta como cierre; el equipo de sldb decide si `declared_target_nodes` acepta directorios; CI confirma ausencia de fallas nuevas.
