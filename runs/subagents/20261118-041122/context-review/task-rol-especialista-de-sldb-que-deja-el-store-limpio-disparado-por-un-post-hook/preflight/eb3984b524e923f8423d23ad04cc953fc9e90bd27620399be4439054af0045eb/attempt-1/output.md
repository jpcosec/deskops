## REFORMULACION
Propósito: crear en el repo `deskops` un RoleDoc de especialista de `sldb` que, disparado por un post-hook, deje limpio el store del desk. Resultado: RoleDoc creado con `deskops add role`; nuevo modo de `deskops runtime template` con su `agents.md`; prueba que materializa el template; manual del operador documentando el hook de transición a closeout. Archivos previstos: `deskops/runtime/scion.py`, `tests/test_scion_runtime.py`, `docs/operator-manual.md`. Es una tarea `task.code` ejecutable, no un agregado. Límites: dentro, RoleDoc, modo/template, prueba y manual; fuera, cambios en `sldb`, que el especialista toque código o cierre tareas, y declarar el hook en desks reales.

## AMBIGUEDADES
1. “disparado por un post-hook” y “transicion a closeout”: no se define evento, nombre, formato ni punto de registro del hook. Obliga a inventar su contrato.
2. “en un modo propio”: no se indica identificador del modo ni variables del template. Obliga a inventar nombre y parámetros.
3. “dejar por escrito en una nota del inbox”: no se especifica ruta, formato ni esquema de la nota. Obliga a inventar destino y estructura.
4. “corregir con el CLI lo que sea mecanico”: no se delimita qué drift es mecánico frente a decisión humana. Obliga a inventar la frontera.
5. “anclas perdidas”: no se define su detección ni reparación. Obliga a inferir semántica de `sldb`.
6. “una prueba que materializa el template”: no se concreta qué asserts ni aislamiento temporal. Obliga a inventar alcance del test.
7. “## Implementation Path” está vacío. Obliga a inventar la ruta concreta de implementación.

## DRY-RUN
Hipotéticamente, un ejecutor leería el TaskDoc, `deskops/runtime/scion.py`, `tests/test_scion_runtime.py`, `docs/operator-manual.md`, RoleDocs y templates existentes, y convenciones de `deskops add role`. Prevé: añadir RoleDoc; implementar modo/template y `agents.md`; añadir test de materialización; documentar el hook. Dependencias: CLIs `deskops`/`sldb`, registro de templates y harness pytest. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py` y `deskops graph missing --root .`. No se ejecuta nada.

## FUTURO
Un humano debe decidir contrato del post-hook, nombre del modo, formato del inbox y frontera mecánico/decisión. Otro nodo podría implementar el hook real o declararlo en desks; esta tarea solo lo documenta.
