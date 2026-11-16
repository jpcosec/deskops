## REFORMULACION
Propósito: corregir `closeout verify` y `closeout commit` para que la compuerta atom|materialization cuente como evidencia los ids del campo `atoms` de la tarea, además de los `atom-*` de `references`. Resultado: cambios en `deskops/services/closeout_gates.py` y `deskops/services/closure.py`, tests en `tests/test_closeout_gates.py` y validaciones pytest. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no cambiar otras compuertas ni el formato del reporte; materialization no cambia; contar todos los valores de `atoms` sin filtro por prefijo; no tocar el status `draft`; tests de Validation fuera de `files` solo si el cambio los rompe legítimamente.

## AMBIGUEDADES
1. “La compuerta atom|materialization de closeout verify y de closeout commit…” frente a “La compuerta de materialization no cambia.” Obliga a inventar si el cambio aplica solo a la parte atom, a commit, o a ambas rutas, y en qué función.
2. “Unir task.atoms a los atom-* de references al armar la evidencia de atomo.” No define estructura de evidencia, deduplicación ni orden; obliga a inventar la forma exacta del merge.
3. “se cuentan todos los valores del campo atoms (es una lista tipada de AtomDoc…)” no dice cómo extraer el id de cada `AtomDoc`; obliga a inventar atributo, normalización y posible conversión.
4. “solo si el cambio los rompe por una razon legitima” no define legitimidad; obliga a inventar el criterio para editar tests de Validation.
5. “Sin fallas nuevas: cada test que falle…” no fija si el baseline se corre antes o después ni cómo registrar la lista; obliga a inventar el procedimiento de comparación.

## DRY-RUN
Lecturas: TaskDoc, pill, `closeout_gates.py:100-113`, `closure.py:1241` y `1288-1293`, tests citados. Cambios previstos: ampliar la evidencia de átomo con todos los valores de `task.atoms` y agregar dos casos de test: tarea con `atoms` y sin `atom-*` en `references` pasa; tarea sin ninguno sigue fallando. Dependencias: modelo `AtomDoc`, flujo verify/commit y fixtures de tests. Validaciones futuras: los cuatro comandos pytest indicados, suite completa y baseline en worktree limpio para fallas; informe con fallas de baseline. Sin ejecutar nada.

## FUTURO
El ejecutor futuro implementará y entregará código, tests e informe; otro nodo o humano ejecutará/aceptará las validaciones y decidirá sobre fallas de baseline. No es un agregado: es una tarea ejecutable `task.code`.
