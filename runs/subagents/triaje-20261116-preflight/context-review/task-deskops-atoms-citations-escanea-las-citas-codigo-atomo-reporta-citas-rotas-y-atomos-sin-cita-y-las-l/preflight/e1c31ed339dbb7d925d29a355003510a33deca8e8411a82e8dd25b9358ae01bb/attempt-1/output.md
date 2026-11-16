## REFORMULACION
Propósito: dotar a deskops de un verbo que audite citas código→átomo. Resultado: `deskops atoms citations [--check] [--write] --root .`, con detección de citas rotas, aviso de átomos sin cita y arista `cited_by` consultable desde `show atom`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `atoms.py`, `registry.py`, relación/checks y tests; no modificar repos de AntonIA ni renombrar átomos.

## AMBIGUEDADES
1. «--check sale con 1 si un id citado no existe en desk/atoms y avisa (exit 0) por cada atomo sin cita»: no aclara la precedencia si coexisten cita rota y huérfanos; obliga a inventar el código de salida global.
2. «registra una arista cited_by modulo->atomo»: no define tipo, esquema ni dirección persistida; obliga a inventar el `RelationDoc` y su semántica.
3. «bloque 'Atoms:' del docstring de modulo» y «un id por linea en columna 0»: no define terminador, comentarios, espacios ni ids inválidos; obliga a inventar la gramática.
4. «'# Atom: <id>' en el resto de archivos versionados (git ls-files)»: no excluye binarios, generados ni ficheros sin texto; obliga a inventar filtros.
5. «show atom lista los citadores tras --write»: no fija formato ni si lee el grafo persistido; obliga a inventar la salida.

## DRY-RUN
Nodo ejecutable, no agregado. Lecturas: TaskDoc, `services/atoms.py`, `cli/registry.py`, `graph/checks.py`, tests y estado de `desk/atoms`. Cambios previstos: parser AST+regex, verbo y ayuda, códigos de salida, `RelationDoc cited_by`, listado en `show atom`, tests sandbox y goldens. Dependencias: API de sldb, almacén de átomos y `git ls-files`. Validaciones futuras: los cinco `pytest` citados, incluida suite completa y ausencia de fallas nuevas respecto de main. Sin ejecutar nada.

## FUTURO
Un nodo implementador producirá código y tests. Un humano o la API de sldb decidirá el tipo exacto de `cited_by` y la semántica de códigos de salida si no están normados. CI/main determinará si aparecen fallas nuevas.
