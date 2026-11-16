# Veredicto del tester deskops-t-0d2935319adb

Tarea: task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc
Entrega: cambios sin commitear en deskops/services/closure.py y tests/test_materialization_targets_outside_package.py (ejecutor deskops-e-312954356a7f).

**VEREDICTO: APROBADO**

## Comprobaciones (evidencia en validation.log)

1. Scope: el diff toca solo los dos archivos de `files:`. No cambia la compuerta de átomos ni sldb.
   - `target_covers(target, path)` (deskops/services/closure.py:87) cumple la precisión del preflight 1: POSIX relativo, quita `./` inicial y la barra final, no resuelve symlinks, distingue mayúsculas y cubre si `path == target` o `path.startswith(target + "/")`. No exige que el directorio exista. Está junto a la cobertura de materializations y se usa en ella (closure.py:1375-1377).
   - Bug de la nota inbox 20261116-070913 (el prefijo `test_file:`): `_missing_target_path` (closure.py:73) quita el prefijo `<kind>:` antes de comparar (closure.py:1402). Lo cubre el test parametrizado `tests/notations`. Lo comprobé en una copia donde la comparación no quita el prefijo: solo falla el caso `tests/notations` (rc=1).
   - Una materialization a la que le falta algo más que su directorio sigue inválida, porque `all(...)` exige que cada referencia faltante sea el target declarado. Lo comprobé con un test ad hoc en una copia en /dev/shm: con `--source-atoms atom-directory-target-atom,atom-no-existe`, el archivo interior queda `missing_changed_file_link` y no aparece ninguna evidencia `->{inside}` (2 passed).
2. Tests, de a un archivo y sin lock: test_materialization_targets_outside_package.py 18 passed; test_closeout_gates.py 5 passed; test_closeout.py 59 passed; test_closeout_declared_evidence.py 19 passed; test_view_goldens.py 1 passed. Todos con rc=0.
3. Reproducción: con el closure.py de HEAD en una copia en /dev/shm, los 14 tests nuevos fallan (12 de target_covers por ImportError y 2 de closeout verify).
4. La nota a sldb existe en /mnt/ssd/proyectos/SLDB_1/sldb/desk/inbox/20261116-054845-suggestion-declared-target-nodes-aceptar-un-directorio-como-target-declarado.md. Tiene el título pedido y un cuerpo con el caso y la salida de `graph missing` del sandbox (rc=1). message-send.log registra la entrega con rc=0.
5. No corrí la suite completa (la corre el integrador).

## Hallazgos y riesgos (no bloqueantes)

- No hay un test commiteado que pruebe que la materialization con otra referencia faltante sigue inválida. Solo lo verifiqué ad hoc. Recomiendo añadirlo en una tarea futura.
- closure.py:1375: la cobertura de directorio considera cualquier materialization del grafo, no solo las de la tarea. Es coherente con el comportamiento previo de las aristas de archivo, pero el goal dice "de la tarea".
- closure.py:80: `_missing_target_path` quita cualquier prefijo `palabra:` sin `/`. Un target real con `:` en su primer segmento sería un caso límite improbable.
- closure.py:1399: toma `provenance_path` solo de `missing[0]`. Es correcto mientras todas las entradas vengan del mismo documento.
- El `_cli` del test ahora antepone el checkout a PYTHONPATH. Está dentro del scope (archivo de tests) y es razonable.
- En validation.log, los comandos de pytest llevan `-p no:cacheprovider` para no escribir caché en el checkout.
